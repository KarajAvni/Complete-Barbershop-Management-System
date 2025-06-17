# bookings/models.py
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone
from barbers.models import Barber

class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    duration_minutes = models.IntegerField(default=30)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - ${self.price}"

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Changed from 'auth.User'
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    barber = models.ForeignKey(Barber, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)
    rejection_reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date', 'time']
        unique_together = ('barber', 'date', 'time')

    def __str__(self):
        return f"{self.client.username} - {self.barber} - {self.date} {self.time}"

    def clean(self):
        # Validate that the booking is not in the past (FIXED: Added null checks)
        if self.date and self.date < timezone.now().date():
            raise ValidationError("Cannot book appointments in the past.")
        
        # Validate that the barber is available (FIXED: Added proper null and existence checks)
        if self.barber_id:  # Check if barber_id exists instead of barber object
            try:
                barber = Barber.objects.get(id=self.barber_id)
                if not barber.available:
                    raise ValidationError("This barber is not currently available.")
            except Barber.DoesNotExist:
                raise ValidationError("Selected barber does not exist.")

    @property
    def is_past(self):
        return self.date < timezone.now().date()

    @property
    def can_cancel(self):
        return self.status in ['pending', 'approved'] and not self.is_past

class FavoriteBarber(models.Model):
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Changed from 'auth.User'
        on_delete=models.CASCADE,
        related_name='favorite_barbers'
    )
    barber = models.ForeignKey(Barber, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('client', 'barber')

    def __str__(self):
        return f"{self.client.username} ❤️ {self.barber}"