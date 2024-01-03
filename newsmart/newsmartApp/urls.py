from .views import *
from django.urls import path

urlpatterns = [
    path("user_registration/", userRegistration),
    path("user_login/", login),
    path("send-otp/", sendOtp)
]
