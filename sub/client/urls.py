from django.urls import path
from .views import (client_profile_view, client_articles_view, create_subscription, account_management, update_paypal_subscription, update_sub_success, delete_client)

urlpatterns = [
    path('client-profile/',client_profile_view.as_view(), name='client-profile'),
    path('read-articles/',client_articles_view.as_view(), name='client-read-articles'),
    path('subscription/<subID>/<plan>/',create_subscription.as_view(), name='create-subscription'),
    path('management/',account_management.as_view(), name='account_management'),
    path('update-paypal-subscription/',update_paypal_subscription.as_view(), name='update-subscription'),
    path('update-success/',update_sub_success.as_view(), name='update-subscription-success'),
    path('delete-account/',delete_client.as_view(), name='client-delete-account'),
]
