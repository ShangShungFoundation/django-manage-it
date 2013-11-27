from django.utils import simplejson

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, UserManager

from assets.models import Item
from lib.model_diff_mixin import ModelDiffMixin

STATUSES = (
    (1, "open"),
    (2, "in work"),
    (3, "closed"),
    (4, "defunkt"),
    (5, "duplicate"),
)

IMPACT_GRADES = [
    (1, "High"),
    (2, "Medium"),
    (3, "Low"),
]

PRIORITY_GRADES = (
    (1, "Critical"),
    (2, "High"),
    (3, "Moderate"),
    (4, "Low"),
    (5, "Planning"),
)

PRORITY_MATRIX = dict(
    _1_1 = 1,
    _1_2 = 2,
    _1_3= 3,
    _2_1 = 2,
    _2_2 = 3,
    _2_3 = 4,
    _3_1 = 3,
    _3_2 = 4,
    _3_3 = 5,
)


class IncidentManager(models.Manager):
    def get_queryset(self):
        return super(IncidentManager, self).get_queryset().order_by("-status")


class Incident(models.Model, ModelDiffMixin):
    """
    Rufly following ITIL Incident Mangement
    
    https://wiki.servicenow.com/index.php?title=ITIL_Incident_Management
    """
    objects = IncidentManager() 
    
    
    title = models.CharField(_("subject"), max_length=100, )
    description = models.TextField(_(u"description"), max_length=64)
    
    created = models.DateTimeField(auto_now_add=True, verbose_name=_(u"created"))
    created_by = models.ForeignKey(User)
    
    status = models.SmallIntegerField(_(u"status"), choices=STATUSES)

    affected_devices = models.ManyToManyField(Item, null=True, blank=True, 
            verbose_name=_(u"affected devices"))
    
    #prioritzation
    impact = models.SmallIntegerField(_(u"impact"), choices=IMPACT_GRADES, default=2)
    urgency = models.SmallIntegerField(_(u"urgency"), choices=IMPACT_GRADES, default=2)
    priority = models.SmallIntegerField(_(u"priority"), choices=PRIORITY_GRADES)
    
    class Meta:
        ordering = ['status']
        verbose_name = _(u"incident")
        verbose_name_plural = _(u"incidents")
        
    def __unicode__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        #self.created_by_id = 1
        priority_index = "_%s_%s" % (self.impact, self.urgency)
        self.priority = PRORITY_MATRIX[priority_index]
        if not self.id:
            self.status = 1
        super(Incident, self).save(*args, **kwargs)
        
    @models.permalink
    def get_absolute_url(self):
        return ('incident_view', [str(self.id)])



class IncidentFolowupManager(models.Manager):
    def get_queryset(self):
        return super(IncidentFolowupManager, self).get_queryset().order_by("created_at")
    
    
INCIDENT_STATUS_TYPES = (
    (1, "status change"),
    (2, "comment"),
    (3, "proposal"),
)

class IncidentFolowup(models.Model):
    
    objects = IncidentFolowupManager()
    
    incident = models.ForeignKey(Incident, verbose_name=_(u"item"))
    status_change = models.TextField(_(u"status change"),
          blank=True, null=True,)
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_(u"created_at"))
    created_by = models.ForeignKey(User)
    
    observations = models.TextField(_(u"observations"),)
    
    class Meta:
        ordering = ['incident']
        verbose_name = _(u"incident following")
        verbose_name_plural = _(u"incident following")        
        
    def __unicode__(self):
        return self.incident.title
    
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
        
        changes = simplejson.loads(self.status_change)
        return [self.display_change(f, changes[f]) for f in changes.keys()]
       
    @models.permalink
    def get_absolute_url(self):
        return ('group_view', [str(self.id)])
