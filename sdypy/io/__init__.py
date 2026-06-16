"""sdypy.io - unified I/O for structural dynamics: UFF (pyuff), LVM (lvm_read), MRAW (pyMRAW) and SFMOV readers exposed under the sdypy namespace."""

from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("sdypy-io")
except PackageNotFoundError:  # source checkout without installed metadata
    __version__ = "0+unknown"

import pyuff as uff
import lvm_read as lvm
import pyMRAW as mraw
from .sfmov import sfmov

__all__ = ["uff", "lvm", "mraw", "sfmov"]
