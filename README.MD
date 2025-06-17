# 💈 The Barbershop - Professional Booking Management System

![Django](https://img.shields.io/badge/Django-5.0.2-green.svg)
![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple.svg)
![License](https://img.shields.io/badge/License-Commercial-red.svg)

A complete, modern barbershop management system built with Django and Bootstrap. Perfect for barbershops, salons, and beauty service businesses.

## 🎯 **Demo**
- **Live Demo**: [Coming Soon]
- **Documentation**: This README

## ✨ **Key Features**

### 🔐 **User Management**
- **Role-based Authentication**: Clients, Barbers, Admin
- **Secure Registration & Login**: Email verification ready
- **User Profiles**: Customizable client and barber profiles
- **Admin Dashboard**: Complete business oversight

### 📅 **Smart Booking System**
- **Real-time Availability**: Dynamic time slot checking
- **Booking Workflow**: Request → Approve/Reject → Complete
- **Automatic Scheduling**: Prevents double bookings
- **24hr Cancellation Policy**: Built-in business rules

### 📧 **Email Notifications**
- **Instant Notifications**: All booking status changes
- **Professional Templates**: Branded email communications
- **Multi-recipient**: Clients and barbers stay informed
- **SMTP Ready**: Gmail, SendGrid, or any email service

### 👨‍💼 **Barber Management**
- **Individual Profiles**: Photos, specialties, ratings
- **Schedule Management**: Custom working hours per barber
- **Performance Tracking**: Revenue and booking analytics
- **Review System**: Client feedback and ratings

### 💰 **Business Intelligence**
- **Revenue Tracking**: Daily, weekly, monthly reports
- **Service Management**: Pricing and duration control
- **Client Analytics**: Booking history and preferences
- **Admin Insights**: Complete business overview

### 🎨 **Modern Design**
- **Responsive Layout**: Perfect on all devices
- **Bootstrap 5**: Latest styling framework
- **Dark/Light Theme**: Professional appearance
- **Mobile Optimized**: Touch-friendly interface

## 🛠️ **Technical Specifications**

### **Backend**
- **Framework**: Django 5.0.2
- **Database**: SQLite (dev) / PostgreSQL (production)
- **Authentication**: Django's built-in auth system
- **Email**: SMTP with HTML templates

### **Frontend**
- **CSS Framework**: Bootstrap 5.3
- **JavaScript**: Vanilla JS + AJAX
- **Icons**: Bootstrap Icons
- **Forms**: Django Crispy Forms

### **Architecture**
- **Design Pattern**: Model-View-Template (MVT)
- **Code Structure**: Modular Django apps
- **Security**: CSRF protection, user permissions
- **Performance**: Optimized queries and caching ready

## 📋 **Requirements**

### **System Requirements**
- Python 3.11 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### **Python Dependencies**
```txt
Django==5.0.2
Pillow==10.0.0
python-decouple==3.8
django-crispy-forms==2.0
crispy-bootstrap5==0.7
```

## 🚀 **Installation Guide**

### **Step 1: Download & Extract**
```bash
# Extract the downloaded files
unzip barbershop-management-system.zip
cd barbershop-management-system
```

### **Step 2: Set Up Virtual Environment**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### **Step 3: Install Dependencies**
```bash
# Install required packages
pip install -r requirements.txt
```

### **Step 4: Environment Configuration**
Create a `.env` file in the project root:
```env
SECRET_KEY=your-super-secret-key-here
DEBUG=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### **Step 5: Database Setup**
```bash
# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Load sample data (optional)
python manage.py create_sample_data
```

### **Step 6: Start Development Server**
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` to see your barbershop system!

## ⚙️ **Configuration Guide**

### **Email Setup**
The system supports multiple email backends:

**Gmail SMTP (Recommended):**
```python
# In settings.py
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
```

**For Development:**
```python
# Console backend (prints emails to terminal)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

### **Business Settings**
Customize your barbershop details in the admin panel:
- Shop name and contact information
- Business hours and holiday schedules
- Service pricing and duration
- Email templates and branding

## 📁 **File Structure**

```
barbershop_app/
├── accounts/                 # User management
│   ├── models.py            # User, ClientProfile models
│   ├── views.py             # Authentication, dashboards
│   ├── decorators.py        # Role-based access control
│   └── management/          # Management commands
├── barbers/                 # Barber management
│   ├── models.py            # Barber, Review, Schedule models
│   ├── views.py             # Barber profiles and listings
│   └── admin.py             # Admin interface
├── bookings/                # Booking system
│   ├── models.py            # Booking, Service models
│   ├── views.py             # Booking workflow
│   ├── forms.py             # Booking forms
│   ├── email_utils.py       # Email notifications
│   └── management/          # Booking commands
├── shop/                    # Business management
│   ├── models.py            # Revenue, Settings models
│   ├── views.py             # Analytics and reporting
│   └── admin.py             # Shop administration
├── templates/               # HTML templates
│   ├── base.html            # Base template
│   ├── accounts/            # User templates
│   ├── barbers/             # Barber templates
│   ├── bookings/            # Booking templates
│   └── registration/        # Auth templates
├── static/                  # Static files
│   ├── css/                 # Stylesheets
│   ├── js/                  # JavaScript files
│   └── images/              # Images and icons
├── media/                   # User uploads
├── requirements.txt         # Python dependencies
├── manage.py               # Django management script
└── README.md               # This documentation
```

## 🎨 **Customization Guide**

### **Branding & Styling**
1. **Logo**: Replace logo in `static/images/`
2. **Colors**: Edit CSS variables in `static/css/style.css`
3. **Fonts**: Update font imports in `base.html`
4. **Email Templates**: Modify `bookings/email_utils.py`

### **Business Logic**
1. **Services**: Add/edit in Django admin or `bookings/models.py`
2. **Working Hours**: Configure in barber schedules
3. **Pricing**: Manage through service pricing
4. **Policies**: Update cancellation rules in `bookings/views.py`

### **Advanced Customization**
- **Payment Integration**: Add Stripe/PayPal to booking flow
- **SMS Notifications**: Integrate Twilio for text alerts
- **Multi-location**: Extend models for multiple shops
- **API**: Add Django REST framework for mobile apps

## 🔧 **Admin Features**

Access the admin panel at `/admin/` with superuser credentials:

### **User Management**
- Create and manage user accounts
- Assign roles (Client, Barber, Admin)
- View user activity and statistics

### **Service Management**
- Add/edit services and pricing
- Set service duration and descriptions
- Manage service availability

### **Booking Oversight**
- View all bookings across the system
- Override booking statuses if needed
- Export booking data and reports

### **Business Analytics**
- Revenue tracking and reporting
- Popular services and barbers
- Client retention metrics

## 🎯 **User Workflows**

### **Client Journey**
1. **Registration**: Sign up with email verification
2. **Browse Barbers**: View profiles, ratings, availability
3. **Book Service**: Select service, barber, date, time
4. **Get Confirmed**: Receive email when barber approves
5. **Attend Appointment**: Show up and enjoy service
6. **Leave Review**: Rate and review the experience

### **Barber Workflow**
1. **Profile Setup**: Add photo, specialties, schedule
2. **Manage Bookings**: Approve/reject incoming requests
3. **Track Schedule**: View daily/weekly appointments
4. **Complete Services**: Mark appointments as finished
5. **View Analytics**: Check earnings and performance

### **Admin Operations**
1. **System Setup**: Configure business settings
2. **User Management**: Create barber accounts
3. **Monitor Business**: Track revenue and bookings
4. **Generate Reports**: Export data for analysis

## 🛡️ **Security Features**

- **CSRF Protection**: All forms protected against CSRF attacks
- **User Authentication**: Secure login with session management
- **Role-based Access**: Proper permission checking
- **SQL Injection Protection**: Django ORM prevents SQL injection
- **XSS Protection**: Template auto-escaping enabled
- **Secure Headers**: Security middleware enabled

## 📱 **Mobile Compatibility**

- **Responsive Design**: Works perfectly on all screen sizes
- **Touch Optimized**: Mobile-friendly buttons and forms
- **Fast Loading**: Optimized for mobile networks
- **App-like Experience**: PWA-ready architecture

## 🐛 **Troubleshooting**

### **Common Issues**

**Email not sending:**
```python
# Check email settings in settings.py
# For Gmail, ensure "Less secure app access" is enabled
# Or use App Passwords for 2FA accounts
```

**Static files not loading:**
```bash
# Collect static files for production
python manage.py collectstatic
```

**Database errors:**
```bash
# Reset database if needed
python manage.py flush
python manage.py migrate
```

**Permission errors:**
```python
# Check user roles in admin panel
# Ensure proper decorator usage in views
```

### **Getting Help**
1. Check this documentation first
2. Review Django official documentation
3. Contact support (see below)

## 📞 **Support & Updates**

### **What's Included**
- ✅ Full source code with comments
- ✅ Detailed documentation (this file)
- ✅ Installation support via email
- ✅ 6 months of free updates
- ✅ Bug fixes and security patches

### **Support Channels**
- **Documentation**: This README file
- **Response Time**: Within 24 hours (weekdays)

### **Update Policy**
- Minor updates and bug fixes: Free for 6 months
- Major feature additions: Paid upgrades available
- Security patches: Always free

## 📄 **License**

This is a commercial product licensed for:
- ✅ Personal and commercial use
- ✅ Client projects and freelance work
- ✅ Modification and customization
- ❌ Resale or redistribution of source code
- ❌ Creating competing products

## 🙏 **Credits**

### **Built With**
- [Django](https://djangoproject.com/) - Web framework
- [Bootstrap 5](https://getbootstrap.com/) - CSS framework
- [Bootstrap Icons](https://icons.getbootstrap.com/) - Icon library

### **Created By**
**AK**  
Version 1.0.0  
Created with ❤️ for the barbering community

---

## 🚀 **Quick Start Checklist**

- [ ] Extract files and create virtual environment
- [ ] Install dependencies with `pip install -r requirements.txt`
- [ ] Create `.env` file with your settings
- [ ] Run `python manage.py migrate`
- [ ] Create superuser with `python manage.py createsuperuser`
- [ ] Start server with `python manage.py runserver`
- [ ] Visit `http://127.0.0.1:8000` and explore!

**Enjoy your new barbershop management system!** 💈✨