# bookings/urls.py
from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('book/', views.book_appointment, name='book'),
    path('history/', views.booking_history, name='history'),
    path('manage/', views.manage_bookings, name='manage'),
    path('<int:pk>/', views.booking_detail, name='detail'),
    path('<int:pk>/approve/', views.approve_booking, name='approve'),
    path('<int:pk>/reject/', views.reject_booking, name='reject'),
    path('<int:pk>/cancel/', views.cancel_booking, name='cancel'),
    path('api/available-slots/', views.get_available_slots, name='available_slots'),
    path('api/available-times/', views.get_available_slots, name='available_times'),  # ADD THIS LINE
]