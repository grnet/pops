import json
import rrdtool
import time

from django.db.models import Avg, Min, Max
from django.core.urlresolvers import reverse
from django.conf import settings
from django.shortcuts import get_object_or_404

from network.models import City, Location, Ifce
import gevent


institutions = {
    'GRNET_DC': 'GRNET Datacenter',
    'COMMERCIAL_FACILITY': 'Comercial Colocation Facility',
    'OTHER': False,
}

images = {
    'GRNET_DC:ACCESS_L2': 'grnet-access-l2',
    'GRNET_DC:ACCESS_OPTICAL': 'grnet-access-optical',
    'GRNET_DC:CORE': 'grnet-core',
    'GRNET_DC:DISTRIBUTION': 'grnet-distribution',
    'GRNET_DC:PASS-THROUGH': 'pass-through',
    'COMMERCIAL_FACILITY:CORE': 'commercial-core',
    'COMMERCIAL_FACILITY:DISTRIBUTION': 'commercial-distribution',
    'COMMERCIAL_FACILITY:PASS-THROUGH': 'pass-through',
    'COMMERCIAL_FACILITY:ACCESS_L2': 'commercial-access-l2',
    'COMMERCIAL_FACILITY:ACCESS_OPTICAL': 'commercial-access-optical',
    'UNI:ACCESS_L2': 'customer-access-l2',
    'UNI:ACCESS_OPTICAL': 'customer-access-optical',
    'UNI:CUSTOMER': 'customer2',
    'UNI:CORE': 'customer-core',
    'UNI:DISTRIBUTION': 'customer-distribution',
    'UNI:PASS-THROUGH': 'pass-through',
    'OTHER': 'unknown'
}

type_dict = {
    'ACCESS_L2': 'Access (L2)',
    'ACCESS_OPTICAL': 'Access (Optical)',
    'CORE': 'GRNET Core',
    'DISTRIBUTION': 'Distribution',
    'PASS-THROUGH': 'Pass Trough',
    'CUSTOMER': 'Member'
}


def get_edges_of_map():
    # set the edges of the screen
    maxlat = -90.0
    minlat = 90.0
    maxlng = -180.0
    minlng = 180.0
    return (maxlat, minlat, maxlng, minlng)


def get_all_pops(url, tag=None):
    maxlat, minlat, maxlng, minlng = get_edges_of_map()
    coords = {}
    parents = City.objects.all().select_related('location_set')
    response = []
    for parent in parents:
        if not parent.name:
            continue
        children = parent.location_set.filter(geo_lat__gt=0)
        if tag:
            children = children.filter(peersite__peer_id__peer_tag__icontains=tag)
        if not children:
            continue
        resp = {}
        resp = children.aggregate(geolat=Avg('geo_lat'), geolng=Avg('geo_lng'))
        resp['name'] = parent.name
        resp['locations'] = len(children)
        resp['url'] = reverse('api:pops', args=(parent.name,))
        has_children = False
        for child in children:
            nodes = child.node_set.count()
            peer_sites = child.peersite_set.filter(peer_id__valid=True)
            if not nodes and not peer_sites:
                continue
            has_children = True
            # set the edges of the screen
            if child.geo_lat > maxlat:
                maxlat = child.geo_lat
            if child.geo_lat < minlat:
                minlat = child.geo_lat
            if child.geo_lng > maxlng:
                maxlng = child.geo_lng
            if child.geo_lng < minlng:
                minlng = child.geo_lng
            coords['maxlat'] = maxlat
            coords['minlat'] = minlat
            coords['maxlng'] = maxlng
            coords['minlng'] = minlng
        if has_children:
            response.append(resp)
    return json.dumps(
        {'url': url, 'pins': response, 'coords': coords, 'tag': tag}
    )


def sites_connected_through(site):
    result = []
    for through_site in site.connects.all():
        peer_site_location = through_site.site.peer_site_location
        try:
            inst = peer_site_location.institution if peer_site_location.institution in institutions.keys() else 'UNI'
        except:
            continue
        image = '%s:%s' % (inst, peer_site_location.type)
        display_inst = institutions.get(peer_site_location.institution, 'OTHER') if peer_site_location.institution in institutions.keys() else 'hosted by GRNET member (%s)' % (peer_site_location.institution)
        result.append({
            'name': through_site.site.to_short_string(),
            'display_name': through_site.site.to_short_string(),
            'lat': peer_site_location.geo_lat,
            'lng': peer_site_location.geo_lng,
            'image': images.get(image) or images.get('OTHER'),
            'inst': inst,
            'institution': display_inst,
            'address': peer_site_location.address,
            'details_url': reverse('api:location', kwargs={'location': site.peer_site_location.name})
        })
    return result


