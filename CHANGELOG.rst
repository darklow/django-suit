Changelog
=========

Only important changes are mentioned below. See `commit log <https://github.com/darklow/django-suit/commits/develop>`_, `closed issues <https://github.com/darklow/django-suit/issues?direction=desc&sort=updated&state=closed>`_ and `closed pull
requests <https://github.com/darklow/django-suit/pulls?q=sort%3Aupdated-desc+is%3Apr+is%3Aclosed>`_ for full changes.

v0.2.26 (2018-02-24)
--------------------

* [Fix] Django 2.0 support.
* [Fix] Minor fixes by PR.


v0.2.25 (2017-03-30)
--------------------

* [Fix] Fixes missing original time/date widget icons.
* [Fix] Fixes missing menu when using with Django Channels.


v0.2.24 (2017-01-27)
--------------------

* [Fix] Sortable inlines required fields detection fix (related to jQuery update).
* [Fix] More precise SPAN selector not to mess up editors and other content in stacked inlines.


v0.2.23 (2016-12-06)
--------------------

* [Fix] Fieldset newlines fix, jQuery tab fix and few other minor bugs by PR.


v0.2.22 (2016-11-11)
--------------------

* [Fix] Upgrade to jQuery 2.2.4 when using Django >= 1.9


v0.2.21 (2016-08-18)
--------------------

* [Fix] Django 1.10 compatibility and Travis tests fixes


v0.2.20 (2016-08-09)
--------------------

* [Fix] Django 1.10 compatibility fixes `#526 <https://github.com/darklow/django-suit/pull/526>`_


v0.2.19 (2016-06-23)
--------------------

* [Fix] Multiple fixes by Pull Requests


v0.2.18 (2016-03-03)
--------------------

* [Fix] Django 1.9 time and date widgets fixes `#481 <https://github.com/darklow/django-suit/issues/481>`_


v0.2.18 (2016-03-03)
--------------------

* [Fix] Django 1.9 time and date widgets fixes `#481 <https://github.com/darklow/django-suit/issues/481>`_


v0.2.17 (2016-02-23)
--------------------

* [Fix] Django 1.9 and Python 3 Compatibility fixes.


v0.2.16 (2016-01-16)
--------------------

* [Fix] Django 1.9 Compatibility fixes.


v0.2.15 (2015-09-28)
--------------------

* [Fix] Multiple Django 1.8/1.9/1.10 DeprecationWarning and compatibility fixes.
* [Fix] Fixed bug with not showing login errors in Django>1.8 `#410 <https://github.com/darklow/django-suit/pull/410>`_
* [Fix] Menu fixes and improvements `#430 <https://github.com/darklow/django-suit/pull/430>`_
* [Fix] Reversion app support fixes `#424 <https://github.com/darklow/django-suit/pull/424>`_
* [Feature] New `before_suit_styles` block in base.html `#408 <https://github.com/darklow/django-suit/pull/408>`_


v0.2.14 (2015-07-23)
--------------------

* [Fix] Django 1.8/1.9 DeprecationWarning fixes. `#396 <https://github.com/darklow/django-suit/issues/396>`_ `#365 <https://github.com/darklow/django-suit/pull/365>`_ `#383 <https://github.com/darklow/django-suit/issues/383>`_
* [Feature] Django 1.8 show_change_link inlines parameter implementation. `#366 <https://github.com/darklow/django-suit/issues/366>`_
* [Fix] Fix issues related to Django 1.7 opts.module_name to opts.model_name transition. `#405 <https://github.com/darklow/django-suit/issues/405>`_
* [Fix] Add {% welcome-msg %} block around welcome message text. `#379 <https://github.com/darklow/django-suit/issues/379>`_


v0.2.13 (2015-04-22)
--------------------

* [Fix] Django 1.8 related fixes
* [Fix] Minor fixes and accepted PR: `#358 <https://github.com/darklow/django-suit/pull/358>`_ `#322 <https://github.com/darklow/django-suit/pull/322>`_ `#356 <https://github.com/darklow/django-suit/pull/356>`_ `#357 <https://github.com/darklow/django-suit/pull/357>`_ `#325 <https://github.com/darklow/django-suit/pull/325>`_ `#333 <https://github.com/darklow/django-suit/pull/333>`_ `#351 <https://github.com/darklow/django-suit/pull/351>`_ `#354 <https://github.com/darklow/django-suit/issues/354>`_ `#360 <https://github.com/darklow/django-suit/issues/360>`_
* [Tests] Fixed Django 1.8 and deprecated travis tests


