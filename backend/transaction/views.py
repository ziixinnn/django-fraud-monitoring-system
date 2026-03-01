from rest_framework.views import APIView
from rest_framework.response import Response
from .use_cases import manual_update_status, process_transaction
from .models import Transaction
from django.db.models import Q
from .serializers import CustomerHistoryTransactionSerializer, ManualUpdateTransactionSerializer, TransactionDetailSerializer, TransactionListSerializer, TransactionSerializer
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.authentication import BasicAuthentication
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class TransactionCreateView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = TransactionSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)

        transactions = serializer.save()

        channel_layer = get_channel_layer()

        for transaction in transactions:
            process_transaction(transaction)

            if channel_layer:
                async_to_sync(channel_layer.group_send)(
                    "transaction_room",
                    {
                        "type": "transaction.created",
                        "data": TransactionListSerializer(transaction).data,
                    }
                )

        return Response(
            TransactionListSerializer(transactions, many=True).data,
            status=201
        )
    
class TransactionListView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        transactions = Transaction.objects.all()
        serializer = TransactionListSerializer(transactions, many=True)

        return Response(serializer.data)

class TransactionDetailView(APIView):

    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):

        try:
            transaction = Transaction.objects.get(pk=pk)
        except Transaction.DoesNotExist:
            return Response({'error': 'Transaction not found'}, status=404)
        
        serializer = TransactionDetailSerializer(transaction)

        return Response(serializer.data)

@method_decorator(csrf_exempt, name="dispatch")
class ManualUpdateTransactionView(APIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [BasicAuthentication]

    def post(self, request, pk):

        try:
            transaction = Transaction.objects.get(pk=pk)
        except Transaction.DoesNotExist:
            return Response({'error': 'Transaction not found'}, status=404)
        
        serializer = ManualUpdateTransactionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        updated_status = serializer.validated_data["action"]
        manual_update_status(updated_status, transaction)
        
        return Response(serializer.data, status=201)
    
class CustomerHistoryTransactionView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, customer_id):

        type = request.query_params.get("type")

        transactions = Transaction.objects.filter(
            Q(sender_acc__customer_id=customer_id) |
            Q(receiver_acc__customer_id=customer_id)
        ).order_by("-timestamp")

        if type == "Expenses":
            transactions = transactions.filter(sender_acc__customer_id=customer_id).exclude(receiver_acc__customer_id=customer_id).order_by("-timestamp")
        elif type == "Savings":
            transactions = transactions.filter(sender_acc__customer_id=customer_id, receiver_acc__customer_id=customer_id).order_by("-timestamp")
        elif type == "Income":
            transactions = transactions.filter(receiver_acc__customer_id=customer_id).exclude(sender_acc__customer_id=customer_id).order_by("-timestamp")

        serializer = CustomerHistoryTransactionSerializer(
            transactions,
            many=True,
            context={"customer_id": customer_id}
        )

        return Response(serializer.data)