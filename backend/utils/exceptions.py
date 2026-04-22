"""
utils/exceptions.py
Custom DRF exception handler that wraps all errors in the spec JSON format:
  { "status": "error", "message": "..." }
"""
import logging
from rest_framework.views import exception_handler
from rest_framework.response import Response

logger = logging.getLogger("ebnk.exceptions")


def custom_exception_handler(exc, context):
    """
    Override DRF's default exception handler to return spec-compliant JSON.
    Non-DRF exceptions (e.g. unhandled Python errors) return 500.
    """
    response = exception_handler(exc, context)

    if response is not None:
        # DRF handled it — reformat the response body
        detail = response.data
        if isinstance(detail, dict) and "detail" in detail:
            message = str(detail["detail"])
        elif isinstance(detail, list):
            message = "; ".join(str(d) for d in detail)
        else:
            message = str(detail)

        logger.warning("API error [%d]: %s", response.status_code, message)
        response.data = {"status": "error", "message": message}
    else:
        # Unhandled exception — log it and return 500
        logger.exception("Unhandled exception in view: %s", exc)
        response = Response(
            {"status": "error", "message": "An internal server error occurred."},
            status=500,
        )

    return response
