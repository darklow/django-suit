from django.conf import settings
from django.contrib.admin import ModelAdmin

VERSION = '0.9.1'

# Reverse default actions position
ModelAdmin.actions_on_top = False
ModelAdmin.actions_on_bottom = True

# Who uses 100 items per page at all?
ModelAdmin.list_per_page = 20

def default_config():
    return {
        'ADMIN_NAME': 'Django Suit v%s' % VERSION,
        'ADMIN_SHORT_NAME': 'Django Suit',
        'COPYRIGHT': 'Copyright &copy; 2013 DjangoSuit.com<br>Developed by <a '
                     'href="http://djangoSuit.com" target="_blank">DjangoSuit'
                     '.com</a>',
        'HEADER_DATE_FORMAT': 'l, jS F Y',
        'HEADER_TIME_FORMAT': 'H:i',

        # form
        'CONFIRM_UNSAVED_CHANGES': True,
        'ALERT_UNSAVED_CHANGES': True,
    }


def get_config(param=None):
    config_key = 'SUIT_CONFIG'
    if hasattr(settings, config_key):
        config = getattr(settings, config_key, {})
        if param:
            value = None
            if param in config:
                value = config.get(param)

            if value is None:
                value = default_config().get(param)

            return value

        return config
