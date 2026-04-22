"""
routes/transaction.py
Transaction views — thin layer, zero business logic.

Endpoints:
  POST /api/transaction/transfer
  GET  /api/transaction/history
"""
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from services import transaction_service
from utils.responses import success_response, error_response


# ─── POST /api/transaction/transfer ──────────────────────────────────────────
class TransferView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        receiver_email = request.data.get("receiver_email", "")
        amount = request.data.get("amount")

        if not receiver_email or amount is None:
            return error_response(
                "Both 'receiver_email' and 'amount' are required.", http_code=400
            )

        try:
            result = transaction_service.transfer(
                sender_user_id=request.user.id,
                receiver_email=receiver_email,
                amount=amount,
            )
            return success_response(result)
        except ValueError as exc:
            return error_response(str(exc), http_code=400)


# ─── GET /api/transaction/history ────────────────────────────────────────────
class TransactionHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            page = int(request.query_params.get("page", 1))
            page_size = min(int(request.query_params.get("page_size", 20)), 100)
        except (ValueError, TypeError):
            return error_response("Invalid pagination parameters.", http_code=400)

        try:
            data = transaction_service.get_history(
                user_id=request.user.id,
                page=page,
                page_size=page_size,
            )
            return success_response(data)
        except ValueError as exc:
            return error_response(str(exc), http_code=404)
