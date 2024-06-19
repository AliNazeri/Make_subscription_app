from django.db import models
from .manages import CustomUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone

class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = None
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=60)
    
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True) # change to false if email is connected
    is_writer = models.BooleanField(default=False, verbose_name="Are you a writer?")
    date_joined = models.TimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
    def __str__(self):
        return self.email
