# accounts/management/commands/create_sample_data.py
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from barbers.models import Barber, BarberSchedule, Review
from bookings.models import Service, Booking, FavoriteBarber
from shop.models import ShopSettings
from datetime import time, date, timedelta
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates sample data for testing'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating sample data...')
        
        # Create Shop Settings
        shop, created = ShopSettings.objects.get_or_create(
            name="The Elite Barbershop",
            defaults={
                'address': '123 Main Street, Downtown, NY 10001',
                'phone': '(555) 123-4567',
                'email': 'info@elitebarbershop.com',
                'opening_time': time(9, 0),
                'closing_time': time(19, 0),
                'slot_duration': 30,
                'max_advance_booking_days': 30,
                'cancellation_hours': 24,
            }
        )
        self.stdout.write(self.style.SUCCESS(f'✓ Shop settings {"created" if created else "already exists"}'))
        
        # Create Services
        services_data = [
            {'name': 'Classic Haircut', 'price': 30.00, 'duration_minutes': 30, 'description': 'Traditional haircut with styling'},
            {'name': 'Beard Trim', 'price': 20.00, 'duration_minutes': 20, 'description': 'Professional beard shaping and trim'},
            {'name': 'Hair + Beard Combo', 'price': 45.00, 'duration_minutes': 45, 'description': 'Complete grooming package'},
            {'name': 'Kids Haircut', 'price': 25.00, 'duration_minutes': 25, 'description': 'Gentle haircut for children under 12'},
            {'name': 'Hot Shave', 'price': 35.00, 'duration_minutes': 40, 'description': 'Classic hot towel shave'},
            {'name': 'Hair Design', 'price': 40.00, 'duration_minutes': 45, 'description': 'Creative cuts with designs'},
        ]
        
        services = []
        for service_data in services_data:
            service, created = Service.objects.get_or_create(
                name=service_data['name'],
                defaults=service_data
            )
            services.append(service)
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Created service: {service.name}'))
        
        # Create Barbers
        barber_data = [
            {
                'username': 'john_barber',
                'email': 'john@barbershop.com',
                'first_name': 'John',
                'last_name': 'Smith',
                'bio': 'Master barber with 10+ years experience. Specializing in modern cuts and traditional styles.',
                'experience_years': 10,
                'specialties': 'Fades, Pompadours, Classic Cuts',
                'hourly_rate': 40.00
            },
            {
                'username': 'mike_stylist',
                'email': 'mike@barbershop.com',
                'first_name': 'Mike',
                'last_name': 'Johnson',
                'bio': 'Creative stylist specializing in modern trends and hair designs.',
                'experience_years': 7,
                'specialties': 'Hair Design, Modern Cuts, Color',
                'hourly_rate': 35.00
            },
            {
                'username': 'alex_barber',
                'email': 'alex@barbershop.com',
                'first_name': 'Alex',
                'last_name': 'Williams',
                'bio': 'Expert in beard grooming and classic barbering techniques.',
                'experience_years': 5,
                'specialties': 'Beard Grooming, Hot Shaves, Classic Cuts',
                'hourly_rate': 30.00
            }
        ]
        
        barbers = []
        for data in barber_data:
            user, user_created = User.objects.get_or_create(
                username=data['username'],
                defaults={
                    'email': data['email'],
                    'first_name': data['first_name'],
                    'last_name': data['last_name'],
                    'is_barber': True
                }
            )
            
            if user_created:
                user.set_password('barbershop123')
                user.save()
                self.stdout.write(self.style.SUCCESS(f'✓ Created barber user: {user.username}'))
            
            barber, barber_created = Barber.objects.get_or_create(
                user=user,
                defaults={
                    'bio': data['bio'],
                    'experience_years': data['experience_years'],
                    'specialties': data['specialties'],
                    'hourly_rate': data['hourly_rate'],
                    'available': True
                }
            )
            barbers.append(barber)
            
            # Create schedule for each barber (Monday to Saturday, 9 AM to 6 PM)
            for day in range(6):  # 0=Monday to 5=Saturday
                schedule, created = BarberSchedule.objects.get_or_create(
                    barber=barber,
                    weekday=day,
                    defaults={
                        'start_time': time(9, 0),
                        'end_time': time(18, 0),
                        'is_working': True
                    }
                )
        
        # Create Client Users
        client_data = [
            {'username': 'client1', 'email': 'client1@example.com', 'first_name': 'David', 'last_name': 'Brown'},
            {'username': 'client2', 'email': 'client2@example.com', 'first_name': 'James', 'last_name': 'Davis'},
            {'username': 'client3', 'email': 'client3@example.com', 'first_name': 'Robert', 'last_name': 'Miller'},
            {'username': 'client4', 'email': 'client4@example.com', 'first_name': 'William', 'last_name': 'Wilson'},
        ]
        
        clients = []
        for data in client_data:
            user, created = User.objects.get_or_create(
                username=data['username'],
                defaults={
                    'email': data['email'],
                    'first_name': data['first_name'],
                    'last_name': data['last_name']
                }
            )
            
            if created:
                user.set_password('client123')
                user.save()
                self.stdout.write(self.style.SUCCESS(f'✓ Created client user: {user.username}'))
            clients.append(user)
        
        # Create some bookings
        statuses = ['completed', 'approved', 'pending']
        today = timezone.now().date()
        
        for i in range(20):
            # Random date within last 30 days and next 7 days
            days_offset = random.randint(-30, 7)
            booking_date = today + timedelta(days=days_offset)
            
            # Random time between 9 AM and 5 PM
            hour = random.randint(9, 17)
            booking_time = time(hour, random.choice([0, 30]))
            
            # Determine status based on date
            if booking_date < today:
                status = 'completed'
            elif booking_date == today:
                status = random.choice(['approved', 'pending'])
            else:
                status = random.choice(['approved', 'pending'])
            
            booking = Booking.objects.create(
                client=random.choice(clients),
                barber=random.choice(barbers),
                service=random.choice(services),
                date=booking_date,
                time=booking_time,
                status=status,
                notes=f'Booking #{i+1}'
            )
            
        self.stdout.write(self.style.SUCCESS('✓ Created sample bookings'))
        
        # Create some reviews for completed bookings
        completed_bookings = Booking.objects.filter(status='completed')
        review_comments = [
            "Excellent service! Very professional.",
            "Great haircut, exactly what I wanted.",
            "Always a pleasure, highly recommend!",
            "Quick and efficient service.",
            "Best barber in town!",
            "Very satisfied with the results.",
        ]
        
        for booking in completed_bookings[:10]:  # Create reviews for first 10 completed bookings
            Review.objects.get_or_create(
                barber=booking.barber,
                client=booking.client,
                defaults={
                    'rating': random.randint(4, 5),
                    'comment': random.choice(review_comments)
                }
            )
        
        self.stdout.write(self.style.SUCCESS('✓ Created sample reviews'))
        
        # Create some favorite barbers
        for client in clients[:2]:
            for barber in barbers[:2]:
                FavoriteBarber.objects.get_or_create(
                    client=client,
                    barber=barber
                )
        
        self.stdout.write(self.style.SUCCESS('✓ Created favorite barbers'))
        
        # Summary
        self.stdout.write(self.style.SUCCESS('\n' + '='*50))
        self.stdout.write(self.style.SUCCESS('Sample data created successfully!'))
        self.stdout.write(self.style.SUCCESS('='*50))
        self.stdout.write(self.style.WARNING('\nLogin credentials:'))
        self.stdout.write('Barbers: john_barber, mike_stylist, alex_barber (password: barbershop123)')
        self.stdout.write('Clients: client1, client2, client3, client4 (password: client123)')
        self.stdout.write(self.style.WARNING('\nYou can now login and test the application!'))