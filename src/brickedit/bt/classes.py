from .. import p
from brci.vec import Vec3, Vec4
from base import *

from typing import Final



class ScalableBrickMeta(BrickMeta):
    
    def base_properties(self) -> dict[str, object]:
        return {
            p.BRICK_MATERIAL: p.BrickMaterial.PLASTIC
        }
        
SCALABLE_BRICK = ScalableBrickMeta('ScalableBrick')