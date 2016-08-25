import logging
from django import template
from django.http import HttpRequest
from suit.menu import MenuManager

register = template.Library()


@register.assignment_tag(takes_context=True)
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
                template_response = admin.site.index(request)
                available_apps = template_response.context_data['app_list']
            except Exception:
                pass

    if not available_apps:
        logging.warn('Django Suit was unable to retrieve apps list for menu.')
        return None

    return MenuManager(available_apps, context, request)
