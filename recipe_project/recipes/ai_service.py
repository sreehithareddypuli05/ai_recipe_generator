"""
Enhanced AI Recipe Generator Service
This module handles AI-powered recipe generation using Ollama (Local AI - 100% Free!)
"""
import json
import random
import requests


class AIRecipeGenerator:
    """
    Service class for generating recipes using AI (Ollama - Local & Free)
    """
    
    def __init__(self):
        # Ollama runs locally on port 11434
        self.ollama_url = "http://localhost:11434/api/generate"
        self.model = "llama3.2"  # or "mistral", "phi3", etc.
        self.use_api = self._check_ollama_available()
        
        if self.use_api:
            print(f"✅ AI Recipe Generator: Using Ollama ({self.model}) - Local & Free!")
        else:
            print("⚠️  Ollama not running. Install from: https://ollama.ai")
    
    def _check_ollama_available(self):
        """Check if Ollama is running"""
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=2)
            return response.status_code == 200
        except:
            return False
    
    def generate_recipe(self, ingredients, cuisine_type='', difficulty=''):
        """
        Generate a recipe based on available ingredients
        
        Args:
            ingredients (str): Comma-separated list of ingredients
            cuisine_type (str): Optional cuisine preference
            difficulty (str): Optional difficulty level
            
        Returns:
            dict: Recipe data with name, ingredients, steps, etc.
        """
        if self.use_api:
            return self._generate_with_ollama(ingredients, cuisine_type, difficulty)
        else:
            return self._generate_fallback(ingredients, cuisine_type, difficulty)
    
    def _generate_with_ollama(self, ingredients, cuisine_type, difficulty):
        """
        Generate recipe using Ollama (Local AI)
        """
        try:
            # Create detailed prompt for recipe generation
            prompt = self._create_detailed_prompt(ingredients, cuisine_type, difficulty)
            
            print(f"🤖 Generating recipe with Ollama ({self.model})...")
            
            # Call Ollama API
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9
                }
            }
            
            response = requests.post(
                self.ollama_url,
                json=payload,
                timeout=60  # Ollama might take longer on first run
            )
            
            if response.status_code == 200:
                result = response.json()
                response_text = result.get('response', '')
                
                print("✅ Recipe generated successfully!")
                
                # Parse the response
                return self._parse_api_response(response_text, cuisine_type, difficulty)
            else:
                print(f"❌ Ollama Error: {response.status_code}")
                return self._generate_fallback(ingredients, cuisine_type, difficulty)
                
        except requests.exceptions.ConnectionError:
            print("❌ Cannot connect to Ollama. Make sure it's running!")
            print("   Start Ollama with: ollama serve")
            return self._generate_fallback(ingredients, cuisine_type, difficulty)
        except Exception as e:
            print(f"❌ Error: {e}")
            return self._generate_fallback(ingredients, cuisine_type, difficulty)
    
    def _create_detailed_prompt(self, ingredients, cuisine_type, difficulty):
        """
        Create a detailed prompt for recipe generation
        """
        prompt = f"""You are a professional chef. Create a detailed recipe using these ingredients: {ingredients}

"""
        
        if cuisine_type:
            prompt += f"Cuisine Style: {cuisine_type.title()}\n"
        
        if difficulty:
            prompt += f"Difficulty Level: {difficulty.title()}\n"
        
        prompt += """
Format your response EXACTLY like this:

RECIPE NAME: [Creative recipe name]

COOKING TIME: [Number only, e.g., 30]

SERVINGS: [Number only, e.g., 4]

INGREDIENTS:
- [Amount] [ingredient 1]
- [Amount] [ingredient 2]

PREPARATION STEPS:
1. [Detailed step 1]
2. [Detailed step 2]

TIPS:
- [Helpful cooking tip]

Be specific with measurements and cooking times."""
        
        return prompt
    
    def _parse_api_response(self, response_text, cuisine_type, difficulty):
        """
        Parse the API response into structured recipe data
        """
        lines = response_text.strip().split('\n')
        
        recipe_data = {
            'recipe_name': 'AI Generated Recipe',
            'ingredients': '',
            'preparation_steps': '',
            'cooking_time': 30,
            'servings': 4,
            'difficulty': difficulty or 'medium',
            'category': self._determine_category(cuisine_type)
        }
        
        current_section = None
        ingredients_list = []
        steps_list = []
        tips_list = []
        
        for line in lines:
            line = line.strip()
            
            # Parse recipe name
            if line.startswith('RECIPE NAME:'):
                recipe_data['recipe_name'] = line.replace('RECIPE NAME:', '').strip()
            
            # Parse cooking time
            elif line.startswith('COOKING TIME:'):
                try:
                    time_str = line.replace('COOKING TIME:', '').strip()
                    # Extract just the number
                    time_num = ''.join(filter(str.isdigit, time_str.split()[0]))
                    if time_num:
                        recipe_data['cooking_time'] = int(time_num)
                except:
                    recipe_data['cooking_time'] = 30
            
            # Parse servings
            elif line.startswith('SERVINGS:'):
                try:
                    servings_str = line.replace('SERVINGS:', '').strip()
                    servings_num = ''.join(filter(str.isdigit, servings_str.split()[0]))
                    if servings_num:
                        recipe_data['servings'] = int(servings_num)
                except:
                    recipe_data['servings'] = 4
            
            # Identify sections
            elif line.startswith('INGREDIENTS:'):
                current_section = 'ingredients'
            elif line.startswith('PREPARATION STEPS:') or line.startswith('INSTRUCTIONS:'):
                current_section = 'steps'
            elif line.startswith('TIPS:'):
                current_section = 'tips'
            
            # Parse ingredients
            elif current_section == 'ingredients' and line:
                # Clean up ingredient line
                cleaned = line.lstrip('- ').lstrip('• ').lstrip('* ').lstrip('·')
                if cleaned and not cleaned.startswith('PREPARATION'):
                    ingredients_list.append(cleaned)
            
            # Parse steps
            elif current_section == 'steps' and line:
                # Clean up step line
                cleaned = line.lstrip('- ').lstrip('• ').lstrip('* ')
                # Remove step numbers if present
                if cleaned:
                    # Remove leading numbers and dots/parentheses
                    import re
                    cleaned = re.sub(r'^\d+[\.\)]\s*', '', cleaned)
                    if cleaned and not cleaned.startswith('TIPS'):
                        steps_list.append(cleaned)
            
            # Parse tips
            elif current_section == 'tips' and line:
                cleaned = line.lstrip('- ').lstrip('• ').lstrip('* ')
                if cleaned:
                    tips_list.append(cleaned)
        
        # Combine ingredients
        recipe_data['ingredients'] = '\n'.join(ingredients_list)
        
        # Combine steps with tips
        all_steps = steps_list
        if tips_list:
            all_steps.append('\n--- Cooking Tips ---')
            all_steps.extend(tips_list)
        
        recipe_data['preparation_steps'] = '\n'.join(all_steps)
        
        # Validate we got something useful
        if not ingredients_list or not steps_list:
            print("⚠️  API response parsing incomplete, using fallback")
            return self._generate_fallback(
                ', '.join(ingredients_list) if ingredients_list else 'mixed ingredients',
                cuisine_type,
                difficulty
            )
        
        return recipe_data
    
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
        Generate recipe using rule-based logic (fallback when Ollama is not available)
        """
        ingredient_list = [ing.strip() for ing in ingredients.split(',')]
        
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
                f"Add {ingredient_list[0] if ingredient_list else 'main ingredient'} and cook for 5-7 minutes until tender",
                f"Add remaining ingredients and season with salt and pepper",
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
                f"Sear {ingredient_list[0] if ingredient_list else 'main ingredient'} until golden brown, about 3-4 minutes per side",
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
                f"Add {ingredient_list[0] if ingredient_list else 'main ingredient'} and cook for 5-7 minutes",
                "Add garlic and aromatics, cook until fragrant",
                f"Add remaining ingredients and season well",
                "Simmer for 20-25 minutes, stirring occasionally",
                "Taste and adjust seasoning as needed",
                "Serve hot, garnished with fresh herbs"
            ]
            cooking_time = random.choice([25, 30, 35])
        
        # Add tips
        tips = [
            "\n--- Cooking Tips ---",
            f"For best results, use fresh {ingredient_list[0] if ingredient_list else 'ingredients'}",
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