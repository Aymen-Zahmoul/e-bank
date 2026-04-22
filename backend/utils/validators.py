"""
utils/validators.py
Strict input validation helpers called from services layer.
"""
import re
from decimal import Decimal


EMAIL_REGEX = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


def validate_positive_amount(amount) -> Decimal:
    """
    Convert *amount* to Decimal and verify it is strictly > 0.
    Raises ValueError with a user-facing message on failure.
    """
    try:
        value = Decimal(str(amount))
    except Exception:
        raise ValueError("Amount must be a valid number.")
    if value <= Decimal("0"):
        raise ValueError("Amount must be greater than zero.")
    return value


def validate_email(email: str) -> str:
    """
    Verify basic email structure.
    Raises ValueError with a user-facing message on failure.
    """
    if not email or not EMAIL_REGEX.match(email.strip()):
        raise ValueError("A valid email address is required.")
    return email.strip().lower()


def validate_non_empty(value: str, field_name: str = "Field") -> str:
    """Ensure a string field is not empty or whitespace-only."""
    if not value or not value.strip():
        raise ValueError(f"{field_name} must not be empty.")
    return value.strip()
