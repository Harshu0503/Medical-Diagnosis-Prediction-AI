import streamlit as st
import requests
from auth import authenticate
from disease_modules.diabetes import show_diabetes_page
from disease_modules.heart_disease import show_heart_page
from disease_modules.parkinsons import show_parkinsons_page
from disease_modules.lung_cancer import show_lung_cancer_page
from disease_modules.hypothyroid import show_thyroid_page
from disease_modules.covid_prediction import show_covid_page
from models import load_models  # ✅ Fixed import

# GitHub base URL for raw files (for CSS only)
GITHUB_BASE_URL = "https://raw.githubusercontent.com/Harshu0503/Medical-Diagnosis-Prediction-AI/master/"

# Set Streamlit page configuration
st.set_page_config(page_title="AI Medical Diagnosis", page_icon="⚕️", layout="wide")

# Load and apply custom CSS from GitHub
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

# Main Streamlit app
def main():
    load_css()

    # Authenticate user
    if not authenticate():
        return

    st.title("🧠 AI Medical Diagnosis System")

    # Load models
    try:
        models = load_models()
    except Exception as e:
        st.error(f"❌ Failed to load models: {e}")
        st.stop()

    # Define available disease prediction options
    disease_options = {
        "diabetes": "Diabetes Prediction",
        "heart": "Heart Disease Prediction",
        "parkinsons": "Parkinson's Prediction",
        "lung_cancer": "Lung Cancer Prediction",
        "thyroid": "Hypo-Thyroid Prediction",
        "covid": "COVID-19 Prediction"
    }

    # Read query params and get selected disease
    query_params = st.query_params  # ✅ New usage
    selected_key = query_params.get("page", "diabetes")
    default_label = disease_options.get(selected_key, "Diabetes Prediction")

    # Center dropdown
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        disease = st.selectbox(
            "🩺 Select a Disease Prediction Model",
            list(disease_options.values()),
            index=list(disease_options.values()).index(default_label)
        )

    # Get disease key from value
    selected_key = next(k for k, v in disease_options.items() if v == disease)
    st.query_params.page = selected_key  # ✅ Update using new method

    # Show selected prediction module
    if selected_key == "diabetes":
        if "diabetes" in models:
            show_diabetes_page(models["diabetes"])
        else:
            st.error("❌ Diabetes Model not loaded. Please check model availability.")
    elif selected_key == "heart":
        if "heart" in models:
            show_heart_page(models["heart"])
        else:
            st.error("❌ Heart Model not loaded. Please check model availability.")
    elif selected_key == "parkinsons":
        if "parkinsons" in models:
            show_parkinsons_page(models["parkinsons"])
        else:
            st.error("❌ Parkinsons Model not loaded. Please check model availability.")
    elif selected_key == "lung_cancer":
        if "lung_cancer" in models:
            show_lung_cancer_page(models["lung_cancer"])
        else:
            st.error("❌ Lung Cancer Model not loaded. Please check model availability.")
    elif selected_key == "thyroid":
        if "thyroid" in models:
            show_thyroid_page(models["thyroid"])
        else:
            st.error("❌ Thyroid Model not loaded. Please check model availability.")
    
elif selected_key == "covid":
        if "covid" in models:
            show_thyroid_page(models["covid"])
        else:
            st.error("❌ Covid19 Model not loaded. Please check model availability.")
# Run the app
if __name__ == "__main__":
    main()
