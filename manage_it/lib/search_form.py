# -*- coding: UTF-8 -*-
import urllib
 
 
# http://www.julienphalip.com/blog/2008/08/16/addng-search-django-site-snap/
# http://www.nomadjourney.com/2009/04/dynamic-django-queries-with-kwargs/
def search(request, SearchForm, queryset, search_method='GET', allow_empty=True, *args, **kwargs):
    """
    search-form built from model
    """
    new_data = {}
    
    # HACK to eliminate 'ManagementForm data is missing or has been tampered with' error
    if len(request.GET) == 1 and request.GET.get(u'page', None):
	request_query = {}
    else:
	request_query = request.GET
    form = SearchForm(request_query or None)
    
    if request.method.upper() == search_method:
        
        new_data = request_query.copy()
        q_args = {}

        if hasattr(form, "fields"):
	    fields = form.fields
        else:
	    fields = form.extra_forms[0].fields
	for i in new_data:
            e = i[11:]
            if e in fields and new_data[i] != '':
                if hasattr(fields[e], 'queryset'):
                    q_args[str('%s__id' % e)] = new_data[i]
                    #q = Q( **{ e + '__id' : new_data[e]} )
                else:
                    q_args[str('%s__exact' % e)] = new_data[i]
                    #q = Q( **{ e+ '__exact' : new_data[e] }  )

        queryset = queryset.filter(**q_args) 
    
    return dict(
        query=urllib.urlencode(new_data),
        queryset=queryset,
        search_form=form,
    )
