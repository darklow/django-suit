from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils import unittest
from django.contrib.admin import site
from suit.templatetags.suit_menu import Menu, get_menu
from django.test.client import Client


class GetMenuTestCase(unittest.TestCase):
    def setUp(self):
        self.client = Client()

        # Create superuser and login
        username = 'superuser'
        password = 'test12345'
        self.user = User.objects.create_superuser(username=username,
                                                  password=password,
                                                  email='test@test.com')
        self.client.login(username=username, password=password)

        # Set test settings
        settings.SUIT_CONFIG = {
            # 'ADMIN_NAME': 'Admin app name',
            # 'HEADER_DATE_FORMAT': 'l, j. F Y',
            # 'HEADER_TIME_FORMAT': 'H:i',

            # forms
            # 'SHOW_REQUIRED_ASTERISK': False,  # Default True
            # 'CONFIRM_UNSAVED_CHANGES': False, # Default True

            # menu
            'SEARCH_URL': 'admin:examples_country_changelist',
            'MENU_ICONS': {
                'auth': 'icon-lock',
                'examples': 'icon-leaf',
                'integrations': 'icon-globe',
            },
            'MENU_ORDER': (
                ('examples', ('country', 'continent', 'kitchensink')),
                (('Integrations', '', 'icon-globe'),
                 ('examples.city', 'examples.category')),
                ('auth', ('user', 'group')),
                (('Custom view', '/admin/custom/', 'icon-cog',
                  ('auth.add_group',)), (
                     ('Custom link', '/admin/custom/'),
                     ('Check out error 404', '/admin/non-existant/'),
                 )),
            ),

            # misc
            'LIST_PER_PAGE': 15
        }

        # Go to /admin/ and init menu component
        response = self.client.get(reverse('admin:index'))
        template_response = site.index(response._request)
        app_list = template_response.context_data['app_list']
        self.menu = Menu(response.context, response._request, app_list)

    def test_menu_init(self):
        """Menu is initialized"""
        self.assertEqual(self.menu.request, )
        # self.assertEqual(self.lion.speak(), 'The lion says "roar"')
        # self.assertEqual(self.cat.speak(), 'The cat says "meow"')

