import pickle

def load_models():
    """Load all ML models with error handling"""
    models = {
        'diabetes': None,
        'heart': None,
        'parkinsons': None,
        'lung_cancer': None,
        'thyroid': None
    }

    try:
        models['diabetes'] = pickle.load(open('H:/Harshu/Projects/Medical Disease Prediction/Models/diabetes_model.sav', 'rb'))
        models['heart'] = pickle.load(open('H:/Harshu/Projects/Medical Disease Prediction/Models/heart_disease_model.sav', 'rb'))
        models['parkinsons'] = pickle.load(open('H:/Harshu/Projects/Medical Disease Prediction/Models/parkinsons_model.sav', 'rb'))
        models['lung_cancer'] = pickle.load(open('H:/Harshu/Projects/Medical Disease Prediction/Models/lungs_disease_model.sav', 'rb'))
        models['thyroid'] = pickle.load(open('H:/Harshu/Projects/Medical Disease Prediction/Models/Thyroid_model.sav', 'rb'))
    except Exception as e:
        print(f"Model loading failed: {e}")
        raise e  # Let the main app handle or crash with a clear error

    return models