v0.2.12 (2014-11-19)
--------------------

* [Fix] Raise an exception if inline fields are defined as tuple. `#302 <https://github.com/darklow/django-suit/pull/302>`_ [Thanks to @peterfarrell]
* [Fix] Fixes change_form first field focus. `#290 <https://github.com/darklow/django-suit/pull/290>`_ `#295 <https://github.com/darklow/django-suit/issues/295>`_ [Thanks to @cybersimon]
* [Fix] Django 1.7: Fix LinkedSelect if extra url args. `#310 <https://github.com/darklow/django-suit/issues/310>`_ `#294 <https://github.com/darklow/django-suit/issues/294>`_


v0.2.11 (2014-09-11)
--------------------

* [Fix] Django 1.7 compatibility fixes


v0.2.10 (2014-09-04)
--------------------

* [Fix] Fixes `#257 <https://github.com/darklow/django-suit/pull/257>`_ Fix for django-filer>=0.9.6 [Thanks to @mkutgt72]
* [Fix] Fixes `#266 <https://github.com/darklow/django-suit/pull/266>`_ Fixed issue where SortableGenericInlines would break whenever adding blank inline forms [Thanks to @sixthgear]
* [Fix] Fixes `#270 <https://github.com/darklow/django-suit/pull/270>`_ Use get_absolute_url() if the object has_absolute_url is True [Thanks to @stvbdn]


v0.2.9 (2014-06-20)
-------------------

* [Fix] Fixes `#240 <https://github.com/darklow/django-suit/issues/240>`_ Unable to save inline models with a FileField and "sortable" enabled.
* [Fix] Fixes `#232 <https://github.com/darklow/django-suit/issues/232>`_ Inline sortable error when model features only FKs


v0.2.8 (2014-04-22)
-------------------

* [Feature] Mark active search filters. Show label prefix in selected filter option. Closes `#207 <https://github.com/darklow/django-suit/issues/207>`_


v0.2.7 (2014-03-21)
-------------------

* [Feature] `Sortables <http://django-suit.readthedocs.org/en/develop/sortables.html>`_ for `StackedInline <http://djangosuit.com/admin/examples/kitchensink/3/>`_ and Generic inlines added. Closes `#137 <https://github.com/darklow/django-suit/issues/137>`_
* [Fix] Fixes `#209 <https://github.com/darklow/django-suit/issues/209>`_ Wrap jQuery autosize in Suit jQuery scope
* [Fix] Fixes `#206 <https://github.com/darklow/django-suit/pull/206>`_ Fixed exception when menu config is Unicode [Thanks to @kane-c]
* [Fix] Fixes `#90 <https://github.com/darklow/django-suit/issues/90>`_ Django test sometimes crashes, because of Django Suit
* [Fix] Fixes login template for custom user model `#200 <https://github.com/darklow/django-suit/pull/200>`_ [Thanks to @theskumar]


v0.2.6 (2014-02-14)
-------------------

* [Fix] Fixes `#190 <https://github.com/darklow/django-suit/issues/190>`_ Django 1.6 compatibility issue: Search fails in popups
* [Fix] Fixes `#198 <https://github.com/darklow/django-suit/pull/198>`_ Remove unknown variable: "onclick_attrib" [Thanks to @blueyed]
* [Fix] Fixes `#105 <https://github.com/darklow/django-suit/issues/105>`_ AdminSite detection support for various python/django versions
* [Fix] Fixes translation issues `#162 <https://github.com/darklow/django-suit/pull/162>`_  `#175 <https://github.com/darklow/django-suit/issues/175>`_


v0.2.5 (2013-09-30)
-------------------

