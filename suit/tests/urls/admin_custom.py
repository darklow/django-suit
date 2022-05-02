from django.contrib import admin

admin.autodiscover()

# Examples for custom menu
try:
    from django.conf.urls import patterns, include, url
    urlpatterns = patterns('',
        url(r'^foo/bar/', include(admin.site.urls)),
    )
except ImportError:
    from django.urls import re_path
    urlpatterns = [
       re_path(r'^foo/bar/', include(admin.site.urls)),
   ]
