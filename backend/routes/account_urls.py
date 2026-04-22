"""URL patterns for /api/account/"""
from django.urls import path
from routes.account import BalanceView, AccountDetailsView

urlpatterns = [
    path("balance", BalanceView.as_view(), name="account-balance"),
    path("details", AccountDetailsView.as_view(), name="account-details"),
]
