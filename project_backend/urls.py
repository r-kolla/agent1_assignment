from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.urls import path, include, re_path
from django.views.generic import TemplateView


def root_redirect(request):
    return redirect('/api/agent1/')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('agent1.urls')), 
    path("api/agent1/", include("agent1.urls")),
    
    re_path(r'^(?!static/|api/|admin/).*', TemplateView.as_view(template_name="index.html")),
    ]
