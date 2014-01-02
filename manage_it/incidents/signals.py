from django.db.models.signals import post_save

from notifications.notify import notify
from organizations.models import IncidentNotificationGroupNotDefined

from organizations.models import OrganizationGroup

from models import Incident  # IncidentFollowup

INCIDENT_MSG = """Incident #%s at %s: %s %s"""


def signal_incident(sender, instance, created, **kwargs):

    """signal only on ceration since updates will
    be signaled by signal_newfollowup"""
    if not kwargs.get("update_fields"):
        submitter = instance.submited_by
        org = instance.organization
        msg = INCIDENT_MSG % (
            instance.id, org.name,
            instance.subject, instance.get_absolute_url())

        incident_notification_group = OrganizationGroup.objects.filter(
            role="incident_notification_group",
            org=org)

        if not incident_notification_group[0]:
            raise IncidentNotificationGroupNotDefined()
        notification_group = list(
            incident_notification_group.group.user_set.all())
        receivers = [submitter] + notification_group
        notify(submitter, receivers, msg, 3)


def signal_followup(sender, instance, created, **kwargs):
    # send to author
    # send to managers
    pass



post_save.connect(signal_incident, sender=Incident)
#post_save.connect(signal_followup, sender=IncidentFollowup)