"""
utils/middleware.py
Request/response logging middleware.
Logs method, path, status code, and elapsed time for every request.
"""
import time
import logging

logger = logging.getLogger("ebnk.requests")


class RequestLoggingMiddleware:
    """WSGI middleware that logs every HTTP request handled by Django."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start = time.monotonic()
        response = self.get_response(request)
        elapsed_ms = (time.monotonic() - start) * 1000
        logger.info(
            "%s %s → %d (%.1fms)",
            request.method,
            request.path,
            response.status_code,
            elapsed_ms,
        )
        return response
