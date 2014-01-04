# -*- coding: utf-8 -*-
from django.db import models
from django.utils.encoding import force_unicode
from django.utils.translation import ugettext_lazy as _

from django.conf import settings

LEVEL_CHOICES = (
    (1, _("mesage")),
    (2, _("warning")),
    (3, _("error")),
)

STATUS = (
    (1, _("pending")),
    (2, _("delivered")),
    (3, _("read")))


class Notification(models.Model):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="related_senders",
        verbose_name=_(u"User"))
    receptor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="related_receptors",
        verbose_name=_(u"receptor"))
    message = models.TextField(_(u"message"))
    level = models.IntegerField(
        _(u"level"), choices=LEVEL_CHOICES)
    created = models.DateTimeField(
        _(u"created"), auto_now_add=True)
    modified = models.DateTimeField(
        _(u"modified"), auto_now=True)
    url = models.URLField(
        _(u"url"), blank=True, null=True)
    status = models.IntegerField(
        _(u"status"), choices=STATUS, default=2)
    expires = models.DateTimeField(
        _(u"expires"), null=True, blank=True)

    def __unicode__(self):
        return force_unicode(self.message)


def notify(user, message, level=1, **kwargs):
    notification = Notification(
        user=user,
        message=message,
        level=level)
    notification.save()
    return
