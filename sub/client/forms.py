from django.forms import ModelForm
from account.models import CustomUser

class client_profile_form(ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name','last_name','email']
        exclude = ['password1','password2']