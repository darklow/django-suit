Form tabs
=========

Form tabs help you organize form fieldsets and inlines into tabs. Before reading further, take a look on the tabs `in the demo app <http://djangosuit.com/admin/examples/country/234/>`_.

**Under the hood**: Tabs are based on mostly ``CSS/JS`` solution, therefore integration of tabs is simple and non intrusive - all your form handling will work the same as before.

To organize form into tabs you must:

1. Add ``suit_form_tabs`` parameter to your ``ModelAdmin`` class::

    # (TAB_NAME, TAB_TITLE)
    suit_form_tabs = (('general', 'General'), ('advanced', 'Advanced Settings'))

2. Add ``'suit-tab suit-tab-TAB_NAME'`` to ``fieldset classes``, where ``TAB_NAME`` matches tab name you want to show fieldset in.
3. To use with inlines, specify same css classes in ``suit_classes`` parameter for ``inline`` classes


Example
-------
::

    from django.contrib import admin
    from .models import Country


    class CityInline(admin.TabularInline):
        model = City
        suit_classes = 'suit-tab suit-tab-cities'


    class CountryAdmin(admin.ModelAdmin):
        inlines = (CityInline,)

        fieldsets = [
            (None, {
                'classes': ('suit-tab', 'suit-tab-general',),
                'fields': ['name', 'continent',]
            }),
            ('Statistics', {
                'classes': ('suit-tab', 'suit-tab-general',),
                'fields': ['area', 'population']}),
            ('Architecture', {
                'classes': ('suit-tab', 'suit-tab-cities',),
                'fields': ['architecture']}),
        ]

        suit_form_tabs = (('general', 'General'), ('cities', 'Cities'),
                     ('info', 'Info on tabs'))

        # Read about form includes in next section
        suit_form_includes = (
            ('admin/examples/country/custom_include.html', 'middle', 'cities'),
            ('admin/examples/country/tab_info.html', '', 'info'),
        )


    admin.site.register(Country, CountryAdmin)

Same way you can organize any HTML into tabs, just wrap it in previously mentioned CSS classes:

.. code-block:: html

  <div class="suit-tab suit-tab-TAB_NAME">...</div>

Preview
-------

  .. image:: _static/img/form_tabs.png
     :target: http://djangosuit.com/admin/examples/country/234/


Form Includes
-------------

Django Suit provides handy shortcut to include templates into forms.

See :doc:`/form_includes`
