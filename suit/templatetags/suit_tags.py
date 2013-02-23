from django import template
from django.contrib.admin.util import lookup_field
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import NoReverseMatch, reverse
from django.db.models import ForeignKey
from django.template.defaulttags import NowNode
from django.utils.safestring import mark_safe
from suit import get_config

register = template.Library()


@register.filter(name='suit_conf')
def suit_conf(name):
    value = get_config(name)
    return mark_safe(value) if isinstance(value, basestring) else value


@register.tag
def suit_date(parser, token):
    return NowNode(get_config('HEADER_DATE_FORMAT'))


@register.tag
def suit_time(parser, token):
    return NowNode(get_config('HEADER_TIME_FORMAT'))


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
            admin_url = get_admin_url(value)
        except NoReverseMatch:
            admin_url = None
        if admin_url:
            displayed = u"<a href='%s'>%s</a>" % (admin_url, displayed)
    return mark_safe(displayed)


#adapted from http://djangosnippets.org/snippets/1916/
def get_admin_url(obj):
    content_type = ContentType.objects.get_for_model(obj.__class__)
    return reverse(
        "admin:%s_%s_change" % (content_type.app_label, content_type.model),
        args=[obj.pk])

