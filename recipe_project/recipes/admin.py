from django.contrib import admin
from .models import Recipe


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """
    Admin interface for Recipe model
    """
    list_display = ['recipe_name', 'category', 'difficulty', 'cooking_time',
                    'servings', 'is_ai_generated', 'has_video', 'created_at']
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
        ('Video', {
            'fields': ('youtube_link',),
            'description': 'Optional — link a YouTube video for this recipe.'
        }),
        ('Metadata', {
            'fields': ('is_ai_generated', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def has_video(self, obj):
        return bool(obj.youtube_link)
    has_video.boolean = True
    has_video.short_description = 'Has Video'