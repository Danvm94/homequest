from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit
from allauth.account.forms import LoginForm, SignupForm


class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-12 mx-auto'
        self.helper.field_class = 'col-lg-12 mx-auto'
        self.helper.layout = Layout(
            Field('login', css_class='form-control mb-1'),
            Field('password', css_class='form-control mb-1'),
            Field('remember', css_class='form-check-input mb-1'),
        )


class CustomSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super(CustomSignupForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-12 mx-auto'
        self.helper.field_class = 'col-lg-12 mx-auto'
        self.helper.layout = Layout(
            Field('email', css_class='form-control mb-1'),
            Field('username', css_class='form-control mb-1'),
            Field('password1', css_class='form-control mb-1'),
            Field('password2', css_class='form-control mb-1'),
        )
