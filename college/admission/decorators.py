from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def admin_required(view_func):
    """Decorator to check if user is admin"""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Please login to access this page.')
            return redirect('login')
        
        if not (request.user.is_staff or request.user.is_superuser):
            messages.error(request, 'You do not have permission to access this page.')
            return redirect('home')
        
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def student_required(view_func):
    """Decorator to check if user is a student"""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Please login to access this page.')
            return redirect('login')
        
        # Check if user has student profile
        try:
            student = request.user.student_profile
        except:
            messages.error(request, 'Student profile not found.')
            return redirect('home')
        
        return view_func(request, *args, **kwargs)
    return _wrapped_view