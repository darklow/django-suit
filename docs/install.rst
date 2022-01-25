Install
=======

To install Django Suit

1. Install Django Suit v2 using ``pip`` or ``easy_install``::

    pip install django-suit-v2-pm


2. Create ``SuitConfig`` class and add it to the ``INSTALLED_APPS`` **before** ``django.contrib.admin`` app:

.. code-block:: py

    # my_project_app/apps.py
    from suit.apps import DjangoSuitConfig

    class SuitConfig(DjangoSuitConfig):
        layout = 'horizontal'


.. code-block:: py

    INSTALLED_APPS = (
        ...
        'my_project_app.apps.SuitConfig',
        'django.contrib.admin',
    )

