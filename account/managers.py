from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _



class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email_or_mobile, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email_or_mobile:
            raise ValueError(_('email_or_mobile cannot be blank'))
        user = self.model(email_or_mobile=email_or_mobile, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email_or_mobile, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email_or_mobile, password, **extra_fields)