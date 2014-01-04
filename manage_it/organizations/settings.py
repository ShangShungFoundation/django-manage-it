from django.utils.translation import ugettext_lazy as _
from django.conf import settings


ORG_GROUP_ROLES = (
    ("staff_group", _("Staff group")),
    ("admin_group", _("Admin group")),
    ("accounting_group", _("Accounting group")),
    ("incident_notification_group", _("Incident notification group")),
    ("top_group", _("Top group")),
    ("vip_group", _("VIP group")),
    ("purchase_notification_group", _("Purchase notification group")),
)

GROUP_ROLES = getattr(settings, "ORG_GROUP_ROLES", ORG_GROUP_ROLES)

REDIRECT_URL = getattr(settings, "ORG_REDIRECT_URL", "/")

URL_DELIMITER = getattr(settings, "ORG_URL_DELIMITER", "-")

# Superior groups defines groups which are check to be user in superior levels of organization
SUPERIOR_GROUPS = ["admin_group", "accounting_group"]
SUPERIOR_GROUPS = getattr(settings, "ORG_SUPERIOR_GROUPS", SUPERIOR_GROUPS)
