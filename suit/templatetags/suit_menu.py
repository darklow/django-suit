from django import template
from django.core.handlers.wsgi import WSGIRequest
from suit.menu import MenuManager

register = template.Library()


@register.assignment_tag(takes_context=True)
def get_menu(context, request):
    """
    :type request: WSGIRequest
    """
    if not isinstance(request, WSGIRequest):
        return None

    available_apps = context.get('available_apps')
    if not available_apps:
        return None

    return MenuManager(available_apps, context, request)
