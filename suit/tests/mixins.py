from django.conf import settings
from django.contrib.auth.models import User
from django.core.management import call_command
from django.core.urlresolvers import reverse
from django.db.models.loading import load_app
from django.test import TestCase
from random import randint

# Django 1.7 compatiblity
try:
    import django

    django.setup()
except AttributeError:
    pass

class UserTestCaseMixin(TestCase):
    superuser = None
    user = None

    def login_superuser(self):
        if not self.superuser:
            self.superuser = self.create_superuser()
        self.client.login(username=self.superuser.username, password='password')

    def create_superuser(self):
        return User.objects.create_superuser('admin-%s' % str(randint(1, 9999)),
                                             'test@test.com', 'password')

    def create_user(self):
        user = User.objects.create_user('user-%s' % str(randint(1, 9999)),
                                        'test2@test2.com', 'password')
        user.is_staff = True
        user.save()
        return user

    def login_user(self):
        if not self.user:
            self.user = self.create_user()
        self.client.login(username=self.user.username, password='password')

    def get_response(self, url=None):
        url = url or reverse('admin:index')
        self.response = self.client.get(url)


class ModelsTestCaseMixin(TestCase):
    def _pre_setup(self):
        self.saved_INSTALLED_APPS = settings.INSTALLED_APPS
        self.saved_DEBUG = settings.DEBUG
        test_app = 'suit.tests'
        settings.INSTALLED_APPS = tuple(
            list(self.saved_INSTALLED_APPS) + [test_app]
        )
        settings.DEBUG = True
        # load our fake application and syncdb
        load_app(test_app)
        call_command('syncdb', verbosity=0, interactive=False)
        super(ModelsTestCaseMixin, self)._pre_setup()

    def _post_teardown(self):
        settings.INSTALLED_APPS = self.saved_INSTALLED_APPS
        settings.DEBUG = self.saved_DEBUG
        super(ModelsTestCaseMixin, self)._post_teardown()
