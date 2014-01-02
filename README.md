#django-manage-IT

##Basic App Suite for IT Management for organizations
 
IT tool belt implementing some of best practices for IT management. Is in early beta stage so there can be some "rough edges" but it is already useful.

Currently implemeted apps:

###Organization App
This app should reflect organization structure. Stucture can be horizontal or hierarchical with any number of related organization units.
Organization manages users and groups.
Groups gather users with special defined roles. App is necessary for granting user access to manage other application according to user roles.
Users may access only resources related with organization to which they belong ("Staff Group"). Users belonging to "Admin Group" may manage applications on their organization level and all organizations belonging to their organization. Same user may belong to diferent organizations and groups performing diferent roles. Its posible to create users who belong to given group and in the same time are not member of staff group (can be usefull for consultants, etc)

App allows:

* Create any hierarchy of organizations
* Create and manage users related with organization
* Create and manage groups related with IT roles
* Assign users to groups

###Assets Inventory App

* Supports multiple inventories for each organization
* Create asset templates to streamline adding of individual items belonging to the same model.
* Ability to retire & reactivate inventory assets.
* Assign assets to one or more users.
* Assets may have different owners.
* Asset records may have attached files with drivers, manulas, configuration documents etc
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
* Incident Follow Up - keep track of all changes of state and observations following incident
* Change of status of incident triggers email notifications


###Service Management App

* Based on concept of SLA (Service Level Agreement)
* Implements Service dependence
* Each service may have many SLAs with different providers
* SLA may contain few personalized classes of properties
* SLA may have attached files with contract, documentation, manuals etc

###Management Dashboard
Agregates metrics from other apps and displays comprehensive view on actual IT status. 

* Problematic Assets
* Pending Asset Requests
* Unresolved Incidents
* Incident Followup


Installing
----------
Assuming that you got virtualenv (python virtual retirement) created and activated.
Project has been tested againts Django 1.5

Install via pip:

    pip install -e git+git@github.com:ShangShungInstitute/django-it-manager.git#egg=manager-it

Install requirements:

    pip install -e requirements.txt

In "INSTALLED_APPS" in `manage_it/settings.py` file must be present:
```python
    # core apps
    'catalog',
    'assets',
    'incidents',
    'network',
    'services',
    'organizations',
    'notifications',

    # dependency apps
    'pagination',
    'dataforms',
```
Add to 'urlpatterns' in urls.py file:
```python
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
```
Create tables etc.:

    python manage.py syncdb

You may preload dataforms with forms for assets and services:

    python manage.py dataload initial_data.json

Settings
--------
You can personalize follwing setttings in `manage_it/settings.py`:

`ORG_RESPONSE_MATRIX` defines deadlines for incident resolution. Numeric key relates to `PRIORITY_GRADES`, position in tuple relates to `USERS_TYPES`. 
```python
ORG_RESPONSE_MATRIX = dict(
    _1=({min: 30}, {min: 30}, {min: 30, "perma": True}),
    _2=({"hours": 1}, {"hours": 1}, {min: 30, "perma": True}),
    _3=({"hours": 4}, {"hours": 2}, {"hours": 1, "perma": True}),
    _4=({"days": 2}, {"days": 1}, {"hours": 2}),
    _5=({"days": 5}, {"days": 2}, {"days": 2}),
)

ORG_STATUSES = (
    (1, "open"),
    (2, "in work"),
    (3, "closed"),
    (4, "defunkt"),
    (5, "duplicate"),
)

ORG_SERVICE_TYPES = (
    (1, _("Communications")),
    (2, _("Security")),
    (3, _("Servers, Data, Backup")),
    (4, _("Software & Business Applications")),
    (5, _("Web & Collaboration")),
    (6, _("Email & Collaboration")),
)
```
#TODO
Not in order of importance or priority

* [*] Implement Organizations
* [*] User permissions
* [ ] Documentation for users, managers and administrators
* [ ] Login with OAuth
* [*] Relate network connection to inventory
* [ ] Integrate services to incident managent app so incidents can reffer to services
* [ ] Build user interace to create and edit network interfaces in network app
* [ ] Build user interace to create and edit connections in network app
* [ ] Billing against recurrent services, assets etc
* [ ] Trigerring notifications on custom defined conditions and events
* [ ] Network monitoring
* [ ] Refactor Organization as separate project
* [ ] Refactor Location as separate project
* [ ] Multilingual support
* [ ] Logging
* [ ] Auditing 
* [ ] Custom defined workflows for provisions. incident management etc

#Licence
```
The MIT License (MIT)

Copyright (c) 2013 Kamil Selwa

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
```

#Author
Kamil Selwa selwak@gmail.com
