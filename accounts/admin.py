# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from .models import ClientProfile

User = get_user_model()

class ClientProfileInline(admin.StackedInline):
    model = ClientProfile
    can_delete = False
    verbose_name_plural = 'Client Profile'

class UserAdmin(BaseUserAdmin):
    inlines = (ClientProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_barber', 'is_admin', 'is_staff')
    list_filter = ('is_barber', 'is_admin', 'is_staff', 'is_superuser', 'is_active')
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Role Information', {'fields': ('is_barber', 'is_admin')}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Role Information', {'fields': ('is_barber', 'is_admin')}),
    )

# Remove the unregister line - it's causing the error
# admin.site.unregister(User)  # REMOVE THIS LINE

# Register User with custom UserAdmin
admin.site.register(User, UserAdmin)

@admin.register(ClientProfile)
class ClientProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'preferred_barber', 'created_at')
    list_filter = ('created_at', 'preferred_barber')
    search_fields = ('user__username', 'user__email', 'phone')
    raw_id_fields = ('user', 'preferred_barber')