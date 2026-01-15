import io
import struct
from typing import Optional

from .vec import Vec3 as _Vec3
from .brv import BRVFile
from .p import TextMeta as _UserTextSerialization
from .vhelper.time import net_ticks_now as _net_ticks_now


def _encode_author(author: int) -> int:
    """Encodes authors"""
    s = str(author)
    result = 0

    # Process digits in pairs from right to left
    for i, j in enumerate(range(len(s), 0, -2)):
        if j - 2 >= 0:
            seg = s[j-2 : j]
            # Swap digits and shift into place
            result += (int(seg[1]) << 4 | int(seg[0])) << (i * 8)
        else:
            # Single leading digit (odd length)
            result += int(s[0]) << (i * 8 + 4)

    return result



class BRMFile:

    def __init__(self, version: int, brv: Optional[BRVFile] = None):
        self.version = version
        self.brv = brv

    def serialize(
        self,
        file_name: Optional[str] = None,
        description: str = '',
        brick_count: Optional[int] = None,
        size: _Vec3 = _Vec3(0, 0, 0),
        weight: float = 0.0,
        price: float = 0.0,
        author: int = 0,
        visibility: int = 0,
        tags: Optional[list[str]] = None,
        creation_time: int | None = None,
        last_update_time: int | None = None,
    ):
        """Serializes a BRMFile

        Args:
            file_name (Optional[str], optional): Auto-generated if it is an empty string. Can be an
                empty string. Defaults to None.
            description (str, optional): Description. Defaults to ''.
            brick_count (Optional[int], optional): Auto-generated if None and a brv is provided.
                Defaults to None.
            size (_Vec3, optional): Size. Defaults to _Vec3(0, 0, 0).
            weight (float, optional): Weight. Defaults to 0.0.
            price (float, optional): Price. Defaults to 0.0.
            creation_time (int | None, optional): Creation time in BR's format. Defaults to None.
            last_update_time (int | None, optional): Creation time in BR's format. Defaults to None.
        """

        creation_time = _net_ticks_now() if creation_time is None else creation_time
        last_update_time = _net_ticks_now() if last_update_time is None else last_update_time

        if self.brv is not None:
            if brick_count is None:
                brick_count = len(self.brv.bricks)

        if file_name is None:
            file_name = f'BrickEdit-{last_update_time}'

        assert brick_count <= 65_534, "Too many bricks! Max: 65,534"

        # Init buffer
        buffer = io.BytesIO()

        # No repeated global lookups
        write = buffer.write

        # Precompile struct
        pack_B = struct.Struct('B').pack   # 'B'  → uint8
        pack_H = struct.Struct('<H').pack  # '<H' → uint16 LE
        # pack_I = struct.Struct('<I').pack  # '<I' → uint32 LE
        pack_Q = struct.Struct('<Q').pack  # '<Q' → uint64 LE
        pack_f = struct.Struct('<f').pack  # '<f' → sp float LE
        pack_vec3 = struct.Struct('<3f').pack

        # Write version
        write(pack_B(self.version))

        # Write name
        write(_UserTextSerialization.serialize(file_name, self.version, {}))
        # Write description
        write(_UserTextSerialization.serialize(description, self.version, {}))

        # Write brick count
        write(pack_H(brick_count))

        # Write size
        write(pack_vec3(*size.as_tuple()))

        # Write weight and price
        write(pack_f(weight))
        write(pack_f(price))

        # Write author
        # Convert author to string.
        write(b'\x1D')  # Steam id stuff
        for b in bytearray(_encode_author(author)):
            write(pack_B(b))

        write(b'\x00\x00\x00\x00')  # TODO

        # Creation and update time
        write(pack_Q(creation_time))
        write(pack_Q(last_update_time))

        write(pack_B(visibility))

        write(pack_H(len(tags)))
        for t in tags:
            write(pack_B(len(t)))
            write(t.encode('ascii'))

        return buffer.getvalue()
