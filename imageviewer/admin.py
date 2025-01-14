from django.contrib import admin
from .models import Tag, Image, CommutationTable

# Register your models here.

admin.site.register(Image)
admin.site.register(Tag)
admin.site.register(CommutationTable)