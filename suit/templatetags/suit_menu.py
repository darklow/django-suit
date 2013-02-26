from django import template
from django.contrib import admin
from django.core.handlers.wsgi import WSGIRequest
from django.core.urlresolvers import reverse
from suit import get_config

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

    return Menu(context, request, app_list).get_app_list()


class Menu(object):
    app_activated = False

    def __init__(self, context, request, app_list):
        self.request = request
        self.app_list = app_list

        # Detect current app, if any
        try:
            self.ctx_app = context['app_label'].lower()
        except Exception:
            self.ctx_app = None

        # Get current model plural name, if any
        try:
            self.ctx_model_plural = context['opts'].verbose_name_plural.lower()
        except Exception:
            self.ctx_model_plural = None

        # Flatten all models from native apps
        self.all_models = [model for app in app_list for model in app['models']]

        # Init config variables
        self.init_config()

        super(Menu, self).__init__()

    def init_config(self):
        self.conf_exclude = get_config('MENU_EXCLUDE')
        self.conf_open_first_child = get_config('MENU_OPEN_FIRST_CHILD')
        self.conf_icons = get_config('MENU_ICONS')
        self.conf_menu_order = get_config('MENU_ORDER')

    def get_app_list(self):

        # Reorder menu first, so new hierarchy is present for marking active
        if self.conf_menu_order:
            self.reorder_apps()

        # Exclude apps
        if self.conf_exclude:
            self.exclude_apps()

        # Add icons and match active
        self.activate_apps()

        return self.app_list

    def activate_apps(self):
        for app in self.app_list:
            app_name = app['name'].lower()

            # Set icon if configured
            if self.conf_icons and app_name in self.conf_icons:
                app['icon'] = self.conf_icons[app_name]

            # Mark as active by url match
            if self.request.path == app['app_url'] and not self.app_activated:
                app['is_active'] = self.app_activated = True

            # Activate and exclude app models
            self.activate_models(app)

            # Set first child url on app unless MENU_OPEN_FIRST_CHILD = False
            if self.conf_open_first_child:
                for app in self.app_list:
                    if 'models' in app and len(app['models']) > 0:
                        app['app_url'] = app['models'][0]['admin_url']

    def activate_models(self, app):
        # Iterate models
        for model in app['models']:
            app_name = app['name'].lower()

            # Exclude if in exclude list
            model_full_name = '%s.%s' % (app_name, self.get_model_name(model))
            if self.conf_exclude and model_full_name in self.conf_exclude:
                app['models'].remove(model)
                continue

            # Mark as active by url or model plural name match
            model['is_active'] = self.request.path == model['admin_url']
            model['is_active'] |= self.ctx_model_plural == model['name'].lower()

            # Mark parent as active too
            if model['is_active'] and not self.app_activated:
                app['is_active'] = True

    def exclude_apps(self):
        for app in self.app_list:
            if self.conf_exclude and app['name'].lower() in self.conf_exclude:
                self.app_list.remove(app)
            continue

    def reorder_apps(self):
        new_apps = []
        for order in self.conf_menu_order:
            final_app = None
            app_name = order[0]
            models_order = order[1] if len(order) > 1 else None

            # If custom app
            if isinstance(app_name, (list, tuple)):
                final_app = self.make_custom_app(app_name)
            else:
                # iterate and match django apps
                for app in self.app_list:
                    if app['name'].lower() == app_name:
                        final_app = app
                        break

            if final_app:
                new_apps.append(final_app)

                if models_order:
                    self.reorder_models(final_app, models_order)

        self.app_list = new_apps

    def reorder_models(self, app, models_order):
        new_models = []
        for model_name in models_order:
            # Custom link
            if isinstance(model_name, (list, tuple)):
                custom_link = self.make_custom_link(model_name)
                if custom_link:
                    new_models.append(custom_link)
                continue

            # Append real model link
            for model in self.all_models:
                if model_name == self.get_model_name(model, '.' in model_name):
                    new_models.append(model)

        app['models'] = new_models

    def make_custom_app(self, app):
        app_len = len(app)
        if app_len < 2:
            raise IndexError(
                'Menu custom app must be list or tuple with at least two '
                'parameters: ('
                '"name", "url", "icon"=None)')

        url = self.reverse_url(app[1])
        custom_app = {'name': app[0], 'app_url': url, 'models': []}

        if app_len >= 3:
            custom_app['icon'] = app[2]

        # Check permissions if provided
        if app_len >= 4:
            if not self.user_has_permission(app[3]):
                return

        return custom_app

    def make_custom_link(self, link):
        app_len = len(link)
        if app_len < 2:
            raise IndexError(
                'Menu custom app must be list or tuple with at least two '
                'parameters: ("name", "url")')

        # Check permissions if provided
        if app_len >= 3:
            if not self.user_has_permission(link[2]):
                return

        url = self.reverse_url(link[1])
        return {'name': link[0], 'admin_url': link[1]}

    def user_has_permission(self, perms):
        perms = perms if isinstance(perms, (list, tuple)) else (perms,)
        return self.request.user.has_perms(perms)

    def get_model_name(self, model, is_full_name=False):
        """
        Get model name by its last part of url
        """
        url_parts = model['admin_url'].rstrip('/').split('/')
        if is_full_name:
            return '.'.join(url_parts[-2:])
        return url_parts[-1]

    def reverse_url(self, url):
        if not url or '/' in url:
            return url
        try:
            return reverse(url)
        except:
            return url
