from django.db import models
from profiles.models import CustomUser
from cloudinary.models import CloudinaryField
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.core.exceptions import ValidationError


class RealEstateAgent(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    license_no = models.CharField(
        max_length=9,
        validators=[
            MinLengthValidator(limit_value=9,
                               message="License number must be 9 characters."),
            MaxLengthValidator(limit_value=9,
                               message="License number must be 9 characters.")
        ]
    )
    telephone_no = models.CharField(
        max_length=9,
        validators=[
            MinLengthValidator(
                limit_value=9,
                message="Telephone number must be 9 characters."),
            MaxLengthValidator(
                limit_value=9,
                message="Telephone number must be 9 characters.")
        ]
    )

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    def formatted_name(self):
        return f'{self.user.first_name} {self.user.last_name}'

    def formatted_telephone(self):
        return "({}) {}-{}".format(self.telephone_no[:2],
                                   self.telephone_no[2:6],
                                   self.telephone_no[6:])


class State(models.Model):
    id = models.AutoField(primary_key=True)
    state_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.state_name


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
    gone = models.BooleanField(default=False)

    def formatted_price_euro(self):
        return "€{:,.2f}".format(self.price)

    def formatted_type(self):
        return f'FOR {self.property_type.upper()}'

    def formatted_size(self):
        return f'{self.size} m²'

    def formatted_state(self):
        return self.state.state_name


class Images(models.Model):
    id = models.AutoField(primary_key=True)
    property = models.ForeignKey(
        Property, on_delete=models.CASCADE, related_name='images')
    image = CloudinaryField('image', default='', blank=True,
                            folder='homequest/media')

    def __str__(self):
        return f"Image for Property: {self.property.pk}"
