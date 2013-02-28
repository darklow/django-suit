Configuration
=============

You can customize Django Suit behaviour by adding ``SUIT_CONFIG`` configuration variable to your Django project ``settings.py`` file.::

  SUIT_CONFIG = {
      'PARAM': VALUE,
      'PARAM2': VALUE2
      ...
  }

Default values are the ones specified in examples.

Header
------

Header related parameters

ADMIN_NAME
^^^^^^^^^^

Admin name that will appear in header <title> tags and in footer::

  SUIT_CONFIG = {
      'ADMIN_NAME': 'Django Suit'
  }


HEADER_DATE_FORMAT
^^^^^^^^^^^^^^^^^^
HEADER_TIME_FORMAT
^^^^^^^^^^^^^^^^^^

Header date and time formats. Formatting according to `Django date templatefilter format <https://docs.djangoproject.com/en/dev/ref/templates/builtins/#std:templatefilter-date>`_. Default: as specified in example::

  SUIT_CONFIG = {
      'HEADER_DATE_FORMAT': 'l, j. F Y', # Saturday, 16th March 2013
      'HEADER_TIME_FORMAT': 'H:i',       # 18:42
  }

Forms
-----

SHOW_REQUIRED_ASTERISK
^^^^^^^^^^^^^^^^^^^^^^

Automatically adds asterisk symbol ``*`` to the end of every required field label::

  SUIT_CONFIG = {
      'SHOW_REQUIRED_ASTERISK': True
  }

CONFIRM_UNSAVED_CHANGES
^^^^^^^^^^^^^^^^^^^^^^^

Alert will be shown, when you'll try to leave page, without saving changed form first::

  SUIT_CONFIG = {
      'CONFIRM_UNSAVED_CHANGES': True
  }


Menu
-----

SEARCH_URL
^^^^^^^^^^

We have big plans for this field in the future, by making it global search field. However right now this field works only as a search redirect to any other urls of your admin::

  SUIT_CONFIG = {
      'SEARCH_URL': '/admin/user',

      # Parameter also accepts url name
      'SEARCH_URL': 'admin:auth_user_changelist',

      # Set to empty string if you want to hide search from menu
      'SEARCH_URL': ''
  }

MENU_OPEN_FIRST_CHILD
^^^^^^^^^^^^^^^^^^^^^

Automatically replaces app's (parent link) url with url of first model's url (child)::

  SUIT_CONFIG = {
      'MENU_OPEN_FIRST_CHILD': True
  }


MENU_ICONS
^^^^^^^^^^

Set app icons. Use any of Twitter Bootstrap `icon classes <http://twitter.github.com/bootstrap/base-css.html#icons>`_ or add your own. Twitter Bootstrap icons are provided by `Glyphicons <http://glyphicons.com/>`_::

  SUIT_CONFIG = {
      'MENU_ICONS': {
          'sites': 'icon-leaf',
          'auth': 'icon-lock',
      }
  }

MENU_EXCLUDE
^^^^^^^^^^^^

Exclude any of apps or models. You can exclude whole app or just one model from app::

  SUIT_CONFIG = {
      'MENU_EXCLUDE': ('auth.group', 'auth'),
  }


MENU_ORDER
^^^^^^^^^^

Most powerful of menu parameters. You can reorder, cross link, exclude, and even define custom menu items and child links. Here is full example of ``MENU_ORDER`` from simple existing app reorder to defining custom menu items::

  SUIT_CONFIG = {
      'MENU_ORDER': (

        # To reorder existing apps use following definition
        ('sites',),
        ('auth', ('user', 'group')),

        # If you want to link app models from different app use full name:
        ('sites', ('auth.user', 'auth.group')),

        # To add custom item, define it as tuple or list:
        # For parent: (Name, Link, Icon, Permission) - Last two are optional
        # For child: (Name, Link, Permission) - Last one is optional
        # You can also mix custom and native apps and models
        # Link can be absolute url or url name
        # Permission can be string or tuple/list for multiple
        # If MENU_OPEN_FIRST_CHILD=True and children exists, you can leave parent link blank

        # Example:
        (('Custom link', '/admin/custom/', 'icon-cog', ('auth.add_group',)),
         (
             ('Child 1', '/admin/child/', 'auth.add_user'),
             ('Child 2', '/admin/child2/')
         )
        )
      )
  }

Permissions are verified using `user.has_perms() <https://docs.djangoproject.com/en/dev/ref/contrib/auth/#django.contrib.auth.models.User.has_perm>`_ method.


List
-----

LIST_PER_PAGE
^^^^^^^^^^^^^

Set change_list view ``list_per_page`` parameter globally for whole admin. You can still override this parameter in any ModelAdmin class::

  SUIT_CONFIG = {
      'LIST_PER_PAGE': 20
  }

