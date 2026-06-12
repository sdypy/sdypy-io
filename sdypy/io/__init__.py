"""
A project template for the SDyPy effort..
"""

from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("sdypy-io")
except PackageNotFoundError:  # source checkout without installed metadata
    __version__ = "0+unknown"

import pyuff as uff
import lvm_read as lvm
import pyMRAW as mraw
from .sfmov import sfmov
