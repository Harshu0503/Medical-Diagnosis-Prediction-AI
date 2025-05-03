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

        # Check for valid binary content (to avoid HTML fallback from GitHub)
        content_type = response.headers.get("Content-Type", "")
        if "text/html" in content_type:
            raise ValueError("URL returned HTML instead of a binary file. Check if the URL is a raw link.")

        return pickle.load(io.BytesIO(response.content))

    except Exception as e:
        print(f"❌ Error loading model from {url}: {e}")
        return None

def load_models():
    """
    Load all required ML models from GitHub with error handling.
    Returns a dictionary of models.
    """
    # ✅ Use the RAW GitHub link to directly fetch binary model files
    base_url = "https://raw.githubusercontent.com/Harshu0503/Medical-Diagnosis-Prediction-AI/master/Models/"

    model_files = {
        'diabetes': 'diabetes_model.sav',
        'heart': 'heart_disease_model.sav',
        'parkinsons': 'parkinsons_model.sav',
        'lung_cancer': 'lungs_disease_model.sav',
        'thyroid': 'Models/hypothyroid_rf_model.sav'
    }

    models = {}

    for key, filename in model_files.items():
        full_url = base_url + filename
        print(f"🔄 Loading model: {key} from {full_url}")
        model = fetch_model_from_github(full_url)

        if model is not None:  # ✅ FIXED: Don't use `if model` (ambiguous for NumPy objects)
            print(f"✅ Loaded: {key}")
            models[key] = model
        else:
            print(f"❌ Failed to load model: {key}")

    return models
