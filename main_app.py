import streamlit as st
from models import load_models
from auth import authenticate
from disease_modules.diabetes import show_diabetes_page
from disease_modules.heart_disease import show_heart_page
from disease_modules.parkinsons import show_parkinsons_page
from disease_modules.lung_cancer import show_lung_cancer_page
from disease_modules.hypothyroid import show_thyroid_page

# Set page config first
st.set_page_config(page_title="AI Medical Diagnosis", page_icon="⚕️", layout="wide")

# Load CSS styling
def load_css():
    with open("styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

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
