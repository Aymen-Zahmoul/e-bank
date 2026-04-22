"""
models/apps.py
Django app configuration for the models package.
"""
from django.apps import AppConfig


class ModelsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "models"
    label = "ebnk_models"   # avoids collision with Python's built-in 'models' name

    def ready(self):
        # Ensure all models are imported so Django registers them
        import models.user       # noqa: F401
        import models.account    # noqa: F401
        import models.transaction  # noqa: F401
