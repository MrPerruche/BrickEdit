# pylint: disable=invalid-name
from typing import Final
import struct as _s

from . import base as _b
from . import meta as _m
from .. import var as _v


BRICK_COLOR: Final[str] = 'BrickColor'

@_b.register(BRICK_COLOR)
class BrickColor(_b.PropertyMeta[int]):
    """Brick's color"""

    DEFAULT_COLOR: Final[int] = 0xbcbcbcff

    @staticmethod
    def serialize(
        v: int,
        version: int,
        ref_to_idx: dict[str, int]
    ) -> bytearray | _b.InvalidVersionType:

        if version <= _v.FILE_LEGACY_VERSION:
            return _b.InvalidVersion
        return _s.pack('<I', v)

    @staticmethod
    def deserialize(v: bytearray, version: int) -> int:
        if version <= _v.FILE_LEGACY_VERSION:
            return _b.InvalidVersion
        return _s.unpack('<I', v)[0]


BRICK_MATERIAL = 'BrickMaterial'

@_b.register(BRICK_MATERIAL)
class BrickMaterial(_m.EnumMeta):
    """Brick's material"""

    ALUMINIUM: Final[str] = 'Aluminium'
    BRUSHED_ALUMINIUM: Final[str] = 'BrushedAlu'
    CARBON: Final[str] = 'Carbon'

    RIBBED_ALUMINIUM: Final[str] = 'ChannelledAlu'
    CHROME: Final[str] = 'Chrome'
    FROSTED_GLASS: Final[str] = 'CloudyGlass'

    COPPER: Final[str] = 'Copper'
    FOAM: Final[str] = 'Foam'
    GLASS: Final[str] = 'Glass'

    GLOW: Final[str] = 'Glow'
    GOLD: Final[str] = 'Gold'
    LED_MATRIX: Final[str] = 'LEDMatrix'

    OAK: Final[str] = 'Oak'
    PINE: Final[str] = 'Pine'
    PLASTIC: Final[str] = 'Plastic'

    WEATHERED_WOOD: Final[str] = 'RoughWood'
    RUBBER: Final[str] = 'Rubber'
    RUSTED_STEEL: Final[str] = 'RustedSteel'

    STEEL: Final[str] = 'Steel'
    TUNGSTEN: Final[str] = 'Tungsten'


BRICK_PATTERN: Final[str] = 'BrickPattern'

@_b.register(BRICK_PATTERN)
class BrickPattern(_m.EnumMeta):
    """Brick's pattern"""

    NONE: Final[str] = 'None'
    C_ARMY: Final[str] = 'C_Army'
    C_ARMY_DIGITAL: Final[str] = 'C_Army_Digital'

    C_AUTUMN: Final[str] = 'C_Autumn'
    C_BERLIN_2: Final[str] = 'C_Berlin_2'
    C_BERLIN: Final[str] = 'C_Berlin'

    C_BERLIN_DIGITAL: Final[str] = 'C_Berlin_Digitial'
    C_CRISTAL_CONTRAST: Final[str] = 'C_Cristal_Contrast'
    C_CRISTAL_RED: Final[str] = 'C_Cristal_Red'

    C_DARK: Final[str] = 'C_Dark'
    C_DESERT_2: Final[str] = 'C_Desert_2'
    C_DESERT: Final[str] = 'C_Desert'

    C_DESERT_DIGITAL: Final[str] = 'C_Desert_Digital'
    C_FLECKTARN: Final[str] = 'C_Flecktarn'
    C_HEAT: Final[str] = 'C_Heat'

    C_NAVY: Final[str] = 'C_Navy'
    C_SHARP : Final[str]= 'C_Sharp'
    C_SKY: Final[str] = 'C_Sky'

    C_SWEDEN: Final[str] = 'C_Sweden'
    C_SWIRL: Final[str] = 'C_Swirl'
    C_TIGER: Final[str] = 'C_Tiger'

    C_URBAN: Final[str] = 'C_Urban'
    C_YELLOW: Final[str] = 'C_Yellow'
    P_BURNT: Final[str] = 'P_Burnt'

    P_FIRE: Final[str] = 'P_Fire'
    P_HEXAGON: Final[str] = 'P_Hexagon'
    P_SWIRL_ARABICA: Final[str] = 'P_SwirlArabica'

    P_WARNING: Final[str] = 'P_Warning'
    P_WARNING_RED: Final[str] = 'P_Warning_Red'
    P_YELLOW_CIRCLES: Final[str] = 'P_YellowCircles'


