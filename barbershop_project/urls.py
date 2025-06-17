"""
URL configuration for barbershop_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# barbershop_project/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

def role_based_redirect(request):
    """Redirect users to appropriate dashboard based on their role"""
    if not request.user.is_authenticated:
        return redirect('/accounts/login/')
    
    user = request.user
    
    # Check user role using the User model fields
    if user.is_superuser or user.is_admin:
        return redirect('/admin/')
    elif user.is_barber:
        return redirect('/accounts/dashboard/')  # Will show barber dashboard
    else:  # client
        return redirect('/accounts/dashboard/')  # Will show client dashboard

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('dashboard/', role_based_redirect, name='role_redirect'),
    path('accounts/', include('accounts.urls')),
    path('bookings/', include('bookings.urls')),
    path('barbers/', include('barbers.urls')),
    path('shop/', include('shop.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)