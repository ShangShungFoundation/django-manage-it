# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _


class HerarchyBase(object):

	def get_descendants(self):
        """
        returns descendants of organization
        """
        return Organization.objects.filter(url__startswith="%s_" % self.url)