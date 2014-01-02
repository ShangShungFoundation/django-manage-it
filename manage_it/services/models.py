# -*- coding: utf-8 -*-

import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, Group

from dataforms.models import DataForm

from catalog.models import Location
from organizations.models import Organization
from lib.model_audit import AuditMixin

from settings import SERVICE_TYPES


class Provider(models.Model, AuditMixin):
    #TODO: Contact, extension
    name = models.CharField(max_length=32, verbose_name=_("name"))

    service_type = models.SmallIntegerField(
        _(u"service type"),
        choices=SERVICE_TYPES)

    address_line1 = models.CharField(
        _(u'address 1'),
        max_length=64, null=True, blank=True,)
    address_line2 = models.CharField(max_length=64, null=True, blank=True, )
    phone_number1 = models.CharField(max_length=32, null=True, blank=True, )
    phone_number2 = models.CharField(max_length=32, null=True, blank=True, )

    email = models.EmailField(null=True, blank=True,)
    web = models.CharField(max_length=32, null=True, blank=True, )

    contact_person = models.CharField(
        _("contact person"), max_length=32, null=True, blank=True)

    notes = models.TextField(_(u'notes'), null=True, blank=True,)

    class Meta:
        ordering = ['name']
        verbose_name = _(u"provider")
        verbose_name_plural = _(u"providers")

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('supplier_view', [str(self.id)])


class Service(models.Model, AuditMixin):
    name = models.CharField(_(u'name'), max_length=32)
    description = models.TextField(
        _(u"description"),
        null=True, blank=True)

    service_type = models.SmallIntegerField(
        _(u"service type"),
        choices=SERVICE_TYPES,)

    location = models.ForeignKey(
        Location,
        null=True, blank=True,
        verbose_name=_(u'location'))

    owner = models.ForeignKey(
        Organization,
        verbose_name=_(u'Owner'),
        related_name="related_owners")
    manager = models.ForeignKey(
        User,
        verbose_name=_(u'Manager'))

    user_groups = models.ManyToManyField(
        Group,
        null=True, blank=True,
        verbose_name=_(u'User Groups'),)
    users = models.ManyToManyField(
        User,
        null=True, blank=True,
        related_name="related_users")

    notes = models.TextField(
        _(u"notes"),
        null=True, blank=True)

    depends_on = models.ManyToManyField(
        "Service",
        verbose_name=_(u'depends on'),
        null=True, blank=True)

    class Meta:
        verbose_name = _(u'Service')
        verbose_name_plural = _(u'Services')

    def is_used_by(self, user):
        """ checks if service is used by user"""

        user_groups_id = self.user_groups.values_list("id", flat=True)
        user_membership = user.groups.filter(id__in=user_groups_id)
        return user_membership

    @models.permalink
    def get_absolute_url(self):
        return ('view_service', [str(self.owner.url), str(self.pk)])

    def __unicode__(self):
        return self.name


DOCUMENT_SENSITIVITY = (
    (1, "reserved"),
    (2, "internal"),
    (3, "public"),
)


class SLAManager(models.Manager):
    def in_organization(self, slug):
        return self.filter(service__owner__slug=slug, terminated__isnull=True)


