from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q
from .models import Client, Course, Order, Payment, Class, Enquiry
from .serializers import (
    ClientSearchSerializer, CourseScheduleSerializer, OrderSerializer,
    ServiceInfoSerializer, EnquirySerializer
)

class Agent1ClientSearchView(generics.ListAPIView):
    serializer_class = ClientSearchSerializer
    
    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        if query:
            return Client.objects.filter(
                Q(name__icontains=query) |
                Q(email__icontains=query) |
                Q(phone__icontains=query)
            )
        return Client.objects.none()

class Agent1OrderDetailView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    lookup_field = 'id'

class Agent1CourseScheduleView(generics.ListAPIView):
    serializer_class = CourseScheduleSerializer
    
    def get_queryset(self):
        service_name = self.request.query_params.get('service', '')
        if service_name:
            return Course.objects.filter(name__icontains=service_name, status='active')
        return Course.objects.filter(status='active')

class Agent1ServiceInfoView(generics.ListAPIView):
    queryset = Course.objects.filter(status='active')
    serializer_class = ServiceInfoSerializer

@api_view(['POST'])
def agent1_create_enquiry(request):
    serializer = EnquirySerializer(data=request.data)
    if serializer.is_valid():
        enquiry = serializer.save()
        return Response({
            'id': f"ENQ{enquiry.id}",
            'message': 'Enquiry created successfully',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
