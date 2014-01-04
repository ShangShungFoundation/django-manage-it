# -*- coding: utf-8 -*-
import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from catalog.models import ItemTemplate, Location, Inventory
from dataforms.models import DataForm, Submission, Answer
from organizations.models import Organization


class State(models.Model):
    name = models.CharField(max_length=32, verbose_name=_(u'name'))
    exclusive = models.BooleanField(default=False, verbose_name=_(u'exclusive'))

    class Meta:
        verbose_name = _(u"state")
        verbose_name_plural = _(u"states")

    def __unicode__(self):
        return "%s - %s" % (
            self.name, self.exclusive and _(u'exl') or _(u'inc'))

    @models.permalink
    def get_absolute_url(self):
        return ('state_list', [])


class ItemStateManager(models.Manager):
    def states_for_item(self, item):
        return self.filter(item=item)


class ItemState(models.Model):
    item = models.ForeignKey('Item', verbose_name=_(u"item"))
    state = models.ForeignKey(State, verbose_name=_(u"state"))
    date = models.DateField(verbose_name=_(u"date"), auto_now_add=True)

    objects = ItemStateManager()

    class Meta:
        verbose_name = _(u"item state")
        verbose_name_plural = _(u"item states")

    def __unicode__(self):
        return _(u"%(asset)s, %(state)s since %(date)s") % {
            'asset': self.item,
            'state': self.state.name,
            'date': self.date}

    @models.permalink
    def get_absolute_url(self):
        return ('state_update', [str(self.id)])


class Item(models.Model):
    inventory = models.ForeignKey(Inventory, verbose_name=_(u"inventory"))
    item_template = models.ForeignKey(
        ItemTemplate,
        verbose_name=_(u"item template"))

    item_class = models.ForeignKey(
        DataForm,
        verbose_name=_(u"item class"),
        limit_choices_to={'collection__slug__exact': "assets"},
        related_name="related_forms")

    property_number = models.CharField(
        _(u"asset number (SKU)"),
        max_length=48, unique=True)
    serial_number = models.CharField(
        _(u"serial number"),
        max_length=48, null=True, blank=True)

    location = models.ForeignKey(
        Location,
        verbose_name=_(u"location"),
        null=True, blank=True)
    position = models.TextField(
        _(u"position"),
        null=True, blank=True)
    function = models.TextField(
        _(u"function"),
        null=True, blank=True)
    description = models.TextField(
        _(u"description"),
        null=True, blank=True)
    active = models.BooleanField(default=True)
    state = models.ForeignKey(State, verbose_name=_(u"state"), )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_(u"owner"))
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="users",
        verbose_name=_(u"users"))
    created = models.DateTimeField(default=datetime.datetime.now())

    class Meta:
        ordering = ['property_number']
        verbose_name = _(u"asset")
        verbose_name_plural = _(u"assets")

    @models.permalink
    def get_absolute_url(self):
        return ('item_view', [str(self.id)])

    def __unicode__(self):
        return "%s %s - %s" % (
            self.property_number, self.item_template, self.location)

    def is_orphan(self):
        if self.person_set.all():
            return False
        else:
            return True

    def get_owners(self):
        try:
            return self.person_set.all()
        except:
            return None

    def get_nonowners(self):
        return Person.objects.all().exclude(
            id__in=self.person_set.values_list("id",  flat=True))

    def add_owner(self, person):
        if self not in person.inventory.all():
            person.inventory.add(self)

    def remove_owner(self, person):
#		if self in person.inventory.all():
        #import ipdb; ipdb.set_trace()
        person.inventory.remove(self)

    def states(self):
        return [State.objects.get(pk=id) for id in self.itemstate_set.all().values_list('state', flat=True)]

    def delete(self, *args, **kwargs):
        #delete related answers
        try:
            submission = Submission.objects.get(slug=self.property_number)
            answers = Answer.objects.filter(submission=submission)
            answers.delete()
        except:
            pass
        super(Item, self).delete(*args, **kwargs)


class Person(models.Model):
    last_name = models.CharField(
        _(u"last name"), max_length=32)
    second_last_name = models.CharField(
        _(u"second last name"),
        max_length=32, blank=True, null=True)
    first_name = models.CharField(
        _(u"first name"), max_length=32)
    second_name = models.CharField(
        _(u"second name or initial"),
        max_length=32, blank=True, null=True)
    location = models.ForeignKey(
        Location,
        verbose_name=_(u"location"),
        blank=True, null=True,)

    class Meta:
        ordering = [
            'last_name', 'second_last_name',
            'first_name', 'second_name']
        verbose_name = _(u"person")
        verbose_name_plural = _(u"people")

    @models.permalink
    def get_absolute_url(self):
        return ('person_view', [str(self.id)])

    def __unicode__(self):
        if self.second_last_name:
            second_last_name = " %s" % self.second_last_name
        else:
            second_last_name = ''

        if self.second_name:
            second_name = " %s" % self.second_name
        else:
            second_name = ''

        return "%s%s, %s%s" % (
            self.last_name,
            second_last_name and second_last_name,
            self.first_name, second_name)


class Owner(models.Model):
    name = models.CharField(
        _(u"last name"), max_length=32)
    email = models.EmailField(
        _(u"second last name"),
        max_length=32, blank=True, null=True)

    def __unicode__(self):
        return self.name

RESOURCE_TYPES = (
    (1, _("driver")),
    (2, _("manual")),
    (3, _("configuration")),
)


class Resource(models.Model):
    item = models.ForeignKey(
        Item, verbose_name=_(u"item"))
    resurce_type = models.SmallIntegerField(
        _(u"resource type"),
        choices=RESOURCE_TYPES)
    name = models.CharField(
        _(u"name"), max_length=32)
    file = models.FileField(
        _("file"),
        upload_to="files",
        null=True, blank=True)

    def __unicode__(self):
        return self.name


ASSET_REQUEST_STATUSES = (
    (1, _("open")),
    (2, _("accepted")),
    (3, _("fulfilled")),
    (4, _("rejected")),
)


class AssetRequest(models.Model):
    organization = models.ForeignKey(
        Organization,
        related_name="replaced_organizations",
        verbose_name=_(u"organization"))

    replaced_item = models.ForeignKey(
        Item,
        related_name="replaced_items",
        verbose_name=_(u"item to be replaced"),
        null=True, blank=True)

    new_item = models.ForeignKey(
        Item,
        related_name="new_items",
        verbose_name=_(u"new item"),
        null=True, blank=True)

    item_class = models.ForeignKey(
        DataForm,
        verbose_name=_(u"item class"),
        related_name="related_requests")

    created_at = models.DateTimeField(
        default=datetime.datetime.now())
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_(u"created by"))

    status = models.SmallIntegerField(
        _(u"status"),
        choices=ASSET_REQUEST_STATUSES)

    description = models.TextField(
        _(u"description"),
        null=True, blank=True)

    def __unicode__(self):
        return _(u"new %s requested by %s at %s") % (
            self.item_class,  self.created_by, self.created_at)
