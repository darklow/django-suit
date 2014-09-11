from django.conf import settings
from django.contrib.auth.models import Permission
from django.core.urlresolvers import reverse
from suit.templatetags.suit_menu import get_menu
from suit.tests.mixins import ModelsTestCaseMixin, UserTestCaseMixin
from suit.tests.models import test_app_label

# conditional import, force_unicode was renamed in Django 1.5
try:
    from django.utils.encoding import force_unicode
except ImportError:
    from django.utils.encoding import force_text as force_unicode

app_label = test_app_label()


class SuitMenuTestCase(ModelsTestCaseMixin, UserTestCaseMixin):
    def setUp(self):
        self.setUpConfig()
        self.login_superuser()

    def setUpConfig(self):
        settings.SUIT_CONFIG.update({
            'MENU_OPEN_FIRST_CHILD': True,
            'MENU_ICONS': {
                'auth': 'icon-auth-assert',
            },
            'MENU_EXCLUDE': [],
            'MENU': [
                app_label,
                {'app': app_label},
                {'app': app_label, 'label': 'Custom'},
                {'app': app_label, 'icon': 'icon-test-assert'},
                {'app': app_label, 'icon': ''},
                {'app': app_label, 'icon': None},
                {'app': 'auth'},
                '-',
                {'label': 'Custom', 'url': '/custom/'},
                {'label': 'Custom2', 'url': '/custom2/', 'permissions': 'x'},
                {'label': 'Custom3', 'url': '/custom3/', 'permissions': ('y',)},
                {'label': 'Custom4', 'url': '/custom4/', 'blank': True},
                {'label': 'C4', 'url': '/c/4', 'models': ('book',)},
                {'label': 'C5', 'url': '/c/5', 'models':
                    ('%s.book' % app_label,)},
                {'label': 'C6', 'url': 'admin:index', 'models':
                    ({'label': 'mx', 'url': 'admin:index'},)},
                {'label': 'C7', 'url': '%s.book' % app_label},
                {'app': app_label, 'models': []},
                {'app': app_label, 'models': ['book', 'album']},
                {'app': app_label, 'models': ['%s.book' % app_label,
                                              '%s.album' % app_label]},
                {'app': app_label, 'models': [
                    'book', '%s.book' % app_label,
                    {
                        'model': '%s.album' % app_label,
                        'label': 'Albumzzz',
                        'url': '/albumzzz/',
                    }, {
                        'label': 'CustModel',
                        'url': '/cust-mod/',
                        'permissions': 'z'
                    }]},
            ]
        })

    def setUpOldConfig(self):
        settings.SUIT_CONFIG.update({
            'MENU_OPEN_FIRST_CHILD': False,
            'MENU_ICONS': {
                app_label: 'icon-fire icon-test-against-keyword',
            },
            'MENU_ORDER': (
                (app_label, ('book',)),
                (('Custom app name', '/custom-url-test/', 'icon-custom-app'), (
                    ('Custom link', '/admin/custom/',
                     '%s.add_book' % app_label),
                    ('Check out error 404', '/admin/non-existant/',
                     ('mega-perms',)),
                    '%s.album' % app_label
                )),
                (('Custom app no models', '/custom-app-no-models',
                  '', 'mega-rights'),),
                (('Custom app no models tuple perms', '/custom-app-tuple-perms',
                  '', ('mega-rights',)),),
            ),
            'MENU_EXCLUDE': []
        })
        del settings.SUIT_CONFIG['MENU']

    def make_menu_from_response(self):
        return get_menu(self.response.context[-1], self.response._request)

    def test_menu_search_url_formats(self):
        # Test named url as defined in setUp config
        settings.SUIT_CONFIG['SEARCH_URL'] = 'admin:%s_book_changelist' \
                                             % app_label
        admin_root = reverse('admin:index')
        self.get_response()
        self.assertContains(self.response,
                            'action="%s%s/book/"' % (admin_root, app_label))

        # Test absolute url
        absolute_search_url = '/absolute/search/url'
        settings.SUIT_CONFIG['SEARCH_URL'] = absolute_search_url
        self.get_response()
        self.assertContains(self.response, absolute_search_url)

    def test_menu(self):
        mc = settings.SUIT_CONFIG['MENU']
        self.get_response()
        menu = self.make_menu_from_response()
        self.assertEqual(len(menu), len(mc))

        # as string
        i = 0
        first_model_url = reverse('admin:%s_album_changelist' % app_label)
        self.assertEqual(menu[i]['url'], first_model_url)
        self.assertEqual(len(menu[i]['models']), 3)
        self.assertEqual(menu[i]['name'], mc[i])
        self.assertEqual(menu[i]['label'], app_label.title())
        self.assertEqual(menu[i]['icon'], None)
        self.assertEqual(menu[i]['models'][0]['url'], first_model_url)
        self.assertEqual(force_unicode(menu[0]['models'][0]['label']), 'Albums')

        i += 1 # as dict
        self.assertEqual(menu[i]['url'], first_model_url)
        self.assertEqual(len(menu[i]['models']), 3)

        i += 1 # with label
        self.assertEqual(menu[i]['label'], mc[i]['label'])

        i += 1 # with icon
        self.assertEqual(menu[i]['icon'], mc[i]['icon'])

        i += 1 # with icon=''
        self.assertEqual(menu[i]['icon'], 'icon-')

        i += 1 # with is is None
        self.assertEqual(menu[i]['icon'], 'icon-')

        i += 1 # icon from SUIT_ICONS
        self.assertEqual(menu[i]['icon'], 'icon-auth-assert')

        i += 1 # separator
        self.assertEqual(menu[i]['separator'], True)

        i += 1 # custom app
        self.assertEqual(menu[i]['label'], mc[i]['label'])
        self.assertEqual(menu[i]['url'], mc[i]['url'])

        i += 1 # custom app, with perms as string
        self.assertEqual(menu[i]['label'], mc[i]['label'])

        i += 1 # custom app, with perms as tuple
        self.assertEqual(menu[i]['label'], mc[i]['label'])

        i += 1 # custom app, with perms as tuple
        self.assertEqual(menu[i]['blank'], True)

        i += 1 # custom app with wrong model
        self.assertEqual(menu[i]['label'], mc[i]['label'])
        self.assertEqual(menu[i]['models'], [])
        self.assertEqual(menu[i]['url'], mc[i]['url'])

        i += 1 # custom app with correct model
        first_model_url = reverse('admin:%s_book_changelist' % app_label)
        self.assertEqual(menu[i]['label'], mc[i]['label'])
        self.assertEqual(len(menu[i]['models']), 1)
        self.assertEqual(menu[i]['url'], first_model_url)

        i += 1 # custom app and model with named urls
        expected_url = reverse('admin:index')
        self.assertEqual(menu[i]['url'], expected_url)
        self.assertEqual(menu[i]['models'][0]['url'], expected_url)

        i += 1 # with url by model
        books_url = reverse('admin:%s_book_changelist' % app_label)
        self.assertEqual(menu[i]['url'], books_url)

        i += 1 # with empty models
        self.assertEqual(menu[i]['models'], [])
        self.assertEqual(menu[i]['url'],
                         reverse('admin:app_list', args=[mc[i]['app']]))

        i += 1 # with ordered models
        first_model_url = reverse('admin:%s_book_changelist' % app_label)
        self.assertEqual(menu[i]['models'][0]['url'], first_model_url)
        self.assertEqual(len(menu[i]['models']), 2)

        i += 1 # with prefixed  models
        first_model_url = reverse('admin:%s_book_changelist' % app_label)
        self.assertEqual(menu[i]['models'][0]['url'], first_model_url)
        self.assertEqual(len(menu[i]['models']), 2)

        i += 1 # with dict models
        first_model_url = reverse('admin:%s_book_changelist' % app_label)
        self.assertEqual(menu[i]['models'][0]['url'], first_model_url)
        self.assertEqual(len(menu[i]['models']), 4)
        self.assertEqual(force_unicode(menu[i]['models'][2]['label']),
                         mc[i]['models'][2]['label'])
        self.assertEqual(force_unicode(menu[i]['models'][2]['url']),
                         mc[i]['models'][2]['url'])
        self.assertEqual(force_unicode(menu[i]['models'][3]['label']),
                         mc[i]['models'][3]['label'])
        self.assertEqual(force_unicode(menu[i]['models'][3]['url']),
                         mc[i]['models'][3]['url'])


    def test_menu_app_exclude(self):
        settings.SUIT_CONFIG['MENU'] = ({'app': app_label, 'models': ['book']},
                                        {'app': 'auth'}, 'auth')
        settings.SUIT_CONFIG['MENU_EXCLUDE'] = ('auth', '%s.book' % app_label)
        self.get_response()
        menu = self.make_menu_from_response()
        self.assertEqual(len(menu), 1)
        self.assertEqual(menu[0]['models'], [])

    def test_menu_model_exclude_with_string_app(self):
        settings.SUIT_CONFIG['MENU'] = (app_label,)
        settings.SUIT_CONFIG['MENU_EXCLUDE'] = ('%s.book' % app_label,)
        self.get_response()
        menu = self.make_menu_from_response()
        self.assertEqual(len(menu), 1)
        self.assertEqual(len(menu[0]['models']), 2)

    def test_menu_custom_app(self):
        label = 'custom'
        icon = 'icon-custom'
        settings.SUIT_CONFIG['MENU'] = ({'label': label, 'icon': icon},)
        self.get_response()
        menu = self.make_menu_from_response()
        self.assertEqual(len(menu), 1)
        self.assertEqual(menu[0]['label'], label)
        self.assertEqual(menu[0]['icon'], icon)

    def test_menu_custom_app_permissions(self):
        settings.SUIT_CONFIG['MENU'] = ({'label': 'a',
                                         'permissions': 'secure-perms'},
                                        {'label': 'b',
                                         'permissions': ('secure-perms',)},
                                        {'label': 'c', 'models': [
                                            {'label': 'model1',
                                             'permissions': 'x'}]},)
        self.client.logout()
        self.login_user()
        self.get_response()
        menu = self.make_menu_from_response()
        self.assertEqual(len(menu), 1)
        self.assertEqual(len(menu[0]['models']), 0)

        # Now do the same with super user
        self.client.logout()
        self.login_superuser()
        self.get_response()
        menu = self.make_menu_from_response()
        self.assertEqual(len(menu), 3)
        self.assertEqual(len(menu[2]['models']), 1)

    def test_menu_app_marked_as_active(self):
        self.get_response(reverse('admin:app_list', args=[app_label]))
        self.assertContains(self.response, '<li class="active">')
        menu = self.make_menu_from_response()
        self.assertTrue(menu[0]['is_active'])

    def test_menu_app_marked_as_active_model_link(self):
        settings.SUIT_CONFIG['MENU'] = (
            {'label': '%s-user' % app_label, 'url': '%s.user' % app_label},
            {'label': 'auth-user', 'url': 'auth.user'},
        )
        self.get_response(reverse('admin:auth_user_add'))
        self.assertContains(self.response, '<li class="active">')

        # Test if right user model is activated, when models have identical name
        menu = self.make_menu_from_response()
        self.assertFalse(menu[0]['is_active'])
        self.assertTrue(menu[1]['is_active'])

    def test_menu_model_marked_as_active(self):
        self.get_response(reverse('admin:%s_album_changelist' % app_label))
        menu = self.make_menu_from_response()
        self.assertTrue(menu[0]['is_active'])
        self.assertTrue(menu[0]['models'][0]['is_active'])

    def test_only_native_apps(self):
        del settings.SUIT_CONFIG['MENU']
        if 'MENU_ORDER' in settings.SUIT_CONFIG:
            del settings.SUIT_CONFIG['MENU_ORDER']
        icon = 'icon-auth-assert'
        settings.SUIT_CONFIG['MENU_ICONS'] = {'auth': icon}
        self.get_response()
        menu = self.make_menu_from_response()
        self.assertEqual(len(menu), 4)
        self.assertEqual(menu[0]['icon'], icon)

    def test_user_with_add_but_not_change(self):
        settings.SUIT_CONFIG['MENU'] = ({'app': app_label,
                                         'models': ['book']},
                                        {'app': 'auth'}, 'auth')
        settings.SUIT_CONFIG['MENU_EXCLUDE'] = ()
        self.client.logout()
        self.login_user()
        self.user.user_permissions.add(
            Permission.objects.get(codename='add_book'))
        self.user.save()
        self.get_response()
        menu = self.make_menu_from_response()
        add_book_url = reverse('admin:%s_book_add' % app_label)
        self.assertEqual(menu[0]['url'], add_book_url)
        # self.assertEqual(menu[0]['models'][0]['url'], add_book_url)

    #
    # Tests for old menu config format
    #
    def test_old_menu_init(self):
        # Template usage
        self.client.logout()
        self.login_superuser()
        self.setUpOldConfig()
        self.get_response()
        self.assertTemplateUsed(self.response, 'suit/menu.html')
        self.assertContains(self.response, 'left-nav')
        self.assertContains(self.response, 'icon-test-against-keyword')
        app_list = self.response.context_data['app_list']
        pass
        # print self.response.content

    def test_old_menu_custom_app_and_models(self):
        # Test custom app name, url and icon
        self.setUpOldConfig()
        self.get_response()
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
        self.assertContains(self.response, '%s/album' % app_label)

    def test_old_menu_when_open_first_child_is_true(self):
        # Test custom app name, url and icon
        self.setUpOldConfig()
        settings.SUIT_CONFIG['MENU_OPEN_FIRST_CHILD'] = True
        self.get_response()
        menu_order = settings.SUIT_CONFIG['MENU_ORDER']
        self.assertNotContains(self.response, menu_order[1][0][1])

    def test_old_custom_menu_permissions(self):
        self.client.logout()
        self.login_user()
        self.setUpOldConfig()
        self.get_response()
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

    def test_old_menu_marked_as_active(self):
        self.setUpOldConfig()
        self.get_response(reverse('admin:app_list', args=[app_label]))
        self.assertContains(self.response, '<li class="active">')


class SuitMenuAdminRootURLTestCase(SuitMenuTestCase):
    urls = 'suit.tests.urls.admin_at_root'


class SuitMenuAdminI18NURLTestCase(SuitMenuTestCase):
    urls = 'suit.tests.urls.admin_i18n'


class SuitMenuAdminCustomURLTestCase(SuitMenuTestCase):
    urls = 'suit.tests.urls.admin_custom'
