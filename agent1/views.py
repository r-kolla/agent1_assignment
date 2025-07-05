import json
from django.http import JsonResponse
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, generics
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from .models import Client, Enrollment, Order, Payment, Class, Course, Enquiry
from .serializers import ClientSerializer, EnrollmentSerializer, OrderSerializer, PaymentSerializer, ClassSerializer, CourseSerializer, EnquirySerializer
from .agent1_core import Agent1CustomerSupport

class ClientViewSet(viewsets.ModelViewSet):
    # ... previous code ...
    @action(detail=True, methods=['get'])
    def enrollments(self, request, pk=None):
        enrollments = Enrollment.objects.filter(client_id=pk)
        serializer = EnrollmentSerializer(enrollments, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def pending_dues(self, request, pk=None):
        orders = Order.objects.filter(client_id=pk, status='pending')
        total_due = sum(order.total_amount for order in orders)
        return Response({'pending_dues': total_due})

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['client', 'status']

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['order']

class UpcomingClassList(generics.ListAPIView):
    serializer_class = ClassSerializer

    def get_queryset(self):
        now = timezone.now()
        return Class.objects.filter(start_time__gte=now)

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['instructor', 'status']

class EnquiryViewSet(viewsets.ModelViewSet):
    queryset = Enquiry.objects.all()
    serializer_class = EnquirySerializer


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()  # Add this line
    serializer_class = ClientSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'email', 'status']
    
    @action(detail=True, methods=['get'])
    def enrollments(self, request, pk=None):
        enrollments = Enrollment.objects.filter(client_id=pk)
        serializer = EnrollmentSerializer(enrollments, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def pending_dues(self, request, pk=None):
        orders = Order.objects.filter(client_id=pk, status='pending')
        total_due = sum(order.total_amount for order in orders)
        return Response({'pending_dues': total_due})
    
    

agent1 = Agent1CustomerSupport()

@csrf_exempt
def agent1_chat_api(request):
    if request.method == "POST":
        payload = json.loads(request.body)
        msg = payload.get("message", "")
        resp = agent1.chat(msg)
        return JsonResponse({"response": resp})
    return JsonResponse({"error": "POST only"}, status=405)