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

        # Check for valid binary content
        content_type = response.headers.get("Content-Type", "")
        if "text/html" in content_type:
            raise ValueError("URL returned HTML content, not a binary file.")

        return pickle.load(io.BytesIO(response.content))
    except Exception as e:
        print(f"❌ Error loading model from {url}: {e}")
        return None

def load_models():
    """
    Load all required ML models from GitHub with error handling.
    Returns a dictionary of models.
    """
    # ✅ Raw GitHub URL to model files
    base_url = "https://raw.githubusercontent.com/Harshu0503/Medical-Diagnosis-Prediction-AI/4c9c56746a8c50c719be38519f882c3bacb93cd1/Models/"

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
        print(f"🔄 Loading model: {key} from {full_url}")
        model = fetch_model_from_github(full_url)
        if model:
            print(f"✅ Loaded: {key}")
            models[key] = model
        else:
            print(f"❌ Failed to load model: {key}")
    return models
