<<<<<<< HEAD
# -*- coding: utf-8 -*-
=======
>>>>>>> e8e383c04fc0cad9fc1c95298546cc6b656b7cf7
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from organizations.models import Organization


class Location(models.Model):
    name = models.CharField(_("name"), max_length=32, )
<<<<<<< HEAD
    address_line1 = models.CharField(
        _(u"address 1"),
        max_length=64, null=True, blank=True, )
    address_line2 = models.CharField(
        _(u"address 2"),
        max_length=64, null=True, blank=True, )
    phone_number1 = models.CharField(
        _(u"tel 1"),
        max_length=32, null=True, blank=True, )
    phone_number2 = models.CharField(
        _(u"tel 2"),
        max_length=32, null=True, blank=True, )
    lng = models.CharField(
        _(u"geo longitude"),
        max_length=16, null=True, blank=True, )
    lat = models.CharField(
        _(u"geo latitude"),
        max_length=16, null=True, blank=True, )
=======
    address_line1 = models.CharField(max_length=64, null=True, blank=True, )
    address_line2 = models.CharField(max_length=64, null=True, blank=True, )
    phone_number1 = models.CharField(max_length=32, null=True, blank=True, )
    phone_number2 = models.CharField(max_length=32, null=True, blank=True, )
    lng = models.CharField(max_length=16, null=True, blank=True, )
    lat = models.CharField(max_length=16, null=True, blank=True, )
>>>>>>> e8e383c04fc0cad9fc1c95298546cc6b656b7cf7

    class Meta:
        ordering = ['name']
        verbose_name = _(u"location")
        verbose_name_plural = _(u"locations")

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('location_view', [str(self.id)])


class ItemTemplate(models.Model):
    #item_class = models.ForeignKey(ItemClass)
    description = models.CharField(_(u"description"), max_length=64)
    brand = models.CharField(_(u"brand"), max_length=32, null=True, blank=True)
    model = models.CharField(_(u"model"), max_length=32, null=True, blank=True)
    part_number = models.CharField(
        _(u"part number"),
        max_length=32, null=True, blank=True)
    notes = models.TextField(_(u"notes"), null=True, blank=True)

    product_url = models.URLField(
        u"product url",
        null=True, blank=True,
        max_length=200)
    supplies = models.ManyToManyField(
        "self",
        null=True, blank=True,
        verbose_name=_(u"supplies"))
    suppliers = models.ManyToManyField(
        "Supplier", null=True, blank=True)

    class Meta:
        ordering = ['description']
        verbose_name = _(u"item template")
        verbose_name_plural = _(u"item templates")

    @models.permalink
    def get_absolute_url(self):
        return ('template_view', [str(self.id)])

    def __unicode__(self):
        return self.description


class Log(models.Model):
<<<<<<< HEAD
    # TODO implemet
    timedate = models.DateTimeField(
        _(u"timedate"),
        auto_now_add=True)
    action = models.CharField(
        _(u"action"),
        max_length=32)
=======
    timedate = models.DateTimeField(
        _(u"timedate"),
        auto_now_add=True)
    action = models.CharField(max_length=32)
>>>>>>> e8e383c04fc0cad9fc1c95298546cc6b656b7cf7
    description = models.TextField(
        _(u"description"),
        null=True, blank=True)
    #user = models.ForeignKey(User, unique=True)

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey()

    def __unicode__(self):
#		return "%Y-%m-%d %H:%M:%S" % (self.timedate) #& user  && item
        return "%s, %s - %s" % (self.timedate, self.action, self.content_object)

    @models.permalink
    def get_absolute_url(self):
        return ('log_view', [str(self.id)])


class Inventory(models.Model):
<<<<<<< HEAD
    name = models.CharField(
        _(u'name'), max_length=32, )
=======
    name = models.CharField(_(u'name'), max_length=32, )
>>>>>>> e8e383c04fc0cad9fc1c95298546cc6b656b7cf7
    location = models.ForeignKey(
        Location,
        verbose_name=_(u'location'))
    organization = models.ForeignKey(
        Organization,
        verbose_name=_(u'Organization'))

    class Meta:
        verbose_name = _(u'inventory')
        verbose_name_plural = _(u'inventories')

    @models.permalink
    def get_absolute_url(self):
        return ('inventory', [self.organization.url, self.id])

    def __unicode__(self):
        return self.name


class Supplier(models.Model):
    #TODO: Contact, extension
<<<<<<< HEAD
    name = models.CharField(
        _("name"), max_length=32)
    address_line1 = models.CharField(
        _(u"address 1"),
        max_length=64, null=True, blank=True, )
    address_line2 = models.CharField(
        _(u"address 2"),
        max_length=64, null=True, blank=True, )
    phone_number1 = models.CharField(
        _(u"tel 1"),
        max_length=32, null=True, blank=True, )
    phone_number2 = models.CharField(
        _(u"tel 2"),
=======
    name = models.CharField(max_length=32, verbose_name=_("name"))
    address_line1 = models.CharField(
        _(u'address 1'),
        max_length=64, null=True, blank=True,)
    address_line2 = models.CharField(
        max_length=64, null=True, blank=True, )
    address_line3 = models.CharField(
        max_length=64, null=True, blank=True, )
    address_line4 = models.CharField(
        max_length=64, null=True, blank=True, )
    phone_number1 = models.CharField(
        max_length=32, null=True, blank=True, )
    phone_number2 = models.CharField(
>>>>>>> e8e383c04fc0cad9fc1c95298546cc6b656b7cf7
        max_length=32, null=True, blank=True, )
    email = models.EmailField(
        null=True, blank=True,)
    web = models.CharField(
        max_length=32, null=True, blank=True, )
<<<<<<< HEAD
    notes = models.TextField(
        _(u'notes'), null=True, blank=True,)
=======
    notes = models.TextField(_(u'notes'), null=True, blank=True,)
>>>>>>> e8e383c04fc0cad9fc1c95298546cc6b656b7cf7

    class Meta:
        ordering = ['name']
        verbose_name = _(u"supplier")
        verbose_name_plural = _(u"suppliers")

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('supplier_view', [str(self.id)])
