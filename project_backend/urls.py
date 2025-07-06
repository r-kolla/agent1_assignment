from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

def root_redirect(request):
    return redirect('/api/agent1/')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('agent1.urls')), 
    path("api/agent1/", include("agent1.urls")),
    path('', root_redirect),
]
