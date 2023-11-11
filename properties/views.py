from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.contrib.auth.decorators import user_passes_test
from .utils import get_properties_images, get_property_images
from .forms import PropertyFilterForm, ContactForm, PropertyForm, ImagesForm
from .models import Property, State, RealEstateAgent, Images
from homequest.settings import STRIPE_PUBLIC_KEY, STRIPE_CLIENT_SECRET
from django.contrib import messages
from homequest.settings import DEFAULT_FROM_EMAIL
from cloudinary.uploader import upload


def properties_view(request, property_type):
    # Get all properties
    properties = Property.objects.filter(property_type=property_type,
                                         gone=False)
    properties = properties.order_by('created_at')

    # Initialize the filter form
    available_states = State.objects.values_list('id', 'state_name')
    filter_form = PropertyFilterForm(request.GET,
                                     available_states=available_states)

    # Mapping between form fields and model fields
    field_mapping = {
        'bedrooms': 'bedrooms__in', 'bathrooms': 'bathrooms__in',
        'min_price': 'price__gte', 'max_price': 'price__lte',
        'min_size': 'size__gte', 'max_size': 'size__lte',
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
                if form_field in ['min_price', 'max_price', 'min_size',
                                  'max_size']:
                    filter_conditions[model_field] = float(value)
                else:
                    filter_conditions[model_field] = value

    properties = properties.filter(**filter_conditions)
    # Paginate the properties
    paginator = Paginator(properties, 24)
    page = request.GET.get('page')
    properties = paginator.get_page(page)
    context = {
        'properties': properties,
        'filter_form': filter_form,
    }

    return render(
        request, f'properties-{property_type}.html', context)


def property_view(request, property_id):
    property_object = get_object_or_404(Property, id=property_id)
    agent = property_object.agent

    if request.method == 'POST':
        user = request.user
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = (f'{property_object.address} - '
                       f'{form.cleaned_data["subject"]}')
            message = form.cleaned_data['message']
            recipient_list = [user.email, agent.user.email]
            send_mail(subject, message, DEFAULT_FROM_EMAIL, recipient_list)
            messages.success(request, 'Message sent')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {field}: {error}")
        return redirect('property_detail', property_id)
    elif request.method == 'GET':
        form = ContactForm()
        context = {
            'property': property_object,
            'agent': agent,
            'stripe_public_key': STRIPE_PUBLIC_KEY,
            'client_secret': STRIPE_CLIENT_SECRET,
            'form': form
        }
        return render(request, 'property.html', context)


def agents_view(request):
    agents = RealEstateAgent.objects.order_by('pk')
    context = {
        'agents': agents
    }
    return render(request, 'agents.html', context)


def is_staff(user):
    return user.is_staff


@user_passes_test(is_staff)
def edit_property(request, property_id=None):
    if property_id:
        # Edit an existing property
        property_object = get_object_or_404(Property, id=property_id)
        page = 'edit_property.html'
    else:
        # Create a new property
        property_object = None
        page = 'create_property.html'
    context = dict(backend_form=ImagesForm())
    if request.method == 'POST':
        property_form = PropertyForm(request.POST, request.FILES,
                                     instance=property_object)
        image_form = ImagesForm(request.POST, request.FILES)
        context['posted'] = image_form.instance

        if property_form.is_valid():
            property_object = property_form.save()
            messages.success(
                request,
                'Property updated.' if property_id else 'Property created.')
        if image_form.is_valid():
            if image_form.cleaned_data['image']:
                # Apply Cloudinary transformations before saving
                image_file = image_form.cleaned_data['image']
                result = upload(
                    image_file,
                    folder='homequest/media',
                    transformation=[
                        {'width': 600, 'height': 400, 'crop': 'fill'},
                        # Adjust width and height as needed
                        {'format': 'webp', 'quality': 'auto:best',
                         'flags': 'lossy'}
                    ]
                )
                image_form.instance.property_id = property_object.id
                image_form.instance.image = result['secure_url']
                image_form.save()
        return redirect('property_detail', property_id)

    else:  # Handle GET request
        property_form = PropertyForm(instance=property_object)
        image_form = ImagesForm()

    context = {'property_form': property_form, 'property': property_object,
               'image_form': image_form}
    return render(request, page, context)


@user_passes_test(is_staff)
def delete_image_view(request, image_id):
    image = get_object_or_404(Images, id=image_id)
    property_id = image.property_id  # Save the property ID before deleting
    image.delete()
    messages.success(request, 'Image deleted.')
    return redirect('edit_property_with_id', property_id)


@user_passes_test(is_staff)
def delete_property_view(request, property_id):
    property_obj = get_object_or_404(Property, id=property_id)
    property_obj.delete()
    messages.success(request, 'Property deleted.')
    return redirect('home')
