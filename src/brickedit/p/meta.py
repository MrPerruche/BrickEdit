import struct
from typing import Final

from . import base as _b
# from ..brick import Brick as _Brick



# Ran benchmarks on different possible implementations of EnumMeta and TextMeta:
# - bytearray(bytes() + bytes()) or bytearray((uint8, *bytes())),
# - isascii() or try: ... except UnicodeEncodeError,
# and a few other things. These implementations seem optimal

class Boolean(_b.PropertyMeta[bool]):
    """Base class for booleans"""

    @staticmethod
    def serialize(
        v: bool,
        version: int,
        ref_to_idx: dict[str, int]
    ) -> bytearray:
        return bytearray(int(v))

    @staticmethod
    def deserialize(v: bytearray, version: int) -> bytearray:
        return v == b'\x01'

class EnumMeta(_b.PropertyMeta[str]):
    """Base class for enum properties."""

    @staticmethod
    def serialize(
        v: str,
        version: int,
        ref_to_idx: dict[str, int]
    ) -> bytearray:
        # return bytearray(struct.pack('B', len(v)) + v.encode('ascii'))
        v_bytes = v.encode('ascii')
        return bytearray(struct.pack('B', len(v_bytes)) + v_bytes)

    @staticmethod
    def deserialize(v: bytearray, version: int) -> str:
        return v[1: ].decode('ascii')


class TextMeta(_b.PropertyMeta[str]):
    """Base class for text input properties."""

    @staticmethod
    def serialize(
        v: str,
        version: int,
        ref_to_idx: dict[str, int]
    ) -> bytearray:

        is_ascii = v.isascii()
        v_bytes = v.encode('ascii') if is_ascii else v.encode('utf-16-le')

        len_v = len(v) if is_ascii else -len(v)
        return bytearray(struct.pack('<h', len_v) + v_bytes)

    @staticmethod
    def deserialize(v: bytearray, version: int) -> str:

        text_len = struct.unpack('<h', v[ :2])[0]
        return v[2: ].decode('ascii') if text_len >= 0 else v[2: ].decode('utf-16-le')


class Float32Meta(_b.PropertyMeta[float]):
    """Class for 32-bit floats"""

    @staticmethod
    def serialize(
        v: float,
        version: int,
        ref_to_idx: dict[str, int]
    ) -> bytearray:

        return bytearray(struct.pack('<f', v))

    @staticmethod
    def deserialize(v: bytearray, version: int) -> float:
        return struct.unpack('<f', v)[0]


class UInteger24(_b.PropertyMeta[int]):
    """Class for 24-bit unsigned integers"""

    @staticmethod
    def serialize(
        v: int,
        version: int,
        ref_to_idx: dict[str, int]
    ) -> bytearray:
        return bytearray(struct.pack('<I', v)[ :3])[::-1]

    @staticmethod
    def deserialize(v: bytearray, version: int) -> float:
        return struct.unpack('<I', b'\x00' + v[::-1])[0]


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
    VIEW_PITCH : Final[str]= 'ViewPitch'

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
    ) -> bytearray | _b.InvalidVersionType:

        idx = ref_to_idx.get(v)
        if idx is None:
            raise ValueError(f"Unknown brick reference {v!r}.")
        return bytearray(struct.pack('<H', idx))

    @staticmethod
    def deserialize(v: str, version: int):
        return f'brick_{struct.unpack('<H', v)[0]}'



class SourceBricksMeta(_b.PropertyMeta[tuple[str, ...]]):
    """Class for custom input channel argument"""

    EMPTY: Final[tuple] = ()

    @staticmethod
    def serialize(
        v: tuple[str, ...],
        version: int,
        ref_to_idx: dict[str, int]
    ) -> bytearray | _b.InvalidVersionType:

        idx = []
        for ref in v:
            i = ref_to_idx.get(ref)
            if i is None:
                raise ValueError(f"Unknown brick reference {ref!r}.")
            idx.append(i)
        return bytearray(struct.pack(f'<H{len(idx)}H', len(idx), *idx))

    @staticmethod
    def deserialize(v: bytearray, version: int) -> tuple[str, ...] | _b.InvalidVersionType:
        count = struct.unpack_from('<H', v)[0]
        idx = struct.unpack_from(f'<{count}H', v, offset=2)
        return tuple(f'brick_{i}' for i in idx)


class ValueMeta(Float32Meta):
    """Class for constant value channel argument"""

    DEFAULT_VALUE: Final[float] = 1.0
