
import logging
from functools import wraps

from django.shortcuts import redirect
from django.utils.decorators import available_attrs

from models import Organization, OrganizationGroup

logger = logging.getLogger('django.request')

from settings import REDIRECT_URL


#https://github.com/django/django/blob/master/django/views/decorators/http.py#L31

def get_user_groups(org, usr):
    user_groups = OrganizationGroup.objects.filter(
        org=org,
        group__user=usr)
    return user_groups


def required_member(parameter=None):
    """
    Possible paramenters are defined by roles groups slugs \
    in OrganizationGroup.
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

            user_groups = get_user_groups(request.organization, request.user)
            user_roles = user_groups.values_list("role")
            request.user.roles = user_roles

            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            if user_roles and not parameter:
                # is memaber of any group
                return view_func(request, *args, **kwargs)
            if user_roles and parameter in user_roles:
                return view_func(request, *args, **kwargs)
            return redirect(REDIRECT_URL)
        return inner
    return decorator

manager_required = required_member("admin_group")
manager_required.__doc__ = """Decorator to require that a view \
only accept members belonging to organization maneger group"""

staff_required = required_member("staff_group")
staff_required.__doc__ = "Decorator to require that a view only \
accept members belonging to organization"

acountant_required = required_member("accounting_group")
acountant_required.__doc__ = "Decorator to require that a view \
only accept members belonging to organization acounting group"
