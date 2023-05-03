LVM file format
=================

The ``LVM`` read/write module is a wrapper of the lvm_read_ module.

See the ``lvm_read`` showcase_ for more information.

.. note::

    To use the LVM module from ``SDyPy-io`` package, the import must be changed from:

    .. code:: python

        import lvm_read

    to 

    .. code:: python
        
        from sdypy import io

    All current and future ``lvm_read`` functionality is then available through ``io.lvm``. 
    
    Example:

    .. code:: python

        lvm_data = io.lvm.read('data/beam.lvm') # instead of lvm_read.read('data/beam.uff')
        lvm_data.keys()


.. _lvm_read: https://pypi.org/project/lvm-read/
.. _showcase: https://github.com/openmodal/lvm_read/blob/master/Showcase%20lvm_read.ipynb