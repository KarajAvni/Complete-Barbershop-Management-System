# bookings/email_utils.py
from django.core.mail import send_mail
from django.conf import settings

def send_booking_emails(booking, email_type, **kwargs):
    """
    Send emails for different booking events
    email_type: 'created', 'approved', 'rejected', 'completed', 'cancelled'
    """
    
    # Email subject and content based on type
    if email_type == 'created':
        # Email to client
        send_mail(
            subject=f'Booking Request Submitted - {booking.service.name}',
            message=f'''Hi {booking.client.first_name or booking.client.username},

Your booking request has been submitted successfully!

📅 Service: {booking.service.name}
👨‍💼 Barber: {booking.barber.user.get_full_name() or booking.barber.user.username}
📆 Date: {booking.date.strftime("%A, %B %d, %Y")}
🕐 Time: {booking.time.strftime("%I:%M %p")}
💰 Price: ${booking.service.price}

Your booking is currently PENDING approval from the barber. You'll receive a confirmation email once it's approved.

Notes: {booking.notes or "None"}

Thanks for choosing The Barbershop!
''',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[booking.client.email],
        )
        
        # Email to barber
        send_mail(
            subject=f'New Booking Request - {booking.date} at {booking.time}',
            message=f'''Hi {booking.barber.user.first_name or booking.barber.user.username},

You have a new booking request!

👤 Client: {booking.client.get_full_name() or booking.client.username}
📧 Email: {booking.client.email}
📅 Service: {booking.service.name}
📆 Date: {booking.date.strftime("%A, %B %d, %Y")}
🕐 Time: {booking.time.strftime("%I:%M %p")}
💰 Price: ${booking.service.price}

Client Notes: {booking.notes or "None"}

Please log in to approve or reject this booking request.
''',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[booking.barber.user.email],
        )

    elif email_type == 'approved':
        message = kwargs.get('barber_comment', '')
        send_mail(
            subject=f'Booking Confirmed! - {booking.date} at {booking.time}',
            message=f'''Hi {booking.client.first_name or booking.client.username},

Great news! Your booking has been APPROVED! ✅

📅 Service: {booking.service.name}
👨‍💼 Barber: {booking.barber.user.get_full_name() or booking.barber.user.username}
📆 Date: {booking.date.strftime("%A, %B %d, %Y")}
🕐 Time: {booking.time.strftime("%I:%M %p")}
💰 Price: ${booking.service.price}

{f"Message from barber: {message}" if message else ""}

Please arrive 5 minutes early. We look forward to seeing you!

The Barbershop Team
''',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[booking.client.email],
        )

    elif email_type == 'rejected':
        reason = kwargs.get('rejection_reason', 'No reason provided')
        send_mail(
            subject=f'Booking Request Declined - {booking.date}',
            message=f'''Hi {booking.client.first_name or booking.client.username},

Unfortunately, your booking request for {booking.date.strftime("%A, %B %d")} at {booking.time.strftime("%I:%M %p")} has been declined.

Reason: {reason}

Please feel free to book another time slot that works better. We apologize for any inconvenience.

The Barbershop Team
''',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[booking.client.email],
        )

    elif email_type == 'completed':
        send_mail(
            subject=f'Thank You for Visiting The Barbershop!',
            message=f'''Hi {booking.client.first_name or booking.client.username},

Thank you for your visit today! We hope you're happy with your {booking.service.name}.

📅 Service: {booking.service.name}
👨‍💼 Barber: {booking.barber.user.get_full_name() or booking.barber.user.username}
📆 Date: {booking.date.strftime("%A, %B %d, %Y")}

We'd love to hear about your experience! Please consider leaving a review.

We look forward to seeing you again soon!

The Barbershop Team
''',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[booking.client.email],
        )

    elif email_type == 'cancelled':
        # Email to client
        send_mail(
            subject=f'Booking Cancelled - {booking.date}',
            message=f'''Hi {booking.client.first_name or booking.client.username},

Your booking has been successfully cancelled.

📅 Service: {booking.service.name}
📆 Date: {booking.date.strftime("%A, %B %d, %Y")}
🕐 Time: {booking.time.strftime("%I:%M %p")}

We're sorry to see you go. Feel free to book another appointment anytime!

The Barbershop Team
''',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[booking.client.email],
        )
        
        # Email to barber
        send_mail(
            subject=f'Booking Cancelled - {booking.client.username}',
            message=f'''Hi {booking.barber.user.first_name or booking.barber.user.username},

A booking has been cancelled:

👤 Client: {booking.client.get_full_name() or booking.client.username}
📅 Service: {booking.service.name}
📆 Date: {booking.date.strftime("%A, %B %d, %Y")}
🕐 Time: {booking.time.strftime("%I:%M %p")}

This time slot is now available for other bookings.
''',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[booking.barber.user.email],
        )