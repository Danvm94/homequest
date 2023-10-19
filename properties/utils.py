from .models import Property, Images


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
    for latest_property in latest_properties_list:
        latest_property.images = Images.objects.filter(property=latest_property)
        print(latest_property)
    return latest_properties_list
