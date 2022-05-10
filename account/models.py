from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.utils.crypto import get_random_string
from .managers import CustomUserManager
from datetime import datetime
from django.conf import settings

class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class CustomUser(AbstractBaseUser, PermissionsMixin,TimeStampModel):
    email_or_mobile = models.CharField(max_length=64,unique=True)
    fullname = models.CharField(_('full name'), max_length=64)
    is_verified = models.BooleanField(_('verified'),default=False)
    otp = models.CharField(_('token'), max_length=8)
    expire_at = models.DateTimeField()
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    USERNAME_FIELD = 'email_or_mobile'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email_or_mobile
    
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
