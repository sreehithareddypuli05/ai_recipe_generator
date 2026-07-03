from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import re

from .ai_service import ai_generator

# Common ingredient vocabulary used to pull ingredients out of free-text chat
# messages. Extend this list with anything common in your recipes DB.
KNOWN_INGREDIENTS = [
    'chicken', 'beef', 'pork', 'fish', 'shrimp', 'tofu', 'paneer', 'eggs', 'egg',
    'rice', 'pasta', 'noodles', 'bread', 'potato', 'potatoes', 'onion', 'onions',
    'garlic', 'ginger', 'tomato', 'tomatoes', 'spinach', 'broccoli', 'carrot',
    'carrots', 'bell pepper', 'peppers', 'mushroom', 'mushrooms', 'cheese',
    'milk', 'butter', 'cream', 'yogurt', 'flour', 'sugar', 'beans', 'lentils',
    'chickpeas', 'corn', 'peas', 'cabbage', 'cauliflower', 'zucchini',
    'avocado', 'lemon', 'lime', 'cilantro', 'basil', 'oregano', 'cumin',
    'turmeric', 'chili', 'soy sauce', 'olive oil', 'coconut milk', 'apple',
    'banana', 'mango', 'lettuce', 'cucumber',
]

KNOWN_CUISINES = [
    'italian', 'chinese', 'indian', 'mexican', 'french', 'japanese', 'thai',
    'american',
]

DIFFICULTY_WORDS = {
    'easy': 'easy', 'simple': 'easy', 'quick': 'easy', 'beginner': 'easy',
    'medium': 'medium', 'moderate': 'medium', 'intermediate': 'medium',
    'hard': 'hard', 'difficult': 'hard', 'advanced': 'hard', 'complex': 'hard',
}


def ai_chat_generator(request):
    """
    Interactive recipe chat page (rule-based — no external AI service required)
    """
    context = {
        'has_api_key': True  # always available now, no external service to check
    }
    return render(request, 'recipes/ai_chat.html', context)


def _extract_ingredients(text):
    text_lower = text.lower()
    found = []
    for ing in KNOWN_INGREDIENTS:
        if re.search(r'\b' + re.escape(ing) + r'\b', text_lower):
            found.append(ing)
    return found


def _extract_cuisine(text):
    text_lower = text.lower()
    for cuisine in KNOWN_CUISINES:
        if cuisine in text_lower:
            return cuisine
    return ''


def _extract_difficulty(text):
    text_lower = text.lower()
    for word, level in DIFFICULTY_WORDS.items():
        if re.search(r'\b' + re.escape(word) + r'\b', text_lower):
            return level
    return ''


def _wants_skip(text):
    text_lower = text.lower()
    return any(p in text_lower for p in [
        'surprise me', 'any', "doesn't matter", 'dont care', "don't care",
        'no preference', 'skip', 'whatever',
    ])


@csrf_exempt
def chat_with_ai(request):
    """
    API endpoint for chatting with the (rule-based) recipe assistant.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)

    try:
        data = json.loads(request.body)
        user_message = data.get('message', '')
        conversation_history = data.get('history', [])

        if not user_message:
            return JsonResponse({'error': 'Message is required'}, status=400)

        ai_response, recipe_data = generate_ai_chat_response(user_message, conversation_history)

        return JsonResponse({
            'response': ai_response,
            'recipe': recipe_data,
            'success': True
        })

    except Exception as e:
        print(f"Error in chat_with_ai: {e}")
        return JsonResponse({
            'error': str(e),
            'success': False
        }, status=500)


def generate_ai_chat_response(user_message, conversation_history):
    """
    Rule-based conversational flow:
      1. Collect ingredients across the conversation.
      2. Ask for cuisine preference (once) if not given.
      3. Ask for difficulty (once) if not given.
      4. Generate a recipe via ai_generator and return it formatted as a
         ===RECIPE START===...===RECIPE END=== block, so the existing
         extract_recipe_from_response() keeps working unchanged.

    Returns: (response_text, recipe_data_or_None)
    """
    # Gather everything said so far, plus this new message
    all_user_text = user_message + ' ' + ' '.join(
        m.get('content', '') for m in conversation_history if m.get('role') == 'user'
    )

    ingredients = _extract_ingredients(all_user_text)
    cuisine = _extract_cuisine(all_user_text)
    difficulty = _extract_difficulty(all_user_text)

    # No ingredients yet — greet / ask for them
    if not ingredients:
        if not conversation_history:
            return (
                "Hi! I'm your recipe assistant. 🍳 Tell me what ingredients "
                "you have on hand and I'll whip up a recipe idea for you.",
                None
            )
        return (
            "I didn't quite catch any ingredients there — could you list a "
            "few things you have available (e.g. chicken, rice, onions)?",
            None
        )

    # Have ingredients but no cuisine preference yet, and haven't asked before
    already_asked_cuisine = any(
        'cuisine' in m.get('content', '').lower()
        for m in conversation_history if m.get('role') == 'assistant'
    )
    if not cuisine and not already_asked_cuisine and not _wants_skip(user_message):
        ing_list = ', '.join(ingredients)
        return (
            f"Nice, I see {ing_list}! Do you have a cuisine preference "
            f"(Italian, Indian, Mexican, etc.) — or should I surprise you?",
            None
        )

    # Have ingredients + (cuisine answered or skipped), no difficulty yet
    already_asked_difficulty = any(
        'difficulty' in m.get('content', '').lower() or 'easy, medium' in m.get('content', '').lower()
        for m in conversation_history if m.get('role') == 'assistant'
    )
    if not difficulty and not already_asked_difficulty and not _wants_skip(user_message):
        return (
            "Got it! One more thing — what difficulty level are you going "
            "for: easy, medium, or hard?",
            None
        )

    # We have enough info — generate the recipe
    recipe_data = ai_generator.generate_recipe(
        ingredients=', '.join(ingredients),
        cuisine_type=cuisine,
        difficulty=difficulty
    )

    response_text = (
        f"Here's a recipe idea for you: **{recipe_data['recipe_name']}** 🎉\n\n"
        + _format_recipe_block(recipe_data)
    )

    return response_text, recipe_data


def _format_recipe_block(recipe_data):
    """
    Format a recipe dict into the ===RECIPE START===...===RECIPE END=== text
    block expected by extract_recipe_from_response() and the frontend.
    """
    ingredients_lines = '\n'.join(f"- {line}" for line in recipe_data['ingredients'].split('\n') if line.strip())

    steps_raw = [s for s in recipe_data['preparation_steps'].split('\n') if s.strip()]
    step_lines = []
    step_num = 1
    for s in steps_raw:
        if s.strip().startswith('---'):
            step_lines.append(s)
            continue
        step_lines.append(f"{step_num}. {s}")
        step_num += 1
    steps_text = '\n'.join(step_lines)

    return f"""===RECIPE START===
