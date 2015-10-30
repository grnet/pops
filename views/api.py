# -*- coding: utf-8 -*- vim:encoding=utf-8:
import json
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from network.models import PeerIfces, PeerSite, Location
from utils import (
    get_all_pops,
    get_pops_by_city,
    location_details,
)


def peer_ifces(request, peer_id):
    ifces = PeerIfces.objects.filter(peer__peer_id=peer_id)
    response = []
    for ifce in ifces:
        response.append(ifce.to_dict())
    json_str = json.dumps(response)
    return HttpResponse(
        json_str,
        mimetype='application/json',
        content_type='application/json; charset=utf-8'
    )


def site_devices(request, site_id):
    site = PeerSite.objects.get(pk=site_id)
    if site.peer_id.peer_tag == 'GRNET':
        ifces = PeerIfces.objects.filter(grnet_device_location=site.peer_site_location)
    else:
        ifces = PeerIfces.objects.filter(peer_site__site_id=site_id).order_by('name')
    response = []
    for ifce in ifces:
        found = False
        for r in response:
            if r.get('name') == ifce.name.name:
                r.get('ifces').append(ifce.to_node_dict())
                found = True
        if not found:
            # a = ifce.name.ifce_set.all()[0].description
            if ifce.get_site_location() == ifce.name.location:
                role = 'CPE'
            else:
                role = 'PE'
            response.append({
                'name': ifce.name.name,
                'ifces': [ifce.to_node_dict()],
                # as andreas about that
                'free_ports': [interface.name for interface in ifce.name.ifce_set.filter(description='', status='free')],
                # colocated or not
                'role': role,
                'id': ifce.name.pk
            })
    # testing ifces
    if site_id == '904':
        response.extend([{
            'id': 99999,
            'free_ports': [],
            'role': 'CPE',
            'name': 'lab-ex1.grnet.gr',
            'ifces': [{
                'description': 'test',
                'ifce': 'ge-0/0/0.0',
                "bandwidth": 1000000000,
                "vlans": [
                ],
                "type": "Unknown",
                "id": 999999
            }]
        }])
        response.extend([{
            'id': 999999,
            'free_ports': [],
            'role': 'CPE',
            'name': 'lab-mx1.grnet.gr',
            'ifces': [{
                'description': 'test',
                'ifce': 'ge-1/0/0',
                "bandwidth": 1000000000,
                "vlans": [
                ],
                "type": "Unknown",
                "id": 9999999
            }]
        }])
    elif site_id == '902':
        response.extend([{
            'id': 999999,
            'free_ports': [],
            'role': 'CPE',
            'name': 'lab-ex2.grnet.gr',
            'ifces': [{
                'description': 'test2',
                'ifce': 'ge-0/0/1.0',
                "bandwidth": 1000000000,
                "vlans": [
                ],
                "type": "Unknown",
                "id": 9999909
            }]
        }])
        response.extend([{
            'id': 99999999,
            'free_ports': [],
            'role': 'CPE',
            'name': 'lab-mx2.grnet.gr',
            'ifces': [{
                'description': 'test',
                'ifce': 'ge-1/0/6',
                "bandwidth": 1000000000,
                "vlans": [
                ],
                "type": "Unknown",
                "id": 999999999
            }]
        }])
    json_str = json.dumps(response)
    return HttpResponse(
        json_str,
        mimetype='application/json',
        content_type='application/json; charset=utf-8'
    )


def peer_devices(request, peer_id):
    # dummy DONT COMMIT
    if peer_id in ['998', '999']:
        if peer_id == '998':
            response = [{
                'lab-mx1.grnet.gr ': {
                    'id': 998,
                    'role': 'PE',
                    'ifces': [
                        {
                            'bandwidth': 1000000000,
                            'vlans': [],
                            'port_type': 'SFP-LX',
                            'ifce': 'ge-1/1/8',
                            'description': '[CUSTA@LOCA-1]'
                        }
                    ],
                    'free_ports': [],
                },
                'lab-mx2.grnet.gr ': {
                    'id': 998,
                    'role': 'PE',
                    'ifces': [
                        {
                            'bandwidth': 1000000000,
                            'vlans': [],
                            'port_type': 'SFP-LX',
                            'ifce': 'ge-1/1/8',
                            'description': '[CUSTA@LOCB-1]'
                        }
                    ],
                    'free_ports': [],
                },

            }]
        else:
            response = [{
                'lab-ex1.grnet.gr ': {
                    'id': 999,
                    'role': 'CE',
                    'ifces': [
                        {
                            'bandwidth': 1000000000,
                            'vlans': [],
                            'port_type': 'UTP',
                            'ifce': 'ge-1/1/18',
                            'description': '[CUSTB@LOCA-1]'
                        }
                    ],
                    'free_ports': [],
                },
                'lab-ex2.grnet.gr ': {
                    'id': 999,
                    'role': 'CE',
                    'ifces': [
                        {
                            'bandwidth': 1000000000,
                            'vlans': [],
                            'port_type': 'UTP',
                            'ifce': 'ge-1/1/18',
                            'description': '[CUSTB@LOCB-1]'
                        }
                    ],
                    'free_ports': [],
                },

            }]
    else:
        ifces = PeerIfces.objects.filter(peer__peer_id=peer_id).order_by('name')
        response = []
        for ifce in ifces:
            found = False
            for r in response:
                if r.get('name') == ifce.name.name:
                    r.get('ifces').append(ifce.to_node_dict())
                    found = True
            if not found:
                # a = ifce.name.ifce_set.all()[0].description
                if ifce.get_site_location() == ifce.name.location:
                    role = 'CPE'
                else:
                    role = 'PE'
                response.append({
                    'name': ifce.name.name,
                    'ifces': [ifce.to_node_dict()],
                    # as andreas about that
                    'free_ports': [interface.name for interface in ifce.name.ifce_set.filter(description='', status='free')],
                    # colocated or not
                    'role': role,
                    'id': ifce.name.pk
                })
    json_str = json.dumps(response)
    return HttpResponse(
        json_str,
        mimetype='application/json',
        content_type='application/json; charset=utf-8'
    )


def pops(request, city=None):
    tag = request.GET.get('tag')
    if tag:
        tag = tag.split('?')[0]
    if city:
        url = reverse('api:pops', args=(city,))
        json_str = get_pops_by_city(city, url, tag)
    else:
        url = reverse('api:pops')
        json_str = get_all_pops(url, tag)
    return HttpResponse(
        json_str,
        mimetype='application/json',
        content_type='application/json; charset=utf-8'
    )


def location(request, location=None):
    if location:
        return HttpResponse(
            json.dumps(location_details(location)),
            mimetype='application/json',
            content_type='application/json; charset=utf-8'
        )
    else:
        result = []
        for l in Location.objects.all():
            result.append({
                'id': l.location_id,
                'name': l.name,
                'address': l.address,
            })
        return HttpResponse(
            json.dumps(result),
            mimetype='application/json',
            content_type='application/json; charset=utf-8'
        )


