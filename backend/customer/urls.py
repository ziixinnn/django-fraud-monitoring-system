from django.urls import path

from .views import CustomerRiskProfileView

urlpatterns = [
    path('<str:pk>/', CustomerRiskProfileView.as_view(), name='customer-risk-profile')
]