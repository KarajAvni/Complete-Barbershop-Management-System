# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.db.models import Count, Sum, Avg, Q
from django.utils import timezone
from datetime import datetime, timedelta, time
from django.contrib.auth import get_user_model
from django.db import models

# Import your forms
from .forms import CustomUserCreationForm, ProfileUpdateForm, UserUpdateForm
# Import your models
from .models import ClientProfile
from bookings.models import Booking, Service, FavoriteBarber
from barbers.models import Barber, Review

# Get the User model
User = get_user_model()

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return '/accounts/dashboard/'
    
    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password. Please try again.')
        return super().form_invalid(form)

def custom_login_view(request):
    if request.user.is_authenticated:
        return redirect('/accounts/dashboard/')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.get_full_name() or user.username}!')
                return redirect('/accounts/dashboard/')
            else:
                messages.error(request, 'Invalid username or password. Please try again.')
        else:
            messages.error(request, 'Please enter both username and password.')
    
    return render(request, 'accounts/login.html')

def register(request):
    """Registration view - all new users are clients by default"""
    if request.user.is_authenticated:
        return redirect('/accounts/dashboard/')
        
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # Ensure new registrations are clients (not barbers or admins)
            user.is_barber = False
            user.is_admin = False
            user.save()
            
            # Create client profile
            ClientProfile.objects.create(user=user)
            
            # Log the user in
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to The Barbershop.')
            return redirect('/accounts/dashboard/')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def dashboard(request):
    user = request.user
    
    # Debug prints
    print(f"Dashboard accessed by: {user.username}")
    print(f"Is superuser: {user.is_superuser}")
    print(f"Is admin: {getattr(user, 'is_admin', False)}")
    print(f"Is barber: {getattr(user, 'is_barber', False)}")
    
    # Determine user role and render appropriate dashboard
    if user.is_superuser or getattr(user, 'is_admin', False):
        print("Rendering ADMIN dashboard")
        
        # Admin context
        context = {
            'total_clients': User.objects.filter(
                is_barber=False, 
                is_admin=False, 
                is_superuser=False
            ).count(),
            'total_barbers': Barber.objects.count(),
            'total_bookings': Booking.objects.count(),
            'total_revenue': Booking.objects.filter(status='completed').aggregate(
                total=Sum('service__price'))['total'] or 0,
            'recent_bookings': Booking.objects.select_related(
                'client', 'barber__user', 'service'
            ).order_by('-created_at')[:10],
            'top_barbers': Barber.objects.annotate(
                total_bookings=Count('booking'),
                total_revenue=Sum('booking__service__price', 
                    filter=Q(booking__status='completed'))
            ).order_by('-total_revenue')[:5],
            'popular_services': Service.objects.annotate(
                booking_count=Count('booking')
            ).order_by('-booking_count')[:5],
        }
        return render(request, 'accounts/admin_dashboard.html', context)
    
    elif getattr(user, 'is_barber', False):
        print("Rendering BARBER dashboard")
        
        try:
            # Get barber profile using the correct related name
            barber = Barber.objects.get(user=user)
            
            # Barber context
            today = timezone.now().date()
            context = {
                'barber': barber,
                'pending_bookings': Booking.objects.filter(
                    barber=barber, 
                    status='pending'
                ).select_related('client', 'service').order_by('date', 'time'),
                
                'todays_appointments': Booking.objects.filter(
                    barber=barber,
                    date=today,
                    status='approved'
                ).select_related('client', 'service').order_by('time'),
                
                'week_earnings': Booking.objects.filter(
                    barber=barber,
                    status='completed',
                    date__gte=today - timedelta(days=7)
                ).aggregate(total=Sum('service__price'))['total'] or 0,
                
                'average_rating': Review.objects.filter(
                    barber=barber
                ).aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0,
                
                'total_reviews': Review.objects.filter(barber=barber).count(),
                'total_completed': Booking.objects.filter(
                    barber=barber,
                    status='completed'
                ).count(),
            }
            return render(request, 'accounts/barber_dashboard.html', context)
            
        except Barber.DoesNotExist:
            # If barber profile doesn't exist, create it
            messages.warning(request, "Setting up your barber profile...")
            Barber.objects.create(user=user)
            return redirect('/accounts/dashboard/')
    
    else:
        print("Rendering CLIENT dashboard")
        
        # Client context
        context = {
            'upcoming_bookings': Booking.objects.filter(
                client=user,
                date__gte=timezone.now().date(),
                status__in=['pending', 'approved']
            ).select_related('barber__user', 'service').order_by('date', 'time')[:5],
            
            'total_bookings': Booking.objects.filter(client=user).count(),
            
            'favorite_barbers': FavoriteBarber.objects.filter(
                client=user
            ).select_related('barber__user').count(),
            
            'reviews_given': Review.objects.filter(client=user).count(),
            
            'available_slots': get_available_slots_today(),
            
            'recent_bookings': Booking.objects.filter(
                client=user
            ).select_related('barber__user', 'service').order_by('-created_at')[:5],
        }
        return render(request, 'accounts/client_dashboard.html', context)


def get_available_slots_today():
    """Helper function to get available slots today"""
    today = timezone.now().date()
    current_time = timezone.now().time()
    
    # Define time slots (9 AM to 6 PM)
    time_slots = []
    for hour in range(9, 18):
        slot_time = time(hour, 0)
        if today == timezone.now().date() and slot_time <= current_time:
            continue
            
        # Check if any barber is available at this time
        barbers_available = Barber.objects.filter(
            available=True
        ).exclude(
            booking__date=today,
            booking__time=slot_time,
            booking__status__in=['approved', 'pending']
        ).exists()
        
        if barbers_available:
            time_slots.append({
                'time': slot_time,
                'formatted': slot_time.strftime('%I:%M %p')
            })
    
    return time_slots[:3]  # Return first 3 available slots

@login_required
def profile(request):
    # Get or create client profile for the user
    client_profile, created = ClientProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=client_profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('/accounts/profile/')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=client_profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'profile': client_profile
    }
    return render(request, 'accounts/profile.html', context)

@login_required
def logout_view(request):
    """Custom logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('/')

# Remove the profile_setup view since all registrations are clients