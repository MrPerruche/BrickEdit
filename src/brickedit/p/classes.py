from typing import Final

from .base import *
from .. import serialization as s

BRICK_MATERIAL: Final[str] = 'BrickMaterial'

# Test class. Not a proper implementation.
@register(BRICK_MATERIAL)
class BrickMaterial(PropertyMeta):

    PLASTIC: Final[str] = 'Plastic'

    @staticmethod
    def serialize(v: str, version: int) -> bytearray | InvalidVersionType:
        if version > 6:
            return InvalidVersion
        return s.EnumValue.serialize(v)

    @staticmethod
    def deserialize(v: bytearray, version: int) -> str | InvalidVersionType:
        if version > 6:
            return InvalidVersion
        return s.EnumValue.deserialize(v)

