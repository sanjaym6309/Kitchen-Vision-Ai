# Kitchen Vision 🍳

### Team Members
| Name | Role | Email |
| :--- | :--- | :--- |
| **SARIGASREE SANDHIYAPPAN** | Team Lead | 6314@velsrscollege.com |
| **MONISHA S** | Member | 6288@velsrscollege.com |
| **DIVYA BHARATHI S** | Member | 6251@velsrscollege.com |


AI-Powered Pantry Analysis and Smart Recipe Recommendation System built with Python and Streamlit. This application transforms a snapshot of your pantry into organized ingredient lists, healthy recipe suggestions, and smart grocery checklists.

## Features

- **Pantry Image Analysis**: Upload a picture of your pantry or fridge, and the Gemini Vision AI detects visible food items.
- **Auto-Categorization**: Ingredients are automatically sorted into Storage Types (Dry, Cold, Frozen, Fresh Produce).
- **Smart Recipe Generation**: Suggests 3 beginner-friendly, healthy recipes based almost entirely on what you already have.
- **Health Evaluation**: Rates each generated recipe on a 1-10 nutritional scale with explanations.
- **Grocery Planner & Substitutions**: Cross-references recipe requirements with your pantry, builds a shopping checklist, and offers clever substitutions for missing ingredients.

## Project Structure

```text
Kitchen AI/
├── app.py                      # Main Streamlit user interface
├── requirements.txt            # Python dependencies
├── .env                        # Configuration / API keys
├── services/
│   ├── vision_service.py       # Handles AI image analysis via Gemini 2.5 Flash
│   ├── recipe_service.py       # Generates recipes & health scores via Gemini 2.5 Pro
│   └── grocery_service.py      # Computes missing items and substitutions
└── utils/
    ├── image_utils.py          # OpenCV preprocessing (resize, contrast)
    └── categorization_utils.py # AI-assisted ingredient mapping
```

## Setup & Installation

1. **Clone or Download the Repository**
2. **Install Python 3.9+**
3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure your Environment Variables:**
   Create a `.env` file in the root directory and add your Google Gemini API key:
   ```env
   GEMINI_API_KEY=your_actual_api_key_here
   ```

## Running the Application

Start the Streamlit development server:

```bash
streamlit run app.py
```

The application will launch in your default web browser (usually at `http://localhost:8501`).

## Usage

1. Click **"Browse files"** to upload an image of your kitchen pantry (`.jpg`, `.png`, `.jpeg`).
2. Wait a few moments as the system processes the image, detects ingredients, and categorizes them.
3. Review the **Categorized Pantry** list to see what the AI found.
4. Browse the **Recommended Recipes** tabs to discover meal ideas, complete with prep times and health scores.
5. Check the **Grocery List & Substitutions** section at the bottom of each recipe if you are missing any required ingredients.

## Technologies Used

- **Python**: Core backend logic.
- **Streamlit**: Fast web app framework for the UI.
- **Google Generative AI (Gemini 2.5)**: Powers the vision detection, recipe generation, categorization, and substitution logic.
- **OpenCV (`cv2`)**: Used for image enhancement, resizing, and normalization before passing images to the Vision API.
