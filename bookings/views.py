# bookings/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from django.http import JsonResponse
from datetime import datetime, timedelta, time
from .models import Booking, Service
from .forms import BookingForm
from barbers.models import Barber
from accounts.decorators import client_required, barber_required
from .email_utils import send_booking_emails

@login_required
@client_required
def book_appointment(request):
    """Allow clients to book appointments"""
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.client = request.user
            
            # Check if the slot is still available
            existing = Booking.objects.filter(
                barber=booking.barber,
                date=booking.date,
                time=booking.time,
                status__in=['pending', 'approved']
            ).exists()
            
            if existing:
                messages.error(request, "This time slot is no longer available.")
                return redirect('bookings:book')
            
            booking.save()
            
            # Send email notifications
            send_booking_emails(booking, 'created')
            
            print("New Appointment")  # Debug print
            messages.success(request, "Booking request submitted! The barber will review your request.")
            return redirect('bookings:history')
    else:
        form = BookingForm()
    
    # Get available barbers and services
    services = Service.objects.filter(active=True)
    barbers = Barber.objects.filter(available=True)
    
    context = {
        'form': form,
        'services': services,
        'barbers': barbers,
    }
    return render(request, 'bookings/book_appointment.html', context)

@login_required
@client_required
def booking_history(request):
    """Show client's booking history"""
    bookings = Booking.objects.filter(
        client=request.user
    ).select_related('barber__user', 'service').order_by('-date', '-time')
    
    print(f"Found {bookings.count()} bookings for user {request.user.username}")  # Debug
    for booking in bookings:
        print(f"Booking: {booking.service.name} with {booking.barber} on {booking.date} - Status: {booking.status}")
    
    context = {
        'bookings': bookings,
    }
    return render(request, 'bookings/booking_history.html', context)

@login_required
def booking_detail(request, pk):
    """View booking details"""
    booking = get_object_or_404(Booking, pk=pk)
    
    # Check if user has permission to view this booking
    has_permission = False
    if request.user == booking.client:
        has_permission = True
    elif request.user.is_barber:
        try:
            barber = Barber.objects.get(user=request.user)
            if barber == booking.barber:
                has_permission = True
        except Barber.DoesNotExist:
            pass
    elif request.user.is_superuser or request.user.is_admin:
        has_permission = True
    
    if not has_permission:
        messages.error(request, "You don't have permission to view this booking.")
        return redirect('accounts:dashboard')
    
    context = {
        'booking': booking
    }
    return render(request, 'bookings/booking_detail.html', context)

@login_required
@barber_required
def manage_bookings(request):
    """Allow barbers to manage their bookings"""
    try:
        barber = Barber.objects.get(user=request.user)
    except Barber.DoesNotExist:
        messages.error(request, "Barber profile not found.")
        return redirect('accounts:dashboard')
    
    # Handle POST requests for approve/reject actions
    if request.method == 'POST':
        booking_id = request.POST.get('booking_id')
        action = request.POST.get('action')
        comment = request.POST.get('comment', '')
        
        if booking_id and action:
            try:
                booking = Booking.objects.get(id=booking_id, barber=barber)
                if action == 'approve' and booking.status == 'pending':
                    booking.status = 'approved'
                    booking.barber_comment = comment
                    booking.save()
                    
                    # Send approval email
                    send_booking_emails(booking, 'approved', barber_comment=comment)
                    
                    messages.success(request, f"Booking for {booking.client.get_full_name() or booking.client.username} approved!")
                elif action == 'reject' and booking.status == 'pending':
                    booking.status = 'rejected'
                    booking.rejection_reason = comment
                    booking.save()
                    
                    # Send rejection email
                    send_booking_emails(booking, 'rejected', rejection_reason=comment)
                    
                    messages.success(request, f"Booking for {booking.client.get_full_name() or booking.client.username} rejected.")
                elif action == 'complete' and booking.status == 'approved':
                    booking.status = 'completed'
                    booking.save()
                    
                    # Send completion email
                    send_booking_emails(booking, 'completed')
                    
                    messages.success(request, f"Booking for {booking.client.get_full_name() or booking.client.username} marked as completed!")
            except Booking.DoesNotExist:
                messages.error(request, "Booking not found.")
        
        return redirect('bookings:manage')
    
    # Get bookings for this barber
    all_bookings = Booking.objects.filter(
        barber=barber
    ).select_related('client', 'service').order_by('-date', '-time')
    
    pending_bookings = all_bookings.filter(status='pending')
    approved_bookings = all_bookings.filter(status='approved')
    
    print(f"Barber {barber} has {all_bookings.count()} total bookings, {pending_bookings.count()} pending")
    
    context = {
        'bookings': all_bookings,
        'pending_bookings': pending_bookings,
        'approved_bookings': approved_bookings,
        'pending_count': pending_bookings.count(),
        'barber': barber,
    }
    return render(request, 'bookings/manage_bookings.html', context)

