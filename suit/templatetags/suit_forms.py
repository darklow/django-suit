from django import template
from django.contrib.admin.widgets import ForeignKeyRawIdWidget, \
    RelatedFieldWidgetWrapper
from django.forms.widgets import Input, Textarea, Select
from django.utils.safestring import mark_safe
from suit.config import get_config
from suit.widgets import adjust_widget

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
    adjustable_widgets = (
        Input, Textarea, ForeignKeyRawIdWidget, RelatedFieldWidgetWrapper,
        Select)
    if not hasattr(field, 'field') or \
                    not isinstance(field.field.widget, adjustable_widgets):
        return field
    field = adjust_widget(field)
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
    Return classes for form-column
    """
    css_classes = []
    default_class = get_form_size(fieldset)[1]

    css_classes.append('form-column')

    if not hasattr(field.field, 'field'):
        css_classes.append(default_class)
        return ' '.join(css_classes)

    widget_py_cls = field.field.field.widget.__class__.__name__
    css_classes.append('widget-%s' % widget_py_cls)
    if 'RawIdWidget' in widget_py_cls:
        css_classes.append('form-inline')

    class_by_widget = field.field.field.widget.attrs.get('column_class')
    if class_by_widget:
        del field.field.field.widget.attrs['column_class']
        css_classes.append(class_by_widget)
    else:
        css_classes.append(default_class)

    return ' '.join(css_classes)


@register.filter()
def line_errors_as_data(line):
    if not line.errors:
        return None

    errs = []
    for f in line.fields:
        if f in line.readonly_fields:
            continue
        errs += line.form[f].errors.as_data()
    return errs