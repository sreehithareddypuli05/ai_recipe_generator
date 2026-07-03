"""
model_loader.py

Loads the SentenceTransformer model, FAISS index, and recipes dataset
EXACTLY ONCE per process, at first import (which happens at Django
startup via recipes/apps.py — see integration note below).

Design notes:
- Uses a simple module-level singleton pattern. Python caches imported
  modules, so `from recipes.ai import model_loader` anywhere in the
  codebase will reuse the same in-memory objects — no reloading per request.
- Thread-safety: model/index objects from sentence-transformers and faiss
  are read-only after load and safe for concurrent reads across Django's
  worker threads. Loading itself happens once, before any request is served.
- Fails loudly at startup rather than silently at request time — if the
  model files are missing/corrupt, you want to know immediately, not on
  a user's first search.
"""

import logging
import pickle
import threading
from pathlib import Path

import faiss
import numpy as np
import pandas as pd
from django.conf import settings
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Paths — adjust ONLY if your datasets/models folder is not at project root.
# ---------------------------------------------------------------------------
DATASETS_MODELS_DIR = Path(settings.BASE_DIR) / "datasets" / "models"

EMBEDDINGS_PATH = DATASETS_MODELS_DIR / "recipe_embeddings.npy"
FAISS_INDEX_PATH = DATASETS_MODELS_DIR / "recipe_index.faiss"
RECIPES_PKL_PATH = DATASETS_MODELS_DIR / "recipes.pkl"

SENTENCE_MODEL_NAME = "all-MiniLM-L6-v2"

# ---------------------------------------------------------------------------
# Module-level singletons (populated by _load_all(), called once below)
# ---------------------------------------------------------------------------
_model = None
_index = None
_recipes_df = None
_embeddings = None  # kept in case recommendation.py needs raw vectors

_load_lock = threading.Lock()
_loaded = False


def _load_all() -> None:
    """
    Loads the sentence transformer, FAISS index, and recipes dataframe
    into module-level globals. Guarded by a lock + flag so it truly
    only runs once, even under concurrent access (e.g. Django's
    autoreload spawning threads, or gunicorn preload edge cases).
    """
    global _model, _index, _recipes_df, _embeddings, _loaded

    if _loaded:
        return

    with _load_lock:
        # Double-checked locking: another thread may have finished
        # loading while we were waiting for the lock.
        if _loaded:
            return

        logger.info("AI module: starting one-time model/index/data load...")

        # --- Sentence Transformer ---
        if not DATASETS_MODELS_DIR.exists():
            raise FileNotFoundError(
                f"AI module: datasets/models directory not found at "
                f"{DATASETS_MODELS_DIR}. Check settings.BASE_DIR."
            )

        logger.info("Loading SentenceTransformer '%s'...", SENTENCE_MODEL_NAME)
        _model = SentenceTransformer(SENTENCE_MODEL_NAME)

        # --- FAISS index ---
        if not FAISS_INDEX_PATH.exists():
            raise FileNotFoundError(f"FAISS index not found at {FAISS_INDEX_PATH}")
        logger.info("Loading FAISS index from %s...", FAISS_INDEX_PATH)
        _index = faiss.read_index(str(FAISS_INDEX_PATH))

        # --- Precomputed embeddings (optional, useful for debugging/reuse) ---
        if EMBEDDINGS_PATH.exists():
            logger.info("Loading precomputed embeddings from %s...", EMBEDDINGS_PATH)
            _embeddings = np.load(EMBEDDINGS_PATH)
        else:
            logger.warning(
                "Embeddings file not found at %s — skipping (not required "
                "for inference, FAISS index is sufficient).",
                EMBEDDINGS_PATH,
            )

        # --- recipes.pkl ---
        if not RECIPES_PKL_PATH.exists():
            raise FileNotFoundError(f"recipes.pkl not found at {RECIPES_PKL_PATH}")
        logger.info("Loading recipes.pkl from %s...", RECIPES_PKL_PATH)
        with open(RECIPES_PKL_PATH, "rb") as f:
            raw = pickle.load(f)

        # Normalize to a DataFrame regardless of whether it was pickled
        # as a DataFrame or a list of dicts.
        if isinstance(raw, pd.DataFrame):
            _recipes_df = raw.reset_index(drop=True)
        elif isinstance(raw, list):
            _recipes_df = pd.DataFrame(raw)
        else:
            raise TypeError(
                f"Unsupported type in recipes.pkl: {type(raw)}. "
                "Expected pandas.DataFrame or list[dict]."
            )

        logger.info(
            "AI module load complete. Recipes: %d | FAISS ntotal: %d",
            len(_recipes_df),
            _index.ntotal,
        )
        _loaded = True


# Trigger the load immediately at import time.
_load_all()


# ---------------------------------------------------------------------------
# Public accessors — everything else in the codebase should use these,
# never touch the _model/_index/_recipes_df globals directly.
# ---------------------------------------------------------------------------
def get_model() -> SentenceTransformer:
    return _model


def get_index() -> "faiss.Index":
    return _index


def get_recipes_df() -> pd.DataFrame:
    return _recipes_df


def get_embeddings() -> np.ndarray | None:
    return _embeddings