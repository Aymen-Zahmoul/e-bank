"""
services/account_service.py
Account business logic:
  - get_balance        : return user's current balance
  - get_account_details: return combined user + account data

Routes MUST NOT contain any of this logic.
"""
import logging
from models.account import Account

logger = logging.getLogger("ebnk.account_service")


def get_balance(user_id: int) -> dict:
    """
    Return the current balance for the given user.
    Raises ValueError if no account is found.
    """
    try:
        account = Account.objects.select_related("user").get(user_id=user_id)
    except Account.DoesNotExist:
        logger.error("Balance lookup failed — no account for user_id=%d", user_id)
        raise ValueError("Account not found.")

    return {"balance": str(account.balance), "currency": "USD"}


def get_account_details(user_id: int) -> dict:
    """
    Return full account + user details for the given user.
    Raises ValueError if no account is found.
    """
    try:
        account = Account.objects.select_related("user").get(user_id=user_id)
    except Account.DoesNotExist:
        logger.error("Account detail lookup failed — no account for user_id=%d", user_id)
        raise ValueError("Account not found.")

    user = account.user
    return {
        "account_id": account.id,
        "balance": str(account.balance),
        "currency": "USD",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "member_since": user.created_at.isoformat(),
        },
    }
