from django.contrib import admin
from .models import Prediction

class PredictionAdmin(admin.ModelAdmin):
    list_display = ('prediction_id', 'transaction', 'risk_score', 'fraud_label', 'explanation', 'created_at')

admin.site.register(Prediction, PredictionAdmin)