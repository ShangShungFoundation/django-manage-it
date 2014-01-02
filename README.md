#django-manage-IT

##Basic App Suite for IT Management for organizations
 
IT tool belt implementing best practices. Out of the box supports multiple flat or hierarchical organizations. Each organization can have difrent users with defined roles. Same user may belong to diferent organizations performing diferent roles.

Management Dashboard with most urgent metrics of IT situation like: 
* Problematic Assets
* Pending Asset Requests
* Unresolved Incidents
* Incident Followup

###Organization App
This app should reflect organization structure. It manages users and groups.
Groups gather users with special defined roles. This app is necessary also for granting user access to manage other application according to their roles.
Users may access only resources related with organization to which they belong ("Staff Group"). Users belonging to "Admin Group" may manage applications on their organization level and all organizations subscribed to their organization.

* Create any hierarchy of organizations
* Create and manage users related with organization
* Create and manage groups related with IT roles
* Assign users to groups

###Assets Inventory App

* Multiple inventories for each organization
* Create asset templates to allow for easier adding of individual items of the same kind.
* Ability to retire & reactivate inventory assets.
* Assign assets to one or more users.
* Assets may have different owners.
* Freely defined properties for each asset class.
* User defined locations (with precise geographic position). 
* Search utility
* Export of inventory (or subset defined by search) to Exell file

###Asset Provision Management App

* Tightly integrated with Assets Inventory app.
* Petition Submission for new asset or replacement of defectous one
* Petition Management 
* Email alerts for change of status of petition

###Network Management App

* Tightly integrated with Assets Inventory app.
* Broad definition of network devices (connections can be even USB), so all peripheral devices can be mapped
* Automatic Network topology graph visualization (doesn't require intervention)
* Quick view for: location, state, owner
* Info about each device can be easily access and edited

###Incident Management App

* Automatic incident priority evaluation based on urgency and impact metrics
* Automatic incident resolution deadline evaluation based on user status
* Tightly integrated with Assets Inventory app.
* Incident submission 
* Automatic evaluation of incident priority based on impact and urgency metrics
* Incident Follow Up - keep track of all changes of state and observations following incident
* Change of status of incident triggers email notifications


###Service Management App

* Based on concept of SLA (Service Level Agreement)
* Service dependence
* Each service may have many SLAs with different providers
* SLA may contain few personalized classes of properties
* SLA may have attached files with contract, documentation, manuals etc

Installing
----------
Assuming that you got virtualenv (python virtual retirement) created and activated.
Project has been tested againts Django 1.5

Install via pip:

    pip install -e git+git@github.com:ShangShungInstitute/django-it-manager.git#egg=manager-it

Install requirements:

    pip install -e requirements.txt

In "INSTALLED_APPS" in settings.py file must be present:
    
    # core apps
    'catalog',
    'assets',
    'pagination',
    'incidents',
    'network',
    'services',
    'organizations',
    'notifications',

    # dependency apps
    'dataforms',
    'debug_toolbar',

Add to 'urlpatterns' in urls.py file:
    
    ORG_URL = "(?P<org_url>.+)/"
    
    url(r'^$',
        "organizations.views.list_organizations", name='home'),
    url(r'^admin/',
        include(admin.site.urls)),
    url(r'^%sdashboard/' % ORG_URL,
        "manage_it.views.dashboard", name='dashboard'),
    url(r'^%sinventory/' % ORG_URL,
        include("catalog.urls")),
    url(r'^%sassets/' % ORG_URL,
        include("assets.urls")),
    url(r'^network/',
        include("network.urls")),
    url(r'^%sincidents/' % ORG_URL,
        include("incidents.urls")),
    url(r'^%sservices/' % ORG_URL,
        include('services.urls')),
    url(r'^%sorganization/' % ORG_URL,
        include('organizations.urls')),
    
Create tables etc.:

    python manage.py syncdb

Settings
--------

#TODO
Not in order of importance or priority

* [*] Implement Organizations
* [*] User permissions
* [ ] Documentation for users and managers
* [*] Relate network connection to inventory
* [ ] Build user interace to create and edit network intrfaces in network app
* [ ] Build user interace to create and edit connections in network app
* [ ] Billing
* [ ] Network monitoring
* [ ] Refactor Organization as separate project
* [ ] Refactor Location as separate project
* [ ] Multilingual support
* [ ] Logging
* [ ] Auditing 
* [ ] Custom defined workflows for provisions. incident management etc

#LICENSE

#Author
Kamil Selwa selwak@gmail.com