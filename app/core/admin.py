from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from core import models
from django.utils.translation import gettext as _


@admin.register(models.User)
class UserAdmin(BaseUserAdmin):
    ordering = ['-id']
    list_display = ['first_name', 'last_name', 'email']
    readonly_fields = ['joined_date']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personel Information'), {'fields': ('first_name', 'last_name')}),
        (
            _('Permissions'),
            {
                'fields': ('is_active', 'is_staff', 'is_superuser')
            }
        ),
        (_('Important Dates'), {'fields': ('joined_date', 'last_login')})
    )
    add_fieldsets = (
        (None, {'fields': ('email', 'password1', 'password2')}),
        (_('Personel Information'), {'fields': ('first_name', 'last_name')}),
        (
            _('Permissions'),
            {
                'fields': ('is_active', 'is_staff', 'is_superuser')
            }
        ),
    )


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'user']
