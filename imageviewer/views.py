import os
from django.shortcuts import render, get_object_or_404
from django.conf import settings
from .models import Image, CommutationTable, Tag
from .forms import TagEditForm
from django.http import HttpResponseRedirect
from main.search import search_window
# Create your views here.

def image(request, image_id):
    if request.method == 'POST':
        query = search_window(request)
        return HttpResponseRedirect('/search/' + query)
    image = get_object_or_404(Image, fake_id=image_id)
    tags = []
    for all_tags in image.image_tags.all():
        tags.append(all_tags.tag_name)
    context = {"image": image, "tags": tags}
    return render(request, "imageviewer/image.html", context)

def delete(request, image_id):
    image = get_object_or_404(Image, fake_id=image_id)
    tags_ids = []
    path = str(image.image_path).split()[0].strip('>')
    os.remove(os.path.join(settings.MEDIA_ROOT, path))
    os.remove(os.path.join(settings.MEDIA_ROOT, 'thumbnails', path))
    for tags in image.image_tags.all():
        tags_ids.append(tags.pk)
    for comm_table_id in tags_ids:
        a = CommutationTable.objects.get(image_id=image_id, tag_id=comm_table_id)
        a.delete()
    image.delete()
    i = 0
    for id_shift in range (1, Image.objects.count() + 2):
        t = Image.objects.filter(fake_id = id_shift)
        a = CommutationTable.objects.filter(image_id = id_shift)
        if str(t) == '<QuerySet []>':
            i += 1
            continue
        t.update(fake_id=id_shift-i)
        a.update(image_id=id_shift-i)
    return render(request, "imageviewer/delete.html")

def edittags(request, image_id):
    image = get_object_or_404(Image, fake_id=image_id)
    tags = []
    if request.method == 'POST':
        form = TagEditForm(request.POST)
        for all_tags in image.image_tags.all():
            tags.append(all_tags.tag_name)
        if form.is_valid:
            k = str(request.POST["image_tags"]).split()
            new_tags = list(set(k) - set(tags))
            removed_tags = list(set(tags) - set(k))
            removed_tags_ids = []
            for new_tag in new_tags:
                Tag.objects.get_or_create(tag_name=new_tag)
                q = Tag.objects.get(tag_name=new_tag)
                image.image_tags.add(q)
                image_commutation = CommutationTable.objects.create(image_id=image.fake_id, tag_id=q.pk)
                image_commutation.save()
            for removed_tag in removed_tags:
                q = Tag.objects.get(tag_name=removed_tag)
                removed_tags_ids.append(q.pk)
                t = image.image_tags.get(tag_name=removed_tag)
                image.image_tags.remove(t)
            for removed_tag_id in removed_tags_ids:
                a = CommutationTable.objects.get(image_id=image_id, tag_id=removed_tag_id)
                a.delete()
            image.save()
            tags.clear()
            for all_tags in image.image_tags.all():
                tags.append(all_tags.tag_name)
            return render(request, "imageviewer/edittags.html", {"form": form})
    form = TagEditForm()
    return render(request, "imageviewer/edittags.html", {"form": form})





              
