"""
services/transaction_service.py
Transaction business logic:
  - transfer    : atomic money transfer between accounts
  - get_history : paginated transaction list for a user

TRANSFER RULES (per spec):
  ✓ Sender must be authenticated (enforced at route level)
  ✓ Amount must be > 0
  ✓ Sender must have sufficient balance
  ✓ Receiver must exist
  ✓ Both accounts updated atomically
  ✓ Every attempt is logged — including failures

Routes MUST NOT contain any of this logic.
"""
import logging
from decimal import Decimal

from django.db import transaction as db_transaction

from models.account import Account
from models.transaction import Transaction
from models.user import User
from utils.validators import validate_positive_amount, validate_email

logger = logging.getLogger("ebnk.transaction_service")


def transfer(sender_user_id: int, receiver_email: str, amount) -> dict:
    """
    Transfer *amount* from sender's account to the receiver's account.

    All validation and DB updates happen inside a single atomic block.
    A Transaction record is written regardless of success or failure.

    Returns a dict with transfer summary on success.
    Raises ValueError with a user-facing message on any failure.
    """
    # ── 1. Validate amount ────────────────────────────────────────────────────
    amount = validate_positive_amount(amount)
    receiver_email = validate_email(receiver_email)

    tx_record = None  # will be created inside the atomic block

    try:
        with db_transaction.atomic():
            # ── 2. Fetch sender account (lock the row to prevent race conditions)
            try:
                sender_account = Account.objects.select_for_update().get(
                    user_id=sender_user_id
                )
            except Account.DoesNotExist:
                raise ValueError("Sender account not found.")

            # ── 3. Fetch receiver by email ────────────────────────────────────
            try:
                receiver_user = User.objects.get(email=receiver_email)
            except User.DoesNotExist:
                raise ValueError(f"No user found with email '{receiver_email}'.")

            if receiver_user.id == sender_user_id:
                raise ValueError("You cannot transfer money to yourself.")

            try:
                receiver_account = Account.objects.select_for_update().get(
                    user=receiver_user
                )
            except Account.DoesNotExist:
                raise ValueError("Receiver account not found.")

            # ── 4. Check sufficient balance ───────────────────────────────────
            if sender_account.balance < amount:
                # Log a failed transaction record
                tx_record = Transaction.objects.create(
                    sender=sender_account,
                    receiver=receiver_account,
                    amount=amount,
                    status=Transaction.Status.FAILED,
                )
                logger.warning(
                    "Transfer FAILED (insufficient funds): user_id=%d amount=%s",
                    sender_user_id,
                    amount,
                )
                raise ValueError(
                    f"Insufficient funds. Available balance: {sender_account.balance}"
                )

            # ── 5. Debit sender, credit receiver ──────────────────────────────
            sender_account.balance -= amount
            receiver_account.balance += amount
            sender_account.save(update_fields=["balance"])
            receiver_account.save(update_fields=["balance"])

            # ── 6. Log the successful transaction ─────────────────────────────
            tx_record = Transaction.objects.create(
                sender=sender_account,
                receiver=receiver_account,
                amount=amount,
                status=Transaction.Status.SUCCESS,
            )

        logger.info(
            "Transfer SUCCESS: user_id=%d → %s amount=%s tx_id=%d",
            sender_user_id,
            receiver_email,
            amount,
            tx_record.id,
        )
        return {
            "transaction_id": tx_record.id,
            "amount": str(amount),
            "receiver": receiver_email,
            "status": Transaction.Status.SUCCESS,
            "timestamp": tx_record.timestamp.isoformat(),
        }

    except ValueError:
        # Re-raise validation / business errors as-is
        raise
    except Exception as exc:
        # Unexpected DB or system error
        logger.exception("Unexpected error during transfer: %s", exc)
        raise ValueError("Transfer could not be completed due to a system error.")


def get_history(user_id: int, page: int = 1, page_size: int = 20) -> dict:
    """
    Return paginated transaction history for a user (sent + received).

    Returns a dict with a list of transactions and pagination metadata.
    """
    try:
        account = Account.objects.get(user_id=user_id)
    except Account.DoesNotExist:
        raise ValueError("Account not found.")

    qs = Transaction.objects.filter(
        sender=account
    ) | Transaction.objects.filter(
        receiver=account
    )
    qs = qs.order_by("-timestamp").select_related("sender__user", "receiver__user")

    total = qs.count()
    offset = (page - 1) * page_size
    transactions = qs[offset: offset + page_size]

    items = []
    for tx in transactions:
        items.append({
            "id": tx.id,
            "type": "sent" if tx.sender_id == account.id else "received",
            "amount": str(tx.amount),
            "counterpart_email": (
                tx.receiver.user.email
                if tx.sender_id == account.id
                else tx.sender.user.email
            ),
            "status": tx.status,
            "timestamp": tx.timestamp.isoformat(),
        })

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "transactions": items,
    }
