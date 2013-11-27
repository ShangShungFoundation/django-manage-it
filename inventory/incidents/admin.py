from django.contrib import admin

from models import Incident, IncidentFolowup

class IncidentAdmin(admin.ModelAdmin):
    list_display = ("title", 'created', 'status', 'priority', )
    list_filter = [ 'priority', 'status', ]
    search_fields = ['subject', 'description',]
    readonly_fields = ("priority", "created_by",)
    
    
admin.site.register(Incident, IncidentAdmin)
admin.site.register(IncidentFolowup)