class SLA(models.Model, AuditMixin):

    objects = SLAManager()

    service = models.ForeignKey(
        Service,
        verbose_name=_(u'Service'))
    provider = models.ForeignKey(
        Provider,
        verbose_name=_(u'Provider'))

    service_classes = models.ManyToManyField(
        DataForm,
        verbose_name=_(u"service components"),
        limit_choices_to={'collection__slug__exact': "services"},
        related_name="related_service_classes")

    service_scope = models.TextField(_(u"Service Scope"))

    customer_requirements = models.TextField(
        _(u"Customer Requirements"),
        null=True, blank=True)
    provider_requirements = models.TextField(
        _(u"Provider Requirements"),
        null=True, blank=True)

    coverege_time = models.TextField(
        _(u"Coverege Time"),
        null=True, blank=True)

    support_time = models.TextField(
        _(u"Support Time"),
        null=True, blank=True)

    maintenance = models.TextField(
        _(u"Maitenance Management"),
        null=True, blank=True)

    reviewing = models.TextField(
        _(u"Reporting, Reviewing and Auditing"),
        null=True, blank=True)
    review_period = models.SmallIntegerField(
        _(u"review period"),
        choices=((1, 1), (2, 2)),
        default=1,
        help_text="in years",)

    started = models.DateField(_(u"Service initiated"))
    terminated = models.DateField(
        _(u"Service terminated"),
        null=True, blank=True)

    class Meta:
        #ordering = ['Billing']
        verbose_name = _(u"SLA")
        verbose_name_plural = _(u"SLAs")

    @property
    def active(self):
        if self.terminated:
            return "finished"
        else:
            return "active"

    def __unicode__(self):
        return u"%s privided by %s - %s" % (
            self.service, self.provider, self.active)

    @models.permalink
    def get_absolute_url(self):
        return (
            'sla_view',
            [str(self.service.owner.url), str(self.service_id), str(self.pk)])


DOCUMENT_TYPES = (
    (1, _("contract")),
    (3, _("documenation")),
    (4, _("manual")),
    (5, _("help")),
    (6, _("other")),
)

DOCUMENT_SENSITIVITY = (
    (1, _("reserved")),
    (2, _("internal")),
    (3, _("public")),
)


class Document(models.Model):
    SLA = models.ForeignKey(SLA, verbose_name=_(u"item"))
    document_type = models.SmallIntegerField(
        _(u"document type"),
        choices=DOCUMENT_TYPES)
    name = models.CharField(
        _(u"name"), max_length=32)

    sensitivity = models.SmallIntegerField(
        _(u"sensitivity"), choices=DOCUMENT_SENSITIVITY)

    created_at = models.DateTimeField(default=datetime.datetime.now())
    created_by = models.ForeignKey(User)

    doc = models.FileField(
        "file",
        upload_to="SLA_documents",)

    def __unicode__(self):
        return self.name


# TODO move billing to separate APP

CURRENCIES = (
    (1, u"€"),
    (3, u"$"),
    (4, u"zł"),
)

PAYMENT_METHODS = (
    (1, _("transfer")),
    (3, _("card")),
    (4, _("other")),
)


class SLA_billing(models.Model):
    SLA = models.ForeignKey(SLA)
    billing_amount = models.SmallIntegerField(
        _(u"amount"), )
    billing_currency = models.SmallIntegerField(
        _(u"billing currency"),
        default=1,
        choices=CURRENCIES)
    billing_method = models.SmallIntegerField(
        _(u"billing method"),
        choices=PAYMENT_METHODS)
    billing_period = models.SmallIntegerField(
        _(u"billing period"),
        choices=(
            (1, _("1 month")),
            (2, _("2 months")),
            (6, _("6 months")),
            (12, _("1 year")),
            (24, _("2 years"))),
        default=12,
        null=True, blank=True,)
    account = models.TextField(
        _(u"account/card nr"), null=True, blank=True)
    observations = models.TextField(
        _(u"observations"), null=True, blank=True)

    class Meta:
        #ordering = ['Billing']
        verbose_name = _(u"Billing")
        verbose_name_plural = _(u"Billings")

    def __unicode__(self):
        return u"%s - %s" % (self.SLA.service.name, self.SLA.provider.name)


class Bill(models.Model):
    billing = models.ForeignKey(SLA_billing)

    file = models.FileField(
        "file",
        upload_to="SLA_billing",)

    period = models.DateField(
        default=datetime.datetime.now(),
        help_text=_("billing period againt which bill was issued"))

    created_at = models.DateTimeField(default=datetime.datetime.now())
    created_by = models.ForeignKey(User)

    def __unicode__(self):
        return u"%s %s" % (self.billing, self.period)
