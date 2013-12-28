JavaScript & CSS
================

JavaScript goodies
------------------

Inlines hook
^^^^^^^^^^^^

When working with Django inlines and JavaScript, very often we want to hook/attach to event - when new inline row is added. Django Suit gives us such chance.

Use JavaScript ``Suit.after_inline.register`` to register/attach your function to new inline addition event.

.. code-block:: javascript

  $(function () {
      Suit.after_inline.register('my_unique_func_name', function(inline_prefix, row){
          // Your code here
          console.info(inline_prefix)
          console.info(row)
      });
  });


.. _css-goodies:


jQuery
^^^^^^

Django Suit provides jQuery (currently v1.8.3) and it is using custom namespace to avoid collisions between different apps which also provide jQuery.

To use jQuery from Django Suit package:

.. code-block:: javascript

  // Use Suit.$ instead of $
  Suit.$('.my-selector').addClass('my-class');

  // Or for larger code you can wrap it in following way:
  (function ($) {
      // Here you can use regular $ sign
      $('.my-selector').addClass('my-class');
  }(Suit.$));

  // On document ready example:
  (function ($) {
    $(function () {
        $('.my-selector').addClass('my-class');
    });
  }(Suit.$));


CSS goodies
-----------

`Original <https://docs.djangoproject.com/en/dev/ref/contrib/admin/#django.contrib.admin.ModelAdmin.fieldsets>`_ ``collapse`` and ``wide`` fieldset classes are also supported by Django Suit. Usage::

  from django.contrib.admin import ModelAdmin

  class CountryAdmin(admin.ModelAdmin):
      ...
      fieldsets = [
          (None, {'fields': ['name', 'description']}),

          ('Advanced settings', {
              'classes': ('collapse',),  # Specify fieldset classes here
              'fields': ['hidden_checkbox', 'hidden_choice']}),
      ]

.. |collapse| image:: _static/img/collapse.png

* ``collapse`` CSS class makes fieldset collapsable:

  |collapse|

* ``wide`` CSS class makes fieldset labels wider

* ``full-width`` CSS class hides field label and makes field controls in full width (useful for wysiwyg editors). Because label will be hidden, this class is intended to use one field per fieldset and fieldset title will be used as field title.

  .. image:: _static/img/full-width.png
     :target: http://djangosuit.com/admin/examples/wysiwygeditor/add/


