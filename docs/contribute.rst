Contribute
==========

To contribute to Django Suit fork Django Suit on github and clone it locally:

.. code-block:: bash

    git clone -b v2 git@github.com:YOUR_USERNAME/django-suit.git suit
    cd suit


DEV environment
---------------

After you forked and cloned repository I suggest you create virtual environment using ``virtualenv``. Feel free to use other virtualenv layout, but here is mine:

.. code-block:: bash

    # In cloned suit directory create virtualenv
    virtualenv env

    # Activate virtualenv
    source env/bin/activate

    # Install Django Suit in editable mode
    pip install -e .

    # Install dev and demo app requirements
    pip install -r requirements-dev.txt
    pip install -r demo/requirements.txt

    # Run Django Suit demo app
    python demo/manage.py runserver 0.0.0.0:8000


SASS compiling
--------------

SASS compiling is done in ``nodejs`` using ``gulp`` tasks and ``node-sass`` (uses ``libsass``). Gulp tasks are watching ``.scss`` and ``.html`` files and automatically reload browser on changes, making development much easier.

.. code-block:: bash

    # Install dependencies
    npm install

    # Run Django Suit demo app
    python demo/manage.py runserver 0.0.0.0:8003

    # Run gulp tasks and it should automatically open http://localhost:8005/.
    # If it didn't, open it manually.
    gulp


Documentation
-------------

Compile docs:

.. code-block:: bash

    # Compile docs
    make -C docs html

    # Clean & compile
    make -C docs clean html

Heroku
------
* requirements.txt is loading demo/requirements-heroku.txt
* runtime.txt is setting the python version
* Procfile is defining how to run the app. Actually it runs collectstatic (because the default heroku task can not
use the demo settings), then it creates static directory and finally run the app
* demo/settings-heroku to run with DEBUG=False and static with whitenoise

On Heroku I defined :
* SECRET_KEY
* DISABLE_COLLECTSTATIC = 1
* DJANGO_SETTINGS_MODULE = demo.settings-heroku

