from django.conf.urls import patterns, url

urlpatterns = patterns('organizations.views',
    url(r'^$',
        "view_organization", name='organization'),
    url(r'^user/(?P<user_id>\d+)/$',
        "view_user", name='view_user'),
    url(r'^user/new/$',
        "new_user", name='new_user'),
    url(r'^user/edit/(?P<user_id>\d+)/$',
        "edit_user", name='edit_user'),
    url(r'^new/$',
        "new_organization", name='new_organization'),
    url(r'^(?P<group_role>.+)/$',
        "set_organization_group", name='set_organization_group'),
)
