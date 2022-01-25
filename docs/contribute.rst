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


PyPi
----
Update setup.py

Generate the distribution archives on local machine:

* upgrade your setuptools library on your machine to use the latest version

.. code-block:: bash

    python -m pip install --user --upgrade setuptools wheel


* you need to run the following command from the root directory of your package to generate the distribution files.

.. code-block:: bash

    python setup.py sdist bdist_wheel

* Navigate to https://test.pypi.org/ and Register yourself as an user.

* This will install a package called “twine” on your machine that will help ship the python package to the repositories.

.. code-block:: bash

    python -m pip install --user --upgrade twine

* run the following command to ship the code to TestPyPi first. When you run the command, you will be asked to provide the same credentials using which you have registered your account in the previous step.

.. code-block:: bash

    python -m twine upload --repository testpypi dist/*

* Publish the package to the PyPi repository

.. code-block:: bash

    python -m twine upload dist/*