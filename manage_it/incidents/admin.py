from django.contrib import admin

from models import Incident, IncidentFollowup


class IncidentAdmin(admin.ModelAdmin):
    list_display = ("subject", 'submited_at', 'status', 'priority', )
    list_filter = ['priority', 'status']
    search_fields = ['subject', 'description']
    readonly_fields = ("priority", "submited_by",)

admin.site.register(Incident, IncidentAdmin)
admin.site.register(IncidentFollowup)
