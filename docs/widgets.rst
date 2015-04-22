Widgets
=======

Easiest way to change widget for specific fields is define your own ``ModelForm`` class with ``Meta class`` and ``widgets``. Following this logic, you can override almost any widget in your form.

For example if you want to add some additional CSS class to input you can do following::

  from django.forms import ModelForm, TextInput
  from django.contrib.admin import ModelAdmin
  from .models import Country

  class CountryForm(ModelForm):
      class Meta:
          widgets = {
              'name': TextInput(attrs={'class': 'input-mini'})
          }

  class CountryAdmin(ModelAdmin):
      form = CountryForm
      ...

  admin.site.register(Country, CountryAdmin)


.. note:: If you define some custom fields for your form, you must specify ``model = YourModel`` parameter for ``class Meta``.


NumberInput
-----------

HTML5 number input ``type="number"``::

  from django.forms import ModelForm
  from suit.widgets import NumberInput

  class OrderForm(ModelForm):
      class Meta:
          widgets = {
              'count': NumberInput,

              # Optionally you specify attrs too
              'count': NumberInput(attrs={'class': 'input-mini'})

          }

.. note:: The same result you can achieve with ``HTML5Input(input_type='number')`` widget, this is just a shortcut.

HTML5Input
----------

Specify ``input_type`` and use any of `HTML5 input types <http://www.w3schools.com/html/html5_form_input_types.asp>`_. You can see some HTML5 input examples in Django Suit Demo app in `KitchenSink forms <http://djangosuit.com/admin/examples/kitchensink/2/>`_::


  from django.forms import ModelForm
  from suit.widgets import HTML5Input

  class ProductForm(ModelForm):
      class Meta:
          widgets = {
              'color': HTML5Input(input_type='color'),
          }


.. note:: Not all major browsers support all the new input types. However, you can already start using them; If they are not supported, they will behave as regular text fields. Also not all types are supported by Twitter Bootstrap.


EnclosedInput
-------------

Supports `Twitter Bootstrap prepended/appended form inputs <http://twitter.github.com/bootstrap/base-css.html#forms>`_. ``EnclosedInput`` widget accepts two arguments ``prepend=`` and ``append=``. Values can be ``text``, ``icon-class`` or ``html`` (starts with html tag). You can also use both ``prepend=`` and ``append=`` together::

  from django.forms import ModelForm
  from suit.widgets import EnclosedInput

  class ProductForm(ModelForm):
      class Meta:
          widgets = {

              # Appended by text
              'discount': EnclosedInput(append='%'),
              'size': EnclosedInput(append='m<sup>2</sup>'),

              # By icons
              'email': EnclosedInput(append='icon-envelope'),
              'user': EnclosedInput(prepend='icon-user'),

              # You can also use prepended and appended together
              'price': EnclosedInput(prepend='$', append='.00'),

              # Use HTML for append/prepend (See Twitter Bootstrap docs of supported tags)
              'url': EnclosedInput(prepend='icon-home', append='<input type="button" class="btn"  value="Open link">'),

          }


**Preview:**

  .. image:: _static/img/enclosed_input.png


AutosizedTextarea
-----------------

``AutosizedTextarea`` enables automatic height based on user input for textarea elements. Uses `jQuery Autosize <http://www.jacklmoore.com/autosize>`_ plugin. All the required javascript will be automatically attached. Usage::

  from django.forms import ModelForm
  from suit.widgets import AutosizedTextarea

  class ProductForm(ModelForm):
      class Meta:
          widgets = {
              'description': AutosizedTextarea,

              # You can also specify html attributes
              'description': AutosizedTextarea(attrs={'rows': 3, 'class': 'input-xlarge'}),
          }


For demo - see countries `description field <http://djangosuit.com/admin/examples/country/add/>`_ or kitchensink `tabluar inlines <http://djangosuit.com/admin/examples/kitchensink/add/>`_

.. note:: If you want to change height, when vertical scrollbar appears, use CSS ``max-height`` attribute. By default: ``max-height: 150px``


Date/Time widgets
-----------------

``SuitDateWidget``, ``SuitTimeWidget`` and ``SuitSplitDateTimeWidget`` extends original admin widgets by adding some additional output styling only. Widgets still uses same original JavaScript for calendar and time. You can see example in `Demo app: User changeform <http://djangosuit.com/admin/auth/user/6/>`_::

  from django.forms import ModelForm
  from suit.widgets import SuitDateWidget, SuitTimeWidget, SuitSplitDateTimeWidget

  class UserChangeForm(ModelForm):
      class Meta:
          model = User
          widgets = {
              'last_login': SuitSplitDateTimeWidget,
              'date_joined': SuitSplitDateTimeWidget,
          }



**Preview:**

  .. image:: _static/img/dates.png
     :target: http://djangosuit.com/admin/auth/user/6/


LinkedSelect
------------

Adds link to related item right after select for foreign key fields::

  from django.forms import ModelForm
  from suit.widgets import LinkedSelect

  class CountryForm(UserChangeForm):
      class Meta:
          widgets = {
              'continent': LinkedSelect
          }



**Preview:**

  .. image:: _static/img/linked_select.png
     :target: http://djangosuit.com/admin/examples/kitchensink/2/

