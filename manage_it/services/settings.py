from django.conf import settings

from django.utils.translation import ugettext_lazy as _


ORG_SERVICE_TYPES = (
    (1, _("Communications")),
    (2, _("Security")),
    (3, _("Servers, Data, Backup")),
    (4, _("Software & Business Applications")),
    (5, _("Web & Collaboration")),
    (6, _("Email & Collaboration")),
)

SERVICE_TYPES = getattr(settings, "ORG_SERVICE_TYPES", ORG_SERVICE_TYPES)
