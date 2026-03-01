from rest_framework import serializers
from .models import Customer

class CustomerRiskProfileSerializer(serializers. ModelSerializer):

    joined_since = serializers.SerializerMethodField()
    flagged_times = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields =(
            "customer_name",
            "joined_since",
            "flagged_times",
        )

    def get_joined_since(self, obj):
        return f"Joined since {obj.created_at.strftime('%b %Y')}" #convert timestamp to month and year
    
    def get_flagged_times(self, obj):
        # get total number of alerts has been flagged across all transactions under all accounts of this customer
        flagged_sender_accounts = obj.accounts.filter(sent_transactions__alerts__isnull=False)
        alert_count = flagged_sender_accounts.values("sent_transactions__alerts").count()
        flagged_receiver_accounts = obj.accounts.filter(received_transactions__alerts__isnull=False)
        alert_count += flagged_receiver_accounts.values("received_transactions__alerts").count()
        return f"Has been flagged {alert_count} times"
            
