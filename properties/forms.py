from django import forms
from django.forms import widgets
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit
from crispy_forms.bootstrap import InlineCheckboxes

class PropertyFilterForm(forms.Form):
    bedrooms = forms.MultipleChoiceField(
        choices=[(str(i), str(i) if i < 5 else '5+') for i in range(1, 6)],
        required=False,
        label="Bedrooms",
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'btn-check'}),
    )

    max_price = forms.DecimalField(required=False, label="Maximum Price")

    state = forms.ChoiceField(choices=[], required=False, label="State")

    def __init__(self, *args, **kwargs):
        available_states = kwargs.pop('available_states', [])
        super(PropertyFilterForm, self).__init__(*args, **kwargs)
        self.fields['state'].choices = available_states

        # Create a Crispy Forms helper and define the layout
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-inline'
        self.helper.layout = Layout(
            InlineCheckboxes('bedrooms',
                             template='includes/forms/bedrooms_buttons.html'),
            'max_price',
            Field('state', css_class='custom-select'),
            Submit('submit', 'Apply Filters')
        )
        print(self.helper.layout.fields)