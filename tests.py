from django.test import TestCase
from django.test import Client

from django.core.urlresolvers import reverse


class ApiTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_api_urls(self):
        '''
        Check if api urls exist
        '''
        response = self.client.get(reverse('api:pops'))
        self.assertEqual(response.status_code, 200)

    def test_import_models(self):
        '''
        Check if needed models exist
        '''
        from network.models import PeerIfces, PeerSite

    def test_static(self):
        '''
        Check if static files exist
        '''
        from django.contrib.staticfiles import finders
        self.assertIsNot(finders.find('pops/icons/customer-legend.png'), None)
        self.assertIsNot(finders.find('pops/icons/grnet-legend.png'), None)
        self.assertIsNot(finders.find('pops/icons/commercial-legend.png'), None)
        self.assertIsNot(finders.find('pops/icons/pin-legend.png'), None)
        self.assertIsNot(finders.find('pops/icons/core-legend.png'), None)
        self.assertIsNot(finders.find('pops/icons/access-optical-legend.png'), None)
        self.assertIsNot(finders.find('pops/icons/access-l2-legend.png'), None)
        self.assertIsNot(finders.find('pops/icons/distribution-legend.png'), None)
        self.assertIsNot(finders.find('pops/icons/pass-through-thumb.png'), None)
        self.assertIsNot(finders.find('pops/icons/unknown-thumb.png'), None)
        self.assertIsNot(finders.find('bootstrap/js/bootstrap.js'), None)
        self.assertIsNot(finders.find('pops/js/gmaps.js'), None)
        self.assertIsNot(finders.find('pops/js/underscore-min.js'), None)
        self.assertIsNot(finders.find('bootstrap/css/bootstrap.min.css'), None)
        self.assertIsNot(finders.find('pops/css/maps.css'), None)
