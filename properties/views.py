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
    if filter_form.is_valid():
        data = filter_form.cleaned_data
        print(data['min_price'])
        if data['bedrooms']:
            # Convert the selected bedrooms to integers
            selected_bedrooms = [int(bedroom) for bedroom in data['bedrooms']]
            # Filter the properties based on the selected minimum bedrooms
            properties = properties.filter(bedrooms__in=selected_bedrooms)
            properties = get_properties_images(properties)
        if data['bathrooms']:
            # Convert the selected bedrooms to integers
            selected_bathrooms = [int(bathroom) for bathroom in
                                  data['bathrooms']]
            # Filter the properties based on the selected minimum bedrooms
            properties = properties.filter(bathrooms__in=selected_bathrooms)
            properties = get_properties_images(properties)
        if data['min_price']:
            properties = properties.filter(price__gte=data['min_price'])
            properties = get_properties_images(properties)
        if data['max_price']:
            # Assuming 'max_price' is a Decimal or float field in your model
            properties = properties.filter(price__lte=data['max_price'])
            properties = get_properties_images(properties)
        if data['min_square']:
            properties = properties.filter(price__gte=data['min_square'])
            properties = get_properties_images(properties)
        if data['max_square']:
            # Assuming 'max_price' is a Decimal or float field in your model
            properties = properties.filter(price__lte=data['max_square'])
            properties = get_properties_images(properties)
        if data['state']:
            print(data['state'])
            properties = properties.filter(state=data['state'])
            properties = get_properties_images(properties)


    # Paginate the properties
    paginator = Paginator(properties, 24)  # Show 10 properties per page
    page = request.GET.get('page')
    properties = paginator.get_page(page)
    context = {
        'properties': properties,
        'filter_form': filter_form,
    }

    return render(request, 'properties-sale.html', context)
