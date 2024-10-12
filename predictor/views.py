import os
import numpy as np
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import default_storage
from .forms import ImageUploadForm
from .apps import PredictorConfig
from PIL import Image

def home(request):
    return render(request, 'predictor/home.html')

def preprocess_image(image_path):
    """Preprocess the image: convert to RGB, resize, normalize, and add batch dimension."""
    img = Image.open(image_path).convert('RGB').resize((96, 96))
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

def determine_cancer_stage(confidence_score):
    """
    Determine the cancer stage based on the confidence score.
    Higher confidence scores suggest a more advanced stage.
    """
    if confidence_score >= 90:
        return "Stage IV"
    elif confidence_score >= 70:
        return "Stage III"
    elif confidence_score >= 50:
        return "Stage II"
    elif confidence_score >= 30:
        return "Stage I"
    else:
        return "Pre-cancerous or Benign"

def predict_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                # Extract form data
                patient_id = form.cleaned_data.get('patient_id', 'Not provided')
                age = form.cleaned_data.get('age', 'Not provided')
                gender = form.cleaned_data.get('gender', 'Not provided')
                contact_info = form.cleaned_data.get('contact_info', 'Not provided')
                medical_history = form.cleaned_data.get('medical_history', 'Not provided')
                image = request.FILES.get('image')

                if not image:
                    return render(request, 'predictor/result.html', {'result': 'No image uploaded'})

                # Save and preprocess the image
                temp_image_path = default_storage.save('tmp/' + image.name, image)
                temp_image_full_path = os.path.join(settings.MEDIA_ROOT, temp_image_path)
                img_array = preprocess_image(temp_image_full_path)

                # Predict using the model
                model = PredictorConfig.model
                prediction = model.predict(img_array)

                # Interpret prediction and calculate confidence score
                if prediction[0][0] > 0.5:
                    prediction_result = 'Cancer Detected'
                    confidence_score = round(prediction[0][0] * 100, 2)
                else:
                    prediction_result = 'No Cancer Detected'
                    confidence_score = round((1 - prediction[0][0]) * 100, 2)

                # Determine cancer stage based on the confidence score
                cancer_stage = determine_cancer_stage(confidence_score)

                # Get image URL for display
                image_url = default_storage.url(temp_image_path)

                # Prepare context for rendering
                context = {
                    'result': prediction_result,
                    'confidence_score': confidence_score,
                    'cancer_stage': cancer_stage,
                    'patient_id': patient_id,
                    'age': age,
                    'gender': gender,
                    'contact_info': contact_info,
                    'medical_history': medical_history,
                    'image_url': image_url,
                }

                return render(request, 'predictor/result.html', context)

            except Exception as e:
                return render(request, 'predictor/result.html', {'result': f'Error: {str(e)}'})

        else:
            return render(request, 'predictor/upload.html', {'form': form})

    else:
        form = ImageUploadForm()

    return render(request, 'predictor/upload.html', {'form': form})
