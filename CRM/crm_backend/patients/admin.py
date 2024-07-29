from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Patient, Appointment


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    # Показать дополнительные поля в списке пользователей
    list_display = ('username', 'email', 'first_name', 'last_name', 'position', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'groups', 'user_permissions')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'position')
    ordering = ('-date_joined',)

    # Для полей на странице редактирования
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'position')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'position'),
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Patient)
admin.site.register(Appointment)
