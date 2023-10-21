from django.shortcuts import render
from django.core.paginator import Paginator
from .utils import get_all_properties


# Create your views here.

def properties_sale_view(request):
    properties = get_all_properties('sale')
    # Paginate the properties
    paginator = Paginator(properties, 24)
    page = request.GET.get('page')
    properties = paginator.get_page(page)
    context = {
        'properties': properties
    }
    return render(request, 'properties-sale.html', context)
