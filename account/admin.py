from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser,Contact,FundAccout


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('id','fullname','email_or_mobile', 'is_staff', 'is_active','is_verified','otp','expire_at',"mobile","is_mobile_verified")
    list_filter = ('email_or_mobile', 'is_staff', 'is_active',"fullname","mobile")
    fieldsets = (
        (None, {'fields': ('email_or_mobile', 'password',"mobile","is_mobile_verified")}),
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

class ContactAdmin(admin.ModelAdmin):
    list_display = ["id","user","razorpay_conatct_id"]

class FundAccoutAdmin(admin.ModelAdmin):
    list_display = ["id","user","contact_id","razorpay_fund_id","account_type","ifsc","bank_name","name","account_number","active","make_refund"]

admin.site.register(Contact, ContactAdmin)
admin.site.register(FundAccout, FundAccoutAdmin)
