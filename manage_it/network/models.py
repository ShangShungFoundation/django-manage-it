from django.db import models
from django.utils.translation import ugettext_lazy as _

from assets.models import Item
from catalog.models import Inventory

CONNECTION_TYPES = (
    (1, "Ethernet 1Gb"),
    (2, "Ethernet 100Mb"),
    (3, "WIFI"),
    (4, "Optic Fiber"),
    (5, "USB"),
    (6, "HDMI"),
    (7, "Telephone"),
)


class Network(models.Model):
    """
    ItemConnection for networked assets
    """
    inventory = models.ForeignKey(
        Inventory, verbose_name=_(u"inventory"))
    name = models.CharField(_(u"name"), max_length=100)
    description = models.TextField(blank=True, null=True)
    ip_range = models.CharField(
        _(u"ip_range"),
        blank=True, null=True, max_length=100)

    def __unicode__(self):
        return self.name


class Connection(models.Model):
    """
    ItemConnection for networked assets
    """
    concetion_type = models.SmallIntegerField(
        _(u"link type"), choices=CONNECTION_TYPES)
    device_1 = models.ForeignKey(
        Item, verbose_name=_(u"item 1"), related_name="dev1")
    device_1_interface = models.IPAddressField(
        blank=True, null=True)
    device_1_mac = models.CharField(
        blank=True, null=True, max_length=79)
    device_2 = models.ForeignKey(
        Item, verbose_name=_(u"item 2"), related_name="dev2")
    device_2_interface = models.IPAddressField(
        blank=True, null=True)
    device_2_mac = models.CharField(
        blank=True, null=True, max_length=79)
    description = models.TextField(
        blank=True, null=True)
    network = models.ForeignKey(Network)

    class Meta:
        unique_together = ("device_1", "device_2")

    def __unicode__(self):
        return "%s #%s" % (self.network, self.id)


class Interface(models.Model):
    mac = models.CharField(_(u"MAC"), blank=True, null=True, max_length=79)
    device = models.ForeignKey(Item, verbose_name=_(u"device"))
    description = models.TextField(_(u"description"), blank=True, null=True)

    def __unicode__(self):
        return self.mac
