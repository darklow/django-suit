from django import template
from django.utils.safestring import mark_safe
from suit import config
from suit.config import get_config

register = template.Library()


def get_form_size(fieldset):
    form_size_by_config = get_config('form_size')

    # Fallback to model admin definition
    form_size_by_model_admin = getattr(fieldset.model_admin, 'suit_form_size', {})

    form_size = {}
    form_size.update(form_size_by_config)
    form_size.update(form_size_by_model_admin)

    return form_size


def get_form_class(field, fieldset, idx):
    field_class, extra_class = [], ''
    form_size = get_form_size(fieldset)

    if not form_size:
        raise Exception('"form_size" parameter must be set in Django Suit config')

    # Try field config first
    if not field_class:
        form_size_fields = form_size.get('fields')
        if form_size_fields:
            field_class = form_size_fields.get(field.name)

    # Detect widget class
    try:
        widget_class_name = field.field.widget.__class__.__name__
        print widget_class_name
        # Add CSS class for field by widget name, for easier style targeting
        if idx == 1:
            extra_class = ' widget-%s' % widget_class_name
    except AttributeError:
        widget_class_name = None

    # Try widgets config
    if not field_class and widget_class_name:
        form_size_widgets = form_size.get('widgets')
        if form_size_widgets:
            field_class = form_size_widgets.get(widget_class_name)

    # Try fieldset config
    if not field_class:
        form_size_fieldset = form_size.get('fieldsets')
        if form_size_fieldset:
            field_class = form_size_fieldset.get(fieldset.name)

    # Fallback to default
    if not field_class:
        field_class = form_size.get('default')

    assert len(field_class), \
        'Django Suit form_size definitions must be tuples containing two string items'

    return field_class[idx] + extra_class


@register.filter
def suit_form_label_class(field, fieldset):
    """
    Get CSS class for form-row label column
    """
    return get_form_class(field, fieldset, 0)


@register.filter
def suit_form_field_class(field, fieldset):
    """
    Get CSS class for form-row field column
    """
    return get_form_class(field, fieldset, 1)
