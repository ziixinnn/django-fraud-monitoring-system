import secrets
from django.db import models

TRANSACTION_TYPES = (
    ("CASH_IN", "Cash In"),
    ("CASH_OUT", "Cash Out"),
    ("DEBIT", "Debit"),
    ("PAYMENT", "Payment"),
    ("TRANSFER", "Transfer"),
)

TRANSACTION_STATUSES = (
    ("PENDING_ANALYSIS", "Pending Analysis"),
    ("FLAGGED", "Flagged"),
    ("CLEARED", "Cleared"),
)

FRAUD_STATUSES = (
    ("SUSPICIOUS", "Suspicious"),
    ("SAFE", "Safe"),
)

def generate_transaction_id():
    return "T" + secrets.token_hex(6).upper()

class Transaction(models.Model):
    transaction_id = models.CharField(primary_key=True, max_length=25, default=generate_transaction_id)
    sender_acc = models.ForeignKey("customer.CustomerAccount", on_delete=models.CASCADE, related_name="sent_transactions")
    receiver_acc = models.ForeignKey("customer.CustomerAccount", on_delete=models.CASCADE, related_name="received_transactions")
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=255)
    device_info = models.CharField(max_length=255)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    transaction_status = models.CharField(max_length=20, choices=TRANSACTION_STATUSES, default="PENDING_ANALYSIS")
    fraud_status = models.CharField(max_length=20, choices=FRAUD_STATUSES, blank=True, default='')

    @classmethod
    def create(cls, amount:float, location:str, device_info:str, transaction_type:str, sender_acc:str, receiver_acc:str):
        return cls.objects.create(
            amount=amount,
            location=location,
            device_info=device_info,
            transaction_type=transaction_type,
            transaction_status='PENDING ANALYSIS',
            sender_acc=sender_acc,
            receiver_acc=receiver_acc
        )

    def __str__(self):
        return f"{self.pk} - {self.transaction_type} - {self.amount}"
    
    class Meta:
        db_table = 'transactions'
        ordering = ['-timestamp']
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'

    