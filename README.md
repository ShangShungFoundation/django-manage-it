#django-it-manager

##Basic App Suite for IT Management for small business


###Assets Inventory App

* Create asset templates to allow for easier adding of individual items of the same kind.
* Ability to retire & reactivate inventory assets.
* Assign assets to one or more users.
* Asets may have different owners.
* Freely defined properties for each asset class.
* User defined locations (with precise position). 
* Search utility
* Export of invetory (or subset definde by search) to Exell document

###Asset Provision Management App

* Tightly integrated with Assets Inventory app.
* Comprehensive view on Network topology
* Network topology graph visualization
* Graph visualization is automatic (doesn't require intervention)
* Quick view for: location, state, owner
* Info about each device can be easily access and edited

###Network Management App

* Tigtly integrated with Assets Inventory app.
* Comprehensive view on Network toopology
* Broad definition of network devices: Network concetions can 
* Automatic Network toopology graph visualization (doesnt require intervetion)
* Quick view for: location, state, owner
* Info about each device can be easly accesse and eddited

###Incident Management App

* Tightly integrated with Assets Inventory app.
* Incident submission
* Automatic evaluation of incident priority based on impact and urgency metrics
* Incident Follow Up - keep track of all changes of state and observations following incident
* Email alerts for change of status of incident

Installing
----------
Assuming that you got virtualenv (python virtual envirement) created and activated.

Install via pip:

    pip install -e git+git@github.com:ShangShungInstitute/django-it-manager.git#egg=it-manager

In "INSTALLED_APPS" in settings.py file must be present:
    
    'dataforms',
    'catalog',
    'assets',
    'pagination',
    'incidents',
    'network',

Add to 'urlpatterns' (at the end) urls.py file:
    
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', "inventory.views.dashboard"),
    url(r'^catalog/', include("catalog.urls")),
    url(r'^assets/', include("assets.urls")),
    url(r'^network/', include("network.urls")),
    url(r'^incidents/', include("incidents.urls")),
    
Create tables etc.:

    python manage.py syncdb

#TODO

* [ ] Organizations
* [ ] User permisions
* [ ] Custom defined workflkows (asset provission)

#LICENSE

#Author
Kamil Selwa selwak@gmail.com

