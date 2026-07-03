"""
AI module for the recipes app.

This package is responsible for everything related to the trained
recommendation model: loading it once at process startup, and exposing
a clean service layer (recommendation.py) that views/serializers call.

Do NOT import heavy ML libraries (sentence-transformers, faiss) anywhere
outside model_loader.py. Everything else should import from here.
"""

from .model_loader import get_model, get_index, get_recipes_df
from .recommendation import RecommendationService

__all__ = [
    "get_model",
    "get_index",
    "get_recipes_df",
    "RecommendationService",
]