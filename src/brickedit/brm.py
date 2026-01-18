import io
import struct
from typing import Optional, Any

from .vec import Vec3 as _Vec3
from .brv import BRVFile
from .p import TextMeta as _UserTextSerialization
from .vhelper.time import net_ticks_now as _net_ticks_now
from dataclasses import dataclass 


_ENCODE_2DIGITS = tuple((i % 10) | ((i // 10) << 4) for i in range(100))

def encode_author(author: int) -> int:
    result = 0
    shift = 0
    while author:
        author, byte_value = divmod(author, 100)
        result |= _ENCODE_2DIGITS[byte_value] << shift
        shift += 8
    return result


def decode_author(buf: bytes | bytearray | memoryview) -> int:
    result = 0
    mul = 1
    for b in buf:
        lo = b & 0x0F
        hi = b >> 4

        result += lo * mul
        mul *= 10

        # Avoid branch misprediction penalty
        result += hi * mul
        mul *= 10
    return result


@dataclass(frozen=True, slots=True)
class BRMDeserializationConfig:
    version: bool = False
    name: bool = False
    description: bool = False
    brick_count: bool = False
    size: bool = False
    weight: bool = False
    price: bool = False
    author: bool = False
    creation_time: bool = False
    last_update_time: bool = False
    visibility: bool = False
    tags: bool = False

    _length: int = 0

    def __post_init__(self):
        object.__setattr__(self, "_length", (
            self.version          << 0  |
            self.name             << 1  |
            self.description      << 2  |
            self.brick_count      << 3  |
            self.size             << 4  |
            self.weight           << 5  |
            self.price            << 6  |
            self.author           << 7  |
            self.creation_time    << 8  |
            self.last_update_time << 9  |
            self.visibility       << 10 |
            self.tags             << 11
        ).bit_length())

    def length(self) -> int:
        return self._length



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
        buffer = bytearray()

        # No repeated global lookups
        write = buffer.extend

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
        packed_author = encode_author(author)
        # (... + 7) // 8 is like ceil() for bytes.
        bin_author = packed_author.to_bytes((packed_author.bit_length() + 7)//8, 'little')
        write(bin_author)

        write(b'\x00\x00\x00\x00')  # The 4 forbidden bytes that breaks brms if you edit them

        # Creation and update time
        write(pack_Q(creation_time))
        write(pack_Q(last_update_time))

        write(pack_B(visibility))

        write(pack_H(len(tags)))
        for t in tags:
            write(pack_B(len(t)))
            write(t.encode('ascii'))

        return buffer.getvalue()



    _UNPACK_FROM_B = struct.Struct('B').unpack_from
    _UNPACK_FROM_h = struct.Struct('<h').unpack_from
    _UNPACK_FROM_H = struct.Struct('<H').unpack_from
    _UNPACK_FROM_5f = struct.Struct('<5f').unpack_from
    _UNPACK_FROM_2Q = struct.Struct('<2Q').unpack_from


    def deserialize(self, buffer: bytes | bytearray, config: BRMDeserializationConfig, auto_version: bool = False) -> list[Any]:
        """Deserializes the BRMFile according to the config.

        Args:
            buffer (bytes | bytearray): The buffer to deserialize.
            config (BRMDeserializationConfig): Configuration for deserialization.
            auto_version (bool, optional): If true, will automatically set self.version
                to the version found in the buffer. Defaults to False.

        Returns:
            dict: A dictionary with the deserialized data.
        """

        result = []

        # Get memory view
        mv = memoryview(buffer)

        # Get version before running other stuff
        brm_version: int = mv[0]
        if auto_version:
            self.version = brm_version
        if config.version:
            result.append(brm_version)

        # Precompute, local cache and other variables
        last_step = config.length()
        version = self.version
        offset = 3  # 1 because we already loaded version + 2 because the next value also has a fixed size

        unpack_from_B = self._UNPACK_FROM_B
        unpack_from_h = self._UNPACK_FROM_h
        unpack_from_H = self._UNPACK_FROM_H
        unpack_from_5f = self._UNPACK_FROM_5f
        unpack_from_2Q = self._UNPACK_FROM_2Q


        # -- Name and description
        # for UTF-16, we use -2*name_len because each element in a UTF-16 string is 2 bytes
        #   we use - because utf-16/ascii is indicated by whether the length is negative or not

        if last_step <= 1:
            return result

        name_len, = unpack_from_h(mv, 1)  # Compute before because we use it eitherway
        name_byte_len = name_len if name_len >= 0 else -2*name_len
        if config.name:
            if name_len >= 0:  # ASCII
                name = bytes(mv[offset : offset+name_byte_len]).decode('ascii')
            else:  # UTF-16
                name = bytes(mv[offset : offset+name_byte_len]).decode('utf-16-le')
            result.append(name)
        offset += name_byte_len

        if last_step <= 2:
            return result

        desc_len, = unpack_from_h(mv, offset)
        desc_byte_len = desc_len if desc_len >= 0 else -2*desc_len
        offset += 2
        if config.description:
            if desc_len >= 0:  # ASCII
                desc = bytes(mv[offset : offset+desc_byte_len]).decode('ascii')
            else:  # UTF-16
                desc = bytes(mv[offset : offset+desc_byte_len]).decode('utf-16-le')
            result.append(desc)
        offset += desc_byte_len

        if last_step <= 3:
            return result

        # -- Brick count

        brick_count, = unpack_from_H(mv, offset)
        if config.brick_count:
            result.append(brick_count)
        offset += 2

        if last_step <= 4:
            return result

        # -- Size, weight, price
        sx, sy, sz, weight, price = unpack_from_5f(mv, offset)
        offset += 20
        
        if config.size:
            result.append(_Vec3(sx, sy, sz))
        if config.weight:
            result.append(weight)
        if config.price:
            result.append(price)

        if last_step <= 6:
            return result

        # -- Author (insert thousand miles stare)
        # AUTHOR_MARKER = 0x1D
        # assert mv[offset] == AUTHOR_MARKER
        offset += 1

        author_len, = unpack_from_B(mv, offset)
        offset += 1
        if config.author:
            author = decode_author(mv[offset : offset+author_len])
            result.append(author)
        offset += author_len

        if last_step <= 7:
            return result

        # -- 4 bytes of dread
        offset += 4

        # Create and update time (.NET)
        creation_time, last_update_time = unpack_from_2Q(mv, offset)
        if config.creation_time:
            result.append(creation_time)
        if config.last_update_time:
            result.append(last_update_time)
        offset += 8

        if last_step <= 9:
            return result

        # -- Visibility
        if config.visibility:
            result.append(mv[offset])
        offset += 1

        if last_step <= 10:
            return result

        # -- Tags
        # Do not care about propertly updating offset if we don't load because this is EOF
        if config.tags:
            num_tags, = unpack_from_h(mv, offset)
            offset += 2
            tags = [None] * num_tags
            for i in range(num_tags):
                tag_len = mv[offset]
                offset += 1
                tag = mv[offset : offset+tag_len].decode('ascii')
                offset += tag_len
                tags[i] = tag
            result.append(tags)


        return result
