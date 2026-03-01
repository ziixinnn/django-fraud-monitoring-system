import secrets
from django.db import models

RISK_LEVELS = (
    ("VERY_HIGH", "Very High"),
    ("HIGH", "High"),
    ("MODERATE", "Moderate"),
)

ALERT_STATUSES = (
    ("PENDING", "Pending"),
    ("RESOLVED", "Resolved"),
    ("ESCALATED", "Escalated"),
)

OUTCOMES = (
    ("CONFIRM_FRAUD", "Confirm Fraud"),
    ("FALSE_POSITIVE", "False Positive"),
)

def generate_alert_id():
    return "A" + secrets.token_hex(6).upper()

class Alert(models.Model):
    alert_id = models.CharField(primary_key=True, max_length=25, default=generate_alert_id)
    alert_status = models.CharField(max_length=20, choices=ALERT_STATUSES, default="PENDING")
    transaction = models.ForeignKey('transaction.Transaction', on_delete=models.CASCADE, related_name="alerts")
    risk_level = models.CharField(max_length=20, choices=RISK_LEVELS)
    message = models.TextField()
    snapshot = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    resolution_time = models.DateTimeField(null=True, blank=True)
    outcome = models.CharField(max_length=20, choices=OUTCOMES, null=True, blank=True)
    assigned_staff = models.ForeignKey("staff.Staff", on_delete=models.SET_NULL, related_name="alerts", null=True, blank=True)

    def resolved_time_used(self):
        if not self.resolution_time:
            return None

        delta = self.resolution_time - self.transaction.timestamp
        seconds = int(delta.total_seconds())

        if seconds < 60:
            return f"{seconds}s"

        minutes, seconds = divmod(seconds, 60)
        if minutes < 60:
            return f"{minutes}m {seconds}s"

        hours, minutes = divmod(minutes, 60)
        if hours < 24:
            return f"{hours}h {minutes}m"

        days, hours = divmod(hours, 24)
        return f"{days}d {hours}h"

    def __str__(self):
        return self.pk
    
    class Meta:
        db_table = 'alerts'
        ordering = ['-created_at']
        verbose_name = 'Alert'
        verbose_name_plural = 'Alerts'