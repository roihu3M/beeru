from django import forms
from imageviewer.models import Image

class SearchForm(forms.Form):
    image_tags = forms.CharField(max_length=500)