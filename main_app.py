import streamlit as st
import requests
from auth import authenticate
from disease_modules.diabetes import show_diabetes_page
from disease_modules.heart_disease import show_heart_page
from disease_modules.parkinsons import show_parkinsons_page
from disease_modules.lung_cancer import show_lung_cancer_page
from disease_modules.hypothyroid import show_thyroid_page
from disease_modules.covid_prediction import show_covid_page
from models import load_models

# GitHub base URL for CSS
GITHUB_BASE_URL = "https://raw.githubusercontent.com/Harshu0503/Medical-Diagnosis-Prediction-AI/master/"

# Page config
st.set_page_config(page_title="AI Medical Diagnosis", page_icon="⚕️", layout="wide")

# Load custom CSS
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

def main():
    load_css()

    # Authentication
    if not authenticate():
        return

    # Logout Button on top-right
    col1, col2 = st.columns([5, 1])
    with col2:
        if st.button("Logout"):
            st.session_state.clear()
            st.session_state.logged_out = True
            st.rerun()

    # Centered title using HTML
    st.markdown("<h1 style='text-align: center;'>🧠 AI Medical Diagnosis System</h1>", unsafe_allow_html=True)

    # Load models
    try:
        models = load_models()
    except Exception as e:
        st.error(f"❌ Failed to load models: {e}")
        st.stop()

    # Disease options
    disease_options = {
        "diabetes": "Diabetes Prediction",
        "heart": "Heart Disease Prediction",
        "parkinsons": "Parkinson's Prediction",
        "lung_cancer": "Lung Cancer Prediction",
        "thyroid": "Hypo-Thyroid Prediction",
        "covid": "COVID-19 Prediction"
    }

    # Query param handling
    query_params = st.query_params
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

    # Update query param
    selected_key = next(k for k, v in disease_options.items() if v == disease)
    st.query_params.page = selected_key

    # Display selected page
    if selected_key == "diabetes":
        show_diabetes_page(models["diabetes"])
    elif selected_key == "heart":
        show_heart_page(models["heart"])
    elif selected_key == "parkinsons":
        show_parkinsons_page(models["parkinsons"])
    elif selected_key == "lung_cancer":
        show_lung_cancer_page(models["lung_cancer"])
    elif selected_key == "thyroid":
        show_thyroid_page(models["thyroid"])
    elif selected_key == "covid":
        show_covid_page(models["covid"])

if __name__ == "__main__":
    main()
