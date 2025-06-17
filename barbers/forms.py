# barbers/forms.py
from django import forms
from .models import Review, BarberSchedule, Barber

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(choices=[(i, i) for i in range(1, 6)], attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Share your experience...'}),
        }
        labels = {
            'rating': 'Rating (1-5 stars)',
            'comment': 'Your Review'
        }

class BarberScheduleForm(forms.ModelForm):
    class Meta:
        model = BarberSchedule
        fields = ['weekday', 'start_time', 'end_time', 'is_working']
        widgets = {
            'weekday': forms.Select(attrs={'class': 'form-control'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'is_working': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'weekday': 'Day of Week',
            'start_time': 'Start Time',
            'end_time': 'End Time',
            'is_working': 'Working this day?'
        }

class BarberProfileForm(forms.ModelForm):
    """Form for barbers to update their profile"""
    class Meta:
        model = Barber
        fields = ['bio', 'experience_years', 'specialties', 'hourly_rate', 'photo', 'available']
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'experience_years': forms.NumberInput(attrs={'class': 'form-control'}),
            'specialties': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Fade cuts, Beard trimming'}),
            'hourly_rate': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }