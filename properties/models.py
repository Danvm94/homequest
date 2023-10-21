from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


class RealEstateAgent(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    license_no = models.CharField(max_length=255)


class State(models.Model):
    id = models.AutoField(primary_key=True)
    state_name = models.CharField(max_length=255, unique=True)


class Property(models.Model):
    id = models.AutoField(primary_key=True)
    agent = models.ForeignKey(RealEstateAgent, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    PROPERTY_TYPES = (
        ('sale', 'For Sale'),
        ('rent', 'For Rent'),
    )
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPES)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    title = models.CharField(max_length=255)
    bathrooms = models.PositiveIntegerField()
    bedrooms = models.PositiveIntegerField()
    fireplaces = models.PositiveIntegerField()
    parking_spaces = models.PositiveIntegerField()
    size = models.PositiveIntegerField()

    def formatted_price_euro(self):
        return "€{:,.2f}".format(self.price)

    def formatted_type(self):
        return f'FOR {self.property_type.upper()}'

    def formatted_size(self):
        return f'{self.size} m²'


class Images(models.Model):
    id = models.AutoField(primary_key=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    image = CloudinaryField('image', default='', blank=True,
                            folder='homequest/media')
