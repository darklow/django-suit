from django.contrib.admin.widgets import AdminTimeWidget, AdminDateWidget
from django.forms import TextInput, Select, Textarea
from django.utils.safestring import mark_safe
from django import forms
from django.utils.translation import ugettext as _
from django.contrib.admin.templatetags.admin_static import static

from suit import utils

django_version = utils.django_major_version()


class NumberInput(TextInput):
    """
    HTML5 Number input
    Left for backwards compatibility
    """
    input_type = 'number'


class HTML5Input(TextInput):
    """
    Supports any HTML5 input
    http://www.w3schools.com/html/html5_form_input_types.asp
    """

    def __init__(self, attrs=None, input_type=None):
        self.input_type = input_type
        super(HTML5Input, self).__init__(attrs)


#
class LinkedSelect(Select):
    """
    Linked select - Adds link to foreign item, when used with foreign key field
    """

    def __init__(self, attrs=None, choices=()):
        attrs = _make_attrs(attrs, classes="linked-select")
        super(LinkedSelect, self).__init__(attrs, choices)


class EnclosedInput(TextInput):
    """
    Widget for bootstrap appended/prepended inputs
    """

    def __init__(self, attrs=None, prepend=None, append=None):
        """
        For prepend, append parameters use string like %, $ or html
        """
        self.prepend = prepend
        self.append = append
        super(EnclosedInput, self).__init__(attrs=attrs)

    def enclose_value(self, value):
        """
        If value doesn't starts with html open sign "<", enclose in add-on tag
        """
        if value.startswith("<"):
            return value
        if value.startswith("icon-"):
            value = '<i class="%s"></i>' % value
        return '<span class="add-on">%s</span>' % value

    def render(self, name, value, attrs=None, renderer=None):
        if django_version < (2, 0):
            output = super(EnclosedInput, self).render(name, value, attrs)
        else:
            output = super(EnclosedInput, self).render(name, value, attrs, renderer)

        div_classes = []
        if self.prepend:
            div_classes.append('input-prepend')
            self.prepend = self.enclose_value(self.prepend)
            output = ''.join((self.prepend, output))
        if self.append:
            div_classes.append('input-append')
            self.append = self.enclose_value(self.append)
            output = ''.join((output, self.append))

        return mark_safe(
            '<div class="%s">%s</div>' % (' '.join(div_classes), output))


class AutosizedTextarea(Textarea):
    """
    Autosized Textarea - textarea height dynamically grows based on user input
    """

    def __init__(self, attrs=None):
        new_attrs = _make_attrs(attrs, {"rows": 2}, "autosize")
        super(AutosizedTextarea, self).__init__(new_attrs)

    @property
    def media(self):
        return forms.Media(js=[static("suit/js/jquery.autosize-min.js")])

    def render(self, name, value, attrs=None, renderer=None):
        if django_version < (2, 0):
            output = super(AutosizedTextarea, self).render(name, value, attrs)
        else:
            output = super(AutosizedTextarea, self).render(name, value, attrs, renderer)

        output += mark_safe(
            "<script type=\"text/javascript\">Suit.$('#id_%s').autosize();</script>"
            % name)
        return output


#
# Original date widgets with addition html
#
class SuitDateWidget(AdminDateWidget):
    def __init__(self, attrs=None, format=None):
        defaults = {'placeholder': _('Date:')[:-1]}
        new_attrs = _make_attrs(attrs, defaults, "vDateField input-small")
        super(SuitDateWidget, self).__init__(attrs=new_attrs, format=format)

    def render(self, name, value, attrs=None, renderer=None):
        if django_version < (1, 11):
            output = super(SuitDateWidget, self).render(name, value, attrs)
        else:
            output = super(SuitDateWidget, self).render(name, value, attrs, renderer)
        return mark_safe(
            '<div class="input-append suit-date">%s<span '
            'class="add-on"><i class="icon-calendar"></i></span></div>' %
            output)


class SuitTimeWidget(AdminTimeWidget):
    def __init__(self, attrs=None, format=None):
        defaults = {'placeholder': _('Time:')[:-1]}
        new_attrs = _make_attrs(attrs, defaults, "vTimeField input-small")
        super(SuitTimeWidget, self).__init__(attrs=new_attrs, format=format)

    def render(self, name, value, attrs=None, renderer=None):
        if django_version < (2, 0):
            output = super(SuitTimeWidget, self).render(name, value, attrs)
        else:
            output = super(SuitTimeWidget, self).render(name, value, attrs, renderer)
        return mark_safe(
            '<div class="input-append suit-date suit-time">%s<span '
            'class="add-on"><i class="icon-time"></i></span></div>' %
            output)


class SuitSplitDateTimeWidget(forms.SplitDateTimeWidget):
    """
    A SplitDateTime Widget that has some admin-specific styling.
    """

    def __init__(self, attrs=None):
        widgets = [SuitDateWidget, SuitTimeWidget]
        forms.MultiWidget.__init__(self, widgets, attrs)

    if django_version < (1, 11):
        def format_output(self, rendered_widgets):
            out_tpl = '<div class="datetime">%s %s</div>'
            return mark_safe(out_tpl % (rendered_widgets[0], rendered_widgets[1]))
    else:
        def render(self, name, value, attrs=None, renderer=None):
            output = super(SuitSplitDateTimeWidget, self).render(name, value, attrs, renderer)
            return mark_safe('<div class="datetime">%s</div>' % output)


def _make_attrs(attrs, defaults=None, classes=None):
    result = defaults.copy() if defaults else {}
    if attrs:
        result.update(attrs)
    if classes:
        result["class"] = " ".join((classes, result.get("class", "")))
    return result
