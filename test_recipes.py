import os
from dotenv import load_dotenv
import logging

load_dotenv()
logging.basicConfig(level=logging.INFO)

from services.recipe_service import generate_recipes

ingredients = ['pasta', 'basmati rice', 'brown rice', 'spices', 'canned diced tomatoes', 
               'canned black beans', 'canned garbanzo beans', 'canned corn', 
               'canned green beans', 'salt', 'pepper', 'olive oil', 'cooking oil', 
               'pasta sauce', 'canned soup', 'cheerios cereal', 'granola cereal', 
               'oatmeal', 'butter', 'cream cheese', 'yogurt', 'orange juice', 
               'jam', 'tomatoes', 'eggs', 'lettuce', 'red apples', 'green apples', 
               'milk', 'bottled water', 'frozen peas', 'frozen corn', 'frozen broccoli', 
               'chicken breasts', 'ice cream', 'ice']

print(f"Calling Recipe API with {len(ingredients)} items...")
try:
    recipes = generate_recipes(ingredients)
    print(f"Result (Found {len(recipes)} recipes):")
    if recipes:
        for r in recipes:
            print(f"- {r.get('title')} (Score: {r.get('health_score')})")
    else:
        print("No recipes returned.")
except Exception as e:
    print(f"Exception: {e}")
