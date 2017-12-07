from copy import deepcopy
from django.utils.translation import ugettext_lazy as _


class ChildItem(object):
    def __init__(self, label=None, model=None, url=None, target_blank=False, permissions=None):
        self.label = label
        self.model = model
        self.url = url
        self.target_blank = target_blank
        self.permissions = permissions
        self.is_active = None
        self._is_forbidden = False
        self._parent_item = None
        self._url_name = None

    def _key(self):
        if self._parent_item and self.model and not '.' in self.model:
            return '.'.join([self._parent_item._key(), self.model])
        return self.model


class ParentItem(ChildItem):
    def __init__(self, label=None, app=None, url=None, target_blank=False, permissions=None,
                 children=None, align_right=False, use_first_child_url=True, icon=None):
        super(ParentItem, self).__init__(label, None, url, target_blank, permissions)
        self.user_children = children or []
        self.children = []
        self.align_right = align_right
        self.icon = icon
        self.app = app
        self.use_first_child_url = use_first_child_url

    def _key(self):
        return self.app


class MenuManager(object):
    def __init__(self, available_apps, context, request):
        from .config import get_config_instance, get_current_app

        super(MenuManager, self).__init__()

        # Variable available_apps structure:
        # https://docs.djangoproject.com/en/1.9/ref/contrib/admin/#adminsite-methods
        self.available_apps = available_apps

        self.context = context
        self.request = request
        self.current_app = get_current_app(request)
        self.suit_config = get_config_instance(self.current_app)
        self.user_menu = self.suit_config.menu
        self.menu_items = None
        self.aligned_right_menu_items = []
        self.active_parent_item = None
        self._available_apps = {'apps': {}, 'models': {}}

    def __iter__(self):
        for each in self.get_menu_items():
            yield each

    def get_menu_items(self):
        if self.menu_items is None:
            self.menu_items = self.build_menu()
            if self.suit_config.menu_handler:
                if not callable(self.suit_config.menu_handler):
                    raise TypeError('Django Suit "menu_handler" must callable')
                self.menu_items = self.suit_config.menu_handler(
                    self.menu_items, self.request, self.context)

        return self.menu_items

    def build_menu(self):
        if not self.user_menu:
            self.map_native_apps()
            return self.mark_active(self.build_menu_by_available_apps())

        self.map_native_apps()

        menu_items = []
        user_menu = deepcopy(self.user_menu)
        for parent_item in user_menu:
            native_app = self.find_native_app(parent_item)
            if parent_item.user_children:
                for child_item in parent_item.user_children:
                    child_item._parent_item = parent_item
                    native_model = self.find_native_model(native_app, child_item)
                    self.handle_child_menu(child_item, native_model)

                    # Add allowed children
                    if not child_item._is_forbidden:
                        parent_item.children.append(child_item)

            elif native_app:
                self.make_children_from_native_app(parent_item, native_app)

            self.handle_parent_menu(parent_item, native_app)

            # Add allowed items
            if not self.parent_item_is_forbidden(parent_item, native_app):
                menu_items.append(parent_item)

                if parent_item.align_right and self.suit_config.layout == 'horizontal':
                    self.aligned_right_menu_items.append(parent_item)

        if self.suit_config.menu_show_home:
            home_item = ParentItem(_('Home'), url='admin:index', icon='fa fa-home')
            menu_items.insert(0, self.handle_user_url(home_item))

        return self.mark_active(menu_items)

    def map_native_apps(self):
        """
        Make dictionary of native apps and models for easier matching
        """
        for native_app in self.available_apps:
            app_key = native_app['app_url'].split('/')[-2]
            self._available_apps['apps'][app_key] = native_app
            for native_model in native_app['models']:
                if 'admin_url' not in native_model:
                    # Can happen with incomplete permissions, like Delete only, etc.
                    continue
                model_key = '.'.join(native_model['admin_url'].split('/')[-3:-1])
                native_model['model'] = model_key
                self._available_apps['models'][model_key] = native_model
                model_key2 = '.'.join([app_key, native_model['object_name'].lower()])
                self._available_apps['models'][model_key2] = native_model

    def find_native_app(self, parent_item):
        """
        :type parent_item: ParentItem
        """
        return self._available_apps['apps'].get(parent_item._key())

    def find_native_model(self, native_app, child_item):
        """
        :type native_app: dict
        :type child_item: ChildItem
        """
        return self._available_apps['models'].get(child_item._key())

    def build_menu_by_available_apps(self):
        menu_items = []
        for native_app in self.available_apps:
            parent_item = self.make_parent_from_native_app(native_app)
            menu_items.append(parent_item)
            self.make_children_from_native_app(parent_item, native_app)
            if parent_item.children:
                parent_item.url = parent_item.children[0].url
        return menu_items

    def make_parent_from_native_app(self, native_app):
        """
        :type native_app: dict
        """
        parent_item = ParentItem(native_app['name'], url=native_app['app_url'])
        return parent_item

    def make_children_from_native_app(self, parent_item, native_app):
        """
        :type parent_item: ParentItem
        :type native_app: dict
        """
        for native_model in native_app['models']:
            child_item = self.make_child_from_native_model(native_model)
            parent_item.children.append(child_item)
            child_item._parent_item = parent_item

    def make_child_from_native_model(self, native_model):
        """
        :type native_model: dict
        """
        child_item = ChildItem(native_model['name'],  model=native_model.get('model'), url=native_model['admin_url'])
        return child_item

    def handle_parent_menu(self, parent_item, native_app):
        """
        :type parent_item: ParentItem
        :type native_app: dict
        """
        if not parent_item.label:
            parent_item.label = native_app['name'] if native_app else 'Untitled'
        if not parent_item.url:
            if parent_item.children and parent_item.use_first_child_url:
                parent_item.url = parent_item.children[0].url
            elif native_app:
                parent_item.url = native_app['app_url']
        else:
            self.handle_user_url(parent_item)

    def handle_child_menu(self, child_item, native_model):
        """
        :type child_item: ChildItem
        :type native_model: dict
        """
        # Handle permissions
        if self.child_item_is_forbidden(child_item, native_model):
            return

        # Handle label
        if not child_item.label:
            child_item.label = native_model['name'] if native_model else 'Untitled'

        # Handle URL
        if not child_item.url:
            if native_model:
                child_item.url = native_model['admin_url']
        else:
            self.handle_user_url(child_item)
        if not child_item.url:
            child_item.url = '#not-found'

    def handle_user_url(self, menu_item):
        """
        Evaluate user defined URL
        :type menu_item: ChildItem or ParentItem
        """
        if callable(menu_item.url):
            menu_item.url = menu_item.url(self.request, self.context)
            return menu_item
        if '/' in menu_item.url:
            return menu_item
        try:
            from django.urls import reverse, NoReverseMatch
        except:
            from django.core.urlresolvers import reverse, NoReverseMatch
        try:
            menu_item.url = reverse(menu_item.url, current_app=self.current_app)
            menu_item._url_name = menu_item.url
        except NoReverseMatch:
            pass
        return menu_item

    def parent_item_is_forbidden(self, parent_item, native_app):
        """
        :type parent_item: ParentItem
        """
        # Set as forbidden if model param specified but native_model not found
        if not parent_item.url and not parent_item.children:
            parent_item._is_forbidden = True
            return True

        return self.item_is_forbidden_by_custom_permissions(parent_item)

    def child_item_is_forbidden(self, child_item, native_model):
        """
        :type child_item: ChildItem
        """
        # Set as forbidden if model param specified but native_model not found
        if not child_item.url and not native_model:
            child_item._is_forbidden = True
            return True

        return self.item_is_forbidden_by_custom_permissions(child_item)

    def item_is_forbidden_by_custom_permissions(self, menu_item):
        """
        :type menu_item: ChildItem or ParentItem
        """
        if menu_item.permissions and \
                not self.user_has_permission(menu_item.permissions):
            menu_item._is_forbidden = True
            return True

    def user_has_permission(self, perms):
        perms = perms if isinstance(perms, (list, tuple)) else (perms,)
        return self.request.user.has_perms(perms)

    def mark_active(self, menu_items):
        active_child, active_child_by_url = None, None
        active_parent, active_parent_by_url = None, None

        # Represents: %s.%s % (opts.app_label, opts.app_model_name)
        opts_key = str(self.context.get('opts'))
        url_name = self.context.get('url_name')

        request_path = str(self.request.path)

        for parent_item in menu_items:
            if not active_child:
                for child_item in parent_item.children:
                    if opts_key == child_item._key():
                        active_child = child_item
                        break
                    elif not active_child_by_url and request_path == child_item.url:
                        active_child_by_url = child_item

            if active_child:
                break

            if not active_parent:
                if url_name and url_name == parent_item._url_name or request_path == parent_item.url:
                    active_parent = parent_item

        if not active_child:
            active_child = active_child_by_url

        if active_child:
            active_child.is_active = True
            active_parent = active_child._parent_item

        if active_parent:
            active_parent.is_active = True
            self.active_parent_item = active_parent

        return menu_items
