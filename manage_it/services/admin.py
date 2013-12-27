from django.contrib import admin

from models import Service, Provider, SLA, SLA_billing, Bill, Document


class ItemTemplateAdmin(admin.ModelAdmin):
    filter_horizontal = ('supplies', 'suppliers')

admin.site.register(Service)
admin.site.register(Provider)
admin.site.register(SLA)
admin.site.register(SLA_billing)
admin.site.register(Bill)
admin.site.register(Document)
