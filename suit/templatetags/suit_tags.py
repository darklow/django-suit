import django
from django import template
from django.utils.safestring import mark_safe
from suit import config

register = template.Library()

if django.VERSION < (1, 9):
    simple_tag = register.assignment_tag
else:
    simple_tag = register.simple_tag


@register.filter(name='suit_conf')
def suit_conf(name, request):
    value = config.get_config(name, request)
    return mark_safe(value) if isinstance(value, str) else value


@register.filter(name='suit_body_class')
def suit_body_class(value, request):
    css_classes = []
    config_vars_to_add = ['toggle_changelist_top_actions', 'form_submit_on_right', 'layout']
    for each in config_vars_to_add:
        suit_conf_param = getattr(config.get_config(None, request), each, None)
        if suit_conf_param:
            value = each if isinstance(suit_conf_param, bool) \
                else '_'.join((each, suit_conf_param))
            css_classes.append('suit_%s' % value)
    return ' '.join(css_classes)


@simple_tag
def suit_conf_value(name, model_admin=None):
    if model_admin:
        value_by_ma = getattr(model_admin, 'suit_%s' % name.lower(), None)
        if value_by_ma in ('center', 'right'):
            config.set_config_value(name, value_by_ma)
        else:
            config.reset_config_value(name)
    return suit_conf(name)
