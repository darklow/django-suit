from django.conf.urls import patterns, include, url
from django.contrib import admin
from djangosuit import views

admin.autodiscover()

urlpatterns = patterns('',
    # Examples for custom menu
    url(r'^admin/custom/$', views.custom_view),
    url(r'^admin/', include(admin.site.urls)),
)
