# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.conf import settings


ORG_RESPONSE_MATRIX = dict(
    _1=({min: 30}, {min: 30}, {min: 30, "perma": True}),
    _2=({"hours": 1}, {"hours": 1}, {min: 30, "perma": True}),
    _3=({"hours": 4}, {"hours": 2}, {"hours": 1, "perma": True}),
    _4=({"days": 2}, {"days": 1}, {"hours": 2}),
    _5=({"days": 5}, {"days": 2}, {"days": 2}),
)

RESPONSE_MATRIX = getattr(settings, "ORG_RESPONSE_MATRIX", ORG_RESPONSE_MATRIX)

ORG_STATUSES = (
    (1, _("open")),
    (2, _("in work")),
    (3, _("closed")),
    (4, _("defunkt")),
    (5, _("duplicate")),
)

STATUSES = getattr(settings, "ORG_STATUSES", ORG_STATUSES)
