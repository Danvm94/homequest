from django import forms
from .models import Property, State, Images, RealEstateAgent
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Div, Field
from crispy_forms.bootstrap import InlineCheckboxes


class PropertyFilterForm(forms.Form):
    bedrooms = forms.MultipleChoiceField(
        choices=[(str(i), str(i) if i < 5 else '5+') for i in range(1, 6)],
        required=False,
        label="Bedrooms",
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'btn-check'}),
    )
    bathrooms = forms.MultipleChoiceField(
        choices=[(str(i), str(i) if i < 5 else '5+') for i in range(1, 6)],
        required=False,
        label="Bathrooms",
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'btn-check'}),
    )
    parking = forms.MultipleChoiceField(
        choices=[(str(i), str(i) if i < 4 else '4+') for i in range(0, 5)],
        required=False,
        label="Parking Spaces",
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'btn-check'}),
    )
    min_price = forms.DecimalField(
        required=False,
        label="Minimum Price",
        widget=forms.TextInput(attrs={'placeholder': '0'})
    )
    max_price = forms.DecimalField(
        required=False,
        label="Maximum Price",
        widget=forms.TextInput(attrs={'placeholder': '100000000'})
    )
    min_size = forms.IntegerField(
        required=False,
        label="Minimum Square",
        widget=forms.TextInput(attrs={'placeholder': '0'})
    )
    max_size = forms.IntegerField(
        required=False,
        label="Maximum Square",
        widget=forms.TextInput(attrs={'placeholder': '2000'})
    )

    state = forms.ChoiceField(choices=[], required=False, label="State")

    clear_button = forms.CharField(
        required=False,
        widget=forms.HiddenInput(attrs={'id': 'clear-button'}),
    )

    def __init__(self, *args, **kwargs):
        available_states = kwargs.pop('available_states', [])
        available_states = list(available_states)  # Convert QuerySet to a list
        available_states.insert(0, (
            '', 'All'))  # Insert ('', 'All') as the first item
        super(PropertyFilterForm, self).__init__(*args, **kwargs)
        self.fields['state'].choices = available_states

        # Create a Crispy Forms helper and define the layout
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-inline'
        self.helper.layout = Layout(
            InlineCheckboxes('bedrooms',
                             template='forms/checkbox_toggle_btn.html',
                             ),
            InlineCheckboxes('bathrooms',
                             template='forms/checkbox_toggle_btn.html',
                             ),
            InlineCheckboxes('parking',
                             template='forms/checkbox_toggle_btn.html',
                             ),
            Div(
                Div('min_price', css_class='col-3'),
                Div('max_price', css_class='col-3'),
                Div('min_size', css_class='col-3'),
                Div('max_size', css_class='col-3'),
                css_class='row'
            ),
            Submit('submit',
                   value='Apply Filters',
                   css_class='w-auto mx-auto btn-success'),

        )


class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100, required=True, label="Subject",
                              widget=forms.TextInput(
                                  attrs={'placeholder': 'Enter a subject'}))
    message = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Enter your message'}),
        required=True, label="Message")

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('subject', css_class='form-control'),
            Field('message', css_class='form-control'),
            Submit('submit', 'Send Message', css_class='btn btn-primary')
        )

    def clean_subject(self):
        subject = self.cleaned_data.get('subject')
        if len(subject) < 5:
            raise forms.ValidationError(
                "The subject must be at least 5 characters long.")
        return subject

    def clean_message(self):
        message = self.cleaned_data.get('message')
        if len(message) < 10:
            raise forms.ValidationError(
                "The message must be at least 10 characters long.")
        return message


class PropertyForm(forms.ModelForm):
    class PropertyForm(forms.ModelForm):
        state = forms.ModelChoiceField(
            queryset=State.objects.all(),
            empty_label=None,  # Remove the empty choice
            to_field_name="state_name",
            # Set the field to use 'state_name' as the value
        )
        agent = forms.ModelChoiceField(
            queryset=RealEstateAgent.objects.all(),
            empty_label=None,  # Remove the empty choice
            to_field_name="formatted_name",
        )

    class Meta:
        model = Property
        fields = ['title', 'address', 'state', 'property_type', 'description',
                  'price', 'bathrooms', 'bedrooms', 'fireplaces',
                  'parking_spaces', 'size', 'agent']


class ImagesForm(forms.ModelForm):
    class Meta:
        model = Images
        fields = ['image']
