"""
routes/health.py
GET /api/health — public liveness + DB health check.

Endpoint:
  GET /api/health
"""
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from database.connection import check_db_connection
from utils.responses import success_response, error_response


# ─── GET /api/health ──────────────────────────────────────────────────────────
class HealthView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        db_ok = check_db_connection()
        payload = {
            "api": "ok",
            "database": "ok" if db_ok else "unreachable",
        }
        if db_ok:
            return success_response(payload, http_code=200)
        return error_response("Database unreachable.", http_code=503)
