from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('agent1.urls')), 
    path("api/agent1/", include("agent1.urls")),
]
