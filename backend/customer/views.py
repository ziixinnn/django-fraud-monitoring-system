from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CustomerRiskProfileSerializer
from .models import Customer
from rest_framework.permissions import IsAuthenticated

class CustomerRiskProfileView(APIView):

    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):

        try:
            customer = Customer.objects.get(pk=pk)
        except Customer.DoesNotExist:
            return Response({'error': 'Customer not found'}, status=404)
        
        serializer = CustomerRiskProfileSerializer(customer)

        return Response(serializer.data)