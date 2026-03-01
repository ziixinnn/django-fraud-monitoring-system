from .models import CustomerAccount
from django.db.models import F

def update_account_amount(transaction):
        if transaction.transaction_status != "CLEARED":
            return
        
        sender = transaction.sender_acc
        receiver = transaction.receiver_acc
        amount = transaction.amount
        tx_type = transaction.transaction_type

        if tx_type in ("TRANSFER", "CASH_OUT"):
            if sender.balance < amount:
                raise ValueError("Insufficient balance")

            CustomerAccount.objects.filter(
                account_id=sender.account_id
            ).update(balance=F("balance") - amount)

        if tx_type == "TRANSFER" and receiver:
            CustomerAccount.objects.filter(
                account_id=receiver.account_id
            ).update(balance=F("balance") + amount)

def retrive_customer_history_transactions(customer):
    accounts = customer.accounts.all()
    transactions = []
    for acc in accounts:
        sent = acc.sent_transactions.all()
        received = acc.received_transactions.all()
        for transaction in sent:
            if transaction not in transactions:
                transactions.append(transaction)
        for transaction in received:
            if transaction not in transactions:
                transactions.append(transaction) 
    return transactions
