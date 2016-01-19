Contributing
============

To contribute to Django Suit::

    # Clone forked Django Suit repo
    git clone git@github.com:YOUR_USERNAME/django-suit.git suit

    # Install Django Suit from local fork in editable mode
    pip install -e suit

If you wish to participate in development discussions, join our IRC channel ``#django-suit`` on ``irc.freenode.net``

Tests
-----

When contributing don't forget to test your code by running::

    ./manage.py test suit

CSS/LESS
--------

Contributing on specifically UI/CSS features/fixes have more requirements:

* ``lessc`` compiler - http://lesscss.org/
* ``watchdog`` package - ``pip install watchdog``
* ``django-suit-examples`` - it may be a good idea to add `examples app <https://github.com/darklow/django-suit-examples>`_ to your project

While editing ``.less`` files, run following script, which automatically watches ``.less`` files for changes and compiles them to ``suit.css``::

    python suit/watch_less.py suit/static/suit/less/suit.less


Related packages
----------------

Related packages you can contribute to:

* `django-suit-redactor <https://github.com/darklow/django-suit-redactor>`_ - Imperavi Redactor (WYSIWYG editor) integration app
* `django-suit-ckeditor <https://github.com/darklow/django-suit-ckeditor>`_ - CKEditor (WYSIWYG editor) integration app
* `django-suit-rq <https://github.com/gsmke/django-suit-rq>`_ - Django-RQ (Queuing library) integration app
* `django-suit-examples <https://github.com/darklow/django-suit-examples>`_ - demo app
