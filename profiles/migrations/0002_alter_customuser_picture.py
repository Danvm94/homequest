# Generated by Django 4.2.7 on 2023-11-14 10:23

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='picture',
            field=cloudinary.models.CloudinaryField(default=None, max_length=255, verbose_name='image'),
        ),
    ]
