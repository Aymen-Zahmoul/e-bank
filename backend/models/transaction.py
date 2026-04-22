"""
models/transaction.py
Transaction model — maps to the `transactions` table in PostgreSQL.

Fields (per spec):
  id, sender_id (FK → accounts), receiver_id (FK → accounts),
  amount, timestamp, status (success/failed)
"""
from django.db import models


class Transaction(models.Model):
    """Records every money transfer attempt — both successful and failed."""

    class Status(models.TextChoices):
        SUCCESS = "success", "Success"
        FAILED = "failed", "Failed"

    class Meta:
        db_table = "transactions"
        app_label = "ebnk_models"
        ordering = ["-timestamp"]

    id = models.BigAutoField(primary_key=True)
    sender = models.ForeignKey(
        "ebnk_models.Account",
        on_delete=models.PROTECT,
        related_name="sent_transactions",
        db_column="sender_id",
    )
    receiver = models.ForeignKey(
        "ebnk_models.Account",
        on_delete=models.PROTECT,
        related_name="received_transactions",
        db_column="receiver_id",
    )
    amount = models.DecimalField(max_digits=18, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.FAILED,
    )

    def __str__(self) -> str:
        return (
            f"<Transaction #{self.id} "
            f"{self.sender_id}→{self.receiver_id} "
            f"${self.amount} [{self.status}]>"
        )
