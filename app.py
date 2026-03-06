import streamlit as st
from dotenv import load_dotenv
import os
import logging

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

from utils.image_utils import preprocess_image
from services.vision_service import detect_ingredients
from utils.categorization_utils import categorize_ingredients
from services.recipe_service import generate_recipes
from services.grocery_service import generate_grocery_list_and_subs

# Load environment variables
load_dotenv()

st.set_page_config(
    page_title="Kitchen Vision",
    page_icon="🍳",
    layout="wide"
)

def main():
    st.title("Kitchen Vision 🍳")
    st.subheader("AI-Powered Pantry Analysis and Smart Recipe Recommendation")
    
    st.markdown("Upload an image of your open pantry to get organized ingredients, recipes, and health scores.")
    
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.image(uploaded_file, caption='Uploaded Pantry Image', width='stretch')
            
        with col2:
            st.write("### Analysis Results")
            image_bytes = uploaded_file.getvalue()
            
            with st.spinner("Processing image..."):
                try:
                    processed_bytes = preprocess_image(image_bytes)
                except Exception as e:
                    st.error(f"Error processing image: {e}")
                    return

            with st.spinner("Detecting ingredients using Vision AI..."):
                ingredients = detect_ingredients(processed_bytes)
                
            if not ingredients:
                st.warning("No ingredients detected. Please try a clearer image.")
                return
                
            with st.spinner("Categorizing ingredients..."):
                categorized = categorize_ingredients(ingredients)
                
            st.success(f"Detected {len(ingredients)} ingredients!")
            
            # Display Categorized Items
            st.write("#### 📦 Categorized Pantry")
            cat_cols = st.columns(4)
            categories = ["Dry Storage", "Cold Storage", "Frozen", "Fresh Produce"]
            icons = ["🥫", "🥛", "❄️", "🥬"]
            
            for idx, cat in enumerate(categories):
                with cat_cols[idx]:
                    st.markdown(f"**{icons[idx]} {cat}**")
                    items = categorized.get(cat, [])
                    if items:
                        for item in items:
                            st.markdown(f"- {item.capitalize()}")
                    else:
                        st.markdown("_Empty_")
                        
            st.divider()
            
            # Generate Recipes
            with st.spinner("Generating healthy beginner-friendly recipes..."):
                recipes = generate_recipes(ingredients)
                
            if recipes:
                st.write("#### 🍽️ Recommended Recipes")
                
                recipe_tabs = st.tabs([f"Recipe {i+1}: {r.get('title', 'Untitled')}" for i, r in enumerate(recipes)])
                
                for i, recipe in enumerate(recipes):
                    with recipe_tabs[i]:
                        st.markdown(f"### {recipe.get('title', 'Unknown Recipe')}")
                        
                        r_col1, r_col2 = st.columns([1, 1])
                        
                        with r_col1:
                            st.markdown(f"**⏱️ Prep Time:** {recipe.get('prep_time_mins', 'N/A')} mins")
                            st.markdown(f"**📊 Difficulty:** {recipe.get('difficulty', 'Beginner')}")
                            
                            score = recipe.get('health_score', 'N/A')
                            st.markdown(f"**❤️ Health Score:** {score}/10")
                            st.info(recipe.get('health_explanation', 'No explanation provided.'))
                            
                            st.write("**Ingredients Required:**")
                            recipe_reqs = recipe.get('ingredients_needed', [])
                            for req in recipe_reqs:
                                st.markdown(f"- {req}")
                                
                        with r_col2:
                            st.write("**Instructions:**")
                            for idx, step in enumerate(recipe.get('instructions_3_steps', [])):
                                st.markdown(f"{idx+1}. {step}")
                                
                        st.divider()
                        
                        st.write("#### 🛒 Grocery List & Substitutions")
                        with st.spinner("Checking missing items and finding substitutions..."):
                            subs = generate_grocery_list_and_subs(ingredients, recipe_reqs)
                            
                        if not subs:
                            st.success("You have all the ingredients for this recipe!")
                        else:
                            for sub_item in subs:
                                missing = sub_item.get('missing_item', 'Unknown')
                                alternatives = sub_item.get('substitutes', [])
                                
                                st.markdown(f"**Missing:** `{missing}`")
                                if alternatives:
                                    st.markdown(f"   *Substitutes:* {', '.join(alternatives)}")
                                else:
                                    st.markdown("   *No obvious substitutes.*")

if __name__ == "__main__":
    main()
