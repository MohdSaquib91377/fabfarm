from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('id','fullname','email_or_mobile', 'is_staff', 'is_active','is_verified','otp','expire_at',"mobile","is_mobile_verified")
    list_filter = ('email_or_mobile', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email_or_mobile', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email_or_mobile', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email_or_mobile',)
    ordering = ('email_or_mobile',)


admin.site.register(CustomUser, CustomUserAdmin)