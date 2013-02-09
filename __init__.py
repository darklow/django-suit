from django.conf import settings


def default_config():
    return {
        'ADMIN_NAME': 'Django Suit',
        'ADMIN_SHORT_NAME': 'Django Suit',
        'COPYRIGHT': 'Copyright &copy; 2013 DjangoSuit.com<br>Developed by <a '
                     'href="http://djangoSuit.com" target="_blank">DjangoSuit'
                     '.com</a>',
        'SHOW_REQUIRED_ASTERISK': True,
        'HEADER_DATE_FORMAT': 'l, jS F Y',
        'HEADER_TIME_FORMAT': 'H:i',
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
