import streamlit as st
import requests
import pickle
from auth import authenticate
from disease_modules.diabetes import show_diabetes_page
from disease_modules.heart_disease import show_heart_page
from disease_modules.parkinsons import show_parkinsons_page
from disease_modules.lung_cancer import show_lung_cancer_page
from disease_modules.hypothyroid import show_thyroid_page

# GitHub base URL for raw files
GITHUB_BASE_URL = "https://raw.githubusercontent.com/Harshu0503/Medical-Diagnosis-Prediction-AI/main/"

# Set page config first
st.set_page_config(page_title="AI Medical Diagnosis", page_icon="⚕️", layout="wide")

# Load CSS from GitHub
def load_css():
    url = GITHUB_BASE_URL + "styles.css"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            st.markdown(f"<style>{response.text}</style>", unsafe_allow_html=True)
        else:
            st.warning("⚠️ Unable to load custom CSS.")
    except Exception as e:
        st.warning(f"⚠️ Error loading CSS: {e}")

# Load models from GitHub
def load_models():
    model_files = {
        "diabetes": "Models/diabetes_model.sav",
        "heart": "Models/heart_disease_model.sav",
        "parkinsons": "Models/parkinsons_model.sav",
        "lung_cancer": "Models/lungs_disease_model.sav",
        "thyroid": "Models/Thyroid_model.sav"
    }
    models = {}
    for key, path in model_files.items():
        url = GITHUB_BASE_URL + path
        response = requests.get(url)
        if response.status_code == 200:
            models[key] = pickle.loads(response.content)
        else:
            raise Exception(f"Model '{key}' not found at {url}")
    return models

# Main function
def main():
    load_css()

    # Authenticate user
    if not authenticate():
        return

    st.title("🧠 AI Medical Diagnosis System")

    # Load all models
    try:
        models = load_models()
    except Exception as e:
        st.error(f"❌ Failed to load models: {e}")
        st.stop()

    # Query params getter and setter
    query = st.query_params

    # Disease options
    disease_options = {
        "diabetes": "Diabetes Prediction",
        "heart": "Heart Disease Prediction",
        "parkinsons": "Parkinson's Prediction",
        "lung-cancer": "Lung Cancer Prediction",
        "thyroid": "Hypo-Thyroid Prediction"
    }

    # Get default selection from query param
    selected_key = query.get("page", "diabetes")
    default_label = disease_options.get(selected_key, "Diabetes Prediction")

    # Center the dropdown using columns
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        disease = st.selectbox(
            "🩺 Select a Disease Prediction Model",
            list(disease_options.values()),
            index=list(disease_options.values()).index(default_label)
        )

    # Update query param
    selected_key = [k for k, v in disease_options.items() if v == disease][0]
    query.update(page=selected_key)

    # Show selected disease module
    if disease == "Diabetes Prediction":
        show_diabetes_page(models["diabetes"])
    elif disease == "Heart Disease Prediction":
        show_heart_page(models["heart"])
    elif disease == "Parkinson's Prediction":
        show_parkinsons_page(models["parkinsons"])
    elif disease == "Lung Cancer Prediction":
        show_lung_cancer_page(models["lung_cancer"])
    elif disease == "Hypo-Thyroid Prediction":
        show_thyroid_page(models["thyroid"])

if __name__ == "__main__":
    main()
