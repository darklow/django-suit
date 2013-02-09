from django.contrib.admin.widgets import AdminTimeWidget, AdminDateWidget
from django.forms import DateInput
from django.utils.safestring import mark_safe
from django import forms
from django.utils.translation import ugettext as _


class DatePicker(DateInput):
    """
    Simple html wrapper for DateInput
    """

    def __init__(self, attrs=None, format=None):
        if not attrs: attrs = {}
        if not attrs.has_key('class'): attrs['class'] = ''
        attrs['class'] += '  input-small'
        super(DatePicker, self).__init__(attrs, format)


    def render(self, name, value, attrs=None):
        output = super(DatePicker, self).render(name, value, attrs)
        return mark_safe(
            u'<div class="input-append date datepicker">%s<span '
            u'class="add-on"><i class="icon-calendar"></i></span></div>' %
            output)


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
        final_attrs = {'class': 'vTimeField input-small', 'placeholder': _('Time:')[:-1]}
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
        return mark_safe(u'<div class="datetime">%s %s</div>' % \
                         (rendered_widgets[0], rendered_widgets[1]))
