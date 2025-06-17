# bookings/admin.py
from django.contrib import admin
from .models import Service, Booking, FavoriteBarber

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration_minutes', 'active')  # Changed from 'is_active' to 'active'
    list_filter = ('active',)  # Changed from 'is_active' to 'active'
    search_fields = ('name', 'description')
    ordering = ('name',)
    
    fieldsets = (
        ('Service Information', {
            'fields': ('name', 'description', 'price', 'duration_minutes')
        }),
        ('Status', {
            'fields': ('active',)
        })
    )

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('client', 'barber', 'service', 'date', 'time', 'status', 'created_at')
    list_filter = ('status', 'date', 'created_at')
    search_fields = ('client__username', 'barber__user__username', 'service__name')
    date_hierarchy = 'date'
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Booking Information', {
            'fields': ('client', 'barber', 'service', 'date', 'time')
        }),
        ('Status', {
            'fields': ('status', 'notes', 'rejection_reason')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('client', 'barber__user', 'service')

@admin.register(FavoriteBarber)
class FavoriteBarberAdmin(admin.ModelAdmin):
    list_display = ('client', 'barber', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('client__username', 'barber__user__username')
    date_hierarchy = 'created_at'
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('client', 'barber__user')