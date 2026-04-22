"""URL patterns for /api/health"""
from django.urls import path
from routes.health import HealthView

urlpatterns = [
    path("", HealthView.as_view(), name="health"),
]
