from django.shortcuts import redirect
from django.urls import reverse


class CustomAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        open_paths = [
            # accounts
            reverse('accounts:login'),
            reverse('accounts:register'),
            reverse('accounts:register-verification'),
            reverse('accounts:reset-password'),
            reverse('accounts:reset-password-sent'),
            reverse('accounts:reset-password-confirm'),
            reverse('accounts:reset-password-complete'),
            # admin
            reverse('admin:login'),
        ]

        if not any(request.path.startswith(path) for path in open_paths):
            if not request.user.is_authenticated:
                return redirect("accounts:login")

        return self.get_response(request)
