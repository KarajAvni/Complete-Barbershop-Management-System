# shop/urls.py
from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('revenue/', views.revenue_dashboard, name='revenue'),
    path('schedule/', views.schedule_management, name='schedule'),
    path('settings/', views.shop_settings, name='settings'),
]