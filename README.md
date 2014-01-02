#django-manage-IT

##Basic App Suite for IT Management for organizations
 
IT toolbelt implementing best practices. Out of the box support flat and herachical multiple organizations. Each organization can have difrent users with defined roles.
Main function for organization app is managin user access and capacity to manage difrent resorces as: assests, services etc.

Includes Management Dashboard with most urgent metrics of IT situation like: 
* Problematic Assets
* Pending Asset Requests
* Unresolved Incidents
* Incident Followup

###Organization App

* Create any hierarchy of organizations
* Create and manage users related with organization
* Create and manage groups related with IT roles
* Asign users to groups

###Assets Inventory App

* Multiple inventories for each organization
* Create asset templates to allow for easier adding of individual items of the same kind.
* Ability to retire & reactivate inventory assets.
* Assign assets to one or more users.
* Asets may have different owners.
* Freely defined properties for each asset class.
* User defined locations (with precise geografic position). 
* Search utility
* Export of invetory (or subset defined by search) to Exell document

###Asset Provision Management App

* Tightly integrated with Assets Inventory app.
* Petition Submission for new asset or replacement of defectous one
* Petition Management 
* Email alerts for change of status of petition

###Network Management App

* Tightly integrated with Assets Inventory app.
* Broad definition of network devices (conections can be even USB), so all peripherial devices can be maped
* Automatic Network topology graph visualization (doesn't require intervetion)
* Quick view for: location, state, owner
* Info about each device can be easly accesse and eddited

###Incident Management App

* Automatic incident priority evaluation based on urgency and impact metrics
* Automatic incident resolution deadline evaluation based on user status
* Tightly integrated with Assets Inventory app.
* Incident submission 
* Automatic evaluation of incident priority based on impact and urgency metrics
* Incident Follow Up - keep track of all changes of state and observations following incident
* Change of status of incident triggers email natifications


###Service Management App

* Based on concept of SLA (Service Level Agreement)
* Service dependance
* Each service may have many SLAs with diferent providers
* SLA may contain few personalizad classes of properties
* SLA may have attached files with contract, documentation, manuals etc

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
Not in order of importance or priority

* [*] Implement Organizations
* [*] User permisions
* [ ] Billing
* [ ] Network monitoring
* [ ] Refactor Organization as separate Project
* [ ] Refactor Location as separate project
* [ ] Multilanguage support
* [ ] Logging
* [ ] Auditing 
* [ ] Custom defined workflkows for provisions. incident management etc

#LICENSE

#Author
Kamil Selwa selwak@gmail.com

