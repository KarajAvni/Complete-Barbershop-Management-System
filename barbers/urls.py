# barbers/urls.py
from django.urls import path
from . import views

app_name = 'barbers'

urlpatterns = [
    path('', views.barber_list, name='list'),
    path('<int:pk>/', views.barber_detail, name='detail'),
    path('<int:barber_id>/review/', views.add_review, name='add_review'),
    path('<int:barber_id>/favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('profile/edit/', views.barber_profile_edit, name='profile_edit'),
    path('schedule/', views.barber_schedule, name='schedule'),
]