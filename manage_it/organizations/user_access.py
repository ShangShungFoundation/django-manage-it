
import logging
from functools import wraps

from django.shortcuts import redirect
from django.utils.decorators import available_attrs

from models import Organization, OrganizationGroup

logger = logging.getLogger('django.request')

REDIRECT_URL = "/"
#https://github.com/django/django/blob/master/django/views/decorators/http.py#L31
def required_member(parameter):
    """
    possible paramenters are numerical
    """

    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def inner(request, *args, **kwargs):
            if 'org_url' in kwargs:
                org_url = kwargs["org_url"]
            else:
                org_url = request.path.split("/")[1]
            try:
                request.organization = Organization.objects.get(url=org_url)
            except:
                return redirect(REDIRECT_URL)
            valid_member = OrganizationGroup.objects.filter(
                role__exact=parameter,
                org=request.organization,
                group__user=request.user)
            if valid_member or request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            else:
                return redirect(REDIRECT_URL)
        return inner
    return decorator

manager_required = required_member(2)
manager_required.__doc__ = """Decorator to require that a view \
only accept members belonging to organization maneger group"""

staff_required = required_member(1)
staff_required.__doc__ = "Decorator to require that a view only \
accept members belonging to organization"

acountant_required = required_member(3)
acountant_required.__doc__ = "Decorator to require that a view \
only accept members belonging to organization acounting group"
