# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import Group

from settings import GROUP_ROLES, URL_DELIMITER


class GroupNotDefined(Exception):
    """You must assing incident_notification_group in admin panell."""
    pass


class GroupError(Exception):
    """
    Group not assigned
    """
    pass


class Organization(models.Model):
    #TODO: Contact, extension
    name = models.CharField(_(u'name'), max_length=200, )
    description = models.TextField(
        _(u"description"),
        null=True, blank=True)
    slug = models.SlugField(
        _(u'slug'),
        max_length=200, unique=False,
        help_text="""Organization acronym should be used. \
        Pelase use only low dashes. \
        Must be unique for main organization""")

    url = models.CharField(
        _('URL'),
        unique=True,
        blank=True, null=True,
        max_length=100, db_index=True)

    parent = models.ForeignKey(
        "Organization",
        verbose_name=_("parent organization"),
        related_name='divisions',
        null=True, blank=True)

    phone_number1 = models.CharField(max_length=32, null=True, blank=True, )
    phone_number2 = models.CharField(max_length=32, null=True, blank=True, )

    email = models.EmailField(null=True, blank=True)

    manager = models.CharField(
        _("manager"),
        max_length=32, null=True, blank=True)

    groups = models.ManyToManyField(Group, through='OrganizationGroup')

    staff_group = models.ForeignKey(
        Group,
        verbose_name=_("member group"),
        related_name="related_staff_groups")

    observations = models.TextField(_(u'observations'), null=True, blank=True,)

    class Meta:
        ordering = ['name']
        verbose_name = _(u"Organization")
        verbose_name_plural = _(u"Organizations")
        permissions = (
            ("can_manage_org", "Can manage Organization: create Organization, \
                change data, add / remove groups"),
            ("can_manage_assets", "Can manage Inventories"),
        )

    def save(self, *args, **kwargs):
        """TODO update parent url to propagate changes"""

        if self.parent_id:
            self.url = u"%s%s%s" % (self.parent.url, URL_DELIMITER, self.slug)
            # we must propagate slug change to all children
            for division in self.divisions.all():
                division.save()
        else:
            self.url = self.slug

        super(Organization, self).save(*args, **kwargs)

    #http://stackoverflow.com/questions/5229508/tree-structure-of-parent-child-relation-in-django-templates
    def as_tree(self):
        divisions = list(self.divisions.all())
        branch = bool(divisions)
        yield branch, self
        for child in divisions:
            for next in child.as_tree():
                yield next
        yield branch, None

    def full_name(self):
        return u"%s %s" % (self.parent, self.name)

    @staticmethod
    def get_urls(url):
        return url.split(URL_DELIMITER)

    def get_head_url(self, url):
        return self.get_urls(url)[0]

    def __unicode__(self):
        return self.name

    @property
    def head(self):
        if self.is_head:
            return self
        else:
            head_slug = self.get_urls(self.url)[0]
            return Organization.objects.get(slug=head_slug)

    # herachy methods
    @staticmethod
    def get_organization_urls_from_url(url):
        """
        returns organization from url string
        """
        slugs = url.split("-")
        urls = []
        for i, slug in enumerate(slugs):
            urls.append("-".join(slugs[:i-1*-1]))
        return urls

    def get_organizations_from_urls(self, urls):
        """
        returns organizations from urls list
        """
        return Organization.objects.filter(url__in=urls)

    def get_organizations(self, url=None):
        if not url:
            url = self.url
        organization_urls = self.get_organization_urls_from_url(url)
        organizations = self.get_organizations_from_urls(organization_urls)
        return organizations

    def get_descendants(self):
        """
        returns descendants of organization
        """
        return Organization.objects.filter(url__startswith="%s_" % self.url)

    @staticmethod
    def get_descendants_from_url(url):
        """
        returns descendants of organization
        """
        return Organization.objects.filter(url__startswith="%s_" % url)

    def get_whole_organization(self):
        if self.is_head():
            return self.get_descendants()
        else:
            return self.head.get_descendants()

    def get_parents(self):
        if self.parent:
            return self.parent, self.parent.get_parents()

    def ancestors(self):
        return self.get_parents()[:-1]

    def get_ancestors_property(self, prop):
        """gets properties from ancestors"""

        properties = []
        if self.parent:
            ancestors = self.ancestors()
            for ancestor in ancestors:
                properties.append(getattr(ancestor, prop, None))
        return properties

    def is_head(self):
        return not self.parent_id

    # user revelant
    def is_group_member(self, user, group_role):
        memeber = OrganizationGroup.objects.filter(
            role__exact=group_role,
            org=self,
            group__user=user)
        return memeber

    def is_user_manager(self, user):
        return self.is_group_member(user, "admin_group")

    def is_user_staff(self, user):
        return self.is_group_member(user, "staff_group")

    def is_user_acountant(self, user):
        return self.is_group_member(user, "acounting_group")

    # group revelant
    def get_groups(self):
        return self.groups.all()

    def get_staff(self):
        return self.staff_group.user_set.all()

    @models.permalink
    def get_absolute_url(self):
        return ('organization', [self.url])


class OrganizationGroupManager(models.Manager):
    def get_org_staff_member(self, org, user):
        return self.queryset.filter(
            funk__exact=1,
            org=org,
            group__user=user)


class OrganizationGroup(models.Model):

    GROUP_ROLES = GROUP_ROLES

    #objects = OrganizationGroupManager()

    group = models.ForeignKey(
        Group,
        verbose_name=_("group"),
        related_name="related_organizations")
    org = models.ForeignKey(
        Organization,
        verbose_name=_("organization"),
        related_name="related_groups",
    )
    role = models.CharField(
        _(u"function"),
        max_length=100,
        choices=GROUP_ROLES)

    class Meta:
        unique_together = ('group', 'role',)
        permissions = (
            ("can_manage_group", "Can manage Group: Change name, add / remove users"),
        )

    def __unicode__(self):
        return u"%s" % self.group

    @models.permalink
    def get_absolute_url(self):
        return ("set_organization_group", [self.org, self.role])


def get_organization_groups(org):
    pass
