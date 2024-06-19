from typing import Any
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **kwargs):
        if not email:
            raise ValueError(gettext_lazy("email is required for creating user!"))
        
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()

        return user
    
    def create_superuser(self, email, password, **kwargs):
        
        kwargs.setdefault("is_staff",True)
        kwargs.setdefault("is_superuser",True)
        kwargs.setdefault("is_active",True)

        if kwargs.get("is_staff") is not True:
            raise ValueError(gettext_lazy("superuser must have is_staff=true"))
        if kwargs.get("is_superuser") is not True:
            raise ValueError(gettext_lazy("superuser must have is_superuser=ture"))

        return self.create_user(email, password, **kwargs)
