"""Root URL configuration for e-bnk."""
from django.urls import path, include

urlpatterns = [
    path("api/health",            include("routes.health_urls")),
    path("api/auth/",             include("routes.auth_urls")),
    path("api/account/",          include("routes.account_urls")),
    path("api/transaction/",      include("routes.transaction_urls")),
]
