from django import forms
from django.forms import widgets
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Div
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
    min_square = forms.IntegerField(
        required=False,
        label="Minimum Square",
        widget=forms.TextInput(attrs={'placeholder': '0'})
    )
    max_square = forms.IntegerField(
        required=False,
        label="Maximum Square",
        widget=forms.TextInput(attrs={'placeholder': '2000'})
    )
    text_search = forms.CharField(
        required=False,
        label="Custom Search",
        widget=forms.TextInput(attrs={'placeholder': 'Street name...'}),

    )

    state = forms.ChoiceField(choices=[], required=False, label="State")

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
                Div('min_square', css_class='col-3'),
                Div('max_square', css_class='col-3'),
                css_class='row'
            ),
            Div(
                Div('text_search', css_class='col-3'),
                Div('state', css_class='col-3'),
                css_class='row'
            ),
            Submit('submit',
                   value='Apply Filters',
                   css_class='w-auto mx-auto btn-success')
        )
