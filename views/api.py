# -*- coding: utf-8 -*- vim:encoding=utf-8:
import json
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from network.models import PeerIfces, PeerSite, Location, Ifce, Peer
from utils import (
    get_all_pops,
    get_pops_by_city,
    location_details,
)


def peer_ifces(request, peer_id):
    ifces = PeerIfces.objects.filter(peer__peer_id=peer_id)
    peer = get_object_or_404(Peer, peer_id=peer_id)
    response = []

    for ifce in ifces:
        response.append(ifce.to_dict())

    ifces = Ifce.objects.filter(description__contains=peer.peer_tag).exclude(name__contains='.')
    for ifce in ifces:
        # ingore invalid ifces
        try:
            ifce.tagged_ifce
        except:
            continue
        else:
            response.append({
                'node': ifce.node.name,
                'ifce': ifce.name,
                'site': ifce.description.split('[')[1].split('-')[0]
            })

    json_str = json.dumps(list({v['ifce']: v for v in response}.values()))
    return HttpResponse(
        json_str,
        mimetype='application/json',
        content_type='application/json; charset=utf-8'
    )


def site_devices(request, site_id):
    try:
        site = PeerSite.objects.get(pk=site_id)
    except:
        site = None
    if site:
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
                'type': 'switch' if ifce.name.is_switch else 'router',
                # as andreas about that
                'free_ports': [{
                    'name': interface.name,
                    'bandwidth': interface.bandwidth,
                    'type': interface.ifcetype.get_type(),
                    'id': interface.pk
                } for interface in ifce.name.ifce_set.filter(
                    taggedifce__isnull=True, status='down'
                ).exclude(name__contains='.').exclude(
                    name__contains='ae'
                ).exclude(ifcetype__isnull=True)
                ],
                # colocated or not
                'role': role,
                'id': ifce.name.pk
            })
    # EXTRA CHECK
    fallback_ifces = Ifce.objects.filter(
        description__contains='%s%s' % (site.peer_id.peer_tag, '@%s' % site.site_tag if site.site_tag != 'MAIN' else '')
    ).exclude(name__contains='.')
    for ifce in fallback_ifces:
        found = False
        for r in response:
            if r.get('name') == ifce.node.name:
                r.get('ifces').append(ifce.to_node_dict())
                found = True
        if not found:
            # this is an access switch
            role = 'CPE'
            response.append({
                'name': ifce.node.name,
                'ifces': [ifce.to_node_dict()],
                'type': 'switch' if ifce.node.is_switch else 'router',
                'free_ports': [
                    {
                        'name': interface.name,
                        'bandwidth': interface.bandwidth,
                        'type': interface.ifcetype.get_type()
                    } for interface in ifce.node.ifce_set.filter(
                        taggedifce__isnull=True,
                        status='down',
                        ifcetype__isnull=False
                    ).exclude(
                        name__contains='.'
                    ).exclude(name__contains='ae')
                ],
                # colocated or not
                'role': role,
                'id': ifce.node.pk
            })
    # testing ifces
    if site_id == '904':
        response.extend([{
            'id': 99999,
            'free_ports': [{
                'name': 'ge-0/0/5',
                'bandwidth': 1000000000,
                'type': 'copper',
		"id": 999999
            }],
            'role': 'CPE',
            'name': 'lab-ex1.grnet.gr',
            'ifces': [{
                'description': 'test',
                'ifce': 'ge-0/0/0',
                "bandwidth": 1000000000,
                "vlans": [
                    100
                ],
                "type": "copper",
                "id": 999999
            }]
        }])
        response.extend([{
            'id': 999999,
            'free_ports': [],
            'role': 'PE',
            'name': 'lab-mx1.grnet.gr',
            'ifces': [{
                'description': 'test',
                'ifce': 'ge-1/0/5',
                "bandwidth": 1000000000,
                "vlans": [
                    100
                ],
                "type": "Unknown",
                "id": 9999999
            }]
        }])
    elif site_id == '902':
        response.extend([{
            'id': 999999,
            'free_ports': [{
		'name': 'ge-0/0/3',
                'bandwidth': 1000000000,
                'type': 'copper',
		'id': 999999
                }
            ],
            'role': 'CPE',
            'name': 'lab-ex2.grnet.gr',
            'ifces': [{
                'description': 'test2',
                'ifce': 'ge-0/0/1',
                "bandwidth": 1000000000,
                "vlans": [
                    100
                ],
                "type": "copper",
                "id": 9999909
            }]
        }])
        response.extend([{
            'id': 99999999,
            'free_ports': [],
            'role': 'PE',
            'name': 'lab-mx2.grnet.gr',
            'ifces': [{
                'description': 'test',
                'ifce': 'ge-1/0/8',
                "bandwidth": 1000000000,
                "vlans": [
                    100
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
