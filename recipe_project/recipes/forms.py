from django import forms
from .models import Recipe


class RecipeSearchForm(forms.Form):
    """Form for searching recipes by name"""
    search_query = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search for a recipe...',
            'autocomplete': 'off'
        })
    )


class AIRecipeGeneratorForm(forms.Form):
    """Form for generating AI recipes from ingredients"""
    ingredients = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Enter available ingredients (comma-separated)\nExample: chicken, tomatoes, onions, garlic, rice',
            'rows': 4
        }),
        required=True,
        help_text="Enter the ingredients you have available, separated by commas"
    )
    
    cuisine_type = forms.ChoiceField(
        choices=[
            ('', 'Any Cuisine'),
            ('italian', 'Italian'),
            ('chinese', 'Chinese'),
            ('indian', 'Indian'),
            ('mexican', 'Mexican'),
            ('french', 'French'),
            ('japanese', 'Japanese'),
            ('thai', 'Thai'),
            ('american', 'American'),
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    difficulty = forms.ChoiceField(
        choices=[
            ('', 'Any Difficulty'),
            ('easy', 'Easy'),
            ('medium', 'Medium'),
            ('hard', 'Hard'),
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )


class RecipeForm(forms.ModelForm):
    """Form for manually adding recipes"""
    class Meta:
        model = Recipe
        fields = ['recipe_name', 'ingredients', 'preparation_steps', 
                  'cooking_time', 'servings', 'difficulty', 'category']
        widgets = {
            'recipe_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Recipe Name'
            }),
            'ingredients': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter ingredients, one per line',
                'rows': 6
            }),
            'preparation_steps': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter preparation steps, one per line',
                'rows': 8
            }),
            'cooking_time': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Minutes'
            }),
            'servings': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Number of servings'
            }),
            'difficulty': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }