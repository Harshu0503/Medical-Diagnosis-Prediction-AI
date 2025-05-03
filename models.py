import pickle
import requests
import io

def fetch_model_from_github(url):
    """
    Fetch a .sav model file from a GitHub raw URL and return the deserialized model.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Will raise an exception for non-2xx status codes
        
        # Check if the response contains binary content
        if response.content:
            print("Model fetched successfully.")  # Debugging line to confirm model fetching
            return pickle.load(io.BytesIO(response.content))
        else:
            raise Exception("Model file is empty.")
    except requests.exceptions.RequestException as req_err:
        print(f"Request failed: {req_err}")
    except Exception as e:
        print(f"Error loading model from {url}: {e}")
    return None

def load_models():
    """
    Load all required ML models from GitHub with error handling.
    Returns a dictionary of models.
    """
    base_url = "https://raw.githubusercontent.com/Harshu0503/Medical-Diagnosis-Prediction-AI/master/Models/"

    model_files = {
        'diabetes': 'diabetes_model.sav',
        'heart': 'heart_disease_model.sav',
        'parkinsons': 'parkinsons_model.sav',
        'lung_cancer': 'lungs_disease_model.sav',
        'thyroid': 'hypothyroid_rf_model.sav'  # Correct path for thyroid model
    }

    models = {}
    for key, filename in model_files.items():
        full_url = base_url + filename
        print(f"Fetching model from: {full_url}")  # Debugging line to check the URL being used
        model = fetch_model_from_github(full_url)
        if model:
            models[key] = model
            print(f"Successfully loaded model: {key}")  # Debugging success
        else:
            print(f"❌ Failed to load model: {key} from {full_url}")  # Debugging failure message
    return models
