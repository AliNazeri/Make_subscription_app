from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class user_reg_form(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'password1', 'password2', 'is_writer',]