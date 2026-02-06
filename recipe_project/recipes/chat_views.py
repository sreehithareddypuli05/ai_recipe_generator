from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests


def ai_chat_generator(request):
    """
    Interactive ChatGPT-style recipe generator page (Using Ollama - Local & Free!)
    """
    # Check if Ollama is running
    ollama_available = check_ollama_available()
    
    context = {
        'has_api_key': ollama_available
    }
    return render(request, 'recipes/ai_chat.html', context)


def check_ollama_available():
    """Check if Ollama is running"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=2)
        return response.status_code == 200
    except:
        return False


@csrf_exempt
def chat_with_ai(request):
    """
    API endpoint for chatting with AI to generate recipes
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)
    
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '')
        conversation_history = data.get('history', [])
        
        if not user_message:
            return JsonResponse({'error': 'Message is required'}, status=400)
        
        # Get AI response
        ai_response = generate_ai_chat_response(user_message, conversation_history)
        
        # Check if AI generated a complete recipe
        recipe_data = extract_recipe_from_response(ai_response)
        
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
    Generate AI response using Ollama (Local AI - 100% Free!)
    """
    # Check if Ollama is running
    if not check_ollama_available():
        print("❌ Ollama not running")
        return generate_fallback_response()
    
    try:
        print("✅ Using Ollama (Local AI)")
        
        # Build conversation context
        conversation_context = ""
        
        # Add last 5 messages for context
        for msg in conversation_history[-5:]:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            if role == "user":
                conversation_context += f"\nUser: {content}"
            elif role == "assistant":
                conversation_context += f"\nAssistant: {content}"
        
        # Create the prompt
        full_prompt = f"""You are a friendly AI Recipe Assistant. Help users create recipes through natural conversation.

Guidelines:
- Be warm, conversational, and helpful
- Respond naturally to greetings and casual conversation  
- When users mention ingredients, ask clarifying questions ONE AT A TIME
- Remember what the user has told you
- When you have enough information, generate a complete recipe

When generating a recipe, use this EXACT format:

===RECIPE START===
RECIPE NAME: <creative recipe name>
COOKING TIME: <number only>
SERVINGS: <number only>
DIFFICULTY: <easy/medium/hard>
CATEGORY: <breakfast/lunch/dinner/dessert/snack>

INGREDIENTS:
- <amount> <ingredient>
- <amount> <ingredient>

PREPARATION STEPS:
1. <detailed step>
2. <detailed step>

TIPS:
- <helpful tip>
===RECIPE END===

For casual conversation, respond naturally without the recipe format.

Previous conversation:
{conversation_context}

Current message:
User: {user_message}

Respond as the Assistant (be concise and friendly):"""
        
        # Call Ollama API
        ollama_url = "http://localhost:11434/api/generate"
        payload = {
            "model": "llama3.2",  # You can change this to "mistral", "phi3", etc.
            "prompt": full_prompt,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "top_p": 0.9,
                "num_predict": 500  # Limit response length
            }
        }
        
        print(f"🤖 Calling Ollama...")
        
        response = requests.post(
            ollama_url,
            json=payload,
            timeout=60  # Give Ollama time to respond
        )
        
        if response.status_code == 200:
            result = response.json()
            ai_response = result.get('response', '').strip()
            
            print(f"✅ Got response from Ollama ({len(ai_response)} chars)")
            
            return ai_response
        else:
            print(f"❌ Ollama Error: {response.status_code}")
            return "I'm having trouble right now. Please make sure Ollama is running with: ollama serve"
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Ollama")
        return generate_fallback_response()
    
    except requests.exceptions.Timeout:
        print("⏱️ Ollama timeout")
        return "The AI is taking too long to respond. This might happen on the first request. Please try again!"
    
    except Exception as e:
        print(f"❌ Error: {type(e).__name__}: {e}")
        return f"Something went wrong: {str(e)}"


def generate_fallback_response():
    """
    Generate response when Ollama is not available
    """
    return """⚠️ Ollama is not running!

To use FREE local AI:

1. Install Ollama from: https://ollama.ai
2. Open a terminal and run: ollama pull llama3.2
3. Start Ollama: ollama serve
4. Refresh this page

Ollama is 100% FREE and runs locally on your computer!

Alternative models you can use:
- ollama pull mistral
- ollama pull phi3
- ollama pull gemma2

After setup, you'll have unlimited, free AI with no internet required! 🎉"""


def extract_recipe_from_response(ai_response):
    """
    Extract structured recipe data from AI response
    """
    if '===RECIPE START===' not in ai_response or '===RECIPE END===' not in ai_response:
        return None
    
    try:
        # Extract recipe section
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
                except:
                    pass
            elif line.startswith('SERVINGS:'):
                try:
                    servings_str = line.replace('SERVINGS:', '').strip()
                    recipe_data['servings'] = int(''.join(filter(str.isdigit, servings_str)))
                except:
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
                import re
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
        
        # Create recipe
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