def connects_through(site):
    result = []
    for through_site in site.is_connected_through.all():
        peer_site_location = through_site.through_site.peer_site_location
        inst = peer_site_location.institution if peer_site_location.institution in institutions.keys() else 'UNI'
        image = '%s:%s' % (inst, peer_site_location.type)
        display_inst = institutions.get(peer_site_location.institution, 'OTHER') if peer_site_location.institution in institutions.keys() else 'hosted by GRNET member (%s)' % (peer_site_location.institution)
        result.append({
            'name': through_site.site.to_short_string(),
            'display_name': through_site.site.to_short_string(),
            'lat': peer_site_location.geo_lat,
            'lng': peer_site_location.geo_lng,
            'image': images.get(image) or images.get('OTHER'),
            'inst': inst,
            'institution': display_inst,
            'address': peer_site_location.address,
            'details_url': reverse('api:location', kwargs={'location': site.peer_site_location.name})
        })
    return result


def location_details(location):
    in_this_location = []
    equipment = []
    parent = get_object_or_404(Location, name=location)
    connecting = []
    queryset = parent.peerifces_set.all()
    for peer_ifce in queryset:
        try:
            peer_ifce_location = peer_ifce.grnet_device_location
        except:
            continue
        inst = peer_ifce_location.institution if peer_ifce_location.institution in institutions.keys() else 'UNI'
        image = '%s:%s' % (inst, peer_ifce_location.type)
        display_inst = institutions.get(peer_ifce_location.institution, 'OTHER') if peer_ifce_location.institution in institutions.keys() else 'hosted by GRNET member (%s)' % (peer_ifce_location.institution)
        connecting.append({
            'name': peer_ifce.to_string(),
            'display_name': peer_ifce.to_string(),
            'lat': peer_ifce_location.geo_lat,
            'lng': peer_ifce_location.geo_lng,
            'image': images.get(image) or images.get('OTHER'),
            'inst': inst,
            'institution': display_inst,
            'address': peer_ifce_location.address,
            'details_url': reverse('api:location', kwargs={'location': peer_ifce_location.name})
        })
    for site in parent.peersite_set.all().select_related(
        'peer_id__properties',
        'connects'
    ):
        # Site name and sites through this site
        in_this_location.append({
            'name': site.to_string(),
            'through': sites_connected_through(site),
            'site_connects_through': connects_through(site)
        })
        # for each connection from this location
        if site.site_tag == 'MAIN':
            peer = site.peer_id
            queryset = peer.peerifces_set.filter(peer_site__isnull=True)
        else:
            queryset = site.peerifces_set.all()
        for peer_ifce in queryset:
            try:
                peer_ifce_location = peer_ifce.grnet_device_location
            except:
                continue
            inst = peer_ifce_location.institution if peer_ifce_location.institution in institutions.keys() else 'UNI'
            image = '%s:%s' % (inst, peer_ifce_location.type)
            display_inst = institutions.get(peer_ifce_location.institution, 'OTHER') if peer_ifce_location.institution in institutions.keys() else 'hosted by GRNET member (%s)' % (peer_ifce_location.institution)
            connecting.append({
                'name': peer_ifce.to_string(),
                'display_name': peer_ifce.to_string(),
                'lat': peer_ifce_location.geo_lat,
                'lng': peer_ifce_location.geo_lng,
                'image': images.get(image) or images.get('OTHER'),
                'inst': inst,
                'institution': display_inst,
                'address': peer_ifce_location.address,
                'details_url': reverse('api:location', kwargs={'location': peer_ifce_location.name})
            })
    # for each device in each location
    for node in parent.node_set.all().select_related('peer_site', 'peer_site__peer_id__properties'):
        connected_here = []
        interfaces = []
        try:
            node_dict = {'name': node.name}
        except:
            continue
        # for each connection to this device
        for peer_ifce in node.sites_directly_connected_here():
            peer_ifce_location = peer_ifce.get_site_location()
            if peer_ifce_location:
                inst = peer_ifce_location.institution if peer_ifce_location.institution in institutions.keys() else 'UNI'
                image = '%s:%s' % (inst, peer_ifce_location.type)
                display_inst = institutions.get(peer_ifce_location.institution, 'OTHER') if peer_ifce_location.institution in institutions.keys() else 'hosted by GRNET member (%s)' % (peer_ifce_location.institution)
                connected_here.append({
                    'name': peer_ifce.to_string(),
                    'display_name': peer_ifce.to_string(),
                    'lat': peer_ifce_location.geo_lat,
                    'lng': peer_ifce_location.geo_lng,
                    'image': images.get(image) or images.get('OTHER'),
                    'inst': inst,
                    'institution': display_inst,
                    'address': peer_ifce_location.address,
                    'details_url': reverse('api:location', kwargs={'location': peer_ifce_location.name})
                })
        node_dict.update({'connected_here': connected_here})
        for ifce in node.ifce_set.filter(local_ifce__isnull=False).select_related('local_ifce', 'remote_ifce', 'remote_ifce__node', 'remote_ifce__node__location'):
            for lifce in ifce.local_ifce.all():
                try:
                    remote_ifce_location = lifce.remote_ifce.node.location
                except:
                    continue
                if remote_ifce_location:
                    inst = remote_ifce_location.institution if remote_ifce_location.institution in institutions.keys() else 'UNI'
                    image = '%s:%s' % (inst, remote_ifce_location.type)
                    display_inst = institutions.get(remote_ifce_location.institution, 'OTHER') if remote_ifce_location.institution in institutions.keys() else 'hosted by GRNET member (%s)' % (remote_ifce_location.institution)
                    interfaces.append({
                        'name': lifce.remote_ifce.node.name,
                        'display_name': '%s <- %s' % (ifce.name, lifce.remote_hostname),
                        'lat': remote_ifce_location.geo_lat,
                        'lng': remote_ifce_location.geo_lng,
                        'address': remote_ifce_location.address,
                        'image': images.get(image) or images.get('OTHER'),
                        'inst': inst,
                        'institution': display_inst,
                        'details_url': reverse('api:location', kwargs={'location': remote_ifce_location.name})
                    })
            for lifce in ifce.remote_ifce.all():
                try:
                    remote_ifce_location = lifce.remote_ifce.node.location
                except:
                    continue
                if remote_ifce_location:
                    inst = remote_ifce_location.institution if remote_ifce_location.institution in institutions.keys() else 'UNI'
                    image = '%s:%s' % (inst, remote_ifce_location.type)
                    display_inst = institutions.get(remote_ifce_location.institution, 'OTHER') if remote_ifce_location.institution in institutions.keys() else 'hosted by GRNET member (%s)' % (remote_ifce_location.institution)
                    interfaces.append({
                        'name': lifce.remote_ifce.node.name,
                        'display_name': '%s <- %s' % (ifce.name, lifce.remote_hostname),
                        'lat': remote_ifce_location.geo_lat,
                        'lng': remote_ifce_location.geo_lng,
                        'address': remote_ifce_location.address,
                        'image': images.get(image) or images.get('OTHER'),
                        'inst': inst,
                        'institution': display_inst,
                        'details_url': reverse('api:location', kwargs={'location': remote_ifce_location.name})
                    })
            node_dict.update({'ifces': interfaces})
        equipment.append(node_dict)
    inst = parent.institution if parent.institution in institutions.keys() else 'UNI'
    display_inst = institutions.get(parent.institution, 'OTHER') if parent.institution in institutions.keys() else 'hosted by GRNET member (%s)' % (parent.institution)
    image = '%s:%s' % (inst, parent.type)
    return {
        'name': parent.name,
        'display_type': type_dict.get(parent.type, 'OTHER'),
        'type': parent.type,
        'institution': display_inst,
        'inst': inst,
        'address': parent.address,
        'members_in_this_location': in_this_location,
        'equipment': equipment,
        'lat': parent.geo_lat,
        'lng': parent.geo_lng,
        'location': '%s: %s' % (inst, parent.type),
        'image': images.get(image) or images.get('OTHER'),
        'connecting': connecting or None
    }


