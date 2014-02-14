Form Includes
=============

Django Suit provides handy shortcut to include templates into forms for several positions (top, middle and bottom).

**Under the hood**: Suit includes are nothing but a shortcut. The same can be achieved by extending ``change_form.html`` and hooking into particular blocks. Suit includes can be used in combination with or without :doc:`/form_tabs`.

Each ``suit_form_includes`` item can contain 3 parameters:

1. Path to template (Required)
2. Position: (Optional)
  * ``top`` - above fieldsets:
  * ``middle`` - between fieldsets and inlines
  * ``bottom`` - after inlines (Default)
3. Specify ``TAB_NAME`` if using in combination with :doc:`/form_tabs` (Optional)

Example
-------
::

    from django.contrib import admin
    from .models import Country

    class CountryAdmin(admin.ModelAdmin):
        ...
        suit_form_includes = (
            ('admin/examples/country/custom_include.html', 'middle', 'cities'),
            ('admin/examples/country/tab_info.html', '', 'info'),
            ('admin/examples/country/disclaimer.html'),
        )


Preview
-------

  .. image:: _static/img/form_includes.png
     :target: http://djangosuit.com/admin/examples/country/234/

