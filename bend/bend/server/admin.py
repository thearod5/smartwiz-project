from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from api.models import User


@admin.register(User)  # Registers the User model with the custom admin class
class CustomUserAdmin(UserAdmin):
    # Add custom fields to the admin interface
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('middle_name', 'primary_address')}),
    )

    # List additional fields in the admin list view if needed
    list_display = UserAdmin.list_display + ('middle_name', 'primary_address',)
