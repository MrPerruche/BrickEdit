from brickedit import *

from typing import Final
import os

CREATION_NAME: Final[str] = "TestCreation"
WRITE_PATH: Final[str] = os.path.join(BRICKRIGS_SAVEDREMASTERED, CREATION_NAME)
PYRAMID_SIZE: Final[int] = 11
STEP_SIZE: Final[float] = 0.6

v: VehicleHelper = vh.ValueHelper(FILE_MAIN_VERSION, default_unit=units.METER)
brv = BRVFile()
brm = BRMFile(name='Test creation')

for i in range(0, PYRAMID_SIZE):
    width = STEP_SIZE * (PYRAMID_SIZE - i) # Meters
    pos_z = STEP_SIZE * (i + 0.5)
    brv.add(Brick(bt.SCALABLE_BRICK, pos=v.pos(0, 0, pos_z), ppatch = {  # v.pos returns Vec3
        p.BRICK_COLOR: v.rgba_color(RGBA(0xff3f00ff)),  # Maybe? Haven't figured out details for colors
        p.BRICK_SIZE: v.brick_size(width, width, STEP_SIZE)  # v.brick_size returns Vec3
  }))

brv.write(WRITE_PATH)