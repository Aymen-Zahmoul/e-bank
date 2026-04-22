"""
models/account.py
Account model — maps to the `accounts` table in PostgreSQL.

Fields (per spec):
  id, user_id (FK → users), balance (Decimal, default 0.00)
"""
from django.db import models
from django.conf import settings


class Account(models.Model):
    """One account per user. Balance stored as high-precision Decimal."""

    class Meta:
        db_table = "accounts"
        app_label = "ebnk_models"

    id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="account",
        db_column="user_id",
    )
    balance = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        default=0.00,
    )

    def __str__(self) -> str:
        return f"<Account user={self.user_id} balance={self.balance}>"
