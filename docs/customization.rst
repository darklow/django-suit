Customization
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
