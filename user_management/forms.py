from allauth.account.forms import LoginForm, SignupForm


class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        self.fields['login'].widget.attrs.update({'class': 'form-control '
                                                           'mb-3'})
        self.fields['password'].widget.attrs.update({'class': 'form-control '
                                                              'mb-3'})
        self.fields['remember'].widget.attrs.update(
            {'class': 'form-check-input mb-3 d-block'})


class CustomSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super(CustomSignupForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-control '
                                                           'mb-3'})
        self.fields['username'].widget.attrs.update({'class': 'form-control '
                                                              'mb-3'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control '
                                                               'mb-3'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control '
                                                               'mb-3'})
