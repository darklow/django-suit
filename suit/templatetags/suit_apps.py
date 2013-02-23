from django import template
from django.contrib import admin
from django.core.handlers.wsgi import WSGIRequest
import suit

register = template.Library()


@register.assignment_tag(takes_context=True)
def get_app_list(context, request):
    """
    :type request: WSGIRequest
    """
    if not isinstance(request, WSGIRequest):
        return None

    template_response = admin.site.index(request)
    try:
        app_list = template_response.context_data['app_list']
    except Exception:
        return

    try:
        current_app = context['app_label'].lower()
    except Exception:
        current_app = None

    try:
        curr_model_name_pl = context['opts'].verbose_name_plural.lower()
    except Exception:
        curr_model_name_pl = None

    exclude = suit.get_config('MENU_EXCLUDE')
    open_first_child = suit.get_config('MENU_OPEN_FIRST_CHILD')
    icons = suit.get_config('MENU_ICONS')
    menu_order = suit.get_config('MENU_ORDER')

    for app in app_list:
        app_name = app['name'].lower()

        # Exclude if in exclude list
        if exclude and app_name in exclude:
            app_list.remove(app)
            continue

        # Set icon if configured
        if icons and app_name in icons:
            app['icon'] = icons[app_name]

        # Mark as active by url or app name match
        if request.path == app['app_url'] or \
                        current_app == app_name:
            app['is_active'] = True

        # Iterate models
        for model in app['models']:

            # Exclude if in exclude list
            model_full_name = '%s.%s' % (app_name, get_model_name(model))
            if exclude and model_full_name in exclude:
                app['models'].remove(model)
                continue

            # Mark as active by url or model plural name match
            if request.path == model['admin_url'] or \
                            curr_model_name_pl == model['name'].lower():
                model['is_active'] = True

    # Reorder menu
    if menu_order:
        app_list = reorder_apps(app_list, menu_order)

    # Set first child url unless MENU_PARENT_LINK = True
    if open_first_child:
        for app in app_list:
            app['app_url'] = app['models'][0]['admin_url']

    return app_list


def reorder_apps(app_list, menu_order):
    new_apps = []
    for order in menu_order:
        app_name = order[0]
        models_order = order[1] if len(order) > 1 else None
        for app in app_list:
            if app['name'].lower() == app_name:
                new_apps.append(app)
                app_list.remove(app)
                if models_order:
                    reorder_app_models(app, models_order)
                break

    return new_apps


def reorder_app_models(app, model_order):
    new_models = []
    for model_name in model_order:
        for model in app['models']:
            if model_name == get_model_name(model):
                new_models.append(model)

    app['models'] = new_models


def get_model_name(model):
    """
    Get model name by its last part of url
    """
    return model['admin_url'].rstrip('/').split('/')[-1]
