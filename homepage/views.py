from django.shortcuts import render
from properties.utils import get_latest_properties


# Create your views here.
def index_view(request):
    latest_properties = get_latest_properties(8)

    context = {
        'latest_properties': latest_properties,
    }
    return render(request, 'index.html', context)


def about_view(request):
    return render(request, 'about.html')


def handler404(request, exception):
    return render(request, '404.html', status=404)
