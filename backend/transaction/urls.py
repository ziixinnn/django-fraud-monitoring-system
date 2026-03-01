from django.urls import path
from .views import CustomerHistoryTransactionView, ManualUpdateTransactionView, TransactionCreateView, TransactionDetailView, TransactionListView

urlpatterns = [
    path('post/', TransactionCreateView.as_view(), name='transaction-create'),
    path('get/', TransactionListView.as_view(), name='transaction-list'),
    path('get/<str:pk>/', TransactionDetailView.as_view(), name='transaction-detail'),
    path('post/<str:pk>/action/', ManualUpdateTransactionView.as_view(), name='action-to-transaction'),
    path("<str:customer_id>/", CustomerHistoryTransactionView.as_view(), name="customer-history-transactions"),
]
