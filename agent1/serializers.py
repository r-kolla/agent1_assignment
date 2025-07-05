from rest_framework import serializers
from .models import Course, Enquiry, Enrollment, Order, Payment, Class, Client

class ClientSerializer(serializers.ModelSerializer):
    enrolled_services = serializers.SerializerMethodField()
    
    class Meta:
        model = Client
        fields = ['id', 'name', 'email', 'phone', 'enrolled_services', 'status', 'created_at', 'updated_at']
    
    def get_enrolled_services(self, obj):
        enrollments = Enrollment.objects.filter(client=obj, status='enrolled')
        return [enrollment.course.name for enrollment in enrollments]

class CourseSerializer(serializers.ModelSerializer):
    availability = serializers.SerializerMethodField()
    
    class Meta:
        model = Course
        fields = ['id', 'name', 'instructor', 'description', 'price', 'duration', 'status', 'availability', 'created_at', 'updated_at']
    
    def get_availability(self, obj):
        return "Available" if obj.status == 'active' else "Not Available"

class ClassSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source='course.name', read_only=True)
    instructor = serializers.CharField(source='course.instructor', read_only=True)
    schedule = serializers.SerializerMethodField()
    
    class Meta:
        model = Class
        fields = ['id', 'course_name', 'instructor', 'start_time', 'end_time', 'status', 'schedule', 'created_at', 'updated_at']
    
    def get_schedule(self, obj):
        return f"{obj.start_time.strftime('%A, %B %d')} - {obj.start_time.strftime('%I:%M %p')} to {obj.end_time.strftime('%I:%M %p')}"

class OrderSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client.name', read_only=True)
    client_email = serializers.CharField(source='client.email', read_only=True)
    course_name = serializers.CharField(source='course.name', read_only=True)  # Fixed: was service_name
    payment_status = serializers.SerializerMethodField()
    
    class Meta:
        model = Order
        fields = ['id', 'client', 'client_name', 'client_email', 'course', 'course_name', 
                 'amount', 'status', 'payment_status', 'order_date', 'created_at', 'updated_at']
    
    def get_payment_status(self, obj):
        try:
            payment = Payment.objects.get(order=obj)
            return payment.status
        except Payment.DoesNotExist:
            return "Pending"

class PaymentSerializer(serializers.ModelSerializer):
    order_id = serializers.CharField(source='order.id', read_only=True)
    client_name = serializers.CharField(source='order.client.name', read_only=True)
    course_name = serializers.CharField(source='order.course.name', read_only=True)  # Fixed: was service_name
    
    class Meta:
        model = Payment
        fields = ['id', 'order', 'order_id', 'client_name', 'course_name', 
                 'amount', 'status', 'payment_date', 'created_at', 'updated_at']

class EnrollmentSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client.name', read_only=True)
    course_name = serializers.CharField(source='course.name', read_only=True)
    course_price = serializers.DecimalField(source='course.price', max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = Enrollment
        fields = ['id', 'client', 'client_name', 'course', 'course_name', 
                 'course_price', 'enrollment_date', 'status', 'created_at', 'updated_at']

class EnquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = Enquiry
        fields = ['id', 'name', 'email', 'phone', 'service', 'message', 
                 'status', 'created_at', 'updated_at']

# Agent1-specific serializers
class ClientSearchSerializer(serializers.ModelSerializer):
    enrolled_services = serializers.SerializerMethodField()
    
    class Meta:
        model = Client
        fields = ['name', 'email', 'phone', 'enrolled_services', 'status']
    
    def get_enrolled_services(self, obj):
        enrollments = Enrollment.objects.filter(client=obj, status='enrolled')
        return ", ".join([enrollment.course.name for enrollment in enrollments])

class CourseScheduleSerializer(serializers.ModelSerializer):
    upcoming_classes = serializers.SerializerMethodField()
    
    class Meta:
        model = Course
        fields = ['name', 'instructor', 'price', 'duration', 'upcoming_classes']
    
    def get_upcoming_classes(self, obj):
        from django.utils import timezone
        upcoming = Class.objects.filter(
            course=obj, 
            start_time__gte=timezone.now(),
            status='scheduled'
        ).order_by('start_time')[:5]
        
        return [
            {
                'date': class_obj.start_time.strftime('%A, %B %d'),
                'time': f"{class_obj.start_time.strftime('%I:%M %p')} - {class_obj.end_time.strftime('%I:%M %p')}"
            }
            for class_obj in upcoming
        ]

class ServiceInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['name', 'instructor', 'price', 'duration', 'description', 'status']
