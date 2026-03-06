from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
import logging
from sqlalchemy.orm import Session

# Import existing services
from services.vision_service import detect_ingredients
from utils.categorization_utils import categorize_ingredients
from services.recipe_service import generate_recipes
from services.grocery_service import generate_grocery_list_and_subs
from utils.image_utils import preprocess_image
from database import SessionLocal, AnalysisHistory

load_dotenv()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("kitchen-api")

app = FastAPI(title="Kitchen Vision API")

# Enable CORS for React development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the actual origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Kitchen Vision API is running"}

@app.post("/api/analyze")
async def analyze_pantry(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Complete pipeline: Preprocess -> Detect -> Categorize
    """
    try:
        contents = await file.read()
        
        # 1. Preprocess
        processed_img = preprocess_image(contents)
        
        # 2. Detect
        ingredients = detect_ingredients(processed_img)
        if not ingredients:
            return {
                "success": False,
                "message": "No ingredients detected. Please try a clearer image.",
                "data": None
            }
            
        # 3. Categorize
        categorized = categorize_ingredients(ingredients)
        
        # 4. Generate Initial Recipes (to store in history)
        recipes = generate_recipes(ingredients)

        # 5. Save to History
        history_entry = AnalysisHistory(
            ingredients=ingredients,
            categorized=categorized,
            recipes=recipes
        )
        db.add(history_entry)
        db.commit()
        db.refresh(history_entry)
        
        return {
            "success": True,
            "id": history_entry.id,
            "ingredients": ingredients,
            "categorized": categorized,
            "recipes": recipes
        }
    except Exception as e:
        logger.exception("Error in analysis pipeline")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/history")
async def get_history(db: Session = Depends(get_db)):
    """
    Retrieve all past scan history.
    """
    try:
        history = db.query(AnalysisHistory).order_by(AnalysisHistory.timestamp.desc()).all()
        return {"success": True, "history": history}
    except Exception as e:
        logger.exception("Error fetching history")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/recipes")
async def get_recipes(data: dict):
    """
    Generates recipes based on a list of ingredients.
    Expects: {"ingredients": ["item1", "item2"]}
    """
    ingredients = data.get("ingredients", [])
    if not ingredients:
        raise HTTPException(status_code=400, detail="No ingredients provided")
        
    try:
        recipes = generate_recipes(ingredients)
        return {"success": True, "recipes": recipes}
    except Exception as e:
        logger.exception("Error generating recipes")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/grocery")
async def get_grocery(data: dict):
    """
    Identifies missing items and suggests substitutions.
    Expects: {"available": [...], "recipe": [...]}
    """
    available = data.get("available", [])
    recipe = data.get("recipe", [])
    
    try:
        grocery_data = generate_grocery_list_and_subs(available, recipe)
        return {"success": True, "grocery": grocery_data}
    except Exception as e:
        logger.exception("Error generating grocery list")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
