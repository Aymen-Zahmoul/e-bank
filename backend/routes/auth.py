"""
routes/auth.py
Authentication views — thin layer, zero business logic.

Endpoints:
  POST /api/auth/register
  POST /api/auth/login
  POST /api/auth/logout
"""
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.throttling import AnonRateThrottle

from services import auth_service
from utils.responses import success_response, error_response


class AuthRateThrottle(AnonRateThrottle):
    """Stricter rate limit for auth endpoints (5/min configured in settings)."""
    scope = "auth"


# ─── POST /api/auth/register ──────────────────────────────────────────────────
class RegisterView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [AuthRateThrottle]

    def post(self, request):
        name = request.data.get("name", "")
        email = request.data.get("email", "")
        password = request.data.get("password", "")

        try:
            user_data = auth_service.register_user(name, email, password)
            return success_response({"user": user_data}, http_code=201)
        except ValueError as exc:
            return error_response(str(exc), http_code=400)


# ─── POST /api/auth/login ─────────────────────────────────────────────────────
class LoginView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [AuthRateThrottle]

    def post(self, request):
        email = request.data.get("email", "")
        password = request.data.get("password", "")

        try:
            tokens = auth_service.login_user(email, password)
            return success_response(tokens)
        except ValueError as exc:
            return error_response(str(exc), http_code=401)


# ─── POST /api/auth/logout ────────────────────────────────────────────────────
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh_token", "")
        if not refresh_token:
            return error_response("refresh_token is required.", http_code=400)

        try:
            auth_service.logout_user(refresh_token)
            return success_response({"message": "Successfully logged out."})
        except ValueError as exc:
            return error_response(str(exc), http_code=400)
