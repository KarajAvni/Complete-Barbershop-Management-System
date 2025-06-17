# bookings/forms.py
from django import forms
from .models import Booking, Service
from barbers.models import Barber
from datetime import date, timedelta
from django.utils import timezone

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['barber', 'service', 'date', 'time', 'notes']
        widgets = {
            'barber': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'service': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'min': date.today().strftime('%Y-%m-%d'),
                'max': (date.today() + timedelta(days=30)).strftime('%Y-%m-%d'),
                'required': True
            }),
            'time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time',
                'required': True
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Any special requests or notes for your appointment...'
            }),
        }
        labels = {
            'barber': 'Select Barber',
            'service': 'Select Service',
            'date': 'Appointment Date',
            'time': 'Appointment Time',
            'notes': 'Additional Notes (Optional)',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Fixed: Changed from is_active to available
        self.fields['barber'].queryset = Barber.objects.filter(available=True)
        self.fields['service'].queryset = Service.objects.filter(active=True)
        
        # Add empty labels for dropdowns
        self.fields['barber'].empty_label = "-- Select a Barber --"
        self.fields['service'].empty_label = "-- Select a Service --"
        
    def clean(self):
        cleaned_data = super().clean()
        barber = cleaned_data.get('barber')
        date = cleaned_data.get('date')
        time = cleaned_data.get('time')
        
        if barber and date and time:
            # Check if the slot is already booked
            existing_booking = Booking.objects.filter(
                barber=barber,
                date=date,
                time=time,
                status__in=['pending', 'approved']
            ).exists()
            
            if existing_booking:
                raise forms.ValidationError(
                    "This time slot is already booked. Please select a different time."
                )
        
        # Validate date is not in the past
        if date and date < date.today():
            raise forms.ValidationError("You cannot book appointments in the past.")
        
        # Validate date is not too far in the future (30 days max)
        if date and date > date.today() + timedelta(days=30):
            raise forms.ValidationError("You cannot book appointments more than 30 days in advance.")
        
        return cleaned_data

class BookingStatusForm(forms.ModelForm):
    """Form for barbers to update booking status with comments"""
    rejection_reason = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Please provide a reason for rejection...'
        }),
        required=False,
        label='Reason/Comments'
    )
    
    class Meta:
        model = Booking
        fields = ['status', 'rejection_reason']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
        }