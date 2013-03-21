from django import template
from django.contrib import admin
from django.core.handlers.wsgi import WSGIRequest
from django.core.urlresolvers import reverse
from suit.config import get_config

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
        self.conf_menu = get_config('MENU')

    def get_app_list(self):
        menu = None
        if self.conf_menu:
            menu = self.make_menu(self.conf_menu)
            # elif self.conf_menu_order:
        #     menu = self.make_menu_from_old_format(self.conf_menu_order)

        # Add icons and match active
        # if menu:
        #     self.activate_apps(menu)

        return menu

    def make_menu(self, config):
        menu = []
        for app in config:
            app = self.make_app(app)
            if app:
                menu.append(app)

        return menu

    def make_app(self, app_def):
        if isinstance(app_def, dict):
            app = app_def.copy()
        elif isinstance(app_def, str):
            app = self.make_app_from_native(app_def)
        else:
            raise TypeError('MENU list item must be string or dict. Got %s'
                            % repr(app_def))
        if app:
            return self.process_app(app)

    def process_app(self, app):

        if 'app' in app:
            app = self.process_semi_native_app(app)

        if not app:
            return

        self.ensure_app_keys(app)

        # Process app models
        app = self.process_models(app)

        # Set link from child
        models = app.get('models', [])
        if self.conf_open_first_child and models:
            if 'url' in app:
                app['orig_url'] = app['url']
            app['url'] = models[0]['url']

        return app

    def process_semi_native_app(self, app):
        """
        Process app defined as { app: 'app' }
        """
        app_from_native = self.make_app_from_native(app['app'])
        if app_from_native:
            del app['app']
            app_from_native.update(app)
            return app_from_native

    def make_app_from_native(self, app_name):
        app = self.find_native_app(app_name)
        if app:
            return self.convert_native_app(app, app_name)

    def find_native_app(self, app_name):
        for app in self.app_list:
            if app['name'].lower() == app_name:
                return app

    def convert_native_app(self, native_app, app_name):
        models = []
        native_models = native_app.get('models', {})
        if native_models:
            for model in native_models:
                models.append(self.convert_native_model(model))

        # Skip native apps with no models
        if not models:
            return

        app = {
            'label': native_app['name'],
            'url': native_app['app_url'],
            'models': models,
            'name': app_name
        }

        return app

    def process_models(self, app):
        models = []
        models_def = app.get('models', [])
        for model_def in models_def:
            self.make_model(model_def, app)

        app['models'] = models
        return app

    def make_model(self, model_def):
        if isinstance(model_def, dict):
            model = model_def.copy()
        elif isinstance(model_def, str):
            model = self.make_model_from_native(model_def)
        else:
            raise TypeError('MENU list item must be string or dict. Got %s'
                            % repr(model_def))
        if model:
            return self.process_model(model)

    def make_model_from_native(self, model_name):
        model = self.find_native_model(model_name)
        if model:
            return self.convert_native_app(model, model_name)

    def find_native_model(self, model_name):
        for native_model in self.all_models:
            if model_name == self.get_model_name(native_model,
                                                 '.' in model_name):
                return native_model

    def get_model_name(self, model, is_full_name=False):
        """
        Get model name by its last part of url
        """
        url_parts = model['admin_url'].rstrip('/').split('/')
        if is_full_name:
            return '.'.join(url_parts[-2:])
        return url_parts[-1]

    def convert_native_model(self, model):
        return {
            'label': model['name'],
            'url': model['admin_url'],
        }

    def process_model(self, model):
        if 'app' in model:
            model = self.process_semi_native_model(model)
        return self.ensure_model_keys(model)

    def ensure_app_keys(self, app):
        keys = ['label', 'url', 'icon', 'permissions']
        for key in keys:
            if key not in app:
                app[key] = None

    def ensure_model_keys(self, model):
        keys = ['label', 'url', 'permissions']
        for key in keys:
            if key not in model:
                model[key] = None
