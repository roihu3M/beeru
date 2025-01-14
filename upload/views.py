from PIL import Image as temp_image
import hashlib
from django.shortcuts import render
from django.http import HttpResponseRedirect
from imageviewer.models import Image, Tag, CommutationTable
from .forms import UploadForm
from main.search import search_window
# Create your views here.

def upload(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        entry = Image.objects.create()
        if form.is_valid:
            thumbnail = temp_image.open(request.FILES["image_path"])
            name = hashlib.sha256(thumbnail.tobytes()).hexdigest() + ".jpg"
            thumbnail.save("media/" + name, "JPEG")
            thumbnail.thumbnail((180, 180))
            thumbnail.save("media/thumbnails/" + name, "JPEG")
            entry.image_path = name
            entry.fake_id = Image.objects.count()
            entry.thumbnail_path = "thumbnails/" + entry.image_path.__str__()
            k = str(request.POST["image_tags"]).split()
            for a in k:
                Tag.objects.get_or_create(tag_name=a)
                q = Tag.objects.get(tag_name=a)
                entry.image_tags.add(q)
                image_commutation = CommutationTable.objects.create(image_id=entry.fake_id, tag_id=q.pk)
                image_commutation.save()
            entry.save()
            return HttpResponseRedirect('/upload/success/')
    else:
        form = UploadForm()
        return render(request, "upload.html", {"form": form})

def success(request):
    if request.method == 'POST':
            query = search_window(request)
            return HttpResponseRedirect('/search/' + query)
    return render(request, "success.html")