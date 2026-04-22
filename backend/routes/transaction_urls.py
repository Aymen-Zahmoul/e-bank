"""URL patterns for /api/transaction/"""
from django.urls import path
from routes.transaction import TransferView, TransactionHistoryView

urlpatterns = [
    path("transfer", TransferView.as_view(), name="transaction-transfer"),
    path("history", TransactionHistoryView.as_view(), name="transaction-history"),
]
