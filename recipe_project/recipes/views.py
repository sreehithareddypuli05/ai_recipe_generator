from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Recipe
from .forms import RecipeSearchForm, AIRecipeGeneratorForm, RecipeForm
from .ai_service import ai_generator


def home(request):
    """
    Home page view - displays recent recipes and search functionality
    """
    recent_recipes = Recipe.objects.all()[:6]
    search_form = RecipeSearchForm()
    
    context = {
        'recent_recipes': recent_recipes,
        'search_form': search_form,
        'total_recipes': Recipe.objects.count(),
    }
    return render(request, 'recipes/home.html', context)


def search_recipes(request):
    """
    Search recipes by name using Django ORM
    """
    results = []
    search_query = ''
    
    if request.method == 'GET' and 'search_query' in request.GET:
        form = RecipeSearchForm(request.GET)
        if form.is_valid():
            search_query = form.cleaned_data['search_query']
            
            # Search using Django ORM - case-insensitive search
            results = Recipe.objects.filter(
                Q(recipe_name__icontains=search_query) |
                Q(ingredients__icontains=search_query) |
                Q(category__icontains=search_query)
            ).distinct()
            
            if results.exists():
                messages.success(request, f'Found {results.count()} recipe(s) matching "{search_query}"')
            else:
                messages.info(request, f'No recipes found matching "{search_query}"')
    else:
        form = RecipeSearchForm()
    
    context = {
        'form': form,
        'results': results,
        'search_query': search_query,
    }
    return render(request, 'recipes/search.html', context)


def recipe_detail(request, recipe_id):
    """
    Display detailed view of a single recipe
    """
    recipe = get_object_or_404(Recipe, id=recipe_id)
    
    context = {
        'recipe': recipe,
        'ingredients_list': recipe.get_ingredients_list(),
        'steps_list': recipe.get_steps_list(),
    }
    return render(request, 'recipes/detail.html', context)


def generate_ai_recipe(request):
    """
    Generate recipe using AI based on available ingredients
    """
    generated_recipe = None
    
    if request.method == 'POST':
        form = AIRecipeGeneratorForm(request.POST)
        if form.is_valid():
            ingredients = form.cleaned_data['ingredients']
            cuisine_type = form.cleaned_data.get('cuisine_type', '')
            difficulty = form.cleaned_data.get('difficulty', '')
            
            # Generate recipe using AI service
            recipe_data = ai_generator.generate_recipe(
                ingredients=ingredients,
                cuisine_type=cuisine_type,
                difficulty=difficulty
            )
            
            # Check if recipe with same name exists
            existing_recipe = Recipe.objects.filter(
                recipe_name=recipe_data['recipe_name']
            ).first()
            
            if not existing_recipe:
                # Create and save the recipe
                recipe = Recipe.objects.create(
                    recipe_name=recipe_data['recipe_name'],
                    ingredients=recipe_data['ingredients'],
                    preparation_steps=recipe_data['preparation_steps'],
                    cooking_time=recipe_data.get('cooking_time', 30),
                    servings=recipe_data.get('servings', 4),
                    difficulty=recipe_data.get('difficulty', 'medium'),
                    category=recipe_data.get('category', 'dinner'),
                    is_ai_generated=True
                )
                generated_recipe = recipe
                messages.success(request, f'Recipe "{recipe.recipe_name}" generated successfully!')
            else:
                generated_recipe = existing_recipe
                messages.info(request, f'Recipe "{existing_recipe.recipe_name}" already exists in database!')
    else:
        form = AIRecipeGeneratorForm()
    
    context = {
        'form': form,
        'generated_recipe': generated_recipe,
    }
    return render(request, 'recipes/ai_generator.html', context)


def add_recipe(request):
    """
    Manually add a new recipe
    """
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            recipe = form.save()
            messages.success(request, f'Recipe "{recipe.recipe_name}" added successfully!')
            return redirect('recipe_detail', recipe_id=recipe.id)
    else:
        form = RecipeForm()
    
    context = {
        'form': form,
    }
    return render(request, 'recipes/add_recipe.html', context)


