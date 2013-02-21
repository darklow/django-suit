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
        'VERSION': VERSION,

        # configurable
        'ADMIN_NAME': 'Django Suit',
        'HEADER_DATE_FORMAT': 'l, jS F Y',
        'HEADER_TIME_FORMAT': 'H:i',

        # form
        'SHOW_REQUIRED_ASTERISK': True,
        'CONFIRM_UNSAVED_CHANGES': True,

        # menu
        'MENU_PARENT_LINK': False, # Default False
        'MENU_EXCLUDE': (),
        'MENU_ICONS': {
            'auth': 'icon-lock',
            'sites': 'icon-leaf',
            },
        # 'MENU_ORDER': (
        #     ('sites',),
        #     ('auth', ('user','group')),
        # )
    }


def get_config(param=None):
    config_key = 'SUIT_CONFIG'
    if hasattr(settings, config_key):
        config = getattr(settings, config_key, {})
    else:
        config = default_config()
    if param:
        value = None
        if param in config:
            value = config.get(param)

        if value is None:
            value = default_config().get(param)

        return value

    return config
