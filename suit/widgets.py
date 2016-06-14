from django import forms
from django.forms import Textarea, ClearableFileInput
from django.utils.safestring import mark_safe
from django.contrib.staticfiles.templatetags.staticfiles import static


class AutosizedTextarea(Textarea):
    """
    AutoSized TextArea - TextArea height dynamically grows based on user input
    """

    def __init__(self, attrs=None):
        new_attrs = _make_attrs(attrs, {"rows": 2}, "autosize form-control")
        super(AutosizedTextarea, self).__init__(new_attrs)

    @property
    def media(self):
        return forms.Media(js=[static("suit/js/autosize.min.js")])

    def render(self, name, value, attrs=None):
        output = super(AutosizedTextarea, self).render(name, value, attrs)
        output += mark_safe(
            "<script type=\"text/javascript\">django.jQuery(function () { autosize(document.getElementById('id_%s')); });</script>"
            % name)
        return output


class CharacterCountTextarea(AutosizedTextarea):
    """
    TextArea with character count. Supports also twitter specific count.
    """
    def render(self, name, value, attrs=None):
        output = super(CharacterCountTextarea, self).render(name, value, attrs)
        output += mark_safe(
            "<script type=\"text/javascript\">django.jQuery(function () { django.jQuery('#id_%s').suitCharactersCount(); });</script>"
            % name)
        return output


class ImageWidget(ClearableFileInput):
    def render(self, name, value, attrs=None):
        html = super(ImageWidget, self).render(name, value, attrs)
        if not value or not hasattr(value, 'url') or not value.url:
            return html
        html = u'<div class="ImageWidget"><div class="pull-xs-left"><a href="%s" target="_blank">' \
               u'<img src="%s" width="75"></a></div>' \
               u'%s</div>' % (value.url, value.url, html)
        return mark_safe(html)


def _make_attrs(attrs, defaults=None, classes=None):
    result = defaults.copy() if defaults else {}
    if attrs:
        result.update(attrs)
    if classes:
        result["class"] = " ".join((classes, result.get("class", "")))
    return result
