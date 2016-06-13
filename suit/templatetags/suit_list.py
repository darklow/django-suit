from copy import copy

from django import template
from django.contrib.admin.templatetags.admin_list import result_list
from django.utils.safestring import mark_safe
from inspect import getargspec

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
