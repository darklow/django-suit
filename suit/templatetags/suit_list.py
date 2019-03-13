from copy import copy
from django import template
from django.template import Context
from django.template.loader import get_template
from django.utils.safestring import mark_safe
from django.contrib.admin.views.main import SEARCH_VAR
from suit.apps import ALL_FIELDS
from suit.compat import parse_qs

register = template.Library()


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
    new_attrs = suit_row_attributes(**{'obj': instance, 'request': context.request})
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
def headers_handler(result_headers, cl):
    """
    Adds field name to css class, so we can style specific columns
    """
    # Django class attrib name
    attrib_key = 'class_attrib'

    suit_column_attributes = getattr(cl.model_admin, 'suit_column_attributes', None)
    if not suit_column_attributes:
        return result_headers

    for i, header in enumerate(result_headers):
        field_name = cl.list_display[i]
        attrs = copy(suit_column_attributes(field_name))
        if not attrs:
            continue

        # Validate
        if not isinstance(attrs, dict):
            raise TypeError('"suit_column_attributes" method must return dict. '
                            'Got: %s: %s' % (
                                attrs.__class__.__name__, attrs))

        classes = []
        defined_class = attrs.get('class')
        if defined_class:
            classes.append(defined_class)

        if attrib_key in header:
            existing_class = header[attrib_key].split('"')[1]
            if existing_class:
                classes.append(existing_class)

        if classes:
            attrs['class'] = ' '.join(classes)
            header[attrib_key] = dict_to_attrs(attrs)

    return result_headers


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
                raise TypeError('"suit_cell_attributes" method must return dict. '
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


def dict_to_attrs(attrs):
    return mark_safe(' ' + ' '.join(['%s="%s"' % (k, v)
                                     for k, v in attrs.items()]))


@register.inclusion_tag('suit/search_form.html')
def suit_search_form(cl):
    """
    Displays a search form for searching the list.
    """
    return {
        'cl': cl,
        'show_result_count': cl.result_count != cl.full_result_count,
        'search_var': SEARCH_VAR
    }


@register.simple_tag
def suit_admin_list_filter(cl, spec):
    if spec.template == 'admin/filter.html':
        spec.template = 'admin/filter_horizontal.html'

    tpl = get_template(spec.template)
    choices = list(spec.choices(cl))
    field_key = get_filter_id(spec)
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

    return tpl.render({
        'field_name': field_key,
        'title': spec.title,
        'choices': choices,
        'spec': spec,
    })


def _is_horizontal(horizontal_fields, field):
    return horizontal_fields == ALL_FIELDS or field in horizontal_fields

@register.filter
def suit_list_filter_vertical(filters, cl):
    filter_horizontal = getattr(cl.model_admin, 'suit_list_filter_horizontal', [])
    return [f for f in filters if not _is_horizontal(filter_horizontal, get_filter_id(f))]


@register.filter
def suit_list_filter_horizontal(filters, cl):
    filter_horizontal = getattr(cl.model_admin, 'suit_list_filter_horizontal', [])
    return [f for f in filters if _is_horizontal(filter_horizontal, get_filter_id(f))]


@register.filter
def suit_list_filter_horizontal_params(params, cl):
    # This collects params of vertical filters so they can be rendered as part of horizontal form
    excludes = ['_to_field', '_popup']
    vertical_keys = set()
    for vf in suit_list_filter_vertical(cl.filter_specs, cl):
        vertical_keys |= set(vf.expected_parameters())
    return [p for p in params if p[0] in vertical_keys or p[0] in excludes]


def get_filter_id(spec):
    try:
        return getattr(spec, 'field_path')
    except AttributeError:
        try:
            return getattr(spec, 'parameter_name')
        except AttributeError:
            pass
    return spec.title
