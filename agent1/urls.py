from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    ClientViewSet, OrderViewSet, PaymentViewSet, CourseViewSet,
    EnrollmentViewSet, ClassViewSet, EnquiryViewSet, UpcomingClassList
)

# Create the DRF router
router = DefaultRouter()
router.register(r'clients', ClientViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'payments', PaymentViewSet)
router.register(r'courses', CourseViewSet)
router.register(r'enrollments', EnrollmentViewSet)
router.register(r'classes', ClassViewSet)
router.register(r'enquiries', EnquiryViewSet)

# Define custom URL patterns
urlpatterns = [
    path('classes/upcoming/', UpcomingClassList.as_view(), name='upcoming-classes'),
]

# Add router URLs to urlpatterns
urlpatterns += router.urls
