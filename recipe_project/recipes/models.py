from django.db import models
from django.utils import timezone


class Recipe(models.Model):
    """
    Recipe model to store recipe information
    """
    recipe_name = models.CharField(max_length=200, unique=True)
    ingredients = models.TextField(help_text="Enter ingredients, one per line or comma-separated")
    preparation_steps = models.TextField(help_text="Enter preparation steps")
    cooking_time = models.IntegerField(null=True, blank=True, help_text="Cooking time in minutes")
    servings = models.IntegerField(default=4, help_text="Number of servings")
    difficulty = models.CharField(
        max_length=20,
        choices=[
            ('easy', 'Easy'),
            ('medium', 'Medium'),
            ('hard', 'Hard'),
        ],
        default='medium'
    )
    category = models.CharField(
        max_length=50,
        choices=[
            ('breakfast', 'Breakfast'),
            ('lunch', 'Lunch'),
            ('dinner', 'Dinner'),
            ('dessert', 'Dessert'),
            ('snack', 'Snack'),
            ('appetizer', 'Appetizer'),
        ],
        default='dinner'
    )
    youtube_link = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        help_text="Optional YouTube video link for this recipe (not required)"
    )
    is_ai_generated = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'

    def __str__(self):
        return self.recipe_name

    def get_ingredients_list(self):
        """Return ingredients as a list"""
        if '\n' in self.ingredients:
            return [ing.strip() for ing in self.ingredients.split('\n') if ing.strip()]
        else:
            return [ing.strip() for ing in self.ingredients.split(',') if ing.strip()]

    def get_steps_list(self):
        """Return preparation steps as a list"""
        return [step.strip() for step in self.preparation_steps.split('\n') if step.strip()]