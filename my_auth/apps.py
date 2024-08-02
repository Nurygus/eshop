from django.apps import AppConfig


class MyauthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'my_auth'

    def ready(self):
        # import above schema.py to fix swagger
        from . import schema  # noqa: E402
