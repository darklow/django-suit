from django import template
from django.template.backends.django import Template
from django.template.loader import get_template
from django.template.utils import get_app_template_dirs
from django.utils.safestring import mark_safe
from django.template import TemplateSyntaxError
from django.template.loader_tags import ExtendsNode, do_extends
from suit import config
from django import VERSION as DJANGO_VERSION

register = template.Library()


@register.filter(name='suit_conf')
def suit_conf(name):
    value = config.get_config(name)
    return mark_safe(value) if isinstance(value, str) else value


@register.filter(name='suit_body_class')
def suit_body_class(value):
    css_classes = []
    config_vars_to_add = ['toggle_changelist_top_actions', 'form_submit_on_right']
    for each in config_vars_to_add:
        if getattr(config.suit_config, each):
            css_classes.append('suit_%s' % each)
    return ' '.join(css_classes)


@register.filter(name='suit_conf')
def suit_conf(name):
    value = config.get_config(name)
    return mark_safe(value) if isinstance(value, str) else value


@register.assignment_tag
def suit_conf_value(name, model_admin=None):
    if model_admin:
        value_by_ma = getattr(model_admin, 'suit_%s' % name.lower(), None)
        if value_by_ma in ('center', 'right'):
            config.set_config_value(name, value_by_ma)
        else:
            config.reset_config_value(name)
    return suit_conf(name)


@register.tag('suit_extends')
def do_extends_override(parser, token):
    """
    Simple wrapper to remove "admin:" prefix for Django 1.9+
    For Django 1.8 custom template loader is used to load "app:" prefixed templates
    and avoid circular imports
    """
    if DJANGO_VERSION >= (1, 9):
        token.contents = token.contents.replace('admin:', '')

    # Call original template tag
    extends_node = do_extends(parser, token)
    extends_node.must_be_first = False
    return extends_node
