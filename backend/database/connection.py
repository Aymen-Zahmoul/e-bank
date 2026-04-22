"""
database/connection.py
PostgreSQL connection health check and DSN builder.
Django's ORM handles the actual connection pool; this module
provides a utility to verify the DB is reachable at startup.
"""
import logging
import os

logger = logging.getLogger("ebnk")


def get_database_dsn() -> str:
    """Return the PostgreSQL DSN string built from environment variables."""
    return (
        f"postgresql://{os.getenv('DB_USER', 'postgres')}:"
        f"{os.getenv('DB_PASSWORD', 'postgres')}@"
        f"{os.getenv('DB_HOST', 'localhost')}:"
        f"{os.getenv('DB_PORT', '5432')}/"
        f"{os.getenv('DB_NAME', 'ebnk')}"
    )


def check_db_connection() -> bool:
    """
    Verify that Django can reach the configured database.
    Call this from a management command or health-check endpoint.
    """
    try:
        from django.db import connection
        connection.ensure_connection()
        logger.info("Database connection established successfully.")
        return True
    except Exception as exc:
        logger.error("Database connection failed: %s", exc)
        return False
