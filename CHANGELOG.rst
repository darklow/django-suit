Changelog
=========

v0.2.4 (2013-08-15)
-------------------------------------------------------------

* [Fix] JS Fix preventing empty inline creation when saving inlines with blank inputs.
* [Fix] Fixes `#140 <https://github.com/darklow/django-suit/issues/140>`_ KeyError with latest MPTT library
* [Fix] Fixes `#139 <https://github.com/darklow/django-suit/issues/139>`_ Search form doesn't submit filters on IE10
* See `commit log <https://github.com/darklow/django-suit/commits/develop>`_ and `closed issues <https://github.com/darklow/django-suit/issues?direction=desc&sort=updated&state=closed>`_ for full changes


v0.2.3 (2013-08-01)
-------------------------------------------------------------

* [Feature] Added CSS file for media=print. Reposition/hide unnecessary elements when printing.
* [Feature] More robust URL splitting/parsing for menu which now supports all kind of admin urls including `i18n_patterns` [Thanks to @philippbosch]
* [Feature] List attributes feature improvement: `suit_row_attributes` method now receives also request as an argument. [Thanks to @asteinlein]
* [Fix] CSS improvements for Mac/Safari: `box-shadow` fixes.
* See `commit log <https://github.com/darklow/django-suit/commits/develop>`_ and `closed issues <https://github.com/darklow/django-suit/issues?direction=desc&sort=updated&state=closed>`_ for full changes


v0.2.2 (2013-06-21)
-------------------------------------------------------------

* [Feature] `django-import-export <https://github.com/bmihelac/django-import-export>`_ app support. See `example <http://djangosuit.com/admin/examples/importexportitem/>`_ [Thanks to @jonashaag]
* [Fixes] CSS/Templating fixes and tweaks. See `commit log <https://github.com/darklow/django-suit/commits/develop>`_ and `closed issues <https://github.com/darklow/django-suit/issues?direction=desc&sort=updated&state=closed>`_ for full changes


v0.2.1 (2013-05-11)
-------------------------------------------------------------

* [Feature] Styling list rows and cells based on object instance. Read `Documentation <http://django-suit.readthedocs.org/en/develop/list_attributes.html>`_. See `example <http://djangosuit.com/admin/examples/continent/>`_
* [CSS] Changed selected rows background color to inverse, to avoid color conflict with row "warning" css class
* [Fixes] CSS/Templating fixes and tweaks. See `commit log <https://github.com/darklow/django-suit/commits/develop>`_ and `closed issues <https://github.com/darklow/django-suit/issues?direction=desc&sort=updated&state=closed>`_ for full changes


v0.2.0 (2013-04-29)
-------------------------------------------------------------

* [Major Feature] `Django-CMS <https://github.com/divio/django-cms>`_ support. See full notes here `#77 <https://github.com/darklow/django-suit/issues/77>`_. See `example <http://djangosuit.com/admin/cms/page/>`_
* [Major Feature] `Django-Filer <https://github.com/stefanfoulis/django-filer>`_ support. See `example <http://djangosuit.com/admin/filer/folder/>`_
* [CSS] Selector widget style improvements See `#80 <https://github.com/darklow/django-suit/issues/80#issuecomment-16329776>`_
* [CSS] Main content container now uses Twitter Bootstrap `row-fluid` class. See `#58 <https://github.com/darklow/django-suit/issues/58>`_
* [Refactor] Included jQuery now is using own namespace: `Suit.$`
* [Fix] CSS/Templating fixes and tweaks. See commit log and closed issues for full changes


v0.1.9 (2013-03-25)
-------------------------------------------------------------

* [Feature] `Form tabs <http://django-suit.readthedocs.org/en/develop/form_tabs.html>`_ - help you organize form fieldsets and inlines into tabs. See `example <http://djangosuit.com/admin/examples/country/234/>`_ [Thanks to @phihos]
* [Feature] `Form includes <http://django-suit.readthedocs.org/en/develop/form_includes.html>`_ - shortcut to include templates into forms
* [Feature] `New menu syntax <http://django-suit.readthedocs.org/en/develop/configuration.html#id1>`_ supports app and model labels, separators and more clear definition syntax.


