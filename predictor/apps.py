from django.apps import AppConfig
import os
import tensorflow as tf  # Use the common practice of importing TensorFlow
class PredictorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'predictor'

 # Add this attribute to store the model
    model = None

    def ready(self):
        # Load the model and store it in the 'model' attribute
        model_path = os.path.join(os.path.dirname(__file__), 'models', '1726962858.h5')
        PredictorConfig.model = tf.keras.models.load_model(model_path)  # Use TensorFlow to load the model

        