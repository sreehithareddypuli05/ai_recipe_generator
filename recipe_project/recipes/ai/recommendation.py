"""
recommendation.py

Service layer that turns a list of ingredients into ranked recipe
recommendations. This is the ONLY place business logic for
"ingredients -> recipes" should live. Views call this; this never
touches HTTP request/response objects.
"""

import logging
from typing import Any

import numpy as np

from .model_loader import get_index, get_model, get_recipes_df

logger = logging.getLogger(__name__)

TOP_K = 10

# Column name fallbacks — adjust these to match your actual recipes.pkl
# schema. The service tries each candidate in order and uses the first
# one present in the dataframe.
COLUMN_CANDIDATES = {
    "id": ["id", "recipe_id", "Id"],
    "name": ["name", "title", "recipe_name", "Name"],
    "ingredients": ["ingredients", "ingredient_list", "Ingredients"],
    "steps": ["steps", "instructions", "directions"],
   
    "minutes": ["minutes", "cook_time", "cooking_time", "time"],
}


class RecommendationError(Exception):
    """Raised for invalid input or recoverable service-level failures."""


def _resolve_column(df, key: str) -> str | None:
    for candidate in COLUMN_CANDIDATES[key]:
        if candidate in df.columns:
            return candidate
    return None

def _row_to_dict(row, columns: dict[str, str | None]) -> dict[str, Any]:
    def val(field):
        col = columns.get(field)
        if col is None:
            return None
        v = row[col]
        if isinstance(v, (np.integer,)):
            return int(v)
        if isinstance(v, (np.floating,)):
            return float(v)
        if isinstance(v, np.ndarray):
            v = v.tolist()
        return v

    return {
        "id": val("id"),
        "name": val("name"),
        "ingredients": val("ingredients"),
        "steps": val("steps"),
        "minutes": val("minutes"),
    }
class RecommendationService:
    """
    Stateless service — safe to instantiate per-request (it's cheap;
    it just reads references to the already-loaded singletons).
    """

    def __init__(self):
        self.model = get_model()
        self.index = get_index()
        self.recipes_df = get_recipes_df()
        self._columns = {
            key: _resolve_column(self.recipes_df, key)
            for key in COLUMN_CANDIDATES
        }

    def recommend(self, ingredients: list[str], top_k: int = TOP_K) -> list[dict[str, Any]]:
        """
        Args:
            ingredients: list of ingredient strings, e.g. ["tomato", "onion"]
            top_k: number of results to return.

        Returns:
            List of recipe dicts, sorted by descending similarity score.

        Raises:
            RecommendationError: on invalid/empty input.
        """
        self._validate_input(ingredients)

        query_text = ", ".join(i.strip() for i in ingredients if i.strip())
        logger.debug("Generating embedding for query: %s", query_text)

        query_vector = self.model.encode([query_text], convert_to_numpy=True)
        query_vector = query_vector.astype("float32")

        # If the index was built with normalized (cosine) vectors, normalize
        # the query too for consistent scoring. Safe no-op for L2 indexes
        # built on unnormalized vectors — remove if not applicable to yours.
        faiss_normalize = getattr(self.index, "metric_type", None)
        try:
            import faiss as _faiss
            if faiss_normalize == _faiss.METRIC_INNER_PRODUCT:
                _faiss.normalize_L2(query_vector)
        except Exception:  # pragma: no cover - defensive, non-fatal
            pass

        distances, indices = self.index.search(query_vector, top_k)

        results = []
        for rank, (idx, dist) in enumerate(zip(indices[0], distances[0])):
            if idx == -1 or idx >= len(self.recipes_df):
                continue  # FAISS pads with -1 if fewer than top_k matches exist
            row = self.recipes_df.iloc[idx]
            recipe = _row_to_dict(row, self._columns)
            recipe["score"] = round(float(dist), 4)
            results.append(recipe)

        logger.info(
            "Recommendation query '%s' -> %d results", query_text, len(results)
        )
        return results

    @staticmethod
    def _validate_input(ingredients: Any) -> None:
        if not isinstance(ingredients, list) or not ingredients:
            raise RecommendationError("`ingredients` must be a non-empty list of strings.")
        if not all(isinstance(i, str) for i in ingredients):
            raise RecommendationError("All items in `ingredients` must be strings.")
        if not any(i.strip() for i in ingredients):
            raise RecommendationError("`ingredients` must contain at least one non-empty value.")