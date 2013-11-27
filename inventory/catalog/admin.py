from django.contrib import admin

from models import Location, ItemTemplate, Log, Inventory,\
		InventoryCheckPoint, InventoryCPQty, InventoryTransaction, Supplier

class ItemTemplateAdmin(admin.ModelAdmin):
    filter_horizontal = ('supplies', 'suppliers')

admin.site.register(Location)
admin.site.register(ItemTemplate, ItemTemplateAdmin)
admin.site.register(Log)
admin.site.register(Inventory)
admin.site.register(Supplier)


