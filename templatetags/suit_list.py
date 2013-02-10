from django import template
from django.contrib.admin.helpers import AdminField, AdminReadonlyField
from django.template import Context
from django.template.loader import get_template
from django.utils.safestring import mark_safe
from django.contrib.admin.util import lookup_field
from django.db.models.fields.related import ForeignKey
from django.db.models import ObjectDoesNotExist
from django.core.urlresolvers import reverse, NoReverseMatch
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.views.main import ALL_VAR, PAGE_VAR
from django.utils.html import escape
from urlparse import parse_qs

register = template.Library()

DOT = '.'


@register.simple_tag
def paginator_number(cl, i):
    """
    Generates an individual page index link in a paginated list.
    """
    if i == DOT:
        return u'<li class="disabled"><a href="#" onclick="return false;">..' \
               u'.</a></li>'
    elif i == cl.page_num:
        return mark_safe(
            u'<li class="active"><a href="">%d</a></li> ' % (i + 1))
    else:
        return mark_safe(u'<li><a href="%s"%s>%d</a></li> ' % (
            escape(cl.get_query_string({PAGE_VAR: i})),
            (i == cl.paginator.num_pages - 1 and ' class="end"' or ''),
            i + 1))


@register.simple_tag
def paginator_info(cl):
    paginator = cl.paginator
    entries_from = (
        (paginator.per_page * cl.page_num) + 1) if paginator.count > 0 else 0
    entries_to = entries_from - 1 + paginator.per_page
    entries_to = paginator.count if paginator.count < entries_to else entries_to
    return '%s - %s' % (entries_from, entries_to)


@register.inclusion_tag('admin/pagination.html')
def pagination(cl):
    """
    Generates the series of links to the pages in a paginated list.
    """
    paginator, page_num = cl.paginator, cl.page_num

    pagination_required = (
                              not cl.show_all or not cl.can_show_all) and cl \
                              .multi_page
    if not pagination_required:
        page_range = []
    else:
        ON_EACH_SIDE = 3
        ON_ENDS = 2

        # If there are 10 or fewer pages, display links to every page.
        # Otherwise, do some fancy
        if paginator.num_pages <= 8:
            page_range = range(paginator.num_pages)
        else:
            # Insert "smart" pagination links, so that there are always ON_ENDS
            # links at either end of the list of pages, and there are always
            # ON_EACH_SIDE links at either end of the "current page" link.
            page_range = []
            if page_num > (ON_EACH_SIDE + ON_ENDS):
                page_range.extend(range(0, ON_EACH_SIDE - 1))
                page_range.append(DOT)
                page_range.extend(range(page_num - ON_EACH_SIDE, page_num + 1))
            else:
                page_range.extend(range(0, page_num + 1))
            if page_num < (paginator.num_pages - ON_EACH_SIDE - ON_ENDS - 1):
                page_range.extend(
                    range(page_num + 1, page_num + ON_EACH_SIDE + 1))
                page_range.append(DOT)
                page_range.extend(
                    range(paginator.num_pages - ON_ENDS, paginator.num_pages))
            else:
                page_range.extend(range(page_num + 1, paginator.num_pages))

    need_show_all_link = cl.can_show_all and not cl.show_all and cl.multi_page
    return {
        'cl': cl,
        'pagination_required': pagination_required,
        'show_all_url': need_show_all_link and cl.get_query_string(
            {ALL_VAR: ''}),
        'page_range': page_range,
        'ALL_VAR': ALL_VAR,
        '1': 1,
    }


@register.simple_tag
def suit_list_filter_select(cl, spec):
    tpl = get_template(spec.template)
    choices = list(spec.choices(cl))
    field_key = spec.field.name if hasattr(spec,
                                           'field') else spec.parameter_name
    matched_key = field_key
    for choice in choices:
        query_string = choice['query_string'][1:]
        query_parts = parse_qs(query_string)

        value = ''
        matches = {}
        for key in query_parts.keys():
            if key == field_key:
                value = query_parts[key][0]
                matched_key = key
            elif key.startswith(
                            field_key + '__') or '__' + field_key + '__' in key:
                value = query_parts[key][0]
                matched_key = key

            if value:
                matches[matched_key] = value

        # Iterate matches, use first as actual values, additional for hidden
        i = 0
        for key, value in matches.items():
            if i == 0:
                choice['name'] = key
                choice['val'] = value
            else:
                choice['additional'] = '%s=%s' % (key, value)
            i += 1

    return tpl.render(Context({
        'field_name': field_key,
        'title': spec.title,
        'choices': choices,
        'spec': spec,
    }))


@register.simple_tag
def field_widget_value(field):
    """
    @type field: AdminField
    """
    if isinstance(field, AdminField):
        read_only_field = AdminReadonlyField(field.field.form, field.field.name,
                                             field.is_first)
        return read_only_field.contents()


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
                   'linked_fields') or fieldname not in admin_field \
        .model_admin \
        .linked_fields:
        return displayed

    try:
        fieldtype, attr, value = lookup_field(fieldname, obj,
                                              admin_field.model_admin)
    except ObjectDoesNotExist:
        fieldtype = None
    if isinstance(fieldtype,
                  ForeignKey): #XXX - probably over-simplistic wrt escaping
        try:
            admin_url = get_admin_url(value)
        except NoReverseMatch:
            admin_url = None
        if admin_url:
            displayed = u"<a href='%s' class=\"append-icon\">%s<i " \
                        u"class=\"icon-arrow-right icon-alpha75\"></i></a>" % (
                            admin_url, displayed)
    return mark_safe(displayed)


@register.filter
def inline_form_contents_foreign_linked(inline_admin_form):
    """Return the .original attribute of the inline_admin_form,
    wrapped it in a link to the admin page for that
    object.

    Use by replacing '{{ inline_admin_form.original }}' in an admin template
    (e.g.
    tabular.html) with '{{
    inline_admin_form|inline_form_contents_foreign_linked }}'.
    """
    obj = inline_admin_form.form.instance
    displayed = inline_admin_form.original
    try:
        admin_url = get_admin_url(obj)
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

