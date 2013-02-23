VERSION = '0.1.0'


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
        'SEARCH_URL': 'admin:auth_user_changelist',
        'MENU_OPEN_FIRST_CHILD': True,
        'MENU_EXCLUDE': (),
        'MENU_ICONS': {
            'auth': 'icon-lock',
            'sites': 'icon-leaf',
        },
        # 'MENU_ORDER': (
        #     ('sites',),
        #     ('auth', ('user','group')),
        # )

        # misc
        'LIST_PER_PAGE': 20
    }


from os import getenv

if getenv('DJANGO_SETTINGS_MODULE', None):

    from django.contrib.admin import ModelAdmin
    from django.conf import settings

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

    # Reverse default actions position
    ModelAdmin.actions_on_top = False
    ModelAdmin.actions_on_bottom = True

    # Set global list_per_page
    ModelAdmin.list_per_page = get_config('LIST_PER_PAGE')
