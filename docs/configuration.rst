Configuration
=============

You can customize Django Suit behaviour by adding ``SUIT_CONFIG`` configuration variable to your Django project ``settings.py`` file.::

  SUIT_CONFIG = {
      'PARAM': VALUE,
      'PARAM2': VALUE2
      ...
  }

Default values are the ones specified in examples.

Full example
------------

Configuration sample you can use as a start::

  # Django Suit configuration example
  SUIT_CONFIG = {
      # header
      # 'ADMIN_NAME': 'Django Suit',
      # 'HEADER_DATE_FORMAT': 'l, j. F Y',
      # 'HEADER_TIME_FORMAT': 'H:i',

      # forms
      # 'SHOW_REQUIRED_ASTERISK': True,  # Default True
      # 'CONFIRM_UNSAVED_CHANGES': True, # Default True

      # menu
      # 'SEARCH_URL': '/admin/auth/user/',
      # 'MENU_ICONS': {
      #    'sites': 'icon-leaf',
      #    'auth': 'icon-lock',
      # },
      # 'MENU_OPEN_FIRST_CHILD': True, # Default True
      # 'MENU_EXCLUDE': ('auth.group',),
      # 'MENU': (
      #     'sites',
      #     {'app': 'auth', 'icon':'icon-lock', 'models': ('user', 'group')},
      #     {'label': 'Settings', 'icon':'icon-cog', 'models': ('auth.user', 'auth.group')},
      #     {'label': 'Support', 'icon':'icon-question-sign', 'url': '/support/'},
      # ),

      # misc
      # 'LIST_PER_PAGE': 15
  }


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
----

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

Set app icons. Use any of Twitter Bootstrap `icon classes <http://twitter.github.com/bootstrap/base-css.html#icons>`_ or add your own. Twitter Bootstrap icons are provided by `Glyphicons <http://glyphicons.com/>`_. This parameter is useful, if you don't use ``MENU`` parameter (see below) and just want to set icons for default apps::

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


.. note:: This parameter excludes appp/model only from menu, it doesn't protect from accessing it by url or from app list. Use django user permissions to securely protect app/model.


MENU_ORDER
^^^^^^^^^^

`MENU_ORDER parameter <http://django-suit.readthedocs.org/en/0.1.7/configuration.html#menu-order>`_ is deprecated - use ``MENU`` instead.

MENU
^^^^

Most powerful of menu parameters - one parameter to rule them all :) You can rename, reorder, cross link, exclude apps and models, and even define custom menu items and child links.

Following keys are available for each app and model level links:

* App: ``app``, ``label``, ``url``, ``icon``, ``permissions``, ``blank``
* Model: ``model``, ``label``, ``url``, ``permissions``, ``blank``
* Use ``-`` as separator between apps

``url`` parameter can be:

* Absolute url like ``/custom/``
* Named url like ``admin:index``
* Model name like ``auth.user`` to make link to model changelist
* If ``MENU_OPEN_FIRST_CHILD=True`` and models for app exists, you can skip ``url`` key
* If you add key ``'blank': True`` links will open in new window

``permissions`` are verified using `user.has_perms() <https://docs.djangoproject.com/en/dev/ref/contrib/auth/#django.contrib.auth.models.User.has_perm>`_ method.

A custom application can contain a ``models`` list (or tuple) to customize the application models
list. The ``models`` list can contain model references and model definitions. The model reference
is a string referencing to the model through the application label and model name. The model
name may be globbed to reference all models in the application like 'auth.*'.

Here is full example of ``MENU`` from simple existing app reorder to defining custom menu items::

  SUIT_CONFIG = {
      'MENU': (

          # Keep original label and models
          'sites',

          # Rename app and set icon
          {'app': 'auth', 'label': 'Authorization', 'icon':'icon-lock'},

          # Reorder app models
          {'app': 'auth', 'models': ('user', 'group')},

          # Custom app, with models
          {'label': 'Settings', 'icon':'icon-cog', 'models': ('auth.user', 'auth.group')},

          # Cross-linked models with custom name; Hide default icon
          {'label': 'Custom', 'icon':None, 'models': (
              'auth.group',
              {'model': 'auth.user', 'label': 'Staff'}
          )},

          # Custom app, no models (child links)
          {'label': 'Users', 'url': 'auth.user', 'icon':'icon-user'},

          # Separator
          '-',

          # Custom app and model with permissions
          {'label': 'Secure', 'permissions': 'auth.add_user', 'models': [
              {'label': 'custom-child', 'permissions': ('auth.add_user', 'auth.add_group')}
          ]},
      )
  }



List
----

LIST_PER_PAGE
^^^^^^^^^^^^^

Set change_list view ``list_per_page`` parameter globally for whole admin. You can still override this parameter in any ModelAdmin class::

  SUIT_CONFIG = {
      'LIST_PER_PAGE': 20
  }

