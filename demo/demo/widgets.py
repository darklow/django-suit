from django.conf import settings
from django.forms import forms
from django.contrib.staticfiles.templatetags.staticfiles import static


class Bootstrap4Select(object):
    def build_attrs(self, extra_attrs=None, **kwargs):
        attrs = super(Bootstrap4Select, self).build_attrs(extra_attrs, **kwargs)
        attrs.setdefault('data-theme', 'bootstrap')
        return attrs

    def _get_media(self):
        """
        Construct Media as a dynamic property.
        .. Note:: For more information visit
            https://docs.djangoproject.com/en/1.8/topics/forms/media/#media-as-a-dynamic-property
        """
        return forms.Media(
            js=(
                settings.SELECT2_JS,
                static('django_select2/django_select2.js'),
            ),
            css={'screen': (
                settings.SELECT2_CSS,
                # static('css/select2-bootstrap.css'),
                '//cdnjs.cloudflare.com/ajax/libs/select2-bootstrap-theme/0.1.0-beta.6/select2-bootstrap.min.css',)}
        )

    media = property(_get_media)
