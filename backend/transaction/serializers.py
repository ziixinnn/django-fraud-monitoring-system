from rest_framework import serializers
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = '__all__'
        read_only_fields = (
        "transaction_id",
        "timestamp",
        "transaction_status",
        "fraud_status",
        )

    def create(self, validated_data):
        return Transaction.create(**validated_data)
    
class TransactionListSerializer(serializers.ModelSerializer):

    fraud_status = serializers.CharField(source="get_fraud_status_display")

    class Meta:
        model = Transaction
        fields = (
        "timestamp", 
        "transaction_id", 
        "amount", 
        "location", 
        "fraud_status"
        )

class TransactionDetailSerializer(TransactionListSerializer):

    transaction_status = serializers.CharField(source="get_transaction_status_display")
    transaction_type = serializers.CharField(source="get_transaction_type_display")

    class Meta(TransactionListSerializer.Meta):
        fields = TransactionListSerializer.Meta.fields + (
            "device_info", 
            "transaction_status", 
            "transaction_type", 
    )
        
class ManualUpdateTransactionSerializer(serializers.Serializer):

    ACTION = [
        ("CONFIRM_FRAUD", "Confirm Fraud"),
        ("FALSE_POSITIVE", "False Positive"),
        ("MARK_AS_PENDING", "Mark as Pending")
    ]

    action = serializers.ChoiceField(choices=ACTION)

class CustomerHistoryTransactionSerializer(serializers.ModelSerializer):

    type = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = (
            "sender_acc",
            "receiver_acc",
            "timestamp",
            "amount",
            "transaction_status",
            "type",
        )

    def get_type(self, obj):
        customer_id = self.context.get("customer_id")
        if not customer_id:
            return None

        sender_is_customer = obj.sender_acc.customer_id == customer_id
        receiver_is_customer = obj.receiver_acc.customer_id == customer_id

        if sender_is_customer and receiver_is_customer:
            return "Savings"
        elif sender_is_customer:
            return "Expenses"
        elif receiver_is_customer:
            return "Income"





