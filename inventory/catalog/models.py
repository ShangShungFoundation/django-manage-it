import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.auth.models import User, UserManager
from django.core.urlresolvers import reverse

from dataforms.models import DataForm

class Location(models.Model):
    name = models.CharField(_("name"), max_length=32, )
    address_line1 = models.CharField(max_length=64, null=True, blank=True, )
    address_line2 = models.CharField(max_length=64, null=True, blank=True, )
    address_line3 = models.CharField(max_length=64, null=True, blank=True, )
    address_line4 = models.CharField(max_length=64, null=True, blank=True, )
    phone_number1 = models.CharField(max_length=32, null=True, blank=True, )
    phone_number2 = models.CharField(max_length=32, null=True, blank=True, )
    lng = models.CharField(max_length=16, null=True, blank=True, )
    lat = models.CharField(max_length=16, null=True, blank=True, )

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
    part_number = models.CharField(_(u"part number"), 
            max_length=32, null=True, blank=True)
    notes = models.TextField(_(u"notes"), null=True, blank=True)
    
    product_url = models.URLField(u"product url",
            null=True, blank=True, 
            max_length=200)
    supplies = models.ManyToManyField("self", null=True, blank=True, 
            verbose_name=_(u"supplies"))
    suppliers = models.ManyToManyField("Supplier", null=True, blank=True)
    
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
    timedate = models.DateTimeField(auto_now_add=True, verbose_name=_(u"timedate"))
    action = models.CharField(max_length=32)
    description = models.TextField(verbose_name=_(u"description"), null=True, blank=True)
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
    name = models.CharField(max_length=32, verbose_name=_(u'name'))
    location = models.ForeignKey(Location, verbose_name=_(u'location'))

    class Meta:
        verbose_name = _(u'inventory')
        verbose_name_plural = _(u'inventories')

    @models.permalink
    def get_absolute_url(self):
        return ('inventory_view', [str(self.id)])

    def __unicode__(self):
        return self.name


class InventoryCheckPoint(models.Model):
    inventory = models.ForeignKey(Inventory)
    datetime = models.DateTimeField(default=datetime.datetime.now())
    supplies = models.ManyToManyField(ItemTemplate, null=True, blank=True, through='InventoryCPQty')


class InventoryCPQty(models.Model):
    supply = models.ForeignKey(ItemTemplate)
    check_point = models.ForeignKey(InventoryCheckPoint)
    quantity = models.IntegerField()

    
class InventoryTransaction(models.Model):
    inventory = models.ForeignKey(Inventory)
    supply = models.ForeignKey(ItemTemplate)
    quantity = models.IntegerField()
    date = models.DateField(default=datetime.date.today(), verbose_name=_(u"date"))
    notes = models.TextField(null=True, blank=True)
    
    class Meta:
        verbose_name = _(u'inventory transaction')
        verbose_name_plural = _(u'inventory transactions')
        ordering = ['-date', '-id']

    @models.permalink
    def get_absolute_url(self):
        return ('inventory_transaction_view', [str(self.id)])
    
    def __unicode__(self):
        return "%s: '%s' qty=%s @ %s" % (self.inventory, self.supply, self.quantity, self.date)


class Supplier(models.Model):
    #TODO: Contact, extension
    name = models.CharField(max_length=32, verbose_name=_("name"))
    address_line1 = models.CharField(_(u'address 1'), max_length=64, null=True, blank=True,)
    address_line2 = models.CharField(max_length=64, null=True, blank=True, )
    address_line3 = models.CharField(max_length=64, null=True, blank=True, )
    address_line4 = models.CharField(max_length=64, null=True, blank=True, )
    phone_number1 = models.CharField(max_length=32, null=True, blank=True, )
    phone_number2 = models.CharField(max_length=32, null=True, blank=True, )
    email = models.EmailField( null=True, blank=True,)
    web = models.CharField(max_length=32, null=True, blank=True, )
    notes = models.TextField(_(u'notes'), null=True, blank=True,)
    
    class Meta:
        ordering = ['name']
        verbose_name = _(u"supplier")
        verbose_name_plural = _(u"suppliers")
        
    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('supplier_view', [str(self.id)])
