# barbers/admin.py
from django.contrib import admin
from .models import Barber, Review, BarberSchedule

class BarberScheduleInline(admin.TabularInline):
    model = BarberSchedule
    extra = 1
    max_num = 7  # One for each day of the week

@admin.register(Barber)
class BarberAdmin(admin.ModelAdmin):
    list_display = ('user', 'hourly_rate', 'experience_years', 'available', 'created_at')
    list_filter = ('available', 'experience_years', 'created_at')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'specialties')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [BarberScheduleInline]
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Professional Details', {
            'fields': ('bio', 'experience_years', 'specialties', 'hourly_rate')
        }),
        ('Status', {
            'fields': ('available', 'photo')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('barber', 'client', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('barber__user__username', 'client__username', 'comment')
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Review Information', {
            'fields': ('barber', 'client', 'rating')
        }),
        ('Content', {
            'fields': ('comment',)
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )

@admin.register(BarberSchedule)
class BarberScheduleAdmin(admin.ModelAdmin):
    list_display = ('barber', 'weekday', 'start_time', 'end_time', 'is_working')
    list_filter = ('weekday', 'is_working')
    search_fields = ('barber__user__username',)
    ordering = ['barber', 'weekday']