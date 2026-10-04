import io
from os import write
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
    for b in reversed(buf):
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
    workshop_refs: bool = False
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
            self.workshop_refs    << 8  |
            self.creation_time    << 9  |
            self.last_update_time << 10 |
            self.visibility       << 11 |
            self.tags             << 12
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
        workshop_refs: Optional[list[tuple[str | bytes, int]]] = None,
        visibility: int = 0,
        tags: Optional[list[str]] = None,
        creation_time: int | None = None,
        last_update_time: int | None = None,
    ) -> bytearray:
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
            author (int, optional): Author. Defaults to 0.
            workshop_refs (Optional[list[tuple[str | bytes, int]]], optional): Workshop references. Defaults to None
                WARNING: Automatically places null character. To avoid automatic placement, use bytes instead of str.
            visibility (int, optional): Visibility. Defaults to 0.
            tags (Optional[list[str]], optional): Tags. Defaults to None.
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

        if tags is None:
            tags = []

        if len(tags) > 65_535:
            raise ValueError(f"Too many tags! Max: 65,535, got {len(tags)}")

        # Init buffer
        buffer = bytearray()

        # No repeated global lookups
        write = buffer.extend

        # Precompile struct
        pack_B = struct.Struct('B').pack   # 'B'  → uint8
        pack_H = struct.Struct('<H').pack  # '<H' → uint16 LE
        pack_i = struct.Struct('<i').pack  # '<i' → int32 LE
        pack_I = struct.Struct('<I').pack  # '<I' → uint32 LE
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
        write(pack_B(len(bin_author)))
        write(bin_author)

        # Workshop refs
        refs = workshop_refs or []
        write(pack_I(len(refs)))

        for service, sid in refs:
            if isinstance(service, str):
                if not service.endswith('\0'):
                    service += '\0'
                if service.isascii():
                    write(pack_i(len(service)))
                    write(service.encode('ascii'))
                else:
                    enc = service.encode('utf-16-le')
                    write(pack_i(-(len(enc) // 2)))
                    write(enc)
            else:
                write(pack_i(len(service))); write(service)  # raw ASCII bytes
            write(pack_Q(sid))

        # Creation and update time
        write(pack_Q(creation_time))
        write(pack_Q(last_update_time))

        write(pack_B(visibility))

        tags = (tags or [])[:3]
        tags += ['None'] * (3 - len(tags))
        for t in tags:
            enc = t.encode('ascii')
            write(pack_B(len(enc)))
            write(enc)

        return buffer



    _UNPACK_FROM_B = struct.Struct('B').unpack_from
    _UNPACK_FROM_h = struct.Struct('<h').unpack_from
    _UNPACK_FROM_H = struct.Struct('<H').unpack_from
    _UNPACK_FROM_i = struct.Struct('<i').unpack_from
    _UNPACK_FROM_I = struct.Struct('<I').unpack_from
    _UNPACK_FROM_5f = struct.Struct('<5f').unpack_from
    _UNPACK_FROM_Q = struct.Struct('<Q').unpack_from
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
        unpack_from_i = self._UNPACK_FROM_i
        unpack_from_I = self._UNPACK_FROM_I
        unpack_from_5f = self._UNPACK_FROM_5f
        unpack_from_Q = self._UNPACK_FROM_Q
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

        # -- 4 bytes of dread (workshop refs)
        do_workshop_refs = config.workshop_refs
        workshop_refs_count, = unpack_from_I(mv, offset); offset += 4
        workshop_refs_result = []

        for _ in range(workshop_refs_count):
            # Get service length
            service_len, = unpack_from_i(mv, offset); offset += 4
            is_ascii = service_len >= 0
            service_byte_len = service_len if is_ascii else -2 * service_len

            if do_workshop_refs:
                service = bytes(mv[offset : offset+service_byte_len]).decode('ascii' if is_ascii else 'utf-16-le')
                sid, = unpack_from_Q(mv, offset+service_byte_len)
                workshop_refs_result.append((service, sid))
            offset += service_byte_len + 8

        # Add to result only if we care. Results are not build if we don't btw
        if do_workshop_refs:
            result.append(workshop_refs_result)

        if last_step <= 8:
            return result


        # Create and update time (.NET)
        # DOING STEP 9 & 10 SIMULTANEOUSLY
        creation_time, last_update_time = unpack_from_2Q(mv, offset)
        if config.creation_time:
            result.append(creation_time)
        if config.last_update_time:
            result.append(last_update_time)
        offset += 16

        if last_step <= 10:
            return result

        # -- Visibility
        if config.visibility:
            result.append(mv[offset])
        offset += 1

        if last_step <= 11:
            return result

        # -- Tags
        # Do not care about propertly updating offset if we don't load because this is EOF
        if config.tags:
            tags = []
            for _ in range(3):
                n = mv[offset]; offset += 1
                tags.append(bytes(mv[offset:offset+n]).decode('ascii'))
                offset += n
            result.append(tags)


        return result

