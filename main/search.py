from .forms import SearchForm

def search_window(request):
        form = SearchForm(request.POST)
        if form.is_valid:
            k = str(request.POST["image_tags"]).split()
            query = '?'
            for a in k:
                query = query + ('t=' + a +'&')
            query = query + ('page=1')
            return query