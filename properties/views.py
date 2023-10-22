from django.shortcuts import render
from django.core.paginator import Paginator
from .utils import get_all_properties, get_properties_images
from .forms import PropertyFilterForm
from .models import Property, State


# Create your views here.

def properties_sale_view(request):
    # Get all properties
    properties = Property.objects.filter(property_type='sale')
    properties = properties.order_by('created_at')
    properties = get_properties_images(properties)

    # Initialize the filter form
    available_states = State.objects.values_list('id', 'state_name')
    filter_form = PropertyFilterForm(request.GET,
                                     available_states=available_states)
    selected_bedrooms = request.GET.getlist('bedrooms')
    if filter_form.is_valid():
        if selected_bedrooms:
            # Convert the selected bedrooms to integers
            selected_bedrooms = [int(bedroom) for bedroom in selected_bedrooms]
            print('Selected bedrooms:', selected_bedrooms)

            # Filter the properties based on the selected minimum bedrooms
            properties = properties.filter(bedrooms__in=selected_bedrooms)
            properties = get_properties_images(properties)

    # Paginate the properties
    paginator = Paginator(properties, 24)  # Show 10 properties per page
    page = request.GET.get('page')
    properties = paginator.get_page(page)

    context = {
        'properties': properties,
        'filter_form': filter_form,
        'selected_bedrooms': selected_bedrooms
    }

    return render(request, 'properties-sale.html', context)
