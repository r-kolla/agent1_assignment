from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    ClientViewSet, OrderViewSet, PaymentViewSet, CourseViewSet,
     EnquiryViewSet, UpcomingClassList, agent1_chat_api
)
from . import agent1_api_views

router = DefaultRouter()
router.register(r'clients', ClientViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'payments', PaymentViewSet)
router.register(r'courses', CourseViewSet)

router.register(r'enquiries', EnquiryViewSet)

urlpatterns = [
    path('classes/upcoming/', UpcomingClassList.as_view(), name='upcoming-classes'),
    path('clients/search/', agent1_api_views.Agent1ClientSearchView.as_view(), name='agent1-client-search'),
    path('orders/<str:id>/', agent1_api_views.Agent1OrderDetailView.as_view(), name='agent1-order-detail'),
    path('courses/schedule/', agent1_api_views.Agent1CourseScheduleView.as_view(), name='agent1-course-schedule'),
    path('services/', agent1_api_views.Agent1ServiceInfoView.as_view(), name='agent1-service-info'),
    path('enquiries/', agent1_api_views.agent1_create_enquiry, name='agent1-create-enquiry'),
    path('chat/', agent1_chat_api, name="agent1-chat"),

]

urlpatterns += router.urls
