Sortables
=========

Currently Django Suit supports these types of sortables:

1. Sortable for change list
2. Sortable for ``django-mptt`` tree list
3. Sortable for Tabular, Stacked, GenericTabular, GenericStacked inlines

Limitations
-----------

Since sortables are based on JavaScript solution, there are known limitations:

1. They don't work with pagination.
2. You won't be able to use different list order other than by sortable parameter.

Under the hood
--------------

Widgets add sortable parameter to list_editable fields as simple number inputs. Afterwards JavaScript utils replaces these editable inputs with arrows. Order is not saved instantly, but only when user saves form, which is very handy - user can do sorting first and afterwards save it or cancel if changed his mind.


Change list sortable
--------------------

To use change list sortable you must do following:

1. In your ``models.py`` file add integer property for sortable to you model::

    from django.db import models

    class Continent(models.Model):
        ...
        order = models.PositiveIntegerField()

2. In your in your ``admin.py`` extend ``SortableModelAdmin`` class and specify ``sortable`` name::

    from suit.admin import SortableModelAdmin

    class ContinentAdmin(SortableModelAdmin):
        ...
        sortable = 'order'

That's it, you should see similar picture to example below in your admin now.

.. note:: If you want sortable arrows to appear in different column than last, you can do this by adding sortable field to ``list_editable`` in desired order, for example: ``list_editable=('name', 'order', 'something')``. If you set arrows as first column, you must also define ``list_display_links`` - because arrows can't be displayed also as links.


Example
^^^^^^^

  .. image:: _static/img/changelist_sortable.png
     :target: http://djangosuit.com/admin/examples/continent/

Resources
^^^^^^^^^

* `Live example <http://djangosuit.com/admin/examples/continent/>`_
* `Github source <https://github.com/darklow/django-suit-examples>`_


django-mptt tree sortable
-------------------------

To use sortable on `djang-mptt <https://github.com/django-mptt/django-mptt/>`_ tree, you must follow the same instructions as for change list sortable. Combining with documentation on django-mptt, final code should look like this:

1. Prepare your model in ``models.py`` ::

    from django.db import models
    from mptt.fields import TreeForeignKey
    from mptt.models import MPTTModel

    class Category(MPTTModel):
        name = models.CharField(max_length=64)
        parent = TreeForeignKey('self', null=True, blank=True,
                                related_name='children')

        # Sortable property
        order = models.PositiveIntegerField()

        class MPTTMeta:
            order_insertion_by = ['order']

        # It is required to rebuild tree after save, when using order for mptt-tree
        def save(self, *args, **kwargs):
            super(Category, self).save(*args, **kwargs)
            Category.objects.rebuild()

        def __unicode__(self):
            return self.name


2. Prepare admin class in ``admin.py``::

    from suit.admin import SortableModelAdmin
    from mptt.admin import MPTTModelAdmin
    from .models import Category

    class CategoryAdmin(MPTTModelAdmin, SortableModelAdmin):
        mptt_level_indent = 20
        list_display = ('name', 'slug', 'is_active')
        list_editable = ('is_active',)

        # Specify name of sortable property
        sortable = 'order'

    admin.site.register(Category, CategoryAdmin)

.. note:: ``MPTTModelAdmin`` must be specified "before" ``SortableModelAdmin`` in extend syntax as shown in example.

Example
^^^^^^^

  .. image:: _static/img/mptt_sortable.png
     :target: http://djangosuit.com/admin/examples/category/

Resources
^^^^^^^^^

* `Live example <http://djangosuit.com/admin/examples/category/>`_
* `Github source <https://github.com/darklow/django-suit-examples>`_
* `django-mptt documentation <https://django-mptt.readthedocs.org/en/latest/>`_



Tabular inlines sortable
------------------------

1. In ``models.py`` your model for inlines, should have integer property for sortable, same way as described in all previous sortable examples::

    from django.db import models

    class Country(models.Model):
        ...
        order = models.PositiveIntegerField()


2. In ``admin.py`` inline class must extend ``SortableModelAdmin`` class and specify ``sortable`` name::

    from django.contrib.admin import ModelAdmin
    from suit.admin import SortableTabularInline

    class CountryInline(SortableTabularInline):
        model = Country
        sortable = 'order'

    class ContinentAdmin(ModelAdmin):
        inlines = (CountryInline,)

That's it, you should see similar picture to example below in your admin now.

Example
^^^^^^^

  .. image:: _static/img/tabular_inline_sortable.png
     :target: http://djangosuit.com/admin/examples/continent/9/

Resources
^^^^^^^^^

* `Live example <http://djangosuit.com/admin/examples/continent/9/>`_
* `Live example #2 <http://djangosuit.com/admin/examples/kitchensink/2/>`_
* `Github source <https://github.com/darklow/django-suit-examples>`_


Stacked and Generic inlines sortable
------------------------------------

Implementation of sortables for Stacked and Generic inlines is the same as mentioned above for Tabular inlines. You just have to use appropriate base class instead of ``SortableTabularInline``:

::

    # For Stacked inlines
    from suit.admin import SortableStackedInline

    # For Generic inlines
    from suit.admin import SortableTabularStackedInline
    from suit.admin import SortableGenericStackedInline


Example
^^^^^^^

  .. image:: _static/img/stacked_inline_sortable.png
     :target: http://djangosuit.com/admin/examples/kitchensink/3/

Resources
^^^^^^^^^

* `Live example <http://djangosuit.com/admin/examples/kitchensink/3/>`_
* `Github source <https://github.com/darklow/django-suit-examples>`_
