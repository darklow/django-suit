from django import get_version
from suit import utils
from django.test import TestCase

from suit.templatetags.suit_tags import str_to_version


class UtilsTestCase(TestCase):
    def get_args(self):
        return [1.4, 'x', 1.5, 'y', 's', 'z']

    def test_args_to_dict(self):
        args = self.get_args()
        result = {1.4: 'x', 1.5: 'y', 's': 'z'}
        self.assertEqual(utils.args_to_dict(args), result)

    def test_value_by_version(self):
        args = [utils.django_major_version(), 'a']
        self.assertEqual(utils.value_by_version(args), 'a')

    def test_str_to_version(self):
        return self.assertEqual(str_to_version('1.10.2'), (1, 10, 2))
