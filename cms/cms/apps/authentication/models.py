from django.db import models
from django.core.validators import EmailValidator, RegexValidator, MinLengthValidator
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _

from .manager import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True, validators=[EmailValidator])
    first_name = models.CharField(max_length=10)
    last_name = models.CharField(max_length=10)
    phone = models.CharField(max_length=10)
    address = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=15, null=True, blank=True)
    state = models.CharField(max_length=20, null=True, blank=True)
    country = models.CharField(max_length=20, null=True, blank=True)
    pincode = models.CharField(max_length=6)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone', 'pincode']

    objects = CustomUserManager()

    def __str__(self):
        return self.email
