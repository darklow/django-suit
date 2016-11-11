from copy import copy
from inspect import getargspec
from django import template
from django.template.loader import get_template
from django.utils.safestring import mark_safe
from django.contrib.admin.templatetags.admin_list import result_list
from django.contrib.admin.views.main import ALL_VAR, PAGE_VAR
from django.utils.html import escape
from suit.compat import tpl_context_class

try:
    # Python 3.
    from urllib.parse import parse_qs
except ImportError:
    # Python 2.5+
    from urlparse import urlparse

    try:
        # Python 2.6+
        from urlparse import parse_qs
    except ImportError:
        # Python <=2.5
        from cgi import parse_qs

register = template.Library()

DOT = '.'


@register.simple_tag
def paginator_number(cl, i):
    """
    Generates an individual page index link in a paginated list.
    """
    if i == DOT:
        return mark_safe(
                '<li class="disabled"><a href="#" onclick="return false;">..'
                '.</a></li>')
    elif i == cl.page_num:
        return mark_safe(
            '<li class="active"><a href="">%d</a></li> ' % (i + 1))
    else:
        return mark_safe('<li><a href="%s"%s>%d</a></li> ' % (
            escape(cl.get_query_string({PAGE_VAR: i})),
            (i == cl.paginator.num_pages - 1 and ' class="end"' or ''),
            i + 1))


@register.simple_tag
def paginator_info(cl):
    paginator = cl.paginator

    # If we show all rows of list (without pagination)
    if cl.show_all and cl.can_show_all:
        entries_from = 1 if paginator.count > 0 else 0
        entries_to = paginator.count
    else:
        entries_from = (
            (paginator.per_page * cl.page_num) + 1) if paginator.count > 0 else 0
        entries_to = entries_from - 1 + paginator.per_page
        if paginator.count < entries_to:
            entries_to = paginator.count

    return '%s - %s' % (entries_from, entries_to)


@register.inclusion_tag('admin/pagination.html')
def pagination(cl):
    """
    Generates the series of links to the pages in a paginated list.
    """
    paginator, page_num = cl.paginator, cl.page_num

    pagination_required = (not cl.show_all or not cl.can_show_all) \
        and cl.multi_page
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
    field_key = spec.field_path if hasattr(spec, 'field_path') else \
        spec.parameter_name
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

    return tpl.render(tpl_context_class({
        'field_name': field_key,
        'title': spec.title,
        'choices': choices,
        'spec': spec,
    }))


@register.filter
def headers_handler(result_headers, cl):
    """
    Adds field name to css class, so we can style specific columns
    """
    # field = cl.list_display.get()
    attrib_key = 'class_attrib'
    for i, header in enumerate(result_headers):
        field_name = cl.list_display[i]
        if field_name == 'action_checkbox':
            continue
        if not attrib_key in header:
            header[attrib_key] = mark_safe(' class=""')

        pattern = 'class="'
        if pattern in header[attrib_key]:
            replacement = '%s%s-column ' % (pattern, field_name)
            header[attrib_key] = mark_safe(
                header[attrib_key].replace(pattern, replacement))

    return result_headers


def dict_to_attrs(attrs):
    return mark_safe(' ' + ' '.join(['%s="%s"' % (k, v)
                                     for k, v in attrs.items()]))


@register.inclusion_tag('admin/change_list_results.html', takes_context=True)
def result_list_with_context(context, cl):
    """
    Wraps Djangos default result_list to ammend the context with the request.

    This gives us access to the request in change_list_results.
    """
    res = result_list(cl)
    res['request'] = context['request']
    return res


@register.simple_tag(takes_context=True)
def result_row_attrs(context, cl, row_index):
    """
    Returns row attributes based on object instance
    """
    row_index -= 1
    attrs = {
        'class': 'row1' if row_index % 2 == 0 else 'row2'
    }
    suit_row_attributes = getattr(cl.model_admin, 'suit_row_attributes', None)
    if not suit_row_attributes:
        return dict_to_attrs(attrs)

    instance = cl.result_list[row_index]

    # Backwards compatibility for suit_row_attributes without request argument
    args = getargspec(suit_row_attributes)
    if 'request' in args[0]:
        new_attrs = suit_row_attributes(instance, context['request'])
    else:
        new_attrs = suit_row_attributes(instance)

    if not new_attrs:
        return dict_to_attrs(attrs)

    # Validate
    if not isinstance(new_attrs, dict):
        raise TypeError('"suit_row_attributes" must return dict. Got: %s: %s' %
                        (new_attrs.__class__.__name__, new_attrs))

    # Merge 'class' attribute
    if 'class' in new_attrs:
        attrs['class'] += ' ' + new_attrs.pop('class')

    attrs.update(new_attrs)
    return dict_to_attrs(attrs)


@register.filter
def cells_handler(results, cl):
    """
    Changes result cell attributes based on object instance and field name
    """
    suit_cell_attributes = getattr(cl.model_admin, 'suit_cell_attributes', None)
    if not suit_cell_attributes:
        return results

    class_pattern = 'class="'
    td_pattern = '<td'
    th_pattern = '<th'
    for row, result in enumerate(results):
        instance = cl.result_list[row]
        for col, item in enumerate(result):
            field_name = cl.list_display[col]
            attrs = copy(suit_cell_attributes(instance, field_name))
            if not attrs:
                continue

            # Validate
            if not isinstance(attrs, dict):
                raise TypeError('"suit_cell_attributes" must return dict. '
                                'Got: %s: %s' % (
                                    attrs.__class__.__name__, attrs))

            # Merge 'class' attribute
            if class_pattern in item.split('>')[0] and 'class' in attrs:
                css_class = attrs.pop('class')
                replacement = '%s%s ' % (class_pattern, css_class)
                result[col] = mark_safe(
                    item.replace(class_pattern, replacement))

            # Add rest of attributes if any left
            if attrs:
                cell_pattern = td_pattern if item.startswith(
                    td_pattern) else th_pattern

                result[col] = mark_safe(
                    result[col].replace(cell_pattern,
                                 td_pattern + dict_to_attrs(attrs)))

    return results
