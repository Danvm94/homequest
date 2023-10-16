from django import template
from homepage.forms import CustomLoginForm

register = template.Library()


@register.inclusion_tag('includes/login-modal.html')
def login_form_tag(current_page=None):
    return {'loginform': CustomLoginForm(),
            'redirect_to': current_page}
