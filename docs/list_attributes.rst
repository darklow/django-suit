List attributes
===============

Using few callable helpers you can customize change list row and cell attributes based on object instance variables.


List header columns
-------------------

As soon as you add ``suit`` to your apps, all your changelist table header columns will have specific field CSS class present.

For example for column ``country`` list header tag will look like this ``<th class="country-column">``. Which means you can change it's appearance using CSS.

.. code-block:: css

  .country-column .text, .country-column a {
      text-align: center;
  }


List row attributes
-------------------

To add html attributes like ``class`` or ``data`` to list rows, you must define ``suit_row_attributes`` callable (function). Callable receives object instance and the request as arguments and must return ``dict`` with attributes for current row.

Example::

  from django.contrib.admin import ModelAdmin

  class CountryAdmin(ModelAdmin):
      ...

      def suit_row_attributes(self, obj, request):
          return {'class': 'type-%s' % obj.type}

      # Or bit more advanced example
      def suit_row_attributes(self, obj, request):
          css_class = {
              1: 'success',
              0: 'warning',
              -1: 'error',
          }.get(obj.status)
          if css_class:
              return {'class': css_class, 'data': obj.name}


.. note:: Twitter bootstrap already provides handy CSS classes for table row styling: ``error``, ``warning``, ``info`` and ``success``

Preview:

  .. image:: _static/img/list_attributes.png
     :target: http://djangosuit.com/admin/examples/continent/


List cell attributes
--------------------

To add html attributes like ``class`` or ``data`` to list cells, you must define ``suit_cell_attributes`` callable (function). Callable receives object instance and column name as arguments and must return ``dict`` with attributes for current cell.

Example::

  from django.contrib.admin import ModelAdmin

  class CountryAdmin(ModelAdmin):
      ...

      def suit_cell_attributes(self, obj, column):
          if column == 'countries':
              return {'class': 'text-center'}
          elif column == 'name' and obj.status == -1:
              return {'class': 'text-error'}


.. note:: Twitter bootstrap already provides handy CSS classes for table cell alignment: ``text-left``, ``text-center``, ``text-right``
