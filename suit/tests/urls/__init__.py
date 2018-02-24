import django
from django.conf.urls import include, url
from django.contrib import admin

admin.autodiscover()

try:
    # Django 2.0+
    from django.urls import re_path

    urlpatterns = [
        re_path(r'^admin/', admin.site.urls),
    ]
except ImportError:
    try:
        from django.conf.urls import patterns
        urlpatterns = patterns(
            '',
            # Examples for custom menu
            url(r'^admin/', include(admin.site.urls)),
        )
    except ImportError:  # Django 1.10+
        urlpatterns = [
            url(r'^admin/', include(admin.site.urls)),
        ]
