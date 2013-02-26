from django import template
from django.contrib import admin
from django.core.handlers.wsgi import WSGIRequest
from pprint import pprint
import suit

register = template.Library()


@register.assignment_tag(takes_context=True)
def get_menu(context, request):
    """
    :type request: WSGIRequest
    """
    if not isinstance(request, WSGIRequest):
        return None

    # Try to get app list
    template_response = admin.site.index(request)
    try:
        app_list = template_response.context_data['app_list']
    except Exception:
        return

    # Try to get verbose plural name of model
    try:
        curr_model_name_pl = context['opts'].verbose_name_plural.lower()
    except Exception:
        curr_model_name_pl = None

    all_models = [model for app in app_list for model in app['models']]
    exclude = suit.get_config('MENU_EXCLUDE')
    open_first_child = suit.get_config('MENU_OPEN_FIRST_CHILD')
    icons = suit.get_config('MENU_ICONS')
    menu_order = suit.get_config('MENU_ORDER')

    # Reorder menu first, so new hierarchy is present for marking active
    if menu_order:
        app_list = reorder_menu(app_list, menu_order, all_models, request)

    # Handle exclude and marking as active
    found_active_app = False
    for app in app_list:
        app_name = app['name'].lower()

        # Exclude if in exclude list
        if exclude and app_name in exclude:
            app_list.remove(app)
            continue

        # Set icon if configured
        if icons and app_name in icons:
            app['icon'] = icons[app_name]

        # Mark as active by url match
        if request.path == app['app_url'] and not found_active_app:
            app['is_active'] = found_active_app = True

        # Iterate models
        for model in app['models']:

            # Exclude if in exclude list
            model_full_name = '%s.%s' % (app_name, get_model_name(model))
            if exclude and model_full_name in exclude:
                app['models'].remove(model)
                continue

            # Mark as active by url or model plural name match
            model['is_active'] = request.path == model['admin_url']
            model['is_active'] |= curr_model_name_pl == model['name'].lower()

            # Mark parent as active too
            if model['is_active'] and not found_active_app:
                app['is_active'] = True

    # Set first child url unless MENU_OPEN_FIRST_CHILD = False
    if open_first_child:
        for app in app_list:
            if 'models' in app and len(app['models']) > 0:
                app['app_url'] = app['models'][0]['admin_url']

    return app_list


def reorder_menu(app_list, menu_order, all_models, request):
    new_apps = []
    for order in menu_order:
        final_app = None
        app_name = order[0]
        models_order = order[1] if len(order) > 1 else None

        # If custom app
        if isinstance(app_name, (list, tuple)):
            final_app = make_custom_app(app_name, request)
        else:
            # iterate and match django apps
            for app in app_list:
                if app['name'].lower() == app_name:
                    final_app = app
                    break

        if final_app:
            new_apps.append(final_app)

            if models_order:
                reorder_app_models(final_app, models_order, all_models, request)

    return new_apps


def reorder_app_models(app, model_order, all_models, request=None):
    new_models = []
    for model_name in model_order:
        # Custom link
        if isinstance(model_name, (list, tuple)):
            custom_link = make_custom_link(model_name, request)
            if custom_link:
                new_models.append(custom_link)
            continue

        # Append real model link
        for model in all_models:
            if model_name == get_model_name(model, '.' in model_name):
                new_models.append(model)

    app['models'] = new_models


def get_model_name(model, is_full_name=False):
    """
    Get model name by its last part of url
    """
    url_parts = model['admin_url'].rstrip('/').split('/')
    if is_full_name:
        return '.'.join(url_parts[-2:])
    return url_parts[-1]


def make_custom_app(app, request):
    app_len = len(app)
    if app_len < 2:
        raise IndexError(
            'Menu custom app must be list or tuple with at least two '
            'parameters: ('
            '"name", "url", "icon"=None)')

    custom_app = {'name': app[0], 'app_url': app[1], 'models': []}

    if app_len >= 3:
        custom_app['icon'] = app[2]

    # Check permissions if provided
    if app_len >= 4:
        if not user_has_permission(app[3], request):
            return

    return custom_app


def user_has_permission(perms, request):
    perms = perms if isinstance(perms, (list, tuple)) else (perms,)
    return request.user.has_perms(perms)


def make_custom_link(link, request):
    app_len = len(link)
    if app_len < 2:
        raise IndexError(
            'Menu custom app must be list or tuple with at least two '
            'parameters: ("name", "url")')

    # Check permissions if provided
    if app_len >= 3:
        if not user_has_permission(link[2], request):
            return

    return {'name': link[0], 'admin_url': link[1]}
