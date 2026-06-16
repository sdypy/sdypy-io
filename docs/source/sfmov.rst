SFMOV file format
=================

FLIR SFMOV File Reader.

The ``sfmov`` module provides a direct link to the `pysfmov <https://github.com/LolloCappo/pysfmov>`_ package.

A simple example:

.. code-block:: python

    # Import the module
    from sdypy import io

    # Set the path and the filename
    filename = './data/rec.sfmov'

    # Get data from sfmov file
    data = io.sfmov.get_data(filename)

    # Get meta data from sfmov file
    meta_data = io.sfmov.get_meta_data(filename)

For reference, see the `pyMRAW <https://github.com/LolloCappo/pysfmov>`_.