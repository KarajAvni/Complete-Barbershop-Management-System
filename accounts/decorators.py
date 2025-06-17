# accounts/decorators.py
from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def client_required(view_func):
    """Decorator to ensure only clients can access a view"""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        
        # If user is barber or admin, they shouldn't access client-only views
        if hasattr(request.user, 'is_barber') and request.user.is_barber:
            messages.error(request, "This page is only for clients.")
            return redirect('accounts:dashboard')
        
        if request.user.is_superuser or (hasattr(request.user, 'is_admin') and request.user.is_admin):
            messages.error(request, "This page is only for clients.")
            return redirect('accounts:dashboard')
            
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def barber_required(view_func):
    """Decorator to ensure only barbers can access a view"""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        
        if not (hasattr(request.user, 'is_barber') and request.user.is_barber):
            messages.error(request, "This page is only for barbers.")
            return redirect('accounts:dashboard')
            
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def admin_required(view_func):
    """Decorator to ensure only admins can access a view"""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        
        if not (request.user.is_superuser or (hasattr(request.user, 'is_admin') and request.user.is_admin)):
            messages.error(request, "This page is only for administrators.")
            return redirect('accounts:dashboard')
            
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def barber_or_admin_required(view_func):
    """Decorator to ensure only barbers or admins can access a view"""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        
        is_barber = hasattr(request.user, 'is_barber') and request.user.is_barber
        is_admin = request.user.is_superuser or (hasattr(request.user, 'is_admin') and request.user.is_admin)
        
        if not (is_barber or is_admin):
            messages.error(request, "This page is only for barbers or administrators.")
            return redirect('accounts:dashboard')
            
        return view_func(request, *args, **kwargs)
    return _wrapped_view