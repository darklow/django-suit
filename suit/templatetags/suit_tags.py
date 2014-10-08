from django import template
from django.contrib.admin.util import lookup_field
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import NoReverseMatch, reverse
from django.db.models import ForeignKey
from django.template.defaulttags import NowNode
from django.utils.safestring import mark_safe
from suit import config
from suit import utils

register = template.Library()


@register.filter(name='suit_conf')
def suit_conf(name):
    value = config.get_config(name)
    return mark_safe(value) if isinstance(value, str) else value


@register.filter
def suit_platform(request):
    if not request:
        return ''
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    css = []

    # OS
    if 'Macintosh' in user_agent:
        css.append('os-macos')
    elif 'Linux' in user_agent:
        css.append('os-linux')
    else:
        css.append('os-win')

    # Browser
    if 'Chrome' in user_agent:
        css.append('br-chrome')
    elif 'Firefox' in user_agent:
        css.append('br-firefox')

    return ' '.join(css)


@register.assignment_tag
def suit_conf_value(name, model_admin=None):
    if model_admin:
        value_by_ma = getattr(model_admin, 'suit_%s' % name.lower(), None)
        if value_by_ma in ('center', 'right'):
            config.set_config_value(name, value_by_ma)
        else:
            config.reset_config_value(name)
    return suit_conf(name)


@register.tag
def suit_date(parser, token):
    return NowNode(config.get_config('HEADER_DATE_FORMAT'))


@register.tag
def suit_time(parser, token):
    return NowNode(config.get_config('HEADER_TIME_FORMAT'))


@register.filter
def field_contents_foreign_linked(admin_field):
    """Return the .contents attribute of the admin_field, and if it
    is a foreign key, wrap it in a link to the admin page for that
    object.

    Use by replacing '{{ field.contents }}' in an admin template (e.g.
    fieldset.html) with '{{ field|field_contents_foreign_linked }}'.
    """
    fieldname = admin_field.field['field']
    displayed = admin_field.contents()
    obj = admin_field.form.instance

    if not hasattr(admin_field.model_admin,
                   'linked_readonly_fields') or fieldname not in admin_field \
            .model_admin \
            .linked_readonly_fields:
        return displayed

    try:
        fieldtype, attr, value = lookup_field(fieldname, obj,
                                              admin_field.model_admin)
    except ObjectDoesNotExist:
        fieldtype = None

    if isinstance(fieldtype, ForeignKey):
        try:
            url = admin_url(value)
        except NoReverseMatch:
            url = None
        if url:
            displayed = "<a href='%s'>%s</a>" % (url, displayed)
    return mark_safe(displayed)


@register.filter
def admin_url(obj):
    info = (obj._meta.app_label, obj._meta.module_name)
    return reverse("admin:%s_%s_change" % info, args=[obj.pk])


@register.simple_tag
def suit_bc(*args):
    return utils.value_by_version(args)


@register.assignment_tag
def suit_bc_value(*args):
    return utils.value_by_version(args)
