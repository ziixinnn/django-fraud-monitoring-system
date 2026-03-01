from rest_framework import serializers
from .use_cases import RISK_THRESHOLDS
from .models import Alert

class AlertListSerializer(serializers.ModelSerializer):

    amount = serializers.DecimalField(source="transaction.amount", max_digits=15, decimal_places=2)
    location = serializers.CharField(source="transaction.location")
    timestamp = serializers.DateTimeField(source="transaction.timestamp")
    risk_score = serializers.SerializerMethodField()
    reason = serializers.SerializerMethodField()
    risk_level = serializers.CharField(source="get_risk_level_display")

    class Meta:
        model = Alert
        fields = (
            "alert_id",
            "timestamp", 
            "transaction", 
            "amount", 
            "location", 
            "risk_score",
            "risk_level",
            "reason",
        )

    def get_risk_score(self, obj):
        return obj.snapshot.get('risk_score')
    
    def get_reason(self, obj):
        reason = obj.snapshot.get("reason")

        if isinstance(reason, list):
            return "; ".join(reason)   

        return reason
    
class AlertDetailSerializer(AlertListSerializer):

    device_info = serializers.CharField(source="transaction.device_info")
    transaction_type = serializers.CharField(source="transaction.get_transaction_type_display")
    fraud_status = serializers.CharField(source="transaction.get_fraud_status_display")

    class Meta(AlertListSerializer.Meta):
        fields = AlertListSerializer.Meta.fields + (
            "device_info",
            "transaction_type",
            "fraud_status",
        )

class AlertFraudAnalysisSerializer(serializers.ModelSerializer):

    risk_level = serializers.CharField(source="get_risk_level_display")
    risk_score = serializers.SerializerMethodField()
    reason = serializers.SerializerMethodField()
    risk_thresholds = serializers.SerializerMethodField()

    class Meta:
        model = Alert
        fields = (
            "alert_id",
            "risk_score",
            "risk_level",
            "reason",
            "risk_thresholds",
        )
    
    def get_risk_score(self, obj):
        return obj.snapshot.get('risk_score')

    def get_reason(self, obj):
        reason = obj.snapshot.get("reason")

        if isinstance(reason, list):
            return "; ".join(reason)   

        return reason
    
    def get_risk_thresholds(self,obj):
        return RISK_THRESHOLDS
    
class ResolvedAlertSerializer(serializers.ModelSerializer):

    amount = serializers.DecimalField(source="transaction.amount", max_digits=15, decimal_places=2)
    location = serializers.CharField(source="transaction.location")
    timestamp = serializers.DateTimeField(source="transaction.timestamp")
    device_info = serializers.CharField(source="transaction.device_info")
    transaction_type = serializers.CharField(source="transaction.get_transaction_type_display")
    fraud_status = serializers.CharField(source="transaction.get_fraud_status_display")
    duration = serializers.SerializerMethodField()

    class Meta(AlertListSerializer.Meta):
        fields =  (
            "alert_id",
            "timestamp", 
            "transaction", 
            "amount", 
            "location", 
            "device_info",
            "transaction_type",
            "fraud_status",
            "resolution_time",
            "outcome",
            "duration",
        )

    def get_duration(self, obj):
        return obj.resolved_time_used()
    
class IssueHandoverSerializer(serializers.Serializer):

    HANDOVER_ACTION = [
        ("YES", "Yes"),
        ("NO", "No"),
    ]
    
    issue_handover = serializers.ChoiceField(choices=HANDOVER_ACTION)
    additional_remark = serializers.CharField(required=False, allow_blank=True)
    
