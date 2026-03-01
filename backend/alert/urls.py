from django.urls import path
from .views import AlertDetailView, AlertFraudAnalysisView, AlertListView, IssueHandoverView, ResolvedAlertView

urlpatterns = [
    path('get/', AlertListView.as_view(), name='alert-list'),
    path('get/<str:pk>/', AlertDetailView.as_view(), name='alert-detail'),
    path('get/<str:pk>/analysis', AlertFraudAnalysisView.as_view(), name='alert-fraud-analysis'),
    path('get/<str:pk>/resolved-detail', ResolvedAlertView.as_view(), name='alert-resolved-detail'),
    path('<str:pk>/issue-handover-to-admin', IssueHandoverView.as_view(), name='issue-handover-to-admin')
]