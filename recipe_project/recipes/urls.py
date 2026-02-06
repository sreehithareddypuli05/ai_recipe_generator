from django.urls import path
from . import views
from .import chat_views
urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search_recipes, name='search_recipes'),
    path('recipe/<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),
    path('generate/', views.generate_ai_recipe, name='generate_ai_recipe'),
    path('add/', views.add_recipe, name='add_recipe'),
    path('all/', views.all_recipes, name='all_recipes'),
    path('delete/<int:recipe_id>/', views.delete_recipe, name='delete_recipe'),
     path('ai-chat/', chat_views.ai_chat_generator, name='ai_chat'),
    path('chat-with-ai/', chat_views.chat_with_ai, name='chat_with_ai'),
    path('save-recipe-from-chat/', chat_views.save_recipe_from_chat, name='save_recipe_from_chat'),
]