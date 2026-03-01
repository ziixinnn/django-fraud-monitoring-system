from django.contrib import admin
from .models import Alert

class AlertAdmin(admin.ModelAdmin):
    list_display = ('alert_id', 'transaction', 'risk_level', 'created_at')

admin.site.register(Alert, AlertAdmin)