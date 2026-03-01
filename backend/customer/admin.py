from django.contrib import admin
from .models import Customer, CustomerAccount

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('customer_id', 'customer_name', 'customer_email', 'phone_number', 'created_at', 'updated_at')

admin.site.register(Customer, CustomerAdmin)

class CustomerAccountAdmin(admin.ModelAdmin):
    list_display = ('account_id', 'customer', 'bank_account_number', 'account_type', 'created_at', 'account_status')

admin.site.register(CustomerAccount, CustomerAccountAdmin)