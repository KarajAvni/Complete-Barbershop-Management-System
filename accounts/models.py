#accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

class User(AbstractUser):
    is_barber = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    
    @property
    def is_client(self):
        return not self.is_barber and not self.is_admin and not self.is_superuser
    
    def get_role(self):
        if self.is_superuser or self.is_admin:
            return 'admin'
        elif self.is_barber:
            return 'barber'
        else:
            return 'client'
    
    class Meta:
        db_table = 'auth_user'

# Client Profile model
class ClientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='client_profile')
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='client_photos/', blank=True)
    preferred_barber = models.ForeignKey('barbers.Barber', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s profile"