from django.db import models
from account.models import CustomUser

class subscription(models.Model):
    subscriber_name = models.CharField(max_length=255)
    
    subscription_plan = models.CharField(max_length=1, choices=({'P':'Premium', 'S':'Standard'}))

    subscription_cost = models.CharField(max_length=50)

    paypal_susbscription_id = models.CharField(max_length=300)

    is_active = models.BooleanField(default=False)

    subscriber_user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, unique = True)

    def __str__(self) -> str:
        return f'{self.subscriber_name} - {self.subscription_plan}'
