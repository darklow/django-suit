from django import template
from django.forms.widgets import Input, Textarea
from suit.config import get_config

register = template.Library()


def get_form_size(fieldset):
    default_label_class = get_config('form_size').split(':')

    # Try fieldset definition at first
    size_by_fieldset = get_fieldset_size(fieldset)
    if size_by_fieldset:
        return size_by_fieldset

    # Fallback to model admin definition
    ma_sizes = getattr(fieldset.model_admin, 'suit_form_size', None)
    if ma_sizes:
        return ma_sizes.split(':')

    # Use default values at last
    return default_label_class


def get_fieldset_size(fieldset):
    if fieldset and fieldset.classes and ':' in fieldset.classes:
        for cls in fieldset.classes.split(' '):
            if ':' in cls:
                return cls.split(':')


@register.filter
def suit_form_field(field):
    if not hasattr(field, 'field') or \
            not isinstance(field.field.widget, (Input, Textarea)):
        return field
    field.field.widget.attrs['class'] = \
        '%s form-control' % field.field.widget.attrs.get('class', '')
    return field


@register.filter
def suit_form_label_class(field, fieldset):
    default_class = get_form_size(fieldset)[0]
    if not hasattr(field, 'field'):
        return default_class

    label_class = field.field.widget.attrs.get('label_class')
    if label_class:
        return label_class

    return default_class


@register.filter
def suit_form_field_class(field, fieldset):
    """
    Return all classes with "col-" prefix
    """
    default_class = get_form_size(fieldset)[1]
    if not hasattr(field, 'field'):
        return default_class

    widget_class = field.field.widget.attrs.get('class')
    if widget_class:
        width_classes = [c for c in widget_class.split(' ')
                         if c.startswith('col-')]
        if width_classes:
            return ' '.join(width_classes)

    return default_class
