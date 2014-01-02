# -*- coding: utf-8 -*-
from datetime import timedelta
from django.utils import timezone

from django.utils import simplejson
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from assets.models import Item
from lib.model_diff_mixin import ModelDiffMixin
from organizations.models import Organization

from settings import STATUSES, RESPONSE_MATRIX

IMPACT_GRADES = [
    (1, _("High")),
    (2, _("Medium")),
    (3, _("Low")),
]

PRIORITY_GRADES = (
    (1, _("Critical")),
    (2, _("High")),
    (3, _("Moderate")),
    (4, _("Low")),
    (5, _("Planning")),
)

PRORITY_MATRIX = dict(
    _1_1=1,
    _1_2=2,
    _1_3=3,
    _2_1=2,
    _2_2=3,
    _2_3=4,
    _3_1=3,
    _3_2=4,
    _3_3=5,
)


USERS_TYPES = (
    (1, _("Standart")),
    (2, _("Top")),
    (3, _("VIP")),
)


class IncidentManager(models.Manager):
    def get_queryset(self):
        return super(IncidentManager, self).get_queryset().order_by("-status")


class Incident(models.Model, ModelDiffMixin):
    """
    Ruthly following ITIL Incident Mangement
    https://wiki.servicenow.com/index.php?title=ITIL_Incident_Management
    """
    objects = IncidentManager()

    organization = models.ForeignKey(
        Organization,
        verbose_name=_(u"Organization"))

    subject = models.CharField(_("subject"), max_length=100, )
    description = models.TextField(_(u"description"), max_length=64)

    submited_at = models.DateTimeField(_(u"submited at"), auto_now_add=True)
    submited_by = models.ForeignKey(User, verbose_name=_(u"submited by"))

    assigned_to = models.ForeignKey(
        User,
        verbose_name=_("assigned to"),
        null=True, blank=True,
        related_name="asigned_workers",
        #limit_choices_to=LIMIT_ASIGNED_USERS,
    )

    alternate_user_name = models.CharField(
        _("alternate user name"),
        max_length=100,
        null=True, blank=True,
        help_text="in the case if you are not affected user ")
    alternate_user_email = models.EmailField(
        _("alternate user email"),
        max_length=100,
        null=True, blank=True,
        help_text="in the case if you are not affected user ")
    alternate_user_tel = models.CharField(
        _("alternate user tel"),
        max_length=100,
        null=True, blank=True,
        help_text="in the case if you are not affected user ")

    #prioritzation
    impact = models.SmallIntegerField(
        _(u"impact"), choices=IMPACT_GRADES, default=2)
    urgency = models.SmallIntegerField(
        _(u"urgency"), choices=IMPACT_GRADES, default=2)
    priority = models.SmallIntegerField(
        _(u"priority"), choices=PRIORITY_GRADES)

    status = models.SmallIntegerField(_(u"status"), choices=STATUSES)

    affected_devices = models.ManyToManyField(
        Item,
        verbose_name=_(u"affected devices"),
        null=True, blank=True,)
    affected_software = models.TextField(
        _(u"affected software"),
        null=True, blank=True,
        help_text="Do not use for hardware")
    error_msg = models.TextField(
        _(u"error mesage"),
        null=True, blank=True,
        max_length=64)

    daedline = models.DateTimeField(_(u"respond daedline"), null=True)

    class Meta:
        ordering = ['status']
        verbose_name = _(u"incident")
        verbose_name_plural = _(u"incidents")

    def __unicode__(self):
        return self.subject

    def get_user_type(self):
        if self.organization.is_group_member(self.submited_by, "vip_group"):
            return 3
        if self.organization.is_group_member(self.submited_by, "top_group"):
            return 2
        if self.organization.is_user_staff(self.submited_by):
            return 1
        return None

    def get_priority(self):
        priority_index = "_%s_%s" % (self.impact, self.urgency)
        return PRORITY_MATRIX[priority_index]

    def get_respond_time(self):
        user_type = self.get_user_type()
        return RESPONSE_MATRIX["_%s" % self.priority][user_type or 1]

    def get_deadline(self):
        #import ipdb; ipdb.set_trace()
        return self.submited_at + timedelta(**self.get_respond_time())

    def save(self, *args, **kwargs):
        #self.created_by_id = 1
        if not self.id:
            self.status = 1
            self.submited_at = timezone.now()

        self.priority = self.get_priority()
        self.daedline = self.get_deadline()

        super(Incident, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return ('incident', [self.organization.url, str(self.id)])


class IncidentFolowupManager(models.Manager):
    def get_queryset(self):
        return super(
            IncidentFolowupManager, self).get_queryset().order_by("created_at")


INCIDENT_STATUS_TYPES = (
    (1, _("status change")),
    (2, _("comment")),
    (3, _("proposal")),
)


class IncidentFollowup(models.Model):

    objects = IncidentFolowupManager()

    incident = models.ForeignKey(
        Incident, verbose_name=_(u"item"))
    status_change = models.TextField(
        _(u"status change"),
        blank=True, null=True,)

    created_at = models.DateTimeField(
        _(u"created_at"), auto_now_add=True)
    created_by = models.ForeignKey(User)

    observations = models.TextField(_(u"observations"),)

    class Meta:
        ordering = ['incident']
        verbose_name = _(u"incident following")
        verbose_name_plural = _(u"incident following")

    def __unicode__(self):
        return self.incident.subject

    def display_change(self, field, values):
        choices = self.incident._meta.get_field_by_name(field)[0].choices

        def get_choice(choices, selected):
            for choice in choices:
                if choice[0] == selected:
                    return choice[1]

        return "%s: %s > %s" % (
            field,
            get_choice(choices, values[0]),
            get_choice(choices, values[1])
        )

    def display_changes(self):
        if not self.status_change or self.status_change == "{}":
            return []
        #import ipdb; ipdb.set_trace()
        changes = simplejson.loads(self.status_change)
        return [self.display_change(f, changes[f]) for f in changes.keys()]

    @models.permalink
    def get_absolute_url(self):
        return ('group_view', [str(self.id)])
