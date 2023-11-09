from django.contrib import admin
from .models import Property, Images


# Register your models here.
class ImagesAdmin(admin.ModelAdmin):
    list_display = ('id', 'property', 'image')
    list_filter = ('property',)
    search_fields = ('property__name',)


admin.site.register(Images, ImagesAdmin)
