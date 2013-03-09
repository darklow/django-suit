from django.conf import settings
from django.contrib.auth.models import User
from django.core.management import call_command
from django.db.models.loading import load_app
from django.test import TestCase
from random import randint


class UserTestCaseMixin(TestCase):
    user = None

    def login(self, user=None):
        if not user or not self.user:
            self.user = self.create_superuser()
        self.client.login(username=self.user.username, password='password')

    def create_superuser(self):
        return User.objects.create_superuser('user-%s' % str(randint(1, 9999)),
                                             'test@test.com', 'password')


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
