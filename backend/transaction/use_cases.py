from alert.use_cases import create_alert, update_alert_status
from customer.use_cases import update_account_amount
from prediction.use_cases import predict

def build_balance_snapshot(transaction):
    sender = transaction.sender_acc
    receiver = transaction.receiver_acc
    amount = transaction.amount
    tx_type = transaction.transaction_type

    obo = sender.balance if sender else 0
    if tx_type in ("TRANSFER", "CASH_OUT"):
        nbo = obo - amount
    else:
        nbo = obo
    if receiver:
        obd = receiver.balance
        nbd = obd + amount if tx_type == "TRANSFER" else obd
    else:
        obd = 0
        nbd = 0

    return {
        "oldBalanceOrig": float(obo),
        "newBalanceOrig": float(nbo),
        "oldBalanceDest": float(obd),
        "newBalanceDest": float(nbd),
    }

def process_transaction(transaction):
    snapshot = build_balance_snapshot(transaction)
    prediction=predict(transaction, snapshot)
    update_status(prediction.fraud_label, transaction)
    if prediction.fraud_label in ("FRAUD"):
        create_alert(prediction)
    if transaction.transaction_status == "CLEARED":
        update_account_amount(transaction)

def update_status(fraud_label, transaction):
    if fraud_label == "FRAUD":
        transaction.fraud_status = "SUSPICIOUS"
        transaction.transaction_status = "FLAGGED"

    elif fraud_label == "LEGIT":
        transaction.fraud_status = "SAFE"
        transaction.transaction_status = "CLEARED"

    transaction.save(update_fields=[
        "fraud_status",
        "transaction_status"
    ])

def manual_update_status(updated_status, transaction):
    if updated_status == "CONFIRM_FRAUD":
        update_status('FRAUD', transaction)
    elif updated_status == "FALSE_POSITIVE":
        update_status('LEGIT', transaction)
    else:
        return None
    update_alert_status(updated_status, transaction)