def get_pops_by_city(city, url, tag=None):
    maxlat, minlat, maxlng, minlng = get_edges_of_map()
    # Getting all locations of city
    parents = Location.objects.filter(city=city).filter(geo_lat__gt=0).select_related(
        'city', 'node_set', 'peersite_set', 'peerifces_set'
    )
    if tag:
        parents = parents.filter(peersite__peer_id__peer_tag__icontains=tag)
    coords = parents.aggregate(
        maxlat=Max('geo_lat'),
        maxlng=Max('geo_lng'),
        minlat=Min('geo_lat'),
        minlng=Min('geo_lng')
    )
    response = []
    # for each location
    for parent in parents:
        if not parent.name:
            continue
        inst = parent.institution if parent.institution in institutions.keys() else 'UNI'
        display_inst = institutions.get(parent.institution, 'OTHER') if parent.institution in institutions.keys() else 'hosted by GRNET member (%s)' % (parent.institution)
        image = '%s:%s' % (inst, parent.type)
        resp = {
            'name': parent.name,
            'display_type': type_dict.get(parent.type, 'OTHER'),
            'type': parent.type,
            'institution': display_inst,
            'inst': inst,
            'address': parent.address,
            'lat': parent.geo_lat,
            'lng': parent.geo_lng,
            'image': images.get(image) or images.get('OTHER'),
            'details_url': reverse('api:location', kwargs={'location': parent.name})
        }
        response.append(resp)
    return json.dumps({'url': url, 'pins': response, 'coords': coords, 'city': city})


def last_x_rec(x):
    return range(2, x + 1)
