from django.conf import settings

LIMIT_ASIGNED_USERS = []
NOTIFY_FROM_EMAIL = getattr(settings, "ORG_NOTIFY_FROM_EMAIL", settings.EMAIL)
