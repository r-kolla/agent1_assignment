from django.urls import path
from .views import UpcomingClassList
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('classes/upcoming/', UpcomingClassList.as_view(), name='upcoming-classes'),
    # Add other app-specific endpoints here
]
