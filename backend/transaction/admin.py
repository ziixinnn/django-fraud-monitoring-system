from django.contrib import admin
from .models import Transaction

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'amount', 'timestamp', 'location', 'device_info', 'transaction_type', 'transaction_status', 'fraud_status')

admin.site.register(Transaction, TransactionAdmin)