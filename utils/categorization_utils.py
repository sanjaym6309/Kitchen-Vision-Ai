import json
import google.generativeai as genai
import os
import logging

logger = logging.getLogger(__name__)

def categorize_ingredients(ingredients):
    """
    Categorize a list of ingredients into 'Dry Storage', 'Cold Storage', 'Frozen', or 'Fresh Produce'.
    Uses a lightweight Gemini call (or local logic) to sort them intelligently.
    Returns a dictionary mapping categories to lists of items.
    """
    if not ingredients:
        return {"Dry Storage": [], "Cold Storage": [], "Frozen": [], "Fresh Produce": []}

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        logger.error("GEMINI_API_KEY is not set.")
        raise ValueError("GEMINI_API_KEY is not set.")
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')

    prompt = f'''
    You are an intelligent kitchen assistant. Categorize the following ingredients into exactly four storage types:
    "Dry Storage", "Cold Storage", "Frozen", and "Fresh Produce".

    Ingredients to categorize:
    {json.dumps(ingredients)}

    Return ONLY a raw JSON object where keys are the four categories, and values are arrays of strings (the ingredients).
    Do not use markdown blocks like ```json. Just raw text starting with {{ and ending with }}.
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
            
        categorized = json.loads(text.strip())
        
        # Ensure all required keys exist
        default_categories = ["Dry Storage", "Cold Storage", "Frozen", "Fresh Produce"]
        for cat in default_categories:
            if cat not in categorized:
                categorized[cat] = []
                
        return categorized
    except Exception as e:
        logger.exception(f"Error during categorization: {e}")
        # Fallback to putting everything in Dry Storage if API fails just to not break the UI
        return {
            "Dry Storage": ingredients,
            "Cold Storage": [],
            "Frozen": [],
            "Fresh Produce": []
        }
