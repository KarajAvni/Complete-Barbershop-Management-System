# shop/models.py
from django.db import models
from django.conf import settings
from django.utils import timezone
from barbers.models import Barber

class ShopSettings(models.Model):
    name = models.CharField(max_length=100, default="The Barbershop")
    address = models.TextField()
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    opening_time = models.TimeField(default="09:00")
    closing_time = models.TimeField(default="18:00")
    slot_duration = models.IntegerField(default=30, help_text="Duration of each appointment slot in minutes")
    max_advance_booking_days = models.IntegerField(default=30, help_text="How many days in advance can customers book")
    cancellation_hours = models.IntegerField(default=24, help_text="Minimum hours before appointment to cancel")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Shop Settings"
        verbose_name_plural = "Shop Settings"
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        # Ensure only one ShopSettings instance exists
        if not self.pk and ShopSettings.objects.exists():
            # If creating new instance and one already exists, update existing
            existing = ShopSettings.objects.first()
            self.pk = existing.pk
        super().save(*args, **kwargs)

class Revenue(models.Model):
    barber = models.ForeignKey(Barber, on_delete=models.CASCADE, related_name='revenues')
    booking = models.OneToOneField('bookings.Booking', on_delete=models.CASCADE, related_name='revenue')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2, default=20.00, help_text="Commission percentage for the shop")
    barber_earning = models.DecimalField(max_digits=10, decimal_places=2)
    shop_earning = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.barber} - ${self.amount} - {self.date}"
    
    def save(self, *args, **kwargs):
        # Calculate earnings
        self.shop_earning = self.amount * (self.commission_rate / 100)
        self.barber_earning = self.amount - self.shop_earning
        super().save(*args, **kwargs)

class Expense(models.Model):
    CATEGORY_CHOICES = [
        ('rent', 'Rent'),
        ('utilities', 'Utilities'),
        ('supplies', 'Supplies'),
        ('maintenance', 'Maintenance'),
        ('marketing', 'Marketing'),
        ('other', 'Other'),
    ]
    
    description = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='shop_expenses'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.description} - ${self.amount} - {self.date}"