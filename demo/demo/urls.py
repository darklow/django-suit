"""demo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import RedirectView

from . import views

urlpatterns = [

    # Django Suit custom admin view
    url(r'^admin/custom/$', views.custom_admin_view),

    url(r'^admin/', admin.site.urls),

    # Django-Select2
    url(r'^select2/', include('django_select2.urls')),

    # Documentation url for menu documentation link
    url(r'^admin/custom2/', RedirectView.as_view(url='http://djangosuit.com/support/'), name='django-admindocs-docroot'),

    url(r'^$', views.home, name='home'),
]
