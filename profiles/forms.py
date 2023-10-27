from django import forms
from .models import CustomUser
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit


class ProfileEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProfileEditForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'  # Add Bootstrap CSS class
        self.helper.label_class = 'col-lg-2'  # CSS class for labels
        self.helper.field_class = 'col-lg-10'  # CSS class for form fields
        self.helper.layout = Layout(
            Field('picture', template='forms/image_upload.html'),
            Field('first_name', css_class='form-control'),
            Field('last_name', css_class='form-control'),
            Submit('submit',
                   value='Update',
                   css_class='w-auto mx-auto btn-success')
        )

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'picture']
