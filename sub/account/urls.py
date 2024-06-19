from django.urls import path
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordResetCompleteView, PasswordResetDoneView
from .views import (home_view, register_view, login_view, logout_view,email_verification, email_verification_sent,
                    email_verification_success, email_verification_failed)
urlpatterns = [
    path("", home_view.as_view(), name = ""),
    path("register/", register_view.as_view(), name="register"),
    path("login/", login_view.as_view(), name="login"),
    path("logout/", logout_view.as_view(), name="logout"),

    path('reset_password', PasswordResetView.as_view(), name='reset_password'),
    path('reset_password_sent', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<toekn>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset_complete', PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('email-verification/<str:uidb64>/<str:token>/', email_verification.as_view(), name='email-verification'),
    path('email-verification-sent', email_verification_sent.as_view(), name='email-verification-sent'),
    path('email-verification-success', email_verification_success.as_view(), name='email-verification-success'),
    path('email-verification-failed', email_verification_failed.as_view(), name='email-verification-failed'),
]

