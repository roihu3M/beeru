from django import forms
from .models import Image

class TagEditForm(forms.Form):
    image_tags = forms.CharField(max_length=500)