Django Suit documentation
=========================

**Modern theme for Django admin interface**.

Django Suit is alternative theme/skin/extension for `Django <http://www.djangoproject.com>`_ administration interface.

About
=====

* Home page: http://djangosuit.com
* Demo: http://djangosuit.com/admin/
* Licence and Pricing: http://djangosuit.com/pricing/
* Github: https://github.com/darklow/django-suit
* Demo app on Github: https://github.com/darklow/django-suit-examples
* Changelog: `Changelog.rst <https://github.com/darklow/django-suit/blob/master/CHANGELOG.rst>`_
* Supports: Django 1.4/1.5c2

Installation
============

1. You can get Django Suit by using pip or easy_install::

    pip install django-suit
    # or
    easy_install django-suit

2. You will need to add the ``'suit'`` application to the ``INSTALLED_APPS`` setting of your Django project ``settings.py`` file.::

    INSTALLED_APPS = (
        ...
        'suit',
        'django.contrib.admin',
    )

  .. warning:: ``'suit'`` must be added before ``'django.contrib.admin'``

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

Configuration
=============

You can customize Django Suit behaviour by adding ``SUIT_CONFIG`` configuration variable to your Django project ``settings.py`` file.

.. toctree::
   :maxdepth: 3

   configuration


Template customization
======================

You must extend ``base_site.html`` template to customize footer links, copyright text or to add extra JS/CSS files. Example file is available on `github <https://github.com/darklow/django-suit/blob/master/suit/templates/admin/base_site.html>`_.

Copy customized ``base_site.html`` template file to your project's main application ``template/admin/`` directory and un-comment and edit the blocks you would like to extend.

Alternatively you can copy ``base_site.html`` to any of template directories, which are defined in ``TEMPLATE_DIRS`` setting (if any). By default Django looks in every registered application ``templates/`` dir.

In the same way you can override any of Django Suit admin templates. More about customizing project's templates, you can read in `Django Admin Tutorial <https://docs.djangoproject.com/en/dev/intro/tutorial02/#customizing-your-project-s-templates>`_


Widgets
=======

There are handy widgets included in Django Suit.

.. toctree::
   :maxdepth: 3

   widgets



Sortables
=========

Sortables ar handy tools for ordering different lists

.. toctree::
   :maxdepth: 3

   sortables


Examples
========

Besides documentation examples, Django Suit `demo application <http://djangosuit.com/admin/>`_ source code is also available on separate github repository: `django-suit-examples <https://github.com/darklow/django-suit-examples>`_. If you see anything in demo application, you can always go to this repository and see implementation and code in one of ``models.py`` or ``admin.py`` files

Contribution
============

There will be separate "django-suit-contrib" package available soon with full Django project setup and tests. However if you already are willing to fork, report a bug or suggest a feature, you can do it in our `main github repository <https://github.com/darklow/django-suit>`_.
