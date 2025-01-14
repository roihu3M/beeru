from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from imageviewer.models import Image, Tag, CommutationTable
from main.search import search_window
# Create your views here.

def search(request):
    if request.method == 'POST':
            query = search_window(request)
            return HttpResponseRedirect('/search/' + query)
    tags = request.GET.getlist('t')
    tags_for_link = '?'
    page = request.GET.get('page', default=1)
    images_per_page = 20
    previous_page = int(page) - 1
    next_page = int(page) + 1
    tags_ids = []
    i = 0
    for k in tags:
        if not Tag.objects.filter(tag_name=k):
            if k == '':
                break
            return HttpResponse('Image not found<p><a href="/" ><button>Back to main page</button></a></p>')
        t = Tag.objects.get(tag_name=k)
        tags_ids.append(t.pk)
        tags_for_link = tags_for_link + 't=' + k + '&'
    tags_ids.sort()
    image_ids = set()
    for a in range (1, Image.objects.count() + 1, 1):
        for b in tags_ids:
            image_commutation = CommutationTable.objects.filter(image_id=a, tag_id=b)
            if not image_commutation:
                break
            else:
                i += 1
        if i == len(tags_ids):
            image_ids.add(a)
        i = 0
    image_ids = list(image_ids)
    display_images_start = images_per_page * (int(page) - 1)
    display_images_end = images_per_page * int(page)
    pages_count = Image.objects.filter(fake_id__in=image_ids).count() // images_per_page
    if Image.objects.filter(fake_id__in=image_ids).count() % images_per_page != 0:
        pages_count += 1
    if image_ids:
        image = {
            'image' : Image.objects.filter(fake_id__in=image_ids).order_by('-pk')[display_images_start:display_images_end],
            'pages_count' : pages_count,
            'current_page' : page,
            'tags' : tags_for_link,
            'previous_page' : previous_page,
            'next_page' : next_page
        }
        return render(request, 'search/search.html', image)
    else:
        return HttpResponse('Image not found<p><a href="/" ><button>Back to main page</button></a></p>')