from organizations.models import Organization


class OrganizationMiddleware(object):
    def process_request(self, request):
        org_url = request.path.split("/")[1]
        #import ipdb; ipdb.set_trace()
        try:
            request.organization = Organization.objects.get(url=org_url)
        except:
            request.organization = None
