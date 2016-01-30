Contribute
==========

To contribute to Django Suit:

1. Fork Django Suit and clone it locally::

    git clone -b v2 git@github.com:YOUR_USERNAME/django-suit.git suit


2. Install Django Suit from local fork in editable mode::

    pip install -e suit


SASS compiling
--------------

Install dependencies::

    bower install


Documentation
-------------

Create ``virtualenv`` and install dependencies::

    pip install -r requirements-dev.txt

Compile docs:

.. code-block:: bash

    cd docs
    make html

    # Clean & compile
    make clean html



