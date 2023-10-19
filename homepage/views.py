from django.shortcuts import render
from properties.utils import get_latest_properties


# Create your views here.
def index_view(request):
    latest_properties = get_latest_properties(5)
    context = {
        'latest_properties': latest_properties
    }
    print(latest_properties)
    return render(request, 'index.html', context)
