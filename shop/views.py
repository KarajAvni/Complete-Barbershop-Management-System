# shop/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import datetime, timedelta
from .models import ShopSettings
from .forms import ShopSettingsForm
from bookings.models import Booking
from barbers.models import Barber
from accounts.decorators import admin_required, barber_or_admin_required

@barber_or_admin_required  # BARBERS and ADMINS can view revenue
def revenue_dashboard(request):
    # Get date range from request or default to current month
    end_date = timezone.now().date()
    start_date = end_date.replace(day=1)
    
    if request.GET.get('start_date'):
        start_date = datetime.strptime(request.GET.get('start_date'), '%Y-%m-%d').date()
    if request.GET.get('end_date'):
        end_date = datetime.strptime(request.GET.get('end_date'), '%Y-%m-%d').date()
    
    # Get completed bookings in date range
    completed_bookings = Booking.objects.filter(
        status='completed',
        date__range=[start_date, end_date]
    )
    
    # If user is a barber, only show their revenue
    # FIXED: Use new role system instead of user_profile.user_type
    if request.user.is_barber:
        try:
            barber = Barber.objects.get(user=request.user)
            completed_bookings = completed_bookings.filter(barber=barber)
        except Barber.DoesNotExist:
            completed_bookings = Booking.objects.none()
    
    # Calculate revenue
    total_revenue = sum([booking.service.price for booking in completed_bookings])
    total_bookings = completed_bookings.count()
    
    # Revenue by barber (only for admins)
    barber_revenue = {}
    # FIXED: Use new role system instead of user_profile.user_type
    if request.user.is_admin or request.user.is_superuser:
        for booking in completed_bookings:
            barber_name = str(booking.barber)
            if barber_name not in barber_revenue:
                barber_revenue[barber_name] = {'revenue': 0, 'bookings': 0}
            barber_revenue[barber_name]['revenue'] += float(booking.service.price)
            barber_revenue[barber_name]['bookings'] += 1
    
    # Daily revenue for chart
    daily_revenue = {}
    current_date = start_date
    while current_date <= end_date:
        daily_bookings = completed_bookings.filter(date=current_date)
        daily_revenue[current_date.strftime('%Y-%m-%d')] = sum([booking.service.price for booking in daily_bookings])
        current_date += timedelta(days=1)
    
    context = {
        'total_revenue': total_revenue,
        'total_bookings': total_bookings,
        'barber_revenue': barber_revenue,
        'daily_revenue': daily_revenue,
        'start_date': start_date,
        'end_date': end_date,
        'is_admin': request.user.is_admin or request.user.is_superuser,  # FIXED
    }
    return render(request, 'shop/revenue.html', context)

@barber_or_admin_required  # BARBERS and ADMINS can view schedule
def schedule_management(request):
    barbers = Barber.objects.filter(available=True)  # FIXED: available instead of is_active
    
    # Get upcoming bookings
    upcoming_bookings = Booking.objects.filter(
        date__gte=timezone.now().date(),
        status__in=['pending', 'approved']
    ).order_by('date', 'time')
    
    # If user is a barber, only show their schedule
    # FIXED: Use new role system instead of user_profile.user_type
    if request.user.is_barber:
        try:
            barber = Barber.objects.get(user=request.user)
            barbers = barbers.filter(id=barber.id)
            upcoming_bookings = upcoming_bookings.filter(barber=barber)
        except Barber.DoesNotExist:
            barbers = Barber.objects.none()
            upcoming_bookings = Booking.objects.none()
    
    context = {
        'barbers': barbers,
        'upcoming_bookings': upcoming_bookings,
        'is_admin': request.user.is_admin or request.user.is_superuser,  # FIXED
    }
    return render(request, 'shop/schedule.html', context)

@admin_required  # ONLY ADMINS can modify shop settings
def shop_settings(request):
    settings_obj, created = ShopSettings.objects.get_or_create(pk=1)
    
    if request.method == 'POST':
        form = ShopSettingsForm(request.POST, instance=settings_obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Shop settings updated successfully!')
            return redirect('/shop/settings/')
    else:
        form = ShopSettingsForm(instance=settings_obj)
    
    return render(request, 'shop/settings.html', {'form': form})