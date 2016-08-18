Django Suit documentation
=========================

**Django Suit - Modern theme for Django admin interface**.

About
-----

Django Suit is alternative theme/skin/extension for `Django <http://www.djangoproject.com>`_ admin app (administration interface).

.. |master| image:: https://travis-ci.org/darklow/django-suit.png?branch=master
   :alt: Build Status - master branch
   :target: http://travis-ci.org/darklow/django-suit

Licence
-------

* Django Suit is licensed under `Creative Commons Attribution-NonCommercial 3.0 <http://creativecommons.org/licenses/by-nc/3.0/>`_ license.
* See licence and pricing: http://djangosuit.com/pricing/


Resources
---------

* Home page: http://djangosuit.com
* Demo: http://djangosuit.com/admin/
* Licence and Pricing: http://djangosuit.com/pricing/
* Github: https://github.com/darklow/django-suit
* Demo app on Github: https://github.com/darklow/django-suit-examples
* Changelog: `Changelog.rst <https://github.com/darklow/django-suit/blob/develop/CHANGELOG.rst>`_
* Supports: Django 1.4-1.10. Python: 2.6-3.4 |master|
* `Supported apps`_


Preview
-------

Click on screenshot for live demo:

  .. image:: https://raw.github.com/darklow/django-suit/develop/docs/_static/img/django-suit.png
     :alt: Django Suit Preview
     :target: http://djangosuit.com/admin/


Installation
============

1. You can get stable version of Django Suit by using pip or easy_install::

    pip install django-suit==0.2.21

2. You will need to add the ``'suit'`` application to the ``INSTALLED_APPS`` setting of your Django project ``settings.py`` file.::

    INSTALLED_APPS = (
        ...
        'suit',
        'django.contrib.admin',
    )

  .. important:: ``'suit'`` must be added before ``'django.contrib.admin'`` and if you are using third-party apps with special admin support (like django-cms) you also need to add ``'suit'`` before ``'cms'``.

3. You also need to add ``'django.core.context_processors.request'`` to ``TEMPLATE_CONTEXT_PROCESSORS`` setting in your Django project ``settings.py`` file.::

      from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP

      TEMPLATE_CONTEXT_PROCESSORS = TCP + (
          'django.core.context_processors.request',
      )

  Note: This is required to handle left side menu. If by some reason you removed original Django Suit ``menu.html``, you can skip this.


Deployment
----------

Deployment with Django Suit should not be different than any other Django application. If you have problems with deployment on production, read `Django docs on wsgi <https://docs.djangoproject.com/en/dev/howto/deployment/wsgi/modwsgi/>`_ first.

.. note:: If you deploy your project with Apache or ``Debug=False`` don't forget to run ``./manage.py collectstatic``


Develop branch
--------------

`Develop branch <https://github.com/darklow/django-suit/commits/develop>`_ is considered as release candidate version. Check `commits <https://github.com/darklow/django-suit/commits/develop>`_ and `changelog <https://github.com/darklow/django-suit/blob/develop/CHANGELOG.rst>`_ of develop branch first, before installing develop version. It is quite stable and always tested, but can contain some flaws or behaviour changes too. To install latest develop version use::

  pip uninstall django-suit
  pip install https://github.com/darklow/django-suit/tarball/develop


Bootstrap3 branch
-----------------

`BS3 branch <https://github.com/darklow/django-suit/commits/bs3>`_ is considered as alpha version and is not yet ready for production use. To install latest bs3 version use::

  pip install django-suit==0.3a1


Customization
=============

Configuration
-------------

You can customize Django Suit behaviour by adding ``SUIT_CONFIG`` configuration variable to your Django project ``settings.py`` file.

.. toctree::
   :maxdepth: 3

   configuration


Templates
---------

You must extend ``base_site.html`` template to customize footer links, copyright text or to add extra JS/CSS files. Example file is available on `github <https://github.com/darklow/django-suit/blob/master/suit/templates/admin/base_site.html>`_.

Copy customized ``base_site.html`` `template file <https://github.com/darklow/django-suit/blob/master/suit/templates/admin/base_site.html>`_ to your project's main application ``templates/admin/`` directory and un-comment and edit the blocks you would like to extend.

Alternatively you can copy ``base_site.html`` to any of template directories, which are defined in ``TEMPLATE_DIRS`` setting (if any). By default Django looks in every registered application ``templates/`` dir.

In the same way you can override any of Django Suit admin templates. More about customizing project's templates, you can read in `Django Admin Tutorial <https://docs.djangoproject.com/en/dev/intro/tutorial02/#customizing-your-project-s-templates>`_

Features
========

Widgets
-------

There are handy widgets included in Django Suit.

.. toctree::
   :maxdepth: 3

   widgets


Sortables
---------

Sortables are handy admin tools for ordering different lists.

.. toctree::
   :maxdepth: 3

   sortables


Form tabs
---------

Form tabs help you organize form fieldsets and inlines into tabs.

.. toctree::
   :maxdepth: 1

   form_tabs


Form includes
-------------

Django Suit provides handy shortcut to include templates into forms.

.. toctree::
   :maxdepth: 3

   form_includes


List attributes
---------------

Using few callable helpers you can customize change list row and cell attributes based on object instance variables.

.. toctree::
   :maxdepth: 3

   list_attributes


Wysiwyg editors
---------------

How to use wysiwyg editors in Django Suit.

.. toctree::
   :maxdepth: 3

   wysiwyg


JavaScript and CSS
------------------

.. toctree::
   :maxdepth: 3

   js_css


Support
=======

* Github: Use `django-suit github issues <https://github.com/darklow/django-suit/issues>`_, if you have any problems using Django Suit.


Examples
--------

Besides documentation examples, Django Suit `demo application <http://djangosuit.com/admin/>`_ source code is also available on separate github repository: `django-suit-examples <https://github.com/darklow/django-suit-examples>`_. If you see anything in demo application, you can always go to this repository and see implementation and code in one of ``models.py`` or ``admin.py`` files


Supported apps
--------------

Besides Django admin, Django Suit supports following third-party apps:

* `django-cms <https://github.com/divio/django-cms>`_ (v2.3.5 - v2.4.3) - `Example <http://djangosuit.com/admin/cms/page/>`_ `Read notes <https://github.com/darklow/django-suit/issues/77>`_
* `django-filer <https://github.com/stefanfoulis/django-filer>`_ (since v0.9.4) - `Example <http://djangosuit.com/admin/filer/folder/>`_
* `django-mptt <https://github.com/django-mptt/django-mptt/>`_ - `Example <http://djangosuit.com/admin/examples/category/>`_
* `django-reversion <https://github.com/etianen/django-reversion>`_ - `Example <http://djangosuit.com/admin/examples/reversioneditem/>`_
* `django-import-export <https://github.com/bmihelac/django-import-export>`_ - `Example <http://djangosuit.com/admin/examples/importexportitem/>`_
* Suggest other popular apps you would like to be supported `here <https://github.com/darklow/django-suit/issues/3>`_

.. important:: If you are using third-party apps with special admin support (like django-cms) you also need to add ``'suit'`` before ``'cms'`` in the list of ```INSTALLED_APPS``` in your ```settings.py``` file.


Contributing
============

.. toctree::
   :maxdepth: 3

   contributing
