from django import template
from user_management.forms import CustomLoginForm, CustomSignupForm

register = template.Library()


@register.inclusion_tag('includes/login-modal.html')
def login_form_tag(current_page=None):
    return {'loginform': CustomLoginForm(),
            'redirect_to': current_page}


@register.inclusion_tag('includes/register-modal.html')
def signup_form_tag(current_page=None):
    return {'signupform': CustomSignupForm(),
            'redirect_to': current_page}
