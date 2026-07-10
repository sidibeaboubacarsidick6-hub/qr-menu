from django.shortcuts import redirect
from django.conf import settings


class RedirectAuthenticatedRestaurantMiddleware:
    """
    Empêche les boucles de redirection.
    - Si connecté ET a un restaurant → dashboard
    - Si connecté ET pas de restaurant → message + logout
    - Si pas connecté → login
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Ne s'applique qu'aux URLs dashboard
        if request.path.startswith('/dashboard'):
            if request.user.is_authenticated:
                if not hasattr(request.user, 'restaurant'):
                    from django.contrib.auth import logout
                    logout(request)
                    return redirect('restaurants:login')
        
        return self.get_response(request)
