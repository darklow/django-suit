from datetime import timedelta

from django.core.urlresolvers import reverse
from django.test import TestCase

class RoutesTestCase(TestCase):
    def test_login(self):
        response = self.client.get(reverse('admin:login'))
        self.assertContains(response, 'Log in')