ACTUATOR_MODE: Final[str] = 'ActuatorMode'

@_b.register(ACTUATOR_MODE)
class ActuatorMode(_m.EnumMeta):
    """Actuator mode for actuators"""

    ACCUMULATED: Final[str] = 'Accumulated'
    SEEKING: Final[str] = 'Seeking'
    PHYSICS_DRIVEN: Final[str] = 'PhysicsDriven'
    CYCLE: Final[str] = 'Cycle'
    STATIC: Final[str] = 'Static'
    SPRING: Final[str] = 'Spring'


B_CAN_DISABLE_STEERING: Final[str] = 'bCanDisableSteering'

@_b.register(B_CAN_DISABLE_STEERING)
class BCanDisableSteering(_m.Boolean):
    """Axle can disable steering property"""



B_CAN_INVERT_STEERING: Final[str] = 'bCanInvertSteering'

@_b.register(B_CAN_INVERT_STEERING)
class BCanInvertSteering(_m.Boolean):
    """Axle can invert steering property"""



B_DRIVEN: Final[str] = 'bDriven'

@_b.register(B_DRIVEN)
class BDriven(_m.Boolean):
    """Axle is driven property"""


B_HAS_BRAKE: Final[str] = 'bHasBrake'

@_b.register(B_HAS_BRAKE)
class BHasBrake(_m.Boolean):
    """Axle has brake property"""


B_HAS_HANDBRAKE: Final[str] = 'bHasHandBrake'

@_b.register(B_HAS_HANDBRAKE)
class BHasHandbrake(_m.Boolean):
    """Axle has handbrake property"""


B_INVERT_DRIVE: Final[str] = 'bInvertDrive'

@_b.register(B_INVERT_DRIVE)
class BInvertDrive(_m.Boolean):
    """Invert axle direction property"""


BRAKE_INPUT_CNL_INPUT_AXIS: Final[str] = 'BrakeInputChannel.InputAxis'
BRAKE_INPUT_CNL_SOURCE_BRICKS: Final[str] = 'BrakeInputChannel.SourceBricks'
BRAKE_INPUT_CNL_VALUE: Final[str] = 'BrakeInputChannel.Value'

@_b.register(BRAKE_INPUT_CNL_INPUT_AXIS)
class BrakeInputCnl_InputAxis(_m.InputAxis):
    """Input type for BrakeInputChannel"""

@_b.register(BRAKE_INPUT_CNL_SOURCE_BRICKS)
class BrakeInputCnl_SourceBricks(_m.SourceBricks):
    """Source bricks for BrakeInputChannel"""

@_b.register(BRAKE_INPUT_CNL_VALUE)
class BrakeInputCnl_Value(_m.Value):
    """Constant value for BrakeInputChannel"""


BRAKE_STRENGTH: Final[str] = 'BrakeStrength'

@_b.register(BRAKE_STRENGTH)
class BrakeStrength(_m.Value):
    """Brake strength scale property."""
    BASE: Final[float] = 1.0


B_TANK_DRIVE: Final[str] = 'bTankDrive'

@_b.register(B_TANK_DRIVE)
class BTankDrive(_m.Boolean):
    """Tank drive style property"""


GEAR_RATIO: Final[str] = 'GearRatioScale'

