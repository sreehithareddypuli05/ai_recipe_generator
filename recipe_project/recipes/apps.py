from django.apps import AppConfig


class RecipesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'recipes'
    verbose_name = 'Recipe Management'
    def ready(self):
        # Triggers the one-time model/FAISS/pkl load at Django startup,
        # not on the first incoming request. model_loader.py already
        # loads at import time, but importing it explicitly here
        # guarantees it happens during app startup regardless of import
        # order elsewhere, and makes the intent explicit.
        from recipes.ai import model_loader  # noqa: F401