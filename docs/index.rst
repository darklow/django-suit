Django Suit documentation
=========================

**Modern theme for Django admin interface**.

Django Suit is theme/skin/extension for `Django <http://www.djangoproject.com>`_ administration interface.

Home page: http://djangosuit.com

Getting started
===============

You can get Django Suit by using pip or easy_install::

 pip install django-suit

or::

 easy_install django-suit


Installation
============

You will need to add the **suit** application to the INSTALLED_APPS
setting of your Django project *settings.py* file.::

  INSTALLED_APPS = (
      ...
      'suit',
      'django.contrib.admin',
  )

**Important**: must be added before admin 'django.contrib.admin'


Configuration
=============

You can customize Django Suit behaviour by adding following configuration
variable to your Django project *settings.py* file.::

  # Django Suit configuration example
  # Uncomment and change any of following keys
  SUIT_CONFIG = {
      # header
      # 'ADMIN_NAME': 'Django Suit',
      # 'HEADER_DATE_FORMAT': 'l, j. F Y',
      # 'HEADER_TIME_FORMAT': 'H:i',

      # forms
      # 'SHOW_REQUIRED_ASTERISK': True,  # Default True
      # 'CONFIRM_UNSAVED_CHANGES': True, # Default True

      # menu
      'SEARCH_URL': 'admin:auth_user_changelist',
      'MENU_ICONS': {
          'sites': 'icon-leaf',
          'auth': 'icon-lock',
      },
      # 'MENU_OPEN_FIRST_CHILD': True, # Default True
      # 'MENU_EXCLUDE': ('auth.group',),
      # 'MENU_ORDER': ( # Unlisted apps/models, will also be excluded
      #     ('sites',),
      #     ('auth', ('user','group')),
      # ),

      # misc
      'LIST_PER_PAGE': 15
  }


Customize template
==================

More documentation is on its way...
