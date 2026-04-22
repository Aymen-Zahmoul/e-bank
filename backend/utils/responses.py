"""
utils/responses.py
Standardized JSON response builders matching the spec format:

  Success: { "status": "success", "data": {} }
  Error:   { "status": "error",   "message": "..." }
"""
from rest_framework.response import Response
from rest_framework import status as http_status


def success_response(data: dict, http_code: int = http_status.HTTP_200_OK) -> Response:
    """Return a standardized success JSON response."""
    return Response({"status": "success", "data": data}, status=http_code)


def error_response(message: str, http_code: int = http_status.HTTP_400_BAD_REQUEST) -> Response:
    """Return a standardized error JSON response."""
    return Response({"status": "error", "message": message}, status=http_code)
