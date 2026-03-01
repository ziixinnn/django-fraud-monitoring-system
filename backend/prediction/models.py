import secrets
from django.db import models

FRAUD_LABELS = (
    ("FRAUD", "Fraud"),
    ("LEGIT", "Legitimate"),
)

def generate_prediction_id():
    return "P" + secrets.token_hex(6).upper()

class Prediction(models.Model):
    prediction_id = models.CharField(primary_key=True, max_length=25, default=generate_prediction_id)
    transaction = models.ForeignKey('transaction.Transaction', on_delete=models.CASCADE, related_name='predictions')
    risk_score = models.FloatField(blank=True, null=True)
    fraud_label = models.CharField(max_length=20, blank=True, null=True, choices=FRAUD_LABELS)
    explanation = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.pk
    
    class Meta:
        db_table = 'predictions'
        ordering = ['-created_at']
        verbose_name = 'Prediction'
        verbose_name_plural = 'Predictions'