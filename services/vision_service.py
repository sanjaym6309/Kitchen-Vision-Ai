import google.generativeai as genai
import os
import json
import logging

logger = logging.getLogger(__name__)

def detect_ingredients(image_bytes):
    """
    Calls the Gemini API to detect visible food items from the given image bytes.
    Returns a Python list of ingredient names.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        logger.error("GEMINI_API_KEY is not set.")
        raise ValueError("GEMINI_API_KEY is not set.")
    
    genai.configure(api_key=api_key)
    
    # We use gemini-2.5-flash for fast vision processing
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    prompt = '''
    You are an expert culinary AI. Carefully analyze the provided image of a pantry, fridge, or kitchen.
    List all visible food items and ingredients you can identify. 
    Consolidate duplicate items (e.g. if there are two apples, just list "apple").
    Return ONLY a JSON list of strings, representing the names of the detected ingredients.
    Do not include any formatting like ```json or newlines, just the raw JSON array.
    Example output: ["apple", "rice", "pasta", "tomato sauce"]
    '''
    
    parts = [
        prompt,
        {"mime_type": "image/jpeg", "data": image_bytes}
    ]
    
    try:
        response = model.generate_content(parts)
        text = response.text.strip()
        # Clean up potential markdown formatting if model didn't listen
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        
        try:
            ingredients = json.loads(text.strip())
        except json.JSONDecodeError:
            logger.error(f"Failed to parse JSON. Raw response: {text}")
            return []
            
        if not isinstance(ingredients, list):
            logger.error(f"Expected a list, got {type(ingredients)}: {ingredients}")
            return []
            
        return [str(item).lower() for item in ingredients]
    except Exception as e:
        logger.exception(f"Error calling Vision API: {e}")
        # In case it's a blocked prompt or something like that, try to print the raw response if available
        if 'response' in locals() and hasattr(response, 'text'):
            logger.error(f"Raw response: {response.text}")
        elif 'response' in locals() and hasattr(response, 'prompt_feedback'):
            logger.error(f"Prompt Feedback: {response.prompt_feedback}")
            
        return []
