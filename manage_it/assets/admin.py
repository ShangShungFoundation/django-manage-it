from django.contrib import admin

from assets.models import State, ItemState, Item, Person, Resource


class ItemAdmin(admin.ModelAdmin):
    #list_display = ("property_number", "id", 'item_template', 'item_class', 'owner', 'location', 'state', 'active', )
    list_filter = ['item_class', 'location', 'state', 'inventory']
    search_fields = ['property_number', 'item_template__description']

admin.site.register(State)
admin.site.register(ItemState)
admin.site.register(Item, ItemAdmin)
admin.site.register(Person)
admin.site.register(Resource)
