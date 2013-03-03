from django.contrib.admin.widgets import AdminTimeWidget, AdminDateWidget
from django.forms import TextInput
from django.utils.safestring import mark_safe
from django import forms
from django.utils.translation import ugettext as _


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
        if value.find('<') != 0:
            if value.find('icon-') == 0:
                value = '<i class="%s"></i>' % value
            return u'<span class="add-on">%s</span>' % value
        return value

    def render(self, name, value, attrs=None):
        output = super(EnclosedInput, self).render(name, value, attrs)
        div_classes = []
        if self.prepend:
            div_classes.append('input-prepend')
            self.prepend = self.enclose_value(self.prepend)
            output = u''.join((self.prepend, output))
        if self.append:
            div_classes.append('input-append')
            self.append = self.enclose_value(self.append)
            output = u''.join((output, self.append))

        return mark_safe(
            u'<div class="%s">%s</div>' % (' '.join(div_classes), output))

#
# Original date widgets with addition html
#
class SuitDateWidget(AdminDateWidget):
    def __init__(self, attrs=None, format=None):
        final_attrs = {'class': 'vDateField input-small',
                       'placeholder': _('Date:')[:-1]}
        if attrs is not None:
            final_attrs.update(attrs)
        super(SuitDateWidget, self).__init__(attrs=final_attrs, format=format)

    def render(self, name, value, attrs=None):
        output = super(SuitDateWidget, self).render(name, value, attrs)
        return mark_safe(
            u'<div class="input-append suit-date">%s<span '
            u'class="add-on"><i class="icon-calendar"></i></span></div>' %
            output)


class SuitTimeWidget(AdminTimeWidget):
    def __init__(self, attrs=None, format=None):
        final_attrs = {'class': 'vTimeField input-small',
                       'placeholder': _('Time:')[:-1]}
        if attrs is not None:
            final_attrs.update(attrs)
        super(SuitTimeWidget, self).__init__(attrs=final_attrs, format=format)

    def render(self, name, value, attrs=None):
        output = super(SuitTimeWidget, self).render(name, value, attrs)
        return mark_safe(
            u'<div class="input-append suit-date suit-time">%s<span '
            u'class="add-on"><i class="icon-time"></i></span></div>' %
            output)


class SuitSplitDateTimeWidget(forms.SplitDateTimeWidget):
    """
    A SplitDateTime Widget that has some admin-specific styling.
    """

    def __init__(self, attrs=None):
        widgets = [SuitDateWidget, SuitTimeWidget]
        forms.MultiWidget.__init__(self, widgets, attrs)

    def format_output(self, rendered_widgets):
        out_tpl = u'<div class="datetime">%s %s</div>'
        return mark_safe(out_tpl % (rendered_widgets[0], rendered_widgets[1]))
