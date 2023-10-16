from allauth.account.views import LoginView, SignupView
from django.http import JsonResponse


class CustomLoginView(LoginView):
    def form_invalid(self, form):
        # Check if the request is an AJAX request
        if self.request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            return JsonResponse({'form': form.errors}, status=400)
        return super(CustomLoginView, self).form_invalid(form)


class CustomSignupView(SignupView):
    def form_invalid(self, form):
        # Check if the request is an AJAX request
        if self.request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            print(form.errors)
            print({'form': form.errors})
            return JsonResponse({'form': form.errors}, status=400)
        return super(CustomSignupView, self).form_invalid(form)
