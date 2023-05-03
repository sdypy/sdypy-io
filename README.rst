sdypy-io
========

Read/write experimental and analysis data in the field of structural dynamics. Check out the `documentation <https://pyuff.readthedocs.io/en/latest/index.html>`_.

Currently, the ``SDyPy-io`` package supports the reading and writing of the UFF (Universal File Format) files.

To install the package, run:

.. code:: bash

   pip install sdypy.io

or install the full ``sdypy`` package:

.. code:: bash

   pip install sdypy

Universal File Format read and write
------------------------------------
The UFF class is defined to manipulate the UFF (Universal File Format) files.

Currently supported UFF data-set types:
- 15
- 55
- 58
- 58b
- 82
- 151
- 164
- 2411
- 2412
- 2414
- 2420
- 2429

|pytest|

|binder| to test the *pyuff Showcase.ipynb* online.

.. |binder| image:: http://mybinder.org/badge.svg
   :target: http://mybinder.org:/repo/ladisk/pyuff
.. |pytest| image:: https://github.com/ladisk/pyuff/actions/workflows/python-package.yml/badge.svg
    :target: https://github.com/ladisk/pyuff/actions