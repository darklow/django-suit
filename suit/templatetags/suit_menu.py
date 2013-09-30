from django import template
from django.contrib import admin
from django.core.handlers.wsgi import WSGIRequest
from django.core.urlresolvers import reverse
import warnings
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
        elif self.conf_menu_order:
            menu = self.make_menu_from_old_format(self.conf_menu_order)
        else:
            menu = self.make_menu_from_native_only()

        # Add icons and match active
        if menu:
            self.activate_menu(menu)

        return menu

    def make_menu(self, config):
        menu = []
        if not isinstance(config, (tuple, list)):
            raise TypeError('Django Suit MENU config parameter must be '
                            'tuple or list. Got %s' % repr(config))
        for app in config:
            app = self.make_app(app)
            if app:
                menu.append(app)

        return menu

    def make_app(self, app_def):
        if isinstance(app_def, dict):
            app = app_def.copy()
        elif isinstance(app_def, str):
            if app_def == '-':
                app = self.make_separator()
            else:
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

        # Process icons
        self.process_icons(app)

        # Ensure required keys for template are set
        self.ensure_app_keys(app)

        # Exclude apps
        if self.app_is_excluded(app):
            return

        # Handle app permissions
        if self.app_is_forbidden(app):
            return

        # Process app models
        self.process_models(app)

        # Set link from child
        models = app.get('models', [])
        if self.conf_open_first_child and models:
            app['orig_url'] = app['url']
            app['url'] = models[0]['url']

        # Process absolute/named/model type urls
        app['url'] = self.process_url(app['url'], app)

        return app


    def app_is_forbidden(self, app):
        return app['permissions'] and \
               not self.user_has_permission(app['permissions'])

    def app_is_excluded(self, app):
        return self.conf_exclude and app['name'] in self.conf_exclude

    def process_icons(self, app):
        """
        If icon key is present but value is '' or None, set empty 'icon-'
        If key not found, try to set icon from SUIT_ICONS
        """
        if 'icon' in app:
            app['icon'] = app['icon'] or 'icon-'
        elif self.conf_icons and 'name' in app and \
                        app['name'] in self.conf_icons:
            app['icon'] = self.conf_icons[app['name']]

    def process_semi_native_app(self, app):
        """
        Process app defined as { app: 'app' }
        """
        app_from_native = self.make_app_from_native(app['app'])
        if app_from_native:
            del app['app']
            app_from_native.update(app)
            return app_from_native

    def make_menu_from_native_only(self):
        menu = []
        for app in self.app_list:
            app_name = ''
            app_url = app.get('app_url')
            if app_url:
                app_url_parts = app['app_url'].split('/')
                if len(app_url_parts) > 1:
                    app_name = app_url_parts[-2]
            app = self.convert_native_app(app, app_name)
            if app:
                app = self.process_app(app)
            if app:
                menu.append(app)

        return menu

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
                models.append(self.convert_native_model(model, app_name))

        # Skip native apps with no models
        if not models:
            return

        return {
            'label': native_app['name'],
            'url': native_app['app_url'],
            'models': models,
            'name': app_name
        }

    def make_separator(self):
        return {
            'separator': True
        }

    def process_models(self, app):
        models = []
        models_def = app.get('models', [])
        for model_def in models_def:
            model = self.make_model(model_def, app['name'])
            if model:
                models.append(model)

        app['models'] = models

    def make_model(self, model_def, app_name):
        if isinstance(model_def, dict):
            model = model_def.copy()
        elif isinstance(model_def, str):
            model = self.make_model_from_native(model_def, app_name)
        else:
            raise TypeError('MENU list item must be string or dict. Got %s'
                            % repr(model_def))
        if model:
            return self.process_model(model, app_name)

    def make_model_from_native(self, model_name, app_name):
        model = self.find_native_model(model_name, app_name)
        if model:
            return self.convert_native_model(model, app_name)

    def find_native_model(self, model_name, app_name):
        model_name = self.get_model_name(app_name, model_name)
        for native_model in self.all_models:
            if model_name == self.get_native_model_name(native_model):
                return native_model

    def model_is_excluded(self, model_name):
        return self.conf_exclude and model_name in self.conf_exclude

    def get_model_name(self, app_name, model_name):
        if '.' not in model_name:
            model_name = '%s.%s' % (app_name, model_name)
        return model_name

    def get_native_model_name(self, model):
        """
        Get model name by its last part of url
        """
        url_parts = self.get_native_model_url(model).rstrip('/').split('/')
        root_url_parts = reverse('admin:index').rstrip('/').split('/')
        return '.'.join(url_parts[len(root_url_parts):][:2])

    def convert_native_model(self, model, app_name):
        return {
            'label': model['name'],
            'url': self.get_native_model_url(model),
            'name': self.get_native_model_name(model),
            'app': app_name
        }

    def get_native_model_url(self, model):
        return model.get('admin_url', model.get('add_url', ''))

    def process_model(self, model, app_name):
        if 'model' in model:
            model = self.process_semi_native_model(model, app_name)

        if model:
            self.ensure_model_keys(model)

            if 'app' in model and 'name' in model:
                model_name = self.get_model_name(model['app'], model['name'])

                if self.model_is_excluded(model_name):
                    return

            # Handle model permissions
            if self.model_is_forbidden(model):
                return

            # Detect if named url and convert it to absolute
            model['url'] = self.process_url(model['url'])

            return model

    def model_is_forbidden(self, model):
        return model['permissions'] and \
               not self.user_has_permission(model['permissions'])

    def process_semi_native_model(self, model, app_name):
        """
        Process app defined as { model: 'model' }
        """
        model_from_native = self.make_model_from_native(model['model'],
                                                        app_name)
        if model_from_native:
            del model['model']
            model_from_native.update(model)
            return model_from_native

    def ensure_app_keys(self, app):
        keys = ['label', 'url', 'icon', 'permissions', 'name', 'is_active',
                'blank']
        self.fill_keys(app, keys)

    def ensure_model_keys(self, model):
        keys = ['label', 'url', 'permissions', 'is_active', 'blank']
        self.fill_keys(model, keys)

    def fill_keys(self, dict, keys):
        for key in keys:
            if key not in dict:
                dict[key] = None

    def user_has_permission(self, perms):
        perms = perms if isinstance(perms, (list, tuple)) else (perms,)
        return self.request.user.has_perms(perms)

    def activate_menu(self, menu):
        for app in menu:

            # Make 'model' key as 'models' to unite activation logic
            if 'model' in app and not app['models']:
                app['models'] = [app['model']]

            # Activate models
            if app['models']:
                self.activate_models(app)

            # Mark as active by url match
            if not self.app_activated \
                and (self.request.path == app['url']
                     or self.request.path == app.get('orig_url')):
                app['is_active'] = self.app_activated = True

        if not self.app_activated:
            self.activate_menu_by_url(menu)

        # Last chance, try to activate by name
        if not self.app_activated:
            for app in menu:
                self.activate_models(app, match_by_name=True)

    def activate_models(self, app, match_by_name=False):
        for model in app['models']:
            if not match_by_name:
                # Mark as active by url or model plural name match
                model['is_active'] = self.request.path == model['url']
            else:
                model['is_active'] = self.ctx_model_plural == model[
                    'label'].lower()

            # Mark parent as active too
            if model['is_active'] and not self.app_activated:
                app['is_active'] = self.app_activated = True

    def activate_menu_by_url(self, menu):
        """
        If no active app/model is found in good/correct way, try to match
        by simple "startswith" in request path. Some apps doesn't provide
        nice app_label (django-filer for ex.) therefore this is the only way
        """
        for app in menu:
            for model in app['models']:
                if model['url'] and self.request.path.startswith(model['url']):
                    model['is_active'] = True
                    app['is_active'] = self.app_activated = True
                    break
            if self.app_activated:
                break

        # If still no active app found, match by app original url if any
        if not self.app_activated:
            for app in menu:
                orig_url = app.get('orig_url')
                if orig_url and self.request.path.startswith(orig_url):
                    app['is_active'] = self.app_activated = True

    def process_url(self, url, app=None):
        """
        Try to guess if it is absolute url or named
        """
        if url is None:
            return ''

        if not url or '/' in url:
            return url

        # Model link, ex: 'auth.user'
        if '.' in url:
            url_parts = url.split('.')
            model = self.make_model_from_native(url_parts[1], url_parts[0])
            if model:
                if app:
                    app['model'] = model
                return model['url']

        # Try to resolve as named url, ex: 'admin:index'
        try:
            return reverse(url)
        except:
            return url

    def make_menu_from_old_format(self, conf_order):
        import sys

        if 'test' not in sys.argv:
            warnings.warn(
                'Django Suit "MENU_ORDER" setting is deprecated. Use new "MENU"'
                ' key instead, see Documentation for new syntax.',
                DeprecationWarning)

        new_conf = []
        for order in conf_order:
            new_app = {}
            if isinstance(order, (tuple, list)):
                app_name = order[0]
                models_order = order[1] if len(order) > 1 else None
                if isinstance(app_name, str):
                    new_app['app'] = app_name
                elif isinstance(app_name, (tuple, list)):
                    mapping = ('label', 'url', 'icon', 'permissions')
                    for i, val in enumerate(app_name):
                        new_app[mapping[i]] = val
                if models_order and isinstance(models_order, (tuple, list)):
                    models = []
                    for model in models_order:
                        if isinstance(model, str):
                            models.append({'model': model})
                        elif isinstance(model, (list, tuple)):
                            mapping = ('label', 'url', 'permissions')
                            new_model = {}
                            for i, val in enumerate(model):
                                new_model[mapping[i]] = val
                            models.append(new_model)

                    new_app['models'] = models
            if new_app:
                new_conf.append(new_app)

        return self.make_menu(new_conf)
