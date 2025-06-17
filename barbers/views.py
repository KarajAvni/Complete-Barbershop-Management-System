# barbers/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg, Count
from .models import Barber, Review
from .forms import ReviewForm, BarberProfileForm
from bookings.models import FavoriteBarber
from accounts.decorators import barber_required
from bookings.models import Booking
from django.utils import timezone
from datetime import timedelta

def barber_list(request):
    """List all available barbers"""
    # Fixed: Changed from is_active to available
    barbers = Barber.objects.filter(available=True).select_related('user').annotate(
        avg_rating=Avg('reviews__rating'),
        review_count=Count('reviews')
    )
    
    # Get user's favorite barbers if authenticated
    favorite_barber_ids = []
    if request.user.is_authenticated and not request.user.is_barber:
        favorite_barber_ids = FavoriteBarber.objects.filter(
            client=request.user
        ).values_list('barber_id', flat=True)
    
    context = {
        'barbers': barbers,
        'favorite_barber_ids': list(favorite_barber_ids)
    }
    return render(request, 'barbers/barber_list.html', context)

def barber_detail(request, pk):
    """View detailed barber profile"""
    barber = get_object_or_404(Barber, pk=pk)
    reviews = barber.reviews.all().order_by('-created_at')[:5]
    
    # Check if user can leave a review
    can_review = False
    user_review = None
    
    if request.user.is_authenticated and not request.user.is_barber:
        # Check if user has had a completed booking with this barber
        from bookings.models import Booking
        has_completed_booking = Booking.objects.filter(
            client=request.user,
            barber=barber,
            status='completed'
        ).exists()
        
        if has_completed_booking:
            try:
                user_review = Review.objects.get(client=request.user, barber=barber)
            except Review.DoesNotExist:
                can_review = True
    
    # Check if barber is in user's favorites
    is_favorite = False
    if request.user.is_authenticated and not request.user.is_barber:
        is_favorite = FavoriteBarber.objects.filter(
            client=request.user,
            barber=barber
        ).exists()
    
    context = {
        'barber': barber,
        'reviews': reviews,
        'can_review': can_review,
        'user_review': user_review,
        'is_favorite': is_favorite,
        'avg_rating': barber.average_rating,
        'total_reviews': barber.total_reviews,
    }
    return render(request, 'barbers/barber_detail.html', context)

@login_required
def add_review(request, barber_id):
    """Add a review for a barber"""
    if request.user.is_barber:
        messages.error(request, "Barbers cannot review other barbers.")
        return redirect('barbers:list')
    
    barber = get_object_or_404(Barber, pk=barber_id)
    
    # Check if user has completed booking with this barber
    from bookings.models import Booking
    has_completed_booking = Booking.objects.filter(
        client=request.user,
        barber=barber,
        status='completed'
    ).exists()
    
    if not has_completed_booking:
        messages.error(request, "You can only review barbers you've had appointments with.")
        return redirect('barbers:detail', pk=barber_id)
    
    # Check if review already exists
    if Review.objects.filter(client=request.user, barber=barber).exists():
        messages.warning(request, "You have already reviewed this barber.")
        return redirect('barbers:detail', pk=barber_id)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.client = request.user
            review.barber = barber
            review.save()
            messages.success(request, "Thank you for your review!")
            return redirect('barbers:detail', pk=barber_id)
    else:
        form = ReviewForm()
    
    context = {
        'form': form,
        'barber': barber
    }
    return render(request, 'barbers/add_review.html', context)

@login_required
def toggle_favorite(request, barber_id):
    """Add or remove barber from favorites"""
    if request.user.is_barber:
        messages.error(request, "Barbers cannot have favorite barbers.")
        return redirect('barbers:list')
    
    barber = get_object_or_404(Barber, pk=barber_id)
    
    favorite, created = FavoriteBarber.objects.get_or_create(
        client=request.user,
        barber=barber
    )
    
    if not created:
        favorite.delete()
        messages.success(request, f"{barber} removed from favorites.")
    else:
        messages.success(request, f"{barber} added to favorites!")
    
    # Redirect back to the referring page
    return redirect(request.META.get('HTTP_REFERER', 'barbers:detail'), pk=barber_id)

@login_required
def barber_profile_edit(request):
    """Allow barbers to edit their own profile"""
    if not request.user.is_barber:
        messages.error(request, "Only barbers can access this page.")
        return redirect('accounts:dashboard')
    
    try:
        barber = request.user.barber_profile
    except Barber.DoesNotExist:
        messages.error(request, "Barber profile not found.")
        return redirect('accounts:dashboard')
    
    if request.method == 'POST':
        form = BarberProfileForm(request.POST, request.FILES, instance=barber)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated!")
            return redirect('accounts:dashboard')
    else:
        form = BarberProfileForm(instance=barber)
    
    return render(request, 'barbers/profile_edit.html', {'form': form, 'barber': barber})

@login_required
@barber_required
def barber_schedule(request):
    """Show barber's weekly schedule"""
    try:
        barber = Barber.objects.get(user=request.user)
    except Barber.DoesNotExist:
        messages.error(request, "Barber profile not found.")
        return redirect('accounts:dashboard')
    
    # Get current week's dates
    today = timezone.now().date()
    start_of_week = today - timedelta(days=today.weekday())  # Monday
    end_of_week = start_of_week + timedelta(days=6)  # Sunday
    
    # Get this week's bookings
    week_bookings = Booking.objects.filter(
        barber=barber,
        date__gte=start_of_week,
        date__lte=end_of_week,
        status__in=['approved', 'completed']
    ).order_by('date', 'time')
    
    # Get barber's working schedule
    schedules = barber.schedules.all() if hasattr(barber, 'schedules') else []
    
    # Create week structure
    week_days = []
    for i in range(7):  # Monday to Sunday
        day_date = start_of_week + timedelta(days=i)
        day_bookings = week_bookings.filter(date=day_date)
        day_schedule = None
        
        # Find schedule for this day
        for schedule in schedules:
            if schedule.weekday == i:  # Monday = 0, Sunday = 6
                day_schedule = schedule
                break
        
        week_days.append({
            'date': day_date,
            'day_name': day_date.strftime('%A'),
            'bookings': day_bookings,
            'schedule': day_schedule,
            'is_today': day_date == today,
        })
    
    # Calculate weekly stats
    weekly_stats = {
        'total_appointments': week_bookings.count(),
        'completed_appointments': week_bookings.filter(status='completed').count(),
        'pending_appointments': Booking.objects.filter(
            barber=barber,
            date__gte=start_of_week,
            date__lte=end_of_week,
            status='pending'
        ).count(),
        'week_revenue': sum(booking.service.price for booking in week_bookings.filter(status='completed')),
    }
    
    context = {
        'barber': barber,
        'week_days': week_days,
        'start_of_week': start_of_week,
        'end_of_week': end_of_week,
        'weekly_stats': weekly_stats,
        'today': today,
    }
    
    return render(request, 'barbers/schedule.html', context)