
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth import get_user_model
from .managers import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=150)
    dateOfBirth = models.DateField()
    phone = PhoneNumberField()
    nationalId = models.IntegerField()

    objects = CustomUserManager()


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'nationalId', 'phone', 'dateOfBirth']
