from django import template
from django.utils.safestring import mark_safe
from suit import config

register = template.Library()


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
