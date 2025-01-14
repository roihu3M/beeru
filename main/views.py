from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import SearchForm
from .search import search_window

def index(request):
    if request.method == 'POST':
            query = search_window(request)
            return HttpResponseRedirect('/search/' + query)
    else:
        form = SearchForm()
        return render(request, "main/index.html")
