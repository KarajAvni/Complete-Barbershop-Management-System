# shop/forms.py
from django import forms
from .models import ShopSettings, Expense

class ShopSettingsForm(forms.ModelForm):
    class Meta:
        model = ShopSettings
        fields = ['name', 'address', 'phone', 'email', 'opening_time', 'closing_time',
                 'slot_duration', 'max_advance_booking_days', 'cancellation_hours']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'opening_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'closing_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'slot_duration': forms.NumberInput(attrs={'class': 'form-control'}),
            'max_advance_booking_days': forms.NumberInput(attrs={'class': 'form-control'}),
            'cancellation_hours': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['description', 'category', 'amount', 'date']
        widgets = {
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }