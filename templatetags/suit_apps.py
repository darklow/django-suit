from django import template
from django.contrib import admin

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
        current_model = context['opts'].verbose_name_plural.lower()
    except Exception:
        current_model = None

    for app in app_list:
        if request.path == app['app_url'] or \
                        current_app == app['name'].lower():
            app['is_active'] = True
            for model in app['models']:
                if request.path == model['admin_url'] or \
                                current_model == model['name'].lower():
                    model['is_active'] = True

    return app_list
