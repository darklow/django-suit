from django.test import TestCase
from suit.menu import ParentItem


class TestMenuTestCase(TestCase):
    def setUp(self):
        pass

    def test_method(self):
        """
        Just a dummy test case to satisfy Travis until all the tests are finished
        """
        self.assertEqual(ParentItem(app='abc')._key(), 'abc')