* [Feature] JS: `#147 <https://github.com/darklow/django-suit/pull/147>`_ Avoiding double submit by disabling submit buttons on change form submit [Thanks to @adamJLev]
* [Fix] Fixes `#157 <https://github.com/darklow/django-suit/pull/157>`_ Inline template Django 1.6b4 compatibility issue [Thanks to @nliberg]
* [Fix] Fixes `#146 <https://github.com/darklow/django-suit/issues/146>`_, `#152 <https://github.com/darklow/django-suit/issues/152>`_ Issues related to Sortables
* [Fix] Fixes `#150 <https://github.com/darklow/django-suit/issues/150>`_ Incorrect menu is marked as active when multiple apps have models with same name
* [Fix] Fixes `#149 <https://github.com/darklow/django-suit/issues/149>`_ Moved bootstrap.min.js to the <head> to support bootstrap plugins by media js


v0.2.4 (2013-08-15)
-------------------

* [Fix] JS Fix preventing empty inline creation when saving inlines with blank inputs.
* [Fix] Fixes `#140 <https://github.com/darklow/django-suit/issues/140>`_ KeyError with latest MPTT library
* [Fix] Fixes `#139 <https://github.com/darklow/django-suit/issues/139>`_ Search form doesn't submit filters on IE10


v0.2.3 (2013-08-01)
-------------------

* [Feature] Added CSS file for media=print. Reposition/hide unnecessary elements when printing.
* [Feature] More robust URL splitting/parsing for menu which now supports all kind of admin urls including `i18n_patterns` [Thanks to @philippbosch]
* [Feature] List attributes feature improvement: `suit_row_attributes` method now receives also request as an argument. [Thanks to @asteinlein]
* [Fix] CSS improvements for Mac/Safari: `box-shadow` fixes.


v0.2.2 (2013-06-21)
-------------------

* [Feature] `django-import-export <https://github.com/bmihelac/django-import-export>`_ app support. See `example <http://djangosuit.com/admin/examples/importexportitem/>`_ [Thanks to @jonashaag]
* [Fixes] CSS/Templating fixes and tweaks. See `commit log <https://github.com/darklow/django-suit/commits/develop>`_ and `closed issues <https://github.com/darklow/django-suit/issues?direction=desc&sort=updated&state=closed>`_ for full changes


v0.2.1 (2013-05-11)
-------------------

* [Feature] Styling list rows and cells based on object instance. Read `Documentation <http://django-suit.readthedocs.org/en/develop/list_attributes.html>`_. See `example <http://djangosuit.com/admin/examples/continent/>`_
* [CSS] Changed selected rows background color to inverse, to avoid color conflict with row "warning" css class
* [Fixes] CSS/Templating fixes and tweaks. See `commit log <https://github.com/darklow/django-suit/commits/develop>`_ and `closed issues <https://github.com/darklow/django-suit/issues?direction=desc&sort=updated&state=closed>`_ for full changes


v0.2.0 (2013-04-29)
-------------------

* [Major Feature] `Django-CMS <https://github.com/divio/django-cms>`_ support. See full notes here `#77 <https://github.com/darklow/django-suit/issues/77>`_. See `example <http://djangosuit.com/admin/cms/page/>`_
* [Major Feature] `Django-Filer <https://github.com/stefanfoulis/django-filer>`_ support. See `example <http://djangosuit.com/admin/filer/folder/>`_
* [CSS] Selector widget style improvements See `#80 <https://github.com/darklow/django-suit/issues/80#issuecomment-16329776>`_
* [CSS] Main content container now uses Twitter Bootstrap `row-fluid` class. See `#58 <https://github.com/darklow/django-suit/issues/58>`_
* [Refactor] Included jQuery now is using own namespace: `Suit.$`
* [Fix] CSS/Templating fixes and tweaks. See commit log and closed issues for full changes


v0.1.9 (2013-03-25)
-------------------

* [Feature] `Form tabs <http://django-suit.readthedocs.org/en/develop/form_tabs.html>`_ - help you organize form fieldsets and inlines into tabs. See `example <http://djangosuit.com/admin/examples/country/234/>`_ [Thanks to @phihos]
* [Feature] `Form includes <http://django-suit.readthedocs.org/en/develop/form_includes.html>`_ - shortcut to include templates into forms
* [Feature] `New menu syntax <http://django-suit.readthedocs.org/en/develop/configuration.html#id1>`_ supports app and model labels, separators and more clear definition syntax.


