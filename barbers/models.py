# barbers/models.py
from django.db import models
from django.conf import settings
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

class Barber(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='barber_profile'
    )
    bio = models.TextField(blank=True)
    experience_years = models.IntegerField(default=0)
    specialties = models.CharField(max_length=200, blank=True)
    hourly_rate = models.DecimalField(max_digits=6, decimal_places=2, default=25.00)
    photo = models.ImageField(upload_to='barber_photos/', blank=True)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username}"

    def get_absolute_url(self):
        return reverse('barbers:detail', kwargs={'pk': self.pk})

    @property
    def average_rating(self):
        reviews = self.reviews.all()
        if reviews:
            return sum(review.rating for review in reviews) / len(reviews)
        return 0

    @property
    def total_reviews(self):
        return self.reviews.count()

class BarberSchedule(models.Model):
    WEEKDAY_CHOICES = [
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    ]
    
    barber = models.ForeignKey(Barber, on_delete=models.CASCADE, related_name='schedules')
    weekday = models.IntegerField(choices=WEEKDAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_working = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ('barber', 'weekday')
        ordering = ['weekday', 'start_time']
    
    def __str__(self):
        return f"{self.barber} - {self.get_weekday_display()}: {self.start_time} to {self.end_time}"
    
    def clean(self):
        """Validate that end_time is after start_time"""
        if self.start_time and self.end_time and self.start_time >= self.end_time:
            raise ValidationError("End time must be after start time.")

class Review(models.Model):
    barber = models.ForeignKey(Barber, on_delete=models.CASCADE, related_name='reviews')
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('barber', 'client')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.client.username} - {self.barber.user.username} ({self.rating}/5)"