v0.1.8 (2013-03-20)
-------------------------------------------------------------

* [Feature] `django-reversion <https://github.com/etianen/django-reversion>`_ app support. `Example <http://djangosuit.com/admin/examples/reversioneditem/>`_ [Thanks to @phihos]
* [Feature] `WYSIWYG editors <http://django-suit.readthedocs.org/en/develop/wysiwyg.html>`_ support, examples and docs
* [Feature] `Full-width fieldsets <http://django-suit.readthedocs.org/en/develop/widgets.html#css-goodies>`_
* [Feature] Introduced two related wysiwyg apps `suit-redactor <https://github.com/darklow/django-suit-redactor>`_ and `suit-ckeditor <https://github.com/darklow/django-suit-ckeditor>`_
* [CSS] New "multi-fields in row" look and behaviour.
* [CSS] Support for fieldset "wide" class 
* [Refactor] Major fieldset refactoring to support multi-line labels
* [Fix] Many CSS/Templating fixes and tweaks. See commit log for full changes


v0.1.6, v.0.1.7 (2013-03-10)
-------------------------------------------------------------

* [Tests] Travis CI hooked up - testing against Django 1.4-1.5, Python 2.5-3.3
* [Tests] Tests now cover every class and method in Django Suit
* [Fix] Full support for Python 3.x added
* [Critical] Django 1.4 compatibility restored. Removed django.utils.six (Django 1.4.2)


v0.1.5 (2013-03-10)
-------------------------------------------------------------

* [Feature] New widget: `AutosizedTextarea <http://django-suit.readthedocs.org/en/develop/widgets.html#autosizedtextarea>`_
* [Feature] New widget: `LinkedSelect <http://django-suit.readthedocs.org/en/develop/widgets.html#linkedselect>`_
* [Feature] JavaScript inlines hook: `SuitAfterInline JS hook <http://django-suit.readthedocs.org/en/develop/widgets.html#javascript-goodies>`_
* [Tests] Tests means more stability - bunch of tests added, more to come.
* [Fix/Refactoring] Install breaks under certain conditions #17
* [Fix] Admin save_on_top=True breaks change form #16
* [Fix] Minor bugs and tweaks. See commit log for full changes


v0.1.4 (2013-03-04)
-------------------------------------------------------------

* [Fix] Sortables improvements and fixes #12, #13, #14
* [Fix] Python3 related fixes #11 [Thanks to @coagulant]
* [Fix] Firefox floating problem for list "New" button #15


v0.1.3 (2013-03-03)
-------------------------------------------------------------

* [Feature] `Sortables <http://django-suit.readthedocs.org/en/develop/sortables.html>`_ for `change list <http://djangosuit.com/admin/examples/continent/>`_, `mptt-tree <http://djangosuit.com/admin/examples/category/>`_ list and `tabular inlines <http://djangosuit.com/admin/examples/continent/9/>`_.
* [Feature] `EnclosedInput widget <http://django-suit.readthedocs.org/en/develop/widgets.html#enclosedinput>`_ for Twitter Bootstrap appended/prepended inputs. `Example <http://djangosuit.com/admin/examples/city/5/>`_
* [Feature] `HTML5Input <http://django-suit.readthedocs.org/en/develop/widgets.html#html5input>`_ widget
* [Documentation] Added detailed docs and examples on sortables and widgets
* [Fix] Minor bugs and tweaks. See commit log for full changes


v0.1.2 (2013-02-27)
-------------------------------------------------------------

* [Feature] Customizable menu, cross apps, custom links and menus
* [Refactoring] Moved all static files to separate directory
* [Fix] PEP8 and templates style improvements [Thanks to @peterfschaadt]
* [Fix] Fixed inconsistent styling on login form errors [Thanks to @saippuakauppias]


v0.1.1 (2013-02-25)
-------------------------------------------------------------

* [Feature] Added link to admin home in error templates
* [Feature] Config key SEARCH_URL now supports also absolute urls
* [Fix] SEARCH_URL fallback uses absolute URL instead of urlname


v0.1.0 (2013-02-24)
-------------------------------------------------------------

* First stable version released