RECIPE NAME: {recipe_data['recipe_name']}
COOKING TIME: {recipe_data['cooking_time']}
SERVINGS: {recipe_data['servings']}
DIFFICULTY: {recipe_data['difficulty']}
CATEGORY: {recipe_data['category']}

INGREDIENTS:
{ingredients_lines}

PREPARATION STEPS:
{steps_text}
===RECIPE END==="""


def extract_recipe_from_response(ai_response):
    """
    Extract structured recipe data from an assistant response that contains
    a ===RECIPE START===...===RECIPE END=== block.
    """
    if '===RECIPE START===' not in ai_response or '===RECIPE END===' not in ai_response:
        return None

    try:
        start = ai_response.index('===RECIPE START===') + len('===RECIPE START===')
        end = ai_response.index('===RECIPE END===')
        recipe_text = ai_response[start:end].strip()

        lines = recipe_text.split('\n')

        recipe_data = {
            'recipe_name': '',
            'ingredients': '',
            'preparation_steps': '',
            'cooking_time': 30,
            'servings': 4,
            'difficulty': 'medium',
            'category': 'dinner'
        }

        current_section = None
        ingredients_list = []
        steps_list = []
        tips_list = []

        for line in lines:
            line = line.strip()

            if line.startswith('RECIPE NAME:'):
                recipe_data['recipe_name'] = line.replace('RECIPE NAME:', '').strip()
            elif line.startswith('COOKING TIME:'):
                try:
                    time_str = line.replace('COOKING TIME:', '').strip()
                    recipe_data['cooking_time'] = int(''.join(filter(str.isdigit, time_str)))
                except Exception:
                    pass
            elif line.startswith('SERVINGS:'):
                try:
                    servings_str = line.replace('SERVINGS:', '').strip()
                    recipe_data['servings'] = int(''.join(filter(str.isdigit, servings_str)))
                except Exception:
                    pass
            elif line.startswith('DIFFICULTY:'):
                difficulty = line.replace('DIFFICULTY:', '').strip().lower()
                if difficulty in ['easy', 'medium', 'hard']:
                    recipe_data['difficulty'] = difficulty
            elif line.startswith('CATEGORY:'):
                category = line.replace('CATEGORY:', '').strip().lower()
                if category in ['breakfast', 'lunch', 'dinner', 'dessert', 'snack', 'appetizer']:
                    recipe_data['category'] = category
            elif line.startswith('INGREDIENTS:'):
                current_section = 'ingredients'
            elif line.startswith('PREPARATION STEPS:'):
                current_section = 'steps'
            elif line.startswith('TIPS:'):
                current_section = 'tips'
            elif current_section == 'ingredients' and line:
                cleaned = line.lstrip('- ').lstrip('• ').lstrip('* ')
                if cleaned and not cleaned.startswith('PREPARATION'):
                    ingredients_list.append(cleaned)
            elif current_section == 'steps' and line:
                cleaned = line.lstrip('- ').lstrip('• ').lstrip('* ')
                cleaned = re.sub(r'^\d+[\.\)]\s*', '', cleaned)
                if cleaned and not cleaned.startswith('TIPS'):
                    steps_list.append(cleaned)
            elif current_section == 'tips' and line:
                cleaned = line.lstrip('- ').lstrip('• ').lstrip('* ')
                if cleaned:
                    tips_list.append(cleaned)

        recipe_data['ingredients'] = '\n'.join(ingredients_list)

        all_steps = steps_list
        if tips_list:
            all_steps.append('\n--- Cooking Tips ---')
            all_steps.extend(tips_list)

        recipe_data['preparation_steps'] = '\n'.join(all_steps)

        return recipe_data if recipe_data['recipe_name'] else None

    except Exception as e:
        print(f"Error extracting recipe: {e}")
        return None


@csrf_exempt
def save_recipe_from_chat(request):
    """
    Save recipe generated from chat to database
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)

    try:
        from .models import Recipe

        data = json.loads(request.body)

        recipe = Recipe.objects.create(
            recipe_name=data['recipe_name'],
            ingredients=data['ingredients'],
            preparation_steps=data['preparation_steps'],
            cooking_time=data.get('cooking_time', 30),
            servings=data.get('servings', 4),
            difficulty=data.get('difficulty', 'medium'),
            category=data.get('category', 'dinner'),
            is_ai_generated=True
        )

        return JsonResponse({
            'success': True,
            'recipe_id': recipe.id,
            'message': f'Recipe "{recipe.recipe_name}" saved successfully!'
        })

    except Exception as e:
        return JsonResponse({
            'error': str(e),
            'success': False
        }, status=500)