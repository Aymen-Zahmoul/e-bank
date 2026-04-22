"""
services/auth_service.py
Authentication business logic:
  - register_user   : create User + Account row atomically
  - login_user      : verify credentials, return JWT pair
  - logout_user     : blacklist the refresh token (stateless JWT logout)

Routes MUST NOT contain any of this logic.
"""
import logging
from django.contrib.auth import authenticate
from django.db import IntegrityError, transaction as db_transaction
from rest_framework_simplejwt.tokens import RefreshToken

from models.user import User
from models.account import Account
from utils.validators import validate_email, validate_non_empty

logger = logging.getLogger("ebnk.auth_service")


def register_user(name: str, email: str, password: str) -> dict:
    """
    Create a new user and initialise their bank account.

    Returns a dict with the created user's public data.
    Raises ValueError on validation failure or duplicate email.
    """
    # --- Validate inputs ---
    name = validate_non_empty(name, "Name")
    email = validate_email(email)
    password = validate_non_empty(password, "Password")

    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters long.")

    # --- Create User + Account atomically ---
    try:
        with db_transaction.atomic():
            user = User.objects.create_user(email=email, name=name, password=password)
            Account.objects.create(user=user, balance=0.00)
    except IntegrityError:
        logger.warning("Registration failed — email already exists: %s", email)
        raise ValueError("An account with this email already exists.")

    logger.info("New user registered: %s (id=%d)", email, user.id)
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "created_at": user.created_at.isoformat(),
    }


def login_user(email: str, password: str) -> dict:
    """
    Verify credentials and return a JWT access + refresh token pair.

    Raises ValueError on invalid credentials.
    """
    email = validate_email(email)

    # Django's authenticate() uses the configured PASSWORD_HASHERS (bcrypt)
    user = authenticate(username=email, password=password)
    if user is None:
        logger.warning("Failed login attempt for email: %s", email)
        raise ValueError("Invalid email or password.")

    if not user.is_active:
        raise ValueError("This account has been deactivated.")

    refresh = RefreshToken.for_user(user)
    logger.info("User logged in: %s (id=%d)", email, user.id)
    return {
        "access_token": str(refresh.access_token),
        "refresh_token": str(refresh),
        "token_type": "Bearer",
    }


def logout_user(refresh_token: str) -> None:
    """
    Blacklist the provided refresh token.
    After blacklisting, neither the access nor refresh token can be reused
    (simplejwt's ROTATE_REFRESH_TOKENS + BLACKLIST_AFTER_ROTATION).

    Raises ValueError if the token is already blacklisted or invalid.
    """
    try:
        token = RefreshToken(refresh_token)
        token.blacklist()
        logger.info("Refresh token blacklisted successfully.")
    except Exception as exc:
        logger.warning("Logout failed: %s", exc)
        raise ValueError("Invalid or already expired refresh token.")
