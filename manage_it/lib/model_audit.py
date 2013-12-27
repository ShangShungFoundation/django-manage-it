# -*- coding: utf-8 -*-
import datetime

from django.db import models
from django.contrib.auth.models import User


class AuditMixin(object):
    """
    Audit Mixin
    """
    created_at = models.DateTimeField(default=datetime.datetime.now())
    created_by = models.ForeignKey(User)
