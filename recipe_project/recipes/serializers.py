"""
DRF serializers for the AI recommendation API.

RecommendationRequestSerializer validates incoming ingredient lists.
RecipeResultSerializer shapes outgoing recipe data. Neither touches
the AI module directly — that's recommendation.py's job.
"""

from rest_framework import serializers


class RecommendationRequestSerializer(serializers.Serializer):
    ingredients = serializers.ListField(
        child=serializers.CharField(max_length=100, allow_blank=False),
        min_length=1,
        max_length=30,
        help_text="List of ingredient names, e.g. ['tomato', 'onion', 'cheese']",
    )

    def validate_ingredients(self, value):
        cleaned = [i.strip() for i in value if i.strip()]
        if not cleaned:
            raise serializers.ValidationError(
                "At least one non-empty ingredient is required."
            )
        return cleaned


class RecipeResultSerializer(serializers.Serializer):
    id = serializers.IntegerField(allow_null=True)
    name = serializers.CharField(allow_null=True)
    ingredients = serializers.ListField(child=serializers.CharField(), allow_null=True)
    steps = serializers.ListField(child=serializers.CharField(), allow_null=True)
    
    minutes = serializers.IntegerField(allow_null=True)
    score = serializers.FloatField()