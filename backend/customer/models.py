import secrets
from django.db import models

def generate_customer_id():
    return "C" + secrets.token_hex(6).upper()

def generate_account_id():
    return "A" + secrets.token_hex(6).upper()

ACCOUNT_TYPE = (
    ("SAVINGS", "Savings"),
    ("CREDIT", "Credit")
)

ACCOUNT_STATUSES = (
    ("FROZEN", "Frozen"),
    ("SUSPEND", "Suspend"),
    ("ACTIVE", "Active")
)

class Customer(models.Model):
    customer_id = models.CharField(max_length=25, primary_key=True, default=generate_customer_id)
    customer_name = models.CharField(max_length=50, null=False)
    customer_email= models.EmailField(max_length=100, blank=True)
    phone_number= models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.pk
    
    class Meta:
        db_table = "customers"
        ordering = ["-created_at"]
        verbose_name = "Customer"
        verbose_name_plural = "Customers"

class CustomerAccount(models.Model):
    account_id = models.CharField(primary_key=True, max_length=25, default=generate_account_id)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="accounts")
    bank_account_number = models.CharField(max_length=50, null=False)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPE)
    balance = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, default=0)    
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    account_status = models.CharField(max_length=20, choices=ACCOUNT_STATUSES, default="ACTIVE")

    def __str__(self):
        return self.pk
    
    class Meta:
        db_table = "customer_accounts"
        ordering = ["-created_at"]
        verbose_name = "Account"
        verbose_name_plural = "Accounts"
