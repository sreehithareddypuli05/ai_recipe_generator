"""
AI Recipe Generator Service
This module generates recipes using rule-based logic.
(Ollama integration removed — replace _generate_fallback's internals later
with a call to your trained model once it's ready.)
"""
import random


class AIRecipeGenerator:
    """
    Service class for generating recipes.
    Currently rule-based; swap in a trained model call inside generate_recipe()
    when ready, keeping the same return shape (dict with the keys below).
    """

    def __init__(self):
        print("✅ AI Recipe Generator: rule-based mode (no external AI service)")

    def generate_recipe(self, ingredients, cuisine_type='', difficulty=''):
        """
        Generate a recipe based on available ingredients.

        Args:
            ingredients (str): Comma-separated list of ingredients
            cuisine_type (str): Optional cuisine preference
            difficulty (str): Optional difficulty level

        Returns:
            dict: Recipe data with name, ingredients, steps, etc.
        """
        return self._generate_fallback(ingredients, cuisine_type, difficulty)

    def _determine_category(self, cuisine_type):
        """
        Determine recipe category based on cuisine type
        """
        breakfast_cuisines = ['american', 'french']
        dessert_cuisines = ['french', 'italian']

        if cuisine_type and cuisine_type.lower() in breakfast_cuisines:
            return random.choice(['breakfast', 'dinner'])
        elif cuisine_type and cuisine_type.lower() in dessert_cuisines:
            return random.choice(['dessert', 'dinner'])
        else:
            return 'dinner'

    def _generate_fallback(self, ingredients, cuisine_type, difficulty):
        """
        Generate recipe using rule-based logic
        """
        ingredient_list = [ing.strip() for ing in ingredients.split(',') if ing.strip()]
        if not ingredient_list:
            ingredient_list = ['mixed ingredients']

        # Generate creative recipe name
        main_ingredient = ingredient_list[0] if ingredient_list else "Mixed"

        if cuisine_type:
            styles = {
                'italian': ['Italian', 'Tuscan', 'Roman', 'Sicilian'],
                'chinese': ['Chinese', 'Szechuan', 'Cantonese'],
                'indian': ['Indian', 'Tandoori', 'Curry'],
                'mexican': ['Mexican', 'Tex-Mex', 'Baja'],
                'french': ['French', 'Provençal', 'Parisian'],
                'japanese': ['Japanese', 'Teriyaki', 'Miso'],
                'thai': ['Thai', 'Bangkok', 'Pad'],
                'american': ['American', 'Classic', 'Southern']
            }
            style = random.choice(styles.get(cuisine_type.lower(), ['Homemade']))
        else:
            style = random.choice(["Delicious", "Homemade", "Quick", "Easy", "Traditional", "Classic"])

        dishes = ["Stir-Fry", "Casserole", "Soup", "Bowl", "Salad", "Bake", "Delight", "Special"]
        recipe_name = f"{style} {main_ingredient.title()} {random.choice(dishes)}"

        # Generate ingredients with measurements
        ingredient_details = []
        measurements = ["1 cup", "2 cups", "3 tablespoons", "1/2 cup", "200g", "300g", "1 pound", "2 tablespoons"]

        for ing in ingredient_list:
            measurement = random.choice(measurements)
            ingredient_details.append(f"{measurement} {ing}")

        # Add common pantry items
        pantry_items = [
            "2 tablespoons olive oil",
            "Salt and pepper to taste",
            "1 teaspoon garlic powder",
            "Fresh herbs for garnish",
            "1 tablespoon butter",
            "1/2 teaspoon paprika"
        ]
        ingredient_details.extend(random.sample(pantry_items, 3))

        # Generate preparation steps based on difficulty
        if difficulty == 'easy':
            steps = [
                f"Prepare all ingredients: wash and chop {', '.join(ingredient_list[:3])}",
                "Heat oil in a large pan over medium heat",
                f"Add {ingredient_list[0]} and cook for 5-7 minutes until tender",
                "Add remaining ingredients and season with salt and pepper",
                "Cook for 10-15 minutes, stirring occasionally",
                "Adjust seasoning to taste and serve hot",
                "Garnish with fresh herbs if desired"
            ]
            cooking_time = random.choice([15, 20, 25])
        elif difficulty == 'hard':
            steps = [
                f"Prepare mise en place: precisely dice {', '.join(ingredient_list[:3])}",
                "Preheat oven to 375°F (190°C)",
                "Heat oil in a large oven-safe skillet over medium-high heat",
                f"Sear {ingredient_list[0]} until golden brown, about 3-4 minutes per side",
                "Deglaze pan with wine or broth, scraping up browned bits",
                "Add aromatics and sauté until fragrant",
                "Add remaining ingredients in layers",
                "Transfer to oven and bake for 25-30 minutes",
                "Let rest for 5 minutes before serving",
                "Plate elegantly and garnish"
            ]
            cooking_time = random.choice([45, 50, 60])
        else:  # medium
            steps = [
                f"Prepare all ingredients: wash and chop {', '.join(ingredient_list[:3])}",
                "Heat oil in a large pan over medium heat",
                f"Add {ingredient_list[0]} and cook for 5-7 minutes",
                "Add garlic and aromatics, cook until fragrant",
                "Add remaining ingredients and season well",
                "Simmer for 20-25 minutes, stirring occasionally",
                "Taste and adjust seasoning as needed",
                "Serve hot, garnished with fresh herbs"
            ]
            cooking_time = random.choice([25, 30, 35])

        # Add tips
        tips = [
            "\n--- Cooking Tips ---",
            f"For best results, use fresh {ingredient_list[0]}",
            "Can be made ahead and reheated",
            "Pairs well with rice or crusty bread"
        ]
        steps.extend(tips)

        return {
            'recipe_name': recipe_name,
            'ingredients': '\n'.join(ingredient_details),
            'preparation_steps': '\n'.join(steps),
            'cooking_time': cooking_time,
            'servings': 4,
            'difficulty': difficulty or 'medium',
            'category': self._determine_category(cuisine_type) if cuisine_type else 'dinner'
        }


# Singleton instance
ai_generator = AIRecipeGenerator()