from django import template
from django.contrib import admin
import suit

register = template.Library()


@register.assignment_tag(takes_context=True)
def get_app_list(context, request):
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
    menu_parent_link = suit.get_config('MENU_PARENT_LINK')
    for app in app_list:
        app_name = app['name'].lower()

        # Exclude if in exclude list
        if exclude and app_name in exclude:
            app_list.remove(app)
            continue

        if request.path == app['app_url'] or \
                        current_app == app_name:
            app['is_active'] = True

        if not menu_parent_link:
            app['app_url'] = app['models'][0]['admin_url']

        # Iterate models
        for model in app['models']:
            model_url = model['admin_url']

            # Get model name by url last part
            # Exclude if in exclude list
            model_name = model_url.rstrip('/').split('/')[-1]
            model_full_name = '%s.%s' % (app_name, model_name)

            if exclude and model_full_name in exclude:
                app['models'].remove(model)
                continue

            model_name_pl = model['name'].lower()
            if request.path == model_url or \
                            curr_model_name_pl == model_name_pl:
                model['is_active'] = True

    return app_list
