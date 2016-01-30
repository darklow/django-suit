Install
=======

To install Django Suit

1. Install Django Suit using ``pip`` or ``easy_install``::

    pip install django-suit


2. Add ``suit`` to ``INSTALLED_APPS`` **before** ``django.contrib.admin`` app:

.. code-block:: py

    INSTALLED_APPS = (
        ...
        'suit',
        'django.contrib.admin',
    )

