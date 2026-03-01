from rest_framework.views import APIView
from rest_framework.response import Response
from .use_cases import handover_to_admin
from .models import Alert
from .serializers import AlertDetailSerializer, AlertFraudAnalysisSerializer, AlertListSerializer, IssueHandoverSerializer, ResolvedAlertSerializer
from rest_framework.permissions import IsAuthenticated

class AlertListView(APIView):

    def get(self, request):

        permission_classes = [IsAuthenticated]

        view = request.query_params.get("view")
        alerts = Alert.objects.all()

        if view == "pending":
            alerts = alerts.filter(alert_status='PENDING').order_by("-created_at")
        elif view == "resolved":
            alerts = alerts.filter(alert_status='RESOLVED').order_by("-resolution_time")
        elif view == "high_risk":
            alerts = alerts.filter(risk_level__in=['HIGH', 'VERY_HIGH'], alert_status = 'PENDING').order_by("-created_at")

        serializer = AlertListSerializer(alerts, many=True)

        return Response(serializer.data)
    
class AlertDetailView(APIView):

    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):

        try:
            alert = Alert.objects.get(pk=pk)
        except Alert.DoesNotExist:
            return Response({'error': 'Alert not found'}, status=404)
        
        serializer = AlertDetailSerializer(alert)

        return Response(serializer.data)
    
class AlertFraudAnalysisView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):

        try:
            alert = Alert.objects.get(pk=pk)
        except Alert.DoesNotExist:
            return Response({'error': 'Alert not found'}, status=404)
        
        serializer = AlertFraudAnalysisSerializer(alert)

        customer_id = alert.transaction.sender_acc.customer_id

        data = serializer.data
        data["customer_id"] = customer_id

        return Response(data)
    
class ResolvedAlertView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):

        try:
            alert = Alert.objects.get(pk=pk)
        except Alert.DoesNotExist:
            return Response({'error': 'Alert not found'}, status=404)
        
        serializer = ResolvedAlertSerializer(alert)

        return Response(serializer.data)
    
class IssueHandoverView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):

        try:
            alert=Alert.objects.get(pk=pk)
        except Alert.DoesNotExist:
            return Response({'error': 'Alert not found'}, status=404)
        
        serializer = IssueHandoverSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        issue_handover = serializer.validated_data["issue_handover"]
        additional_remark = serializer.validated_data["additional_remark"]

        handover_to_admin(issue_handover, additional_remark, alert)

        return Response(serializer.data, status=201)





    
        