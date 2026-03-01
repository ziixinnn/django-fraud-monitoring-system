from django.utils import timezone
from transaction.models import Transaction
from .models import Alert
from django.db import models

RISK_THRESHOLDS = {
    "VERY_HIGH": 0.9,
    "HIGH": 0.8,
    "MODERATE": 0.5,
    "LOW": 0.2,
    "VERY_LOW": 0.0,
}

def classify_risk_level(risk_score):
    for risk_level, threshold in RISK_THRESHOLDS.items():
        if risk_score >= threshold:
            return risk_level
        
def update_alert_status(updated_status, transaction):
    if updated_status in ("CONFIRM_FRAUD", "FALSE_POSITIVE", "MARK_AS_PENDING"):
        if updated_status in ("CONFIRM_FRAUD", "FALSE_POSITIVE"):
            alert_status = "RESOLVED"
        elif updated_status == "MARK_AS_PENDING":
            return None
        Alert.objects.filter(transaction=transaction).update(alert_status=alert_status, outcome=updated_status, resolution_time=timezone.now())
    elif updated_status in ("YES"):
        alert_status = "ESCALATED"
    Alert.objects.filter(transaction=transaction).update(alert_status=alert_status)

def create_alert(prediction):

    risk_score = prediction.risk_score
    risk_level = classify_risk_level(risk_score)
    if risk_level in ("LOW", "VERY_LOW"):
        return None
    
    reason = generate_alert_reason(prediction.transaction)

    snapshot = {
        'risk_score': risk_score,
        'reason': reason,
    }

    return Alert.objects.create(
        transaction=prediction.transaction,
        risk_level=risk_level,
        snapshot=snapshot
    )

def generate_alert_reason(transaction):
    reason = []

    qs = Transaction.objects.filter(sender_acc=transaction.sender_acc).exclude(pk=transaction.pk)

    avg_amount = qs.aggregate(avg_amount=models.Avg('amount'))['avg_amount']

    if avg_amount and transaction.amount > 3 * avg_amount:
        reason.append("Unusually high transaction amount")

    if not qs.filter(device_info=transaction.device_info).exists():
        reason.append("Unusual device used")

    if not qs.filter(location=transaction.location).exists():
        reason.append("Unusual transaction location")

    return reason

def handover_to_admin(issue_handover, additional_remark, alert):
    if issue_handover not in "YES":
        return None
    if alert.transaction.fraud_status not in "SUSPICIOUS":
        return None
    snapshot = alert.snapshot
    snapshot["issue_handover_to_admin"] = issue_handover
    snapshot["analyst_note"] = additional_remark
    alert.snapshot = snapshot

    transaction = alert.transaction
    update_alert_status(issue_handover, transaction)

    alert.save(update_fields=["snapshot"])

    return alert
