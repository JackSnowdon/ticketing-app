"""
URL configuration for config project.
"""
from django.contrib import admin
from django.urls import include, path

from api.views.accounts import RegisterAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('tickets/', include('tickets.urls')),
    path('api/auth/register/', RegisterAPIView.as_view(), name='register'),
]
