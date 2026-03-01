from django.apps import AppConfig
from django.conf import settings
import os
# import tensorflow as tf
import joblib

class PredictionConfig(AppConfig):
    # default_auto_field = 'django.db.models.BigAutoField' #auto generate unique ID
    name = 'prediction'

_MODEL = None

def get_model():
    global _MODEL
    if _MODEL is None:
        model_path = os.path.join(
            settings.MODELS,
            "fraud_ensemble_model.pkl"
        )
        _MODEL = joblib.load(model_path)
    return _MODEL

