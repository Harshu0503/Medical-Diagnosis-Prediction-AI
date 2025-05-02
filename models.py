import pickle
import requests
import io

def fetch_model_from_github(url):
    """
    Fetch a .sav model file from a GitHub raw URL and return the deserialized model.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        return pickle.load(io.BytesIO(response.content))
    except Exception as e:
        print(f"Error loading model from {url}: {e}")
        return None

def load_models():
    """
    Load all required ML models from GitHub with error handling.
    Returns a dictionary of models.
    """
    base_url = "https://github.com/Harshu0503/Medical-Diagnosis-Prediction-AI/tree/4c9c56746a8c50c719be38519f882c3bacb93cd1/Models"

    model_files = {
        'diabetes': 'diabetes_model.sav',
        'heart': 'heart_disease_model.sav',
        'parkinsons': 'parkinsons_model.sav',
        'lung_cancer': 'lungs_disease_model.sav',
        'thyroid': 'hypothyroid_rf_model.sav'
    }

    models = {}
    for key, filename in model_files.items():
        full_url = base_url + filename
        model = fetch_model_from_github(full_url)
        if model:
            models[key] = model
        else:
            print(f"❌ Failed to load model: {key} from {full_url}")
    return models
