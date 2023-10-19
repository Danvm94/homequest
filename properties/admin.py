from django.contrib import admin
from .models import Property, Images


# Register your models here.
class ImagesAdmin(admin.ModelAdmin):
    list_display = (
        'property',
        'image'
    )

    def delete_model(self, request, obj):
        # Delete the image from Cloudinary
        if obj.image:
            pub_id = cloudinary.utils.cloudinary_url(obj.image.name,
                                                     resource_type='image')[0]
            cloudinary.uploader.destroy(pub_id)

        # Call the original del method to delete the object from the database
        obj.delete()


admin.site.register(Images, ImagesAdmin)
