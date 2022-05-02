from django.contrib import admin

admin.autodiscover()

try:
    from django.conf.urls import patterns, include, url
    urlpatterns = patterns('',
        # Examples for custom menu
        url(r'^', include(admin.site.urls)),
    )
except ImportError:
    from django.urls import include, re_path

    urlpatterns = [
        re_path(r'^', include(admin.site.urls)),
    ]
