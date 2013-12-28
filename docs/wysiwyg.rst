WYSIWYG editors
===============

If you use third party wysiwyg editor app, you should follow its manual.

If you would like to use save horizontal space, you should use :ref:`full-width fieldset class <css-goodies>` with your wysiwyg editor.

We tested many existing wysiwyg apps, but many of them were missing tests, had implementation or other flaws, so we decided to create our own. We are maintaining two simple wysiwyg apps for `Imperavi Redactor <imperavi.com/redactor/>`_ and `CKEditor <ckeditor.com>`_.

Right now they doesn't support any uploads or anything with Django urls related, however it is planned to improve and update these packages in future.

These packages are independent and Django Suit isn't requirement.


Imperavi Redactor
-----------------

* Package on github: `django-suit-redactor <https://github.com/darklow/django-suit-redactor>`_
* Editor homepage: http://imperavi.com/redactor/
* License: Creative Commons Attribution-**NonCommercial** 3.0 license. For commercial use please buy license `here <http://redactorjs.com/download/>`_.
* Demo: http://djangosuit.com/admin/examples/wysiwygeditor/add/

Install::

1. ``pip install django-suit-redactor``
2. Add ``suit_redactor`` to ``INSTALLED_APPS``
3. Editor options for ``editor_options`` parameter can be found in `Redactor Docs <http://imperavi.com/redactor/docs/settings/>`_

Usage::

  from django.forms import ModelForm
  from django.contrib.admin import ModelAdmin
  from suit_redactor.widgets import RedactorWidget

  class PageForm(ModelForm):
      class Meta:
          widgets = {
              'name': RedactorWidget(editor_options={'lang': 'en'})
          }

  class PageAdmin(ModelAdmin):
      form = PageForm
      fieldsets = [
        ('Body', {'classes': ('full-width',), 'fields': ('body',)})
      ]
      ...

  admin.site.register(Page, PageAdmin)

Preview:

  .. image:: _static/img/full-width.png
     :target: http://djangosuit.com/admin/examples/wysiwygeditor/add/


CKEditor 4.x
------------

* Package on github: `django-suit-ckeditor <https://github.com/darklow/django-suit-ckeditor>`_
* Editor homepage: http://ckeditor.com
* License: GPL, LGPL and MPL Open Source licenses
* Demo: http://djangosuit.com/admin/examples/wysiwygeditor/add/


Install::

1. ``pip install django-suit-ckeditor``
2. Add ``suit_ckeditor`` to ``INSTALLED_APPS``
3. Editor options for ``editor_options`` parameter can be found in `CKEditor Docs <http://docs.ckeditor.com/#!/api/CKEDITOR.config>`_

Usage for CKEditor is the same as for Imperavi Redactor, just change ``RedactorWidget`` to ``CKEditorWidget``::

  from django.forms import ModelForm
  from django.contrib.admin import ModelAdmin
  from suit_ckeditor.widgets import CKEditorWidget

  class PageForm(ModelForm):
      class Meta:
          widgets = {
              'name': CKEditorWidget(editor_options={'startupFocus': True})
          }

  class PageAdmin(ModelAdmin):
      form = PageForm
      fieldsets = [
        ('Body', {'classes': ('full-width',), 'fields': ('body',)})
      ]
      ...

  admin.site.register(Page, PageAdmin)

Preview:

  .. image:: _static/img/ckeditor.png
     :target: http://djangosuit.com/admin/examples/wysiwygeditor/add/


Other wysiwyg apps
------------------

Also you can integrate WYSIWYG editor using any other third party apps.

Few third party apps we tested for Django Suit:

* `django-tinymce <https://github.com/aljosa/django-tinymce>`_ - TinyMCE editor. Tested and works great
* `django-ckeditor <https://github.com/shaunsephton/django-ckeditor>`_ - CK Editor. Works great, but no support for CK Editor 4.x yet
* `django-cked <https://bitbucket.org/ssbb/django-cked>`_ - CK Editor. Quite new and unfortunately not so stable. Supports CK Editor 4.x
* `django-redactorjs <https://github.com/TigorC/django-redactorjs>`_ - Imperavi Redactor.
* `django-redactor <https://github.com/mazelife/django-redactor>`_ - Imperavi Redactor. No Pypi package yet
* See also `WYSIWYG Editors <https://www.djangopackages.com/grids/g/wysiwyg/>`_ grid on DjangoPackages.com

