"""
models/user.py
Custom User model — maps to the `users` table in PostgreSQL.

Fields (per spec):
  id, name, email (unique), password_hash, created_at
"""
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    """Manager that uses email as the unique identifier instead of username."""

    def create_user(self, email: str, name: str, password: str, **extra_fields):
        if not email:
            raise ValueError("Email is required.")
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)  # bcrypt hash via PASSWORD_HASHERS
        user.save(using=self._db)
        return user

    def create_superuser(self, email: str, name: str, password: str, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, name, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model.
    `password` field inherited from AbstractBaseUser stores the hash —
    Django never stores plain-text passwords.
    """

    class Meta:
        db_table = "users"
        app_label = "ebnk_models"

    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, db_index=True)
    # `password` column managed by AbstractBaseUser (stored as `password`)
    created_at = models.DateTimeField(auto_now_add=True)

    # Required by Django admin / permissions
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    def __str__(self) -> str:
        return f"<User {self.email}>"
