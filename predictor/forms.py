from django import forms

class ImageUploadForm(forms.Form):
    patient_id = forms.CharField(label='Patient ID or Card ID', max_length=100, required=True)
    age = forms.IntegerField(label='Age', required=True)
    gender = forms.ChoiceField(
        label='Gender',
        choices=[('Male', 'Male'), ('Female', 'Female')],
        required=True
    )
    contact_info = forms.CharField(label='Contact Information', max_length=255, required=True)
    medical_history = forms.CharField(label='Medical History', widget=forms.Textarea, required=True)
    image = forms.ImageField(label='Upload Image', required=True)
