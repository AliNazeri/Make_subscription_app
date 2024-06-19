from django import forms
from .models import articles

class article_form(forms.ModelForm):
    class Meta:
        model = articles
        fields = ['title','text','is_premium']