def all_recipes(request):
    """
    Display all recipes with filtering options
    """
    recipes = Recipe.objects.all()
    
    # Filter by category if provided
    category = request.GET.get('category')
    if category:
        recipes = recipes.filter(category=category)
    
    # Filter by difficulty if provided
    difficulty = request.GET.get('difficulty')
    if difficulty:
        recipes = recipes.filter(difficulty=difficulty)
    
    # Filter AI generated vs manual
    source = request.GET.get('source')
    if source == 'ai':
        recipes = recipes.filter(is_ai_generated=True)
    elif source == 'manual':
        recipes = recipes.filter(is_ai_generated=False)
    
    context = {
        'recipes': recipes,
        'selected_category': category,
        'selected_difficulty': difficulty,
        'selected_source': source,
    }
    return render(request, 'recipes/all_recipes.html', context)


def delete_recipe(request, recipe_id):
    """
    Delete a recipe
    """
    recipe = get_object_or_404(Recipe, id=recipe_id)
    recipe_name = recipe.recipe_name
    recipe.delete()
    messages.success(request, f'Recipe "{recipe_name}" deleted successfully!')
    return redirect('all_recipes')

"""
Add these imports to the top of your existing recipes/views.py,
and add the RecommendAPIView class anywhere in the file.
"""

import logging

from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from recipes.ai import RecommendationService
from recipes.ai.recommendation import RecommendationError
from recipes.serializers import RecommendationRequestSerializer, RecipeResultSerializer

logger = logging.getLogger(__name__)

# One shared instance — cheap to build (just holds references to the
# singletons from model_loader.py), but no need to rebuild per request.
_recommendation_service = None


def _get_service() -> RecommendationService:
    global _recommendation_service
    if _recommendation_service is None:
        _recommendation_service = RecommendationService()
    return _recommendation_service


class RecommendAPIView(APIView):
    """
    POST /api/recommend/

    Request body:  {"ingredients": ["tomato", "onion", "cheese"]}
    Response body: [{"id": 1, "name": "...", ..., "score": 0.94}, ...]
    """

    def post(self, request):
        request_serializer = RecommendationRequestSerializer(data=request.data)
        if not request_serializer.is_valid():
            logger.warning("Invalid recommend request: %s", request_serializer.errors)
            return Response(
                {"error": "Invalid input.", "details": request_serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        ingredients = request_serializer.validated_data["ingredients"]

        # Cache identical queries (e.g. repeated searches, form resubmits)
        # for a short window — avoids recomputing embeddings + FAISS search.
        cache_key = "recommend:" + ",".join(sorted(i.lower() for i in ingredients))
        cached = cache.get(cache_key)
        if cached is not None:
            logger.debug("Cache hit for %s", cache_key)
            return Response(cached, status=status.HTTP_200_OK)

        try:
            service = _get_service()
            results = service.recommend(ingredients)
        except RecommendationError as e:
            logger.warning("Recommendation validation error: %s", e)
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            # Anything unexpected (model/index in a bad state, etc.) —
            # never leak internals to the client.
            logger.exception("Unexpected error during recommendation")
            return Response(
                {"error": "Something went wrong generating recommendations."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        response_serializer = RecipeResultSerializer(data=results, many=True)
        response_serializer.is_valid(raise_exception=True)
        data = response_serializer.data

        cache.set(cache_key, data, timeout=60 * 10)  # 10 minutes
        return Response(data, status=status.HTTP_200_OK)
    
def ai_recommend_page(request):
    """Renders the AI ingredient-search page (JS calls /api/recommend/)."""
    return render(request, 'recipes/ai_recommend.html')


def ai_recommend_detail_page(request, recipe_id):
    """Renders the detail shell; JS fills it via sessionStorage or /api/recipe/<id>/."""
    return render(request, 'recipes/ai_recommend_detail.html', {'recipe_id': recipe_id})