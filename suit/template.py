from os.path import dirname, join, abspath
from django.template.loaders.filesystem import Loader as FilesystemLoader

_cache = {}


class Loader(FilesystemLoader):
    is_usable = True

    def get_template_sources(self, template_name, template_dirs=None):
        """
        Returns the absolute paths to "template_name" in the specified app.
        If the name does not contain an app name (no colon), an empty list
        is returned.
        The parent FilesystemLoader.load_template_source() will take care
        of the actual loading for us.
        """
        if not ':' in template_name:
            return []
        app_name, template_name = template_name.split(":", 1)
        template_dir = get_app_template_dir(app_name)
        if template_dir:
            return [join(template_dir, template_name)]
        else:
            return []


def get_app_template_dir(app_name):
    """Get the template directory for an application

    We do not use django.db.models.get_app, because this will fail if an
    app does not have any models.

    Returns a full path, or None if the app was not found.
    """
    from django.conf import settings
    from importlib import import_module
    if app_name in _cache:
        return _cache[app_name]
    template_dir = None
    for app in settings.INSTALLED_APPS:
        if app.split('.')[-1] == app_name:
            # Do not hide import errors; these should never happen at this point
            # anyway
            mod = import_module(app)
            template_dir = join(abspath(dirname(mod.__file__)), 'templates')
            break
    _cache[app_name] = template_dir
    return template_dir
