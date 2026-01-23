"""BrickEdit is a python package for working with the .BRV and .BRM file formats, belonging to the game Brick Rigs.
It can read, write, and manipulate the contents of .BRV and .BRM files."""
from .vec import *
from .var import *
from .var import BRICKEDIT_VERSION_FULL as __version__
from .id import *
from .brick import *
from .brv import *
from .brm import *
from . import p
from . import bt
from . import vhelper
