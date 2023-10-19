from allauth.account.views import LoginView, SignupView
from django.http import JsonResponse
from django.contrib import messages
from django.http import HttpResponseRedirect


class CustomLoginView(LoginView):
    def form_invalid(self, form):
        form_errors = form.errors
        error_messages = []

        # Iterate through the form errors and collect all error messages
        for field, errors in form_errors.items():
            for error in errors:
                error_messages.append(error)

        # Add all error messages to the messages framework
        for error_message in error_messages:
            messages.add_message(self.request, messages.ERROR, error_message)

        # Redirect to the referer page
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))


class CustomSignupView(SignupView):
    def form_invalid(self, form):
        form_errors = form.errors
        error_messages = []

        # Iterate through the form errors and collect all error messages
        for field, errors in form_errors.items():
            for error in errors:
                error_messages.append(error)

        # Add all error messages to the messages framework
        for error_message in error_messages:
            messages.add_message(self.request, messages.ERROR, error_message)

        # Redirect to the referer page
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))
