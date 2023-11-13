from django.shortcuts import render
from properties.models import Property


# Create your views here.
def index_view(request):
    properties = Property.objects.all()
    latest_properties = properties.order_by('created_at')[:8]

    context = {
        'latest_properties': latest_properties,
    }
    return render(request, 'index.html', context)


def about_view(request):
    return render(request, 'about.html')


def handler404(request, exception):
    return render(request, '404.html', status=404)
