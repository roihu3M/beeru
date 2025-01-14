from django import forms
from imageviewer.models import Image

class UploadForm(forms.Form):
    image_path = forms.ImageField()
    image_tags = forms.CharField(max_length=500)