v0.1.8 (2013-03-20)
-------------------

* [Feature] `django-reversion <https://github.com/etianen/django-reversion>`_ app support. `Example <http://djangosuit.com/admin/examples/reversioneditem/>`_ [Thanks to @phihos]
* [Feature] `WYSIWYG editors <http://django-suit.readthedocs.org/en/develop/wysiwyg.html>`_ support, examples and docs
* [Feature] `Full-width fieldsets <http://django-suit.readthedocs.org/en/develop/widgets.html#css-goodies>`_
* [Feature] Introduced two related wysiwyg apps `suit-redactor <https://github.com/darklow/django-suit-redactor>`_ and `suit-ckeditor <https://github.com/darklow/django-suit-ckeditor>`_
* [CSS] New "multi-fields in row" look and behaviour.
* [CSS] Support for fieldset "wide" class 
* [Refactor] Major fieldset refactoring to support multi-line labels
* [Fix] Many CSS/Templating fixes and tweaks. See commit log for full changes


v0.1.6, v.0.1.7 (2013-03-10)
----------------------------

* [Tests] Travis CI hooked up - testing against Django 1.4-1.5, Python 2.5-3.3
* [Tests] Tests now cover every class and method in Django Suit
* [Fix] Full support for Python 3.x added
* [Critical] Django 1.4 compatibility restored. Removed django.utils.six (Django 1.4.2)


v0.1.5 (2013-03-10)
-------------------

* [Feature] New widget: `AutosizedTextarea <http://django-suit.readthedocs.org/en/develop/widgets.html#autosizedtextarea>`_
* [Feature] New widget: `LinkedSelect <http://django-suit.readthedocs.org/en/develop/widgets.html#linkedselect>`_
* [Feature] JavaScript inlines hook: `SuitAfterInline JS hook <http://django-suit.readthedocs.org/en/develop/widgets.html#javascript-goodies>`_
* [Tests] Tests means more stability - bunch of tests added, more to come.
* [Fix/Refactoring] Install breaks under certain conditions #17
* [Fix] Admin save_on_top=True breaks change form #16
* [Fix] Minor bugs and tweaks. See commit log for full changes


v0.1.4 (2013-03-04)
-------------------

* [Fix] Sortables improvements and fixes #12, #13, #14
* [Fix] Python3 related fixes #11 [Thanks to @coagulant]
* [Fix] Firefox floating problem for list "New" button #15


v0.1.3 (2013-03-03)
-------------------

* [Feature] `Sortables <http://django-suit.readthedocs.org/en/develop/sortables.html>`_ for `change list <http://djangosuit.com/admin/examples/continent/>`_, `mptt-tree <http://djangosuit.com/admin/examples/category/>`_ list and `tabular inlines <http://djangosuit.com/admin/examples/continent/9/>`_.
* [Feature] `EnclosedInput widget <http://django-suit.readthedocs.org/en/develop/widgets.html#enclosedinput>`_ for Twitter Bootstrap appended/prepended inputs. `Example <http://djangosuit.com/admin/examples/city/5/>`_
* [Feature] `HTML5Input <http://django-suit.readthedocs.org/en/develop/widgets.html#html5input>`_ widget
* [Documentation] Added detailed docs and examples on sortables and widgets
* [Fix] Minor bugs and tweaks. See commit log for full changes


v0.1.2 (2013-02-27)
-------------------

* [Feature] Customizable menu, cross apps, custom links and menus
* [Refactoring] Moved all static files to separate directory
* [Fix] PEP8 and templates style improvements [Thanks to @peterfschaadt]
* [Fix] Fixed inconsistent styling on login form errors [Thanks to @saippuakauppias]


v0.1.1 (2013-02-25)
-------------------

* [Feature] Added link to admin home in error templates
* [Feature] Config key SEARCH_URL now supports also absolute urls
* [Fix] SEARCH_URL fallback uses absolute URL instead of urlname


v0.1.0 (2013-02-24)
-------------------

* First stable version released
