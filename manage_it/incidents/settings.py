from django.conf import settings

LIMIT_ASIGNED_USERS = getattr(settings, "LIMIT_ASIGNED_USERS", [])
INCIDENT_NOTIFICATION = getattr(settings, "INCIDENT_NOTIFICATION", [])
