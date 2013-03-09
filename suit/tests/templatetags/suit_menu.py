from django.conf import settings
from django.core.urlresolvers import reverse
from suit.tests.mixins import ModelsTestCaseMixin, UserTestCaseMixin


class SuitMenuTestCase(ModelsTestCaseMixin, UserTestCaseMixin):
    def perform_response(self):
        self.response = self.client.get(reverse('admin:index'))

    def setUp(self):
        # Menu settings
        settings.SUIT_CONFIG.update({
            'MENU_OPEN_FIRST_CHILD': False,
            'MENU_ICONS': {
                'tests': 'icon-fire icon-test-against-keyword',
            },
            'MENU_ORDER': (
                ('tests', ('book',)),
                (('Custom app name', '/custom-url-test/', 'icon-custom-app'), (
                    ('Custom link', '/admin/custom/', 'tests.add_book'),
                    ('Check out error 404', '/admin/non-existant/',
                     ('mega-perms',)),
                    'tests.album'
                )),
                (('Custom app no models', '/custom-app-no-models',
                  '', 'mega-rights'),),
                (('Custom app no models tuple perms', '/custom-app-tuple-perms',
                  '', ('mega-rights',)),),
            ),
        })
        self.login_superuser()

    def test_menu_init(self):
        # Template usage
        self.perform_response()
        self.assertTemplateUsed(self.response, 'suit/menu.html')
        self.assertContains(self.response, 'left-nav')
        self.assertContains(self.response, 'icon-test-against-keyword')
        app_list = self.response.context_data['app_list']
        pass
        # print self.response.content

    def test_menu_search_url_formats(self):
        # Test named url as defined in setUp config
        settings.SUIT_CONFIG['SEARCH_URL'] = 'admin:tests_book_changelist'
        self.perform_response()
        self.assertContains(self.response, 'action="/admin/tests/book/"')

        # Test absolute url
        absolute_search_url = '/absolute/search/url'
        settings.SUIT_CONFIG['SEARCH_URL'] = absolute_search_url
        self.perform_response()
        self.assertContains(self.response, absolute_search_url)

    def test_menu_custom_app_and_models(self):
        # Test custom app name, url and icon
        self.perform_response()
        menu_order = settings.SUIT_CONFIG['MENU_ORDER']
        self.assertContains(self.response, menu_order[1][0][0])
        self.assertContains(self.response, menu_order[1][0][1])
        self.assertContains(self.response, menu_order[1][0][2])
        # Test custom app no models name, url and icon
        self.assertContains(self.response, menu_order[2][0][0])
        self.assertContains(self.response, menu_order[2][0][1])
        self.assertContains(self.response, menu_order[2][0][2])
        # Test custom app when perms defined but is allowed
        self.assertContains(self.response, menu_order[2][0][0])
        # Test cross-linked app
        self.assertContains(self.response, 'tests/album')

    def test_menu_when_open_first_child_is_true(self):
        # Test custom app name, url and icon
        settings.SUIT_CONFIG['MENU_OPEN_FIRST_CHILD'] = True
        self.perform_response()
        menu_order = settings.SUIT_CONFIG['MENU_ORDER']
        self.assertNotContains(self.response, menu_order[1][0][1])

    def test_custom_menu_permissions(self):
        self.client.logout()
        self.login_user()
        self.perform_response()
        # Test for menu at all for simple user
        self.assertTemplateUsed(self.response, 'suit/menu.html')
        self.assertContains(self.response, 'left-nav')
        menu_order = settings.SUIT_CONFIG['MENU_ORDER']
        # Test custom model when perms defined as string
        self.assertNotContains(self.response, menu_order[1][1][0][0])
        # Test custom model when perms defined as tuple
        self.assertNotContains(self.response, menu_order[1][1][1][0])
        # Test custom app when perms defined as string
        self.assertNotContains(self.response, menu_order[2][0][0])
        # Test custom app when perms defined as tuple
        self.assertNotContains(self.response, menu_order[3][0][0])
