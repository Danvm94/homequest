from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Div
from crispy_forms.bootstrap import InlineCheckboxes


class PropertyCheckoutRent(forms.Form):
    name = forms.CharField(disabled=True)
    surname = forms.CharField(disabled=True)
    phone_number = forms.CharField(
        max_length=15,
        label='Phone Number',
        help_text='Please enter your phone number.',
        required=True,
    )
    delivery_address = forms.CharField()
    tos_agreement = forms.BooleanField(
        widget=forms.CheckboxInput(),
        required=True,
        label='I agree to the Terms of Service',
    )
    contract_agreement = forms.BooleanField(
        widget=forms.CheckboxInput(),
        required=True,
        label='I agree to the Contract Terms',
    )

    def __init__(self, *args, **kwargs):
        user_name = kwargs.pop('user_name', '')
        user_surname = kwargs.pop('user_surname', '')
        super(PropertyCheckoutRent, self).__init__(*args, **kwargs)
        self.fields['name'].initial = user_name
        self.fields['surname'].initial = user_surname

        # Create a Crispy Forms helper and define the layout
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-inline'
        self.helper.layout = Layout(
            Div(
                Div('name', css_class='col-6'),
                Div('surname', css_class='col-6'),
                css_class='row'
            ),
            Div('phone_number'),
            Div('delivery_address'),
            Div(
                Div('tos_agreement', css_class='col-6'),
                Div('contract_agreement', css_class='col-6'),
                css_class='row'
            ),
            Div(css_id='card-element', css_class='row'),
            Div(css_id='card-errors', css_class='row'),

            Submit('submit', value='Apply Filters',
                   css_class='w-auto mx-auto btn-success'),
        )
