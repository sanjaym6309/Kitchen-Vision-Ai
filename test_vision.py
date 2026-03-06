import os
from dotenv import load_dotenv

load_dotenv()

from services.vision_service import detect_ingredients

with open(r"C:\Users\Sanjay\.gemini\antigravity\brain\951788f4-efcf-4c6c-8559-1ac6a59a429c\sample_pantry_1772729712451.png", "rb") as f:
    img_bytes = f.read()
    
print("Calling Vision API...")
try:
    ingredients = detect_ingredients(img_bytes)
    print("Result:")
    print(ingredients)
except Exception as e:
    print(f"Exception: {e}")
