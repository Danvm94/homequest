from allauth.account.forms import LoginForm


class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        self.fields['login'].widget.attrs.update({'class': 'form-control '
                                                           'mb-3'})
        self.fields['password'].widget.attrs.update({'class': 'form-control '
                                                              'mb-3'})
        self.fields['remember'].widget.attrs.update(
            {'class': 'form-check-input mb-3 d-block'})
