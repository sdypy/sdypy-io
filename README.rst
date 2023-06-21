sdypy-io
========

Read/write experimental and analysis data in the field of structural dynamics. Check out the `documentation <https://sdypy-io.readthedocs.io/en/latest/>`_.

Currently, the ``SDyPy-io`` package supports the reading and writing of the UFF (Universal File Format) files and reading of the LVM files.

To use the package, install the ``sdypy`` package:

.. code:: bash

   pip install sdypy

The ``io`` module is imported as follows:

.. code:: python

   from sdypy import io

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

LVM file format
---------------
The ``read`` function parses the LVM file and returns a dictionary with the data.
