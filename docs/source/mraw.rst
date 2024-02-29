MRAW file format
================

Photron MRAW File Reader and Writer.

The ``mraw`` module provides a direct link to the `pyMRAW <https://github.com/ladisk/pyMRAW>`_ package.

A simple example:

.. code-block:: python

    import sdypy as sd

    # Read a MRAW file
    mraw_data, info = sd.io.mraw.load_video('path/to/file.cih')

For reference, see the `pyMRAW <https://github.com/ladisk/pyMRAW>`_.