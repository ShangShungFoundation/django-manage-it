from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import force_unicode

LEVEL_CHOICES = (
    (1, "mesage"),
    (2, "warning"),
    (3, "error"),
)

STATUS = (
    (1, "pending"),
    (2, "delivered"),
    (3, "read"),
)


class Notification(models.Model):
    sender = models.ForeignKey(User, related_name="related_senders")
    receptor = models.ForeignKey(User, related_name="related_receptors")
    message = models.TextField()
    level = models.IntegerField(choices=LEVEL_CHOICES)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    url = models.URLField(blank=True, null=True)
    read = models.BooleanField(default=False)
    status = models.IntegerField(choices=STATUS, default=2)
    expires = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return force_unicode(self.message)


def notify(user, message, level=1, **kwargs):
    notification = Notification(
        user=user,
        message=message,
        level=level)
    notification.save()
    return
