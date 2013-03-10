from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Examples for custom menu
    url(r'^admin/', include(admin.site.urls)),
)
