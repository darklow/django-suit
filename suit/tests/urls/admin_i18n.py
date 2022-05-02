from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin

admin.autodiscover()

try:
    from django.conf.urls import include, url
    urlpatterns = i18n_patterns('',
        # Examples for custom menu
        url(r'^admin/', include(admin.site.urls)),
    )
except ImportError:
    from django.urls import re_path

    urlpatterns = i18n_patterns('',
        # Examples for custom menu
        re_path(r'^admin/', include(admin.site.urls)),
    )
