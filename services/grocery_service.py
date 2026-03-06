import json
import google.generativeai as genai
import os
import logging

logger = logging.getLogger(__name__)


def generate_grocery_list_and_subs(available_ingredients, recipe_ingredients):
    """
    Compares what is needed for a recipe vs what is available.
    Identifies missing ingredients and uses Gemini to suggest substitutes.
    Returns a list of dictionaries with missing items and substitution suggestions.
    """
    # Simply lowercase and strip for basic matching
    avail_lower = set([item.lower().strip() for item in available_ingredients])
    req_lower = set([item.lower().strip() for item in recipe_ingredients])
    
    # Very basic list difference logic. Often NLP is needed to truly match "olive oil" vs "oil"
    missing = list(req_lower - avail_lower)
    
    if not missing:
        return []

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        logger.error("GEMINI_API_KEY is not set.")
        raise ValueError("GEMINI_API_KEY is not set.")
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')

    prompt = f'''
    You are a culinary expert. I need substitutions for the following missing ingredients:
    {json.dumps(missing)}
    
    I currently have these items in my pantry:
    {json.dumps(available_ingredients)}
    
    For each missing ingredient, suggest 1-2 practical substitutes. Prioritize items I already have if they make sense, otherwise suggest common household alternatives.
    
    Return a raw JSON array of objects. Do not use ```json blocks. 
    Format example:
    [
      {{
        "missing_item": "tomato sauce",
        "substitutes": ["crushed tomatoes", "tomato paste with water"]
      }}
    ]
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
            
        subs = json.loads(text.strip())
        return subs
    except Exception as e:
        logger.exception(f"Error generating substitutes: {e}")
        # Fallback format
        return [{"missing_item": item, "substitutes": ["No automated substitute found"]} for item in missing]
