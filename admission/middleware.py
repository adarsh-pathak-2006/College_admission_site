from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings

class LoginRequiredMiddleware:
    """Middleware to require login for certain URLs"""
    
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        # List of URLs that don't require login
        public_paths = [
            reverse('home'),
            reverse('login'),
            reverse('register'),
            '/admin/',
        ]
        
        # Check if the path requires login
        if not request.user.is_authenticated:
            path = request.path_info
            if not any(path.startswith(public) for public in public_paths):
                # Don't redirect if it's a static/media file
                if not path.startswith(settings.STATIC_URL) and not path.startswith(settings.MEDIA_URL):
                    return redirect(f"{reverse('login')}?next={path}")
        
        return self.get_response(request)