from django.contrib.admin import ModelAdmin
from django.conf import settings
from . import VERSION

config_key = 'SUIT_CONFIG'


def default_config():
    return {
        'VERSION': VERSION,

        # configurable
        'THEME': 'dark',
        'ADMIN_NAME': 'Django Suit',
        'HEADER_DATE_FORMAT': 'l, jS F Y',
        'HEADER_TIME_FORMAT': 'H:i',

        # form
        'SHOW_REQUIRED_ASTERISK': True,
        'CONFIRM_UNSAVED_CHANGES': True,

        # menu
        'SEARCH_URL': '/admin/auth/user/',
        'MENU_POSITION': 'vertical',
        'MENU_OPEN_FIRST_CHILD': True,
        'MENU_ICONS': {
            'auth': 'icon-lock',
            'sites': 'icon-leaf',
        },

        # form
        'FORM_SIZE': 'col-sm-2:col-sm-9',

        # 'MENU_EXCLUDE': ('auth.group',),
        # 'MENU': (
        #     'sites',
        #     {'app': 'auth', 'icon':'icon-lock', 'models': ('user', 'group')},
        #     {'label': 'Settings', 'icon':'icon-cog', 'models': ('auth.user', 'auth.group')},
        #     {'label': 'Support', 'icon':'icon-question-sign', 'url': '/support/'},
        # ),

        # list
        'LIST_PER_PAGE': 20,
        'LIST_FILTERS_POSITION': 'right',
    }


def get_config(param=None):
    if hasattr(settings, config_key):
        config = getattr(settings, config_key)
    else:
        config = default_config()
        setattr(settings, config_key, config)
    if param:
        value = config.get(param)
        if value is None:
            value = default_config().get(param)
        return value
    return config


def set_config_value(name, value):
    config = get_config()
    # Store previous value to reset later if needed
    prev_value_key = '_%s' % name
    if prev_value_key not in config:
        config[prev_value_key] = config.get(name)
    config[name] = value


def reset_config_value(name):
    config = getattr(settings, config_key, default_config())
    prev_value_key = '_%s' % name
    if prev_value_key in config:
        config[name] = config.get(prev_value_key)
        del config[prev_value_key]


# Reverse default actions position
ModelAdmin.actions_on_top = False
ModelAdmin.actions_on_bottom = True

# Set global list_per_page
ModelAdmin.list_per_page = get_config('LIST_PER_PAGE')


def setup_filer():
    from suit.widgets import AutosizedTextarea
    from filer.admin.imageadmin import ImageAdminForm
    from filer.admin.fileadmin import FileAdminChangeFrom
    from filer.admin import FolderAdmin

    def ensure_meta_widgets(meta_cls):
        if not hasattr(meta_cls, 'widgets'):
            meta_cls.widgets = {}

        meta_cls.widgets['description'] = AutosizedTextarea

    ensure_meta_widgets(ImageAdminForm.Meta)
    ensure_meta_widgets(FileAdminChangeFrom.Meta)
    FolderAdmin.actions_on_top = False
    FolderAdmin.actions_on_bottom = True


if 'filer' in settings.INSTALLED_APPS:
    setup_filer()