@_b.register(B_TANK_DRIVE)
class GearRatio(_m.Value):
    """Gear Ratio Scale property"""
    BASE: Final[float] = 1.0


INPUT_CNL_INPUT_AXIS: Final[str] = 'InputChannel.InputAxis'
INPUT_CNL_SOURCE_BRICKS: Final[str] = 'InputChannel.SourceBricks'
INPUT_CNL_VALUE: Final[str] = 'InputChannel.Value'

@_b.register(INPUT_CNL_INPUT_AXIS)
class InputCnl_InputAxis(_m.InputAxis):
    """Input type for InputChannel"""

@_b.register(INPUT_CNL_SOURCE_BRICKS)
class InputCnl_SourceBricks(_m.SourceBricks):
    """Source bricks for InputChannel"""

@_b.register(INPUT_CNL_VALUE)
class InputCnl_Value(_m.Value):
    """Constant value for InputChannel"""


MIN_LIMIT: Final[str] = 'MinLimit'

@_b.register(MIN_LIMIT)
class MinLimit(_m.Float32):
    """Minimum limit of an actuator's angle or distance in degrees or centimeters"""


MAX_LIMIT: Final[str] = 'MaxLimit'

@_b.register(MAX_LIMIT)
class MaxLimit(_m.Float32):
    """Maximum limit of an actuator's angle or distance in degrees or centimeters"""


STEERING_INPUT_CNL_INPUT_AXIS: Final[str] = 'SteeringInputChannel.InputAxis'
STEERING_INPUT_CNL_SOURCE_BRICKS: Final[str] = 'SteeringInputChannel.SourceBricks'
STEERING_INPUT_CNL_VALUE: Final[str] = 'SteeringInputChannel.Value'

@_b.register(STEERING_INPUT_CNL_INPUT_AXIS)
class SteeringInputCnl_InputAxis(_m.InputAxis):
    """Input type for SteeringInputChannel"""

@_b.register(STEERING_INPUT_CNL_SOURCE_BRICKS)
class SteeringInputCnl_SourceBricks(_m.SourceBricks):
    """Source bricks for SteeringInputChannel"""

@_b.register(STEERING_INPUT_CNL_VALUE)
class SteeringInputCnl_Value(_m.Value):
    """Constant value for SteeringInputChannel"""



SUSPENSION_LENGTH: Final[str] = 'SuspensionLength'

@_b.register(SUSPENSION_LENGTH)
class SuspensionLength(_m.Float32):
    """Suspension length property"""


SUSPENSION_STIFFNESS: Final[str] = 'SuspensionStiffness'

@_b.register(SUSPENSION_STIFFNESS)
class SuspensionStiffness(_m.Float32):
    """Suspension stiffness property"""


SUSPENSION_DAMPING: Final[str] = 'SuspensionDamping'

@_b.register(SUSPENSION_DAMPING)
class SuspensionDamping(_m.Float32):
    """Suspension daming property"""


THROTTLE_INPUT_CNL_INPUT_AXIS: Final[str] = 'ThrottleInputChannel.InputAxis'
THROTTLE_INPUT_CNL_SOURCE_BRICKS: Final[str] = 'ThrottleInputChannel.SourceBricks'
THROTTLE_INPUT_CNL_VALUE: Final[str] = 'ThrottleInputChannel.Value'

@_b.register(THROTTLE_INPUT_CNL_INPUT_AXIS)
class ThrottleInputCnl_InputAxis(_m.InputAxis):
    """Input type for ThrottleInputChannel"""

@_b.register(THROTTLE_INPUT_CNL_SOURCE_BRICKS)
class ThrottleInputCnl_SourceBricks(_m.SourceBricks):
    """Source bricks for ThrottleInputChannel"""

@_b.register(THROTTLE_INPUT_CNL_VALUE)
class ThrottleInputCnl_Value(_m.Value):
    """Constant value for ThrottleInputChannel"""
