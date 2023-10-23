from .models import Property, Images


def get_properties_images(properties):
    for house in properties:
        house.images = Images.objects.filter(property=house)
    return properties


def get_property_images(property_object):
    property_object.images = Images.objects.filter(property=property_object)
    return property_object

def get_latest_properties(number):
    """
    Retrieve the latest properties from the database.

    This function retrieves the specified number of latest properties
    from the database and sorts them by their 'created_at' timestamp in
    descending order, ensuring that the newest properties appear first.

    Args:
        number (int): The number of latest properties to retrieve.

    Returns:
        QuerySet: A QuerySet containing the latest properties.

    Example:
        To retrieve the 5 latest properties, you can call:
        latest_properties = get_latest_properties(5)
    """
    properties = Property.objects.all()
    latest_properties_list = properties.order_by('id')[:number]
    latest_properties_list = get_properties_images(latest_properties_list)
    for latest_property in latest_properties_list:
        latest_property.images = Images.objects.filter(
            property=latest_property)
    return latest_properties_list


def get_all_properties(property_type):
    properties = Property.objects.filter(property_type=property_type)
    properties = get_properties_images(properties)
    return properties
