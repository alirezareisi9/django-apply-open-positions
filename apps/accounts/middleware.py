from django.shortcuts import redirect


class AuthenticationMiddleware:
    
    def __init__(self, get_response) -> None:
        
        self.get_response = get_response

    
    def __call__(self, request, *args, **kwds):
        
        open_paths = [
            '/login/',
            '/register/',
        ]

        if request.path not in open_paths:
            
            if not request.user.is_authenticated:
                return redirect('accounts:login')

        response = self.get_response(request)
        return response
