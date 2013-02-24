Django Suit documentation
=========================

**Modern theme for Django admin interface**.

Django Suit is theme/skin/extension for `Django <http://www.djangoproject.com>`_ administration interface.

Home page: http://djangosuit.com

Supports: Django 1.4/1.5c2

Getting started
===============

You can get Django Suit by using pip or easy_install::

 pip install django-suit

or::

 easy_install django-suit


Installation
============

You will need to add the **suit** application to the INSTALLED_APPS setting of your Django project *settings.py* file.::

  INSTALLED_APPS = (
      ...
      'suit',
      'django.contrib.admin',
  )

**Important**: must be added before admin 'django.contrib.admin'

You also need to add *'django.core.context_processors.request'* to TEMPLATE_CONTEXT_PROCESSORS setting in your Django project *settings.py* file.::

  from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP

  TEMPLATE_CONTEXT_PROCESSORS = TCP + (
      'django.core.context_processors.request',
  )

Note: This is required to handle left side menu. If by some reason you removed original Django Suit *menu.html*, you can skip this.

Configuration
=============

You can customize Django Suit behaviour by adding following configuration variable to your Django project *settings.py* file.::

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


More documentation about each configuration key is on its way...

Customize templates
===================

To customize footer links, copyright text and to add extra JS/CSS files - you must extend *base_site.html* template. To do this, copy this `base_site.html <https://github.com/darklow/django-suit/blob/master/suit/templates/admin/base_site.html>`_ template example file to your project's main application *template/admin/* directory and uncomment and edit the blocks you would like to extend.

Alternatively you can copy *base_site.html*
to any of template directories, which are defined in TEMPLATE_DIRS setting (if any). By default Django looks in every registered application *templates/* dir.

In same way you can override any of Django Suit and admin templates. More about customizing project's templates, you can read in `Django Admin Tutorial <https://docs.djangoproject.com/en/dev/intro/tutorial02/#customizing-your-project-s-templates>`_

**More documentation is on its way...**