@login_required
@barber_required
def approve_booking(request, pk):
    """Approve a booking request"""
    booking = get_object_or_404(Booking, pk=pk)
    
    try:
        barber = Barber.objects.get(user=request.user)
        if barber != booking.barber:
            messages.error(request, "You can only manage your own bookings.")
            return redirect('bookings:manage')
    except Barber.DoesNotExist:
        messages.error(request, "Barber profile not found.")
        return redirect('bookings:manage')
    
    if booking.status != 'pending':
        messages.warning(request, "This booking has already been processed.")
        return redirect('bookings:manage')
    
    if request.method == 'POST':
        booking.status = 'approved'
        booking.save()
        
        # Send approval email
        send_booking_emails(booking, 'approved')
        
        messages.success(request, f"Booking for {booking.client.get_full_name() or booking.client.username} approved!")
        
    return redirect('bookings:manage')

@login_required
@barber_required
def reject_booking(request, pk):
    """Reject a booking request"""
    booking = get_object_or_404(Booking, pk=pk)
    
    try:
        barber = Barber.objects.get(user=request.user)
        if barber != booking.barber:
            messages.error(request, "You can only manage your own bookings.")
            return redirect('bookings:manage')
    except Barber.DoesNotExist:
        messages.error(request, "Barber profile not found.")
        return redirect('bookings:manage')
    
    if booking.status != 'pending':
        messages.warning(request, "This booking has already been processed.")
        return redirect('bookings:manage')
    
    if request.method == 'POST':
        reason = request.POST.get('rejection_reason', '')
        booking.status = 'rejected'
        booking.rejection_reason = reason
        booking.save()
        
        # Send rejection email
        send_booking_emails(booking, 'rejected', rejection_reason=reason)
        
        messages.success(request, f"Booking for {booking.client.get_full_name() or booking.client.username} rejected.")
        
    return redirect('bookings:manage')

@login_required
@client_required
def cancel_booking(request, pk):
    """Allow clients to cancel their bookings"""
    booking = get_object_or_404(Booking, pk=pk, client=request.user)
    
    # Check if booking can be cancelled (only pending or approved bookings)
    if booking.status not in ['pending', 'approved']:
        messages.error(request, "This booking cannot be cancelled.")
        return redirect('bookings:history')
    
    # Check if it's not too late to cancel (24 hours before appointment)
    appointment_datetime = datetime.combine(booking.date, booking.time)
    if appointment_datetime <= timezone.now() + timedelta(hours=24):
        messages.error(request, "You can only cancel bookings at least 24 hours in advance.")
        return redirect('bookings:history')
    
    if request.method == 'POST':
        booking.status = 'cancelled'
        booking.save()
        
        # Send cancellation emails
        send_booking_emails(booking, 'cancelled')
        
        messages.success(request, "Booking cancelled successfully.")
        
    return redirect('bookings:history')

def get_available_slots(request):
    """AJAX view to get available time slots for a specific barber and date"""
    if request.method == 'GET':
        barber_id = request.GET.get('barber_id')
        date_str = request.GET.get('date')
        
        if not barber_id or not date_str:
            return JsonResponse({'times': []})
        
        try:
            barber = Barber.objects.get(pk=barber_id)
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
            
            # Get barber's schedule for that day
            weekday = date.weekday()
            schedule = barber.schedules.filter(weekday=weekday, is_working=True).first()
            
            if not schedule:
                return JsonResponse({'times': []})
            
            # Generate time slots
            slots = []
            current_time = datetime.combine(date, schedule.start_time)
            end_time = datetime.combine(date, schedule.end_time)
            
            while current_time < end_time:
                # Check if slot is not already booked
                is_booked = Booking.objects.filter(
                    barber=barber,
                    date=date,
                    time=current_time.time(),
                    status__in=['pending', 'approved']
                ).exists()
                
                if not is_booked:
                    # Check if the time is in the future
                    if date > timezone.now().date() or (date == timezone.now().date() and current_time.time() > timezone.now().time()):
                        slots.append(current_time.strftime('%H:%M'))
                
                current_time += timedelta(minutes=30)  # 30-minute slots
            
            return JsonResponse({'times': slots})
            
        except (Barber.DoesNotExist, ValueError):
            return JsonResponse({'times': []})
    
    return JsonResponse({'error': 'Invalid request'}, status=400)