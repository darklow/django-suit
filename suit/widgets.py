from django.contrib.admin.widgets import AdminTimeWidget, AdminDateWidget
from django.forms import TextInput, Select, Textarea
from django.utils.safestring import mark_safe
from django import forms
from django.utils import formats, translation
from django.utils.translation import ugettext as _
from django.contrib.admin.templatetags.admin_static import static
from suit import utils


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
        cls = 'addon'
        if value.startswith("<"):
            cls = 'btn'
        if value.startswith("glyphicon-"):
            value = '<i class="glyphicon %s"></i>' % value
        return '<span class="input-group-%s">%s</span>' % (cls, value)

    def render(self, name, value, attrs=None):
        output = super(EnclosedInput, self).render(name, value, attrs)
        div_classes = []
        if self.prepend:
            # div_classes.append('input-prepend')
            self.prepend = self.enclose_value(self.prepend)
            output = ''.join((self.prepend, output))
        if self.append:
            # div_classes.append('input-append')
            self.append = self.enclose_value(self.append)
            output = ''.join((output, self.append))

        return mark_safe(
            '<div class="input-group %s">%s</div>' % (
                ' '.join(div_classes), output))


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

    def render(self, name, value, attrs=None):
        output = super(AutosizedTextarea, self).render(name, value, attrs)
        output += mark_safe(
            "<script type=\"text/javascript\">Suit.$('#id_%s').autosize("
            ");</script>"
            % name)
        return output


class SuitDateWidget(forms.DateInput):
    @property
    def media(self):
        js = ['datepicker/bootstrap-datepicker.js']
        dp_lang = self.language()
        if dp_lang != 'en':
            js.append('datepicker/locales/bootstrap-datepicker.%s.js' % dp_lang)
        return forms.Media(
            js=[static("suit/js/%s" % path) for path in js],
            css={'all': [static("suit/js/datepicker/css/datepicker3.css")]}
        )

    def __init__(self, attrs=None, format=None):
        attrs = attrs or {}
        self.format = format
        super(SuitDateWidget, self).__init__(attrs=attrs, format=format)

    def language(self):
        lang = str(translation.get_language() or 'en').lower()
        dp_lang = lang
        if lang.startswith('zh-'):
            dp_lang = {
                'zh-cn': 'zh-CN',
                'zh-tw': 'zh-TW'
            }.get(lang, 'en')
        return dp_lang

    def date_format(self):
        return self.format or formats.get_format(self.format_key)[0]

    def datepicker_date_format(self, django_format):
        # django_format = django_format.replace('%', '')
        print django_format
        mapping = {
            '%Y': 'yyyy',
            '%y': 'yy',
            '%m': 'mm',
            '%b': 'M',  # Oct, Nov
            '%B': 'MM',  # October, November
            '%d': 'dd',
            '%M': 'i',
            '%S': 's',
            '.%f': '',  # Microseconds are not supported by datepicker
        }
        for dj_fmt, dp_fmt in mapping.items():
            django_format = django_format.replace(dj_fmt, dp_fmt)

        django_format = django_format.replace('%', '')
        return django_format

    def render(self, name, value, attrs=None):
        output = super(SuitDateWidget, self).render(name, value, attrs)

        # Because we wrap input tag in input-group we must copy data-* attrs
        # for datepicker formats
        attrs = utils.attrs_by_prefix(output, 'data-date-')
        if 'data-date-format' not in attrs:
            attrs['data-date-format'] = self.datepicker_date_format(
                self.date_format())

        attrs = utils.dict_to_attrs(attrs)

        return mark_safe(
            '<div class="input-group date" %s>%s<span '
            'class="input-group-addon"><i class="glyphicon '
            'glyphicon-th"></i></span></div>' % (
                attrs, output))


class SuitDateTimeWidget(forms.DateTimeInput, SuitDateWidget):
    def __init__(self, attrs=None, format=None):
        self.format = format
        attrs = attrs or {}
        attrs['data-date-show-time'] = 'true'
        super(SuitDateTimeWidget, self).__init__(attrs, format)


class SuitTimeWidget(AdminTimeWidget):
    def __init__(self, attrs=None, format=None):
        defaults = {'placeholder': _('Time:')[:-1]}
        new_attrs = _make_attrs(attrs, defaults, "vTimeField input-small")
        super(SuitTimeWidget, self).__init__(attrs=new_attrs, format=format)

    def render(self, name, value, attrs=None):
        output = super(SuitTimeWidget, self).render(name, value, attrs)
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

    def format_output(self, rendered_widgets):
        out_tpl = '<div class="datetime">%s %s</div>'
        return mark_safe(out_tpl % (rendered_widgets[0], rendered_widgets[1]))


def _make_attrs(attrs, defaults=None, classes=None):
    result = defaults.copy() if defaults else {}
    if attrs:
        result.update(attrs)
    if classes:
        result["class"] = " ".join((classes, result.get("class", "")))
    return result
