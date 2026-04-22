"""
routes/account.py
Account views — thin layer, zero business logic.

Endpoints:
  GET /api/account/balance
  GET /api/account/details
"""
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from services import account_service
from utils.responses import success_response, error_response


# ─── GET /api/account/balance ─────────────────────────────────────────────────
class BalanceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            data = account_service.get_balance(request.user.id)
            return success_response(data)
        except ValueError as exc:
            return error_response(str(exc), http_code=404)


# ─── GET /api/account/details ─────────────────────────────────────────────────
class AccountDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            data = account_service.get_account_details(request.user.id)
            return success_response(data)
        except ValueError as exc:
            return error_response(str(exc), http_code=404)
