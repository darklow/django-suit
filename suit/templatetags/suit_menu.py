import logging

import django
from django import template
from django.contrib.admin import AdminSite
from django.http import HttpRequest
try:
    from django.urls import reverse, resolve
except:
    from django.core.urlresolvers import reverse, resolve
from suit.menu import MenuManager

register = template.Library()

if django.VERSION < (1, 9):
    simple_tag = register.assignment_tag
else:
    simple_tag = register.simple_tag


@simple_tag(takes_context=True)
def get_menu(context, request):
    """
    :type request: WSGIRequest
    """
    if not isinstance(request, HttpRequest):
        return None

    # Django 1.9+
    available_apps = context.get('available_apps')
    if not available_apps:

        # Django 1.8 on app index only
        available_apps = context.get('app_list')

        # Django 1.8 on rest of the pages
        if not available_apps:
            try:
                from django.contrib import admin
                template_response = get_admin_site(request.current_app).index(request)
                available_apps = template_response.context_data['app_list']
            except Exception:
                pass

    if not available_apps:
        logging.warn('Django Suit was unable to retrieve apps list for menu.')

    return MenuManager(available_apps, context, request)


def get_admin_site(current_app):
    """
    Method tries to get actual admin.site class, if any custom admin sites
    were used. Couldn't find any other references to actual class other than
    in func_closer dict in index() func returned by resolver.
    """
    try:
        resolver_match = resolve(reverse('%s:index' % current_app))
        # Django 1.9 exposes AdminSite instance directly on view function
        if hasattr(resolver_match.func, 'admin_site'):
            return resolver_match.func.admin_site

        for func_closure in resolver_match.func.__closure__:
            if isinstance(func_closure.cell_contents, AdminSite):
                return func_closure.cell_contents
    except:
        pass
    from django.contrib import admin
    return admin.site
