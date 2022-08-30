from email.policy import default
from sre_constants import CH_LOCALE
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.utils.crypto import get_random_string
from .managers import CustomUserManager
from datetime import datetime
from django.conf import settings
from django.urls import reverse
from django.utils.html import format_html



class TimeStampModel(models.Model):
    id = models.AutoField(primary_key=True,editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class CustomUser(AbstractBaseUser, PermissionsMixin,TimeStampModel):
    GENDER_CHOICES = (
        ("male","Male"),
        ("female","Female"),
    )
    email_or_mobile = models.CharField(max_length=64,unique=True)
    fullname = models.CharField(_('full name'), max_length=64)
    is_verified = models.BooleanField(_('verified'),default=False)
    otp = models.CharField(_('token'), max_length=8)
    expire_at = models.DateTimeField()
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    USERNAME_FIELD = 'email_or_mobile'
    REQUIRED_FIELDS = []
    # mobile field
    mobile = models.BigIntegerField(null=True, blank=True)
    is_mobile_verified = models.BooleanField(default=False)
    # personal information
    gender = models.CharField(_('gender'), max_length=64, blank=True, null=True,choices=GENDER_CHOICES,default="male")

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.email_or_mobile}"
    
    def save(self, *args, **kwargs):
        self.otp = get_random_string(length=6,allowed_chars="0123456789")
        self.expire_at = timezone.now()+settings.OTP['OTP_EXPIRATION_TIME']
        super(CustomUser,self).save(*args, **kwargs)

    @property
    def is_expired(self):
        if not self.expire_at > timezone.now():
            return True
        else:
            return False

class UserAddress(TimeStampModel):
    user = models.ForeignKey(CustomUser,on_delete = models.CASCADE,related_name = "user_address")
    full_name = models.CharField(max_length=24)
    city = models.CharField(max_length=24)
    state = models.CharField(max_length=24)
    country = models.CharField(max_length = 24)
    pincode = models.IntegerField()
    locality = models.CharField(max_length = 64)
    landmark = models.CharField(max_length = 64,null = True)
    address = models.TextField()
    alternate_number = models.BigIntegerField()


    class Meta:
        ordering = ["-id"]


# Razorpay contact
class Contact(TimeStampModel):
    user = models.ForeignKey(CustomUser,on_delete = models.CASCADE,related_name = "contact")
    razorpay_conatct_id = models.CharField(max_length=64,verbose_name=_("razorpay contact id"))

    class Meta:
        ordering = ["-id"]
        db_table = "contacts"
        verbose_name_plural =  _("Razorpay Contact")

# Razorpay fund Acc
class FundAccout(TimeStampModel):
    user = models.ForeignKey(CustomUser,on_delete = models.CASCADE,related_name = "fund_acc")
    contact_id = models.CharField(max_length=64,verbose_name=_("contact id"))
    razorpay_fund_id = models.CharField(max_length=64,verbose_name=_("razorpay fund id"))
    account_type = models.CharField(max_length=64)
    ifsc = models.CharField(max_length = 64)
    bank_name = models.CharField(max_length = 64)
    name = models.CharField(max_length = 64)
    account_number = models.PositiveBigIntegerField()
    active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.id}"

    class Meta:
        ordering = ["-id"]
        verbose_name_plural =  _("Fund Account")
    
    
    
