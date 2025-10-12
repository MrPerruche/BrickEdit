from .base import *
from .. import serialization as s

from typing import Final

BRICK_MATERIAL: Final[str] = 'BrickMaterial'

@register(BRICK_MATERIAL)
class BrickMaterial(PropertyMeta):
    
    PLASTIC: Final[str] = 'Plastic'
    
    @staticmethod
    def serialize(v: str, version: int) -> bytearray:
        if version > 6: return NotImplemented
        return s.String.serialize(v)
    
    @staticmethod
    def deserialize(v: bytearray, version: int) -> str:
        return s.String.deserialize(v)