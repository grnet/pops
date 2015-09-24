from django.shortcuts import render
from django.http import Http404
from django.core.urlresolvers import reverse, NoReverseMatch


# view should be the name of the url from the rest api
def map_view(request, view='default', city=None, location=None):
    if view:
        try:
            if city:
                if location:
                    url = reverse('api:' + view, args=(city, location,))
                else:
                    url = reverse('api:' + view, args=(city,))
            else:
                url = reverse('api:' + view)
        except NoReverseMatch:
            raise Http404
    if request.GET.get('tag'):
        return render(request, 'pops/map.html', {'view': '%s?tag=%s' % (url, request.GET.get('tag')), 'filter': request.GET.get('tag')})
    else:
        return render(request, 'pops/map.html', {'view': url})
