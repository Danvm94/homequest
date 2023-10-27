from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .utils import get_all_properties, get_properties_images, \
    get_property_images
from .forms import PropertyFilterForm
from .models import Property, State, RealEstateAgent
from profiles.utils import get_profile_picture


def properties_view(request, property_type):
    # Get all properties
    properties = Property.objects.filter(property_type=property_type)
    properties = properties.order_by('created_at')
    properties = get_properties_images(properties)

    # Initialize the filter form
    available_states = State.objects.values_list('id', 'state_name')
    filter_form = PropertyFilterForm(request.GET,
                                     available_states=available_states)

    # Mapping between form fields and model fields
    field_mapping = {
        'bedrooms': 'bedrooms__in', 'bathrooms': 'bathrooms__in',
        'min_price': 'price__gte', 'max_price': 'price__lte',
        'min_square': 'square__gte', 'max_square': 'square__lte',
        'state': 'state',
    }

    # Initialize a dictionary to hold filter conditions
    filter_conditions = {}
    if filter_form.is_valid():
        data = filter_form.cleaned_data
        for form_field, model_field in field_mapping.items():
            value = data.get(form_field)
            if value:
                # Handle special cases for Decimal/float fields
                if form_field in ['min_price', 'max_price', 'min_square',
                                  'max_square']:
                    filter_conditions[model_field] = float(value)
                else:
                    filter_conditions[model_field] = value

    properties = properties.filter(**filter_conditions)
    properties = get_properties_images(properties)

    # Paginate the properties
    paginator = Paginator(properties, 24)
    page = request.GET.get('page')
    properties = paginator.get_page(page)
    context = {
        'properties': properties, 'filter_form': filter_form,
    }

    return render(
        request, f'properties-{property_type}.html', context)


def property_view(request, property_id):
    property_object = get_object_or_404(Property, id=property_id)
    property_object = get_property_images(property_object)
    agent = property_object.agent
    agent.profile_picture = get_profile_picture(agent.user)
    context = {
        'property': property_object,
        'agent': agent
    }
    return render(request, 'property.html', context)


def agents_view(request):
    agents = RealEstateAgent.objects.order_by('pk')
    for agent in agents:
        agent.profile_picture = get_profile_picture(agent.user)
    context = {
        'agents': agents
    }
    return render(request, 'agents.html', context)
