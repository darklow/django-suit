from django import get_version
from django.apps import AppConfig
from django.contrib.admin.options import ModelAdmin
from . import VERSION


class DjangoSuitConfig(AppConfig):
    verbose_name = 'Django Suit'
    django_version = get_version()
    name = 'suit'
    version = VERSION

    #: :type: list of suit.menu.ParentItem
    menu = []
    menu_show_home = True

    def __init__(self, app_name, app_module):
        self.setup_model_admin()
        super(DjangoSuitConfig, self).__init__(app_name, app_module)

    def ready(self):
        super(DjangoSuitConfig, self).ready()

    def setup_model_admin(self):
        """
        Override some ModelAdmin defaults
        """
        ModelAdmin.actions_on_top = False
        ModelAdmin.actions_on_bottom = True
