===========
Change logs
===========

Version 0.1.1
=============

:date: 2026-05-17 (Asia/Tokyo)

Fixes
-----

* Align bundled Typst package version with Python package version.

Version 0.1.0
=============

:date: 2026-05-16 (Asia/Tokyo)

Breaking changes
----------------

* Restructure context variables for templates. [ `#44`_ ]

  * Flat context variable structure.
  * Drop ``head`` from template context.

* Restructure writing context. [ `#44`_ ]
* Use Typst package registry for rendering instead of bundled module.
  [ `#44`_ ]

Features
--------

* Convert internal implements to use ``rst2typst`` library. [ `#40`_ ]
* Define autoloader to setup adapter extensions from registered extensions.
  [ `#43`_ ]
* Add support for ``todo`` directive via adapter extension.
* Add visitor/departure for desc nodes (function/class signatures). [ `#47`_ ]
* Restructure block of templates. [ `#48`_ ]
* Add index of confval entry support. [ `#49`_ ]
* Resolve and link cross-references.
* Separate render function into Typst package.

Fixes
-----

* Guard case that author is not set.
* Set full-width into raw content wrapped by figure.
* Update optional nodes to avoid errors.

.. _#40: https://github.com/atsphinx/typst/pull/40
.. _#43: https://github.com/atsphinx/typst/pull/43
.. _#44: https://github.com/atsphinx/typst/pull/44
.. _#47: https://github.com/atsphinx/typst/pull/47
.. _#48: https://github.com/atsphinx/typst/pull/48
.. _#49: https://github.com/atsphinx/typst/pull/49

Version 0.0.5
=============

:date: 2025-09-07 (Asia/Tokyo)

Features
--------

* Support ``admonition`` and inherited directives.
* Support custom font.
* Add "toctree_only" mode on document_settings.

Fixes
-----

* Update escape rule.

Version 0.0.4
=============

:date: 2025-07-29 (Asia/Tokyo)

Breaking changes
----------------

Features
--------

* Copy ``static_path`` assets.
  and add ``typst_static_path`` as configuration.
* Copy document assets (e.g. image files).
* Ignore comment nodes of docutils.
* Enable footnotes.

Fixes
-----

* Remove hash from ``image`` call wrapped by ``figure``.

Others
------

* Restructure element classes.
* Sort visitor/departure methods of translator.
* Experimental support Japanese document.
* Update workspace environment.

Version 0.0.3
=============

:date: 2025-07-26 (Asia/Tokyo)

Breaking changes
----------------

* Change key of ``typst_documents`` from ``'entry'`` to ``'entrypoint'``.
* Change template name of theme.

Features
--------

* Update structure of theme.
* Add theme 'basic' and split some features from 'manual'.
* Theme can pass assets (include any inherited themes)

Fixes
-----

Others
------

Version 0.0.2
=============

:date: 2025-07-23 (Asia/Tokyo)

Fixes
-----

* Controle version using import-metadata.

Others
------

* Restructure modules.

Version 0.0.1
=============

:date: 2025-07-21 (Asia/Tokyo)

First published release.

Features
--------

* Add builders.

Version 0.0.0
=============

:date: 2025-06-13 (Asia/Tokyo)

Initial commit.
