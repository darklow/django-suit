from django import template
from django.template.loader_tags import do_extends
from django import VERSION as DJANGO_VERSION

register = template.Library()

@register.tag('suit_extends')
def do_extends_override(parser, token):
    """
    For Django 1.8 custom template loader is used to load "app:" prefixed templates
    and avoid circular imports.
    For Django 1.9+ "admin:" prefix is removed and regular extend is used.
    """
    if DJANGO_VERSION >= (1, 9):
        token.contents = token.contents.replace('admin:', '')

    # Call original template tag
    return do_extends(parser, token)
