from django import template
from django.conf import settings
from django.template.defaulttags import NowNode
from django.utils.safestring import mark_safe

register = template.Library()

_CONFIG_KEY = 'SUIT_CONFIG'

_DEFAULT_CONFIG = {
    'ADMIN_NAME': 'Django Suit',
    'ADMIN_SHORT_NAME': 'Django Suit',
    'COPYRIGHT': 'Copyright &copy; 2013 DjangoSuit.com<br>Developed by <a '
                 'href="http://djangoSuit.com" target="_blank">DjangoSuit'
                 '.com</a>',
    'SHOW_REQUIRED_ASTERISK': True,
    'HEADER_DATE_FORMAT': 'l, jS F Y',
    'HEADER_TIME_FORMAT': 'H:i',
}


@register.filter(name='suit_conf')
def suit_conf(name):
    value = None
    if hasattr(settings, _CONFIG_KEY):
        config = getattr(settings, _CONFIG_KEY)
        if name in config:
            value = config.get(name)

    if value is None:
        value = _DEFAULT_CONFIG.get(name)

    return mark_safe(value) if isinstance(value, basestring) else value


@register.tag
def suit_date(parser, token):
    return NowNode(suit_conf('HEADER_DATE_FORMAT'))


@register.tag
def suit_time(parser, token):
    return NowNode(suit_conf('HEADER_TIME_FORMAT'))
