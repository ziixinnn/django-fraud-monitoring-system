from django.urls import path
from .views import LoginView, check_auth

urlpatterns = [
    path("login/", LoginView.as_view(), name="staff-login"),
    path("auth/check/", check_auth, name="staff-check-auth"),
]
