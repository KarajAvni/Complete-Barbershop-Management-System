# shop/admin.py
from django.contrib import admin
from .models import ShopSettings, Revenue, Expense

@admin.register(ShopSettings)
class ShopSettingsAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'opening_time', 'closing_time')
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'address', 'phone', 'email')
        }),
        ('Operating Hours', {
            'fields': ('opening_time', 'closing_time')
        }),
        ('Booking Settings', {
            'fields': ('slot_duration', 'max_advance_booking_days', 'cancellation_hours')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    readonly_fields = ('created_at', 'updated_at')
    
    def has_add_permission(self, request):
        # Only allow one instance
        return not ShopSettings.objects.exists()

@admin.register(Revenue)
class RevenueAdmin(admin.ModelAdmin):
    list_display = ('barber', 'booking', 'amount', 'barber_earning', 'shop_earning', 'date')
    list_filter = ('date', 'barber')
    search_fields = ('barber__user__username', 'booking__client__username')
    date_hierarchy = 'date'
    readonly_fields = ('barber_earning', 'shop_earning', 'created_at')
    
    fieldsets = (
        ('Revenue Information', {
            'fields': ('barber', 'booking', 'amount', 'commission_rate', 'date')
        }),
        ('Earnings Breakdown', {
            'fields': ('barber_earning', 'shop_earning'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('barber__user', 'booking__client')

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('description', 'category', 'amount', 'date', 'created_by')
    list_filter = ('category', 'date')
    search_fields = ('description',)
    date_hierarchy = 'date'
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Expense Details', {
            'fields': ('description', 'category', 'amount', 'date')
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at'),
            'classes': ('collapse',)
        })
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating new expense
            obj.created_by = request.user
        super().save_model(request, obj, form, change)