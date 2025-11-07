import io
import struct
from typing import Optional

from .brv import BRVFile
from .p import TextMeta as _UserTextSerialization

class BRMFile:

    def __init__(self, version: int, brv: Optional[BRVFile] = None):
        self.version = version
        self.brv = brv

    def serialize(self):

        # Init buffer
        buffer = io.BytesIO()

        # No repeated global lookups
        write = buffer.write

        # Precompile struct
        pack_B = struct.Struct('B').pack   # 'B'  → uint8
        pack_H = struct.Struct('<H').pack  # '<H' → uint16 LE
        pack_I = struct.Struct('<I').pack  # '<I' → uint32 LE
        pack_f = struct.Struct('<f').pack  # '<f' → sp float LE
        
        write(pack_B(self.version))
        