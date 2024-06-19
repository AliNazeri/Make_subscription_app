from django.db import models
from account.models import CustomUser

class articles(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField(max_length=1000, verbose_name='context')
    publish_date = models.DateTimeField(auto_now_add=True)

    is_premium = models.BooleanField(default=False, verbose_name="Is this only for Premium users?")

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title