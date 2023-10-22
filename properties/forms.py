from django import forms
from django.forms import widgets




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
