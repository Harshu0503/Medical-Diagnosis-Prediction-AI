import pickle
import requests
import io

def fetch_model_from_github(url):
    """Fetch a .sav model file from a GitHub raw URL"""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return pickle.load(io.BytesIO(response.content))
    except Exception as e:
        print(f"Error loading model from {url}: {e}")
        return None

def load_models():
    """Load all ML models from GitHub with error handling"""
    base_url = "https://raw.githubusercontent.com/Harshu0503/Medical-Diagnosis-Prediction-AI/281044719caabf5dabbec3667e81829efaa25aad/Models/"

    model_files = {
        'diabetes': 'diabetes_model.sav',
        'heart': 'heart_disease_model.sav',
        'parkinsons': 'parkinsons_model.sav',
        'lung_cancer': 'lungs_disease_model.sav',
        'thyroid': 'hypothyroid_rf_model.sav',
        'covid': 'covid19_prediction_model.sav'
    }

    models = {}
    for key, filename in model_files.items():
        full_url = base_url + filename
        models[key] = fetch_model_from_github(full_url)

    return models
