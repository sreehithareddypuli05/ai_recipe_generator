from django.contrib import admin
from .models import Recipe


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """
    Admin interface for Recipe model
    """
    list_display = ['recipe_name', 'category', 'difficulty', 'cooking_time', 
                    'servings', 'is_ai_generated', 'created_at']
    list_filter = ['category', 'difficulty', 'is_ai_generated', 'created_at']
    search_fields = ['recipe_name', 'ingredients', 'preparation_steps']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('recipe_name', 'category', 'difficulty')
        }),
        ('Recipe Details', {
            'fields': ('ingredients', 'preparation_steps', 'cooking_time', 'servings')
        }),
        ('Metadata', {
            'fields': ('is_ai_generated', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )