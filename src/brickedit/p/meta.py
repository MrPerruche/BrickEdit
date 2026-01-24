import struct
from typing import Final

from . import base as _b
from .. import vec as _vec
# from ..brick import Brick as _Brick



# Ran benchmarks on different possible implementations of EnumMeta and TextMeta:
# - bytearray(bytes() + bytes()) or bytearray((uint8, *bytes())),
# - isascii() or try: ... except UnicodeEncodeError,
# and a few other things. These implementations seem optimal

_STRUCT_UINT8 = struct.Struct('B')
_STRUCT_UINT16 = struct.Struct('<H')
_STRUCT_INT16 = struct.Struct('<h')
# _STRUCT_UINT32 = struct.Struct('<I')
_STRUCT_UINT32_BIGENDIAN = struct.Struct('>I')
_STRUCT_SPFLOAT = struct.Struct('<f')



class BooleanMeta(_b.PropertyMeta[bool]):
    """Base class for booleans"""

    @staticmethod
    def serialize(
        v: bool,
        version: int,
        ref_to_idx: dict[str, int]
    ) -> bytes:
        return b'\x01' if v else b'\x00' # more efficient than [int(v)] apparently

    @staticmethod
    def deserialize(v: bytes, version: int) -> bool:
        return v == b'\x01'

class EnumMeta(_b.PropertyMeta[str]):
    """Base class for enum properties."""

    @staticmethod
    def serialize(
        v: str,
        version: int,
        ref_to_idx: dict[str, int]
    ) -> bytes:
        # return bytearray(struct.pack('B', len(v)) + v.encode('ascii'))
        v_bytes = v.encode('ascii')
        return _STRUCT_UINT8.pack(len(v_bytes)) + v_bytes

    @staticmethod
    def deserialize(v: bytes, version: int) -> str:
        return v[1: ].decode('ascii')


class TextMeta(_b.PropertyMeta[str]):
    """Base class for text input properties."""

    @staticmethod
    def serialize(
        v: str,
        version: int,
        ref_to_idx: dict[str, int]
    ) -> bytes:

        is_ascii = v.isascii()
        v_bytes = v.encode('ascii') if is_ascii else v.encode('utf-16-le')

        len_v = len(v) if is_ascii else -len(v_bytes) // 2
        return _STRUCT_INT16.pack(len_v) + v_bytes

    @staticmethod
    def deserialize(v: bytes, version: int) -> str:

        text_len = _STRUCT_INT16.unpack(v[ :2])[0]
        return v[2: ].decode('ascii') if text_len >= 0 else v[2: ].decode('utf-16-le')


class Float32Meta(_b.PropertyMeta[float]):
    """Class for 32-bit floats"""

    @staticmethod
    def serialize(
        v: float,
        version: int,
        ref_to_idx: dict[str, int]
    ) -> bytes:

        return _STRUCT_SPFLOAT.pack(v)

    @staticmethod
    def deserialize(v: bytes, version: int) -> float:
        return _STRUCT_SPFLOAT.unpack(v)[0]


_STRUCT_2SPFLOAT = struct.Struct('<2f')

class Vec2Meta(_b.PropertyMeta[_vec.Vec2]):
    """Size of bricks"""

    @staticmethod
    def serialize(
        v: _vec.Vec2,
        version: int,
        ref_to_idx: dict[str, int]
    ) -> bytes:
        return _STRUCT_2SPFLOAT.pack(*v.as_tuple())

    @staticmethod
    def deserialize(v: bytes, version: int) -> _vec.Vec2:
        return _vec.Vec2(*_STRUCT_2SPFLOAT.unpack_from(v))


class Color3ChannelsMeta(_b.PropertyMeta[int]):
    """
    Class for 3-channel colors.
    All 3-channel color properties accepts a 4th channel since BRV15.
    When deserializing in BRV15 and newer, the 4th channel is included.
    By default, Brick Rigs set alpha to 0xff (255). To remove alpha, use value & 0x00ffffff
    """

    @staticmethod
    def serialize(
        v: int,
        version: int,
        ref_to_idx: dict[str, int]
    ) -> bytes:
        # We use big-endian since brickedit represent colors as 0xrrggbbaa
        return _STRUCT_UINT32_BIGENDIAN.pack(v)

    @staticmethod
    def deserialize(v: bytes, version: int) -> float:
        # We use big-endian since brickedit represent colors as 0xrrggbbaa
        return _STRUCT_UINT32_BIGENDIAN.unpack(v)[0]


class Color4ChannelsMeta(_b.PropertyMeta[int]):
    """Class for 4-channel colors"""

    @staticmethod
    def serialize(
        v: int,
        version: int,
        ref_to_idx: dict[str, int]
    ) -> bytes | _b.InvalidVersionType:
        # We use big-endian since brickedit represent colors as 0xrrggbbaa
        return _STRUCT_UINT32_BIGENDIAN.pack(v)

    @staticmethod
    def deserialize(v: bytes, version: int) -> int:
        # We use big-endian since brickedit represent colors as 0xrrggbbaa
        return _STRUCT_UINT32_BIGENDIAN.unpack(v)[0]


class InputAxisMeta(EnumMeta):
    """Class for input channel input axis"""

    NONE: Final[str] = 'None'
    ALWAYS_ON: Final[str] = 'AlwaysOn'
    CUSTOM: Final[str] = 'Custom'

    STEERING: Final[str] = 'Stering'
    STEERING_ALT: Final[str] = 'SteeringAlt'
    THROTTLE: Final[str] = 'Throttle'

    THROTTLE_ALT: Final[str] = 'ThrottleAlt'
    BRAKE: Final[str] = 'Brake'
    BRAKE_ALT: Final[str] = 'BrakeAlt'

    PITCH: Final[str] = 'Pitch'
    PITCH_ALT: Final[str] = 'PitchAlt'
    VIEW_PITCH: Final[str]= 'ViewPitch'

    VIEW_PITCH_ALT: Final[str] = 'ViewPitchAlt'
    VIEW_YAW: Final[str] = 'ViewYaw'
    VIEW_YAW_ALT: Final[str] = 'ViewYawAlt'

    HORN: Final[str] = 'Horn'
    DISABLE_STEERING: Final[str] = 'DisableSteering'
    INVERT_STEERING: Final[str] = 'InvertSteering'

    HANDBRAKE: Final[str] = 'HandBreake'
    OPERATION_MODE: Final[str] = 'OperationMode'
    HEADLIGHT: Final[str] = 'Headlight'

    BEACON: Final[str] = 'Beacon'
    WARNING_LIGHT: Final[str] = 'WarningLight'
    TAILLIGHT: Final[str] = 'Taillight'

    BRAKE_LIGHT: Final[str] = 'BrakeLight'
    REVERSING_LIGHT: Final[str] = 'ReversingLight'
    FIRE_ACTION_1: Final[str] = 'Action1'

    FIRE_ACTION_2: Final[str] = 'Action2'
    FIRE_ACTION_3: Final[str] = 'Action3'
    FIRE_ACTION_4: Final[str] = 'Action4'

    FIRE_ACTION_5: Final[str] = 'Action5'
    FIRE_ACTION_6: Final[str] = 'Action6'
    FIRE_ACTION_7: Final[str] = 'Action7'

    FIRE_ACTION_8: Final[str] = 'Action8'



class SingleSourceBrickMeta(_b.PropertyMeta[str]):
    """Class for single input channel argument (seats, ...)"""

    EMPTY: Final[str] = None

    @staticmethod
    def serialize(
        v: str,
        version: int,
        ref_to_idx: dict[str, int]
    ) -> bytes | _b.InvalidVersionType:

        idx = ref_to_idx.get(v)
        if idx is None:
            raise ValueError(f"Unknown brick reference {v!r}.")
        return _STRUCT_UINT16.pack(idx)

    @staticmethod
    def deserialize(v: str, version: int):
        return f'brick_{_STRUCT_UINT16.unpack(v)[0]}'



class SourceBricksMeta(_b.PropertyMeta[tuple[str, ...]]):
    """Class for custom input channel argument"""

    EMPTY: Final[tuple] = ()

    @staticmethod
    def serialize(
        v: tuple[str, ...],
        version: int,
        ref_to_idx: dict[str, int]
    ) -> bytes | _b.InvalidVersionType:

        idx = []
        for ref in v:
            i = ref_to_idx.get(ref)
            if i is None:
                raise ValueError(f"Unknown brick reference {ref!r}.")
            idx.append(i)
        return struct.pack(f'<H{len(idx)}H', len(idx), *idx)

    @staticmethod
    def deserialize(v: bytes, version: int) -> tuple[str, ...] | _b.InvalidVersionType:
        count = _STRUCT_UINT16.unpack_from(v)[0]
        idx = struct.unpack_from(f'<{count}H', v, offset=2)
        return tuple(f'brick_{i-1}' for i in idx)


class ValueMeta(Float32Meta):
    """Class for constant value channel argument"""

    DEFAULT_VALUE: Final[float] = 1.0
