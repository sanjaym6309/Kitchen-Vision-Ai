import json
import google.generativeai as genai
import os
import logging

logger = logging.getLogger(__name__)

def generate_recipes(available_ingredients):
    """
    Generates 3 beginner-friendly recipes based on the available ingredients.
    Includes health evaluation.
    """
    if not available_ingredients:
        return []

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        logger.error("GEMINI_API_KEY is not set.")
        raise ValueError("GEMINI_API_KEY is not set.")
    
    genai.configure(api_key=api_key)
    # Using 2.5-flash to ensure higher quota availability
    model = genai.GenerativeModel('gemini-2.5-flash')

    prompt = f'''
    You are an expert chef and nutritionist. Based mainly on the following available ingredients, 
    generate EXACTLY 3 simple, beginner-friendly recipes. 
    It is okay to include a few basic pantry staples (like salt, pepper, oil, water) or missing ingredients if necessary, 
    but try to use what is available.
    
    Available ingredients:
    {json.dumps(available_ingredients)}

    For each recipe, also evaluate its health score on a scale of 1-10 based on heuristic logic 
    (ingredient composition, estimated calories, protein content, fiber, fat levels) and provide a short explanation.

    Return the result as a raw JSON array of 3 recipe objects.
    Do not use formatting like ```json. Just return raw JSON.
    Example format for each object in the array:
    {{
      "title": "Recipe Name",
      "ingredients_needed": ["list", "of", "all", "required", "ingredients"],
      "instructions_3_steps": ["step 1", "step 2", "step 3"],
      "prep_time_mins": 15,
      "difficulty": "Beginner",
      "health_score": 8,
      "health_explanation": "Good balance of protein and low in complex fats..."
    }}
    '''

    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
            
        recipes = json.loads(text.strip())
        return recipes
    except Exception as e:
        logger.exception(f"Error generating recipes: {e}")
        return []
