# pylint: disable=invalid-name
from typing import Final
import struct

from . import base as _b
from . import meta as _m
from .. import var as _v
from .. import vec as _vec


_STRUCT_INT8 = struct.Struct('b')
_STRUCT_UINT16 = struct.Struct('<H')
_STRUCT_UINT32 = struct.Struct('<I')
_STRUCT_3SPFLOAT = struct.Struct('<3f')


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
        return bytearray(_STRUCT_UINT32.pack(v))[::-1]

    @staticmethod
    def deserialize(v: bytearray, version: int) -> int:
        if version <= _v.FILE_LEGACY_VERSION:
            return _b.InvalidVersion
        return _STRUCT_UINT32.unpack(v)[0]


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


BRICK_SIZE: Final[str] = 'BrickSize'
@_b.register(BRICK_SIZE)
class BrickSize(_b.PropertyMeta[_vec.Vec3]):
    """Size of bricks"""

    @staticmethod
    def serialize(
        v: _vec.Vec3,
        version: int,
        ref_to_idx: dict[str, int]
    ) -> bytearray:
        return bytearray(_STRUCT_3SPFLOAT.pack(*v.as_tuple()))

    @staticmethod
    def deserialize(v: bytearray, version: int) -> _vec.Vec3:
        return _vec.Vec3(*_STRUCT_3SPFLOAT.unpack_from(v))



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


AMMO_TYPE: Final[str] = 'AmmoType'

@_b.register(AMMO_TYPE)
class AmmoType(_m.EnumMeta):
    """Ammo type of a gun brick"""
    DEFAULT: Final[str] = 'Default'
    INCENDIARY: Final[str] = 'Incendiary'
    HIGH_EXPLOSIVE: Final[str] = 'HighExplosive'
    TARGET_SEEKING: Final[str] = 'TargetSeeking'
    GUIDED: Final[str] = 'Guided'
    FLARE: Final[str] = 'Flare'
    MAX: Final[str] = 'Max'


B_ACCUMULATE_INPUT: Final[str] = 'bAccumulateInput'

@_b.register(B_ACCUMULATE_INPUT)
class BAccumulateInput(_m.Boolean):
    """Flap input is accumulated property"""


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


B_FLUID_DYNAMIC: Final[str] = 'bGenerateLift'

@_b.register(B_DRIVEN)
class BFluidDynamic(_m.Boolean):
    """Brick fluid dynamics (generate lift / aero) property"""


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
class BrakeInputCnl_InputAxis(_m.InputAxisMeta):
    """Input type for BrakeInputChannel"""

@_b.register(BRAKE_INPUT_CNL_SOURCE_BRICKS)
class BrakeInputCnl_SourceBricks(_m.SourceBricksMeta):
    """Source bricks for BrakeInputChannel"""

@_b.register(BRAKE_INPUT_CNL_VALUE)
class BrakeInputCnl_Value(_m.ValueMeta):
    """Constant value for BrakeInputChannel"""


BRAKE_STRENGTH: Final[str] = 'BrakeStrength'

@_b.register(BRAKE_STRENGTH)
class BrakeStrength(_m.ValueMeta):
    """Brake strength scale property."""
    BASE: Final[float] = 1.0


B_INVERT_TANK_STEERING: Final[str] = 'bInvertTankSteering'

@_b.register(B_INVERT_TANK_STEERING)
class BInvertTankSteering(_m.Boolean):
    """Invert tank steering on wheels property"""


B_TANK_DRIVE: Final[str] = 'bTankDrive'

@_b.register(B_TANK_DRIVE)
class BTankDrive(_m.Boolean):
    """Tank drive style property"""


CAMERA_NAME: Final[str] = 'CameraName'

@_b.register(CAMERA_NAME)
class CameraName(_m.TextMeta):
    """Name attributed to the camera"""
    EMPTY: Final[str] = ''


CONNECTOR_SPACING: Final[str] = 'ConnectorSpacing'

@_b.register(CONNECTOR_SPACING)
class ConnectorSpacing(_b.PropertyMeta[int]):

    # Format: zp_zn_yp_yn_xp_xn big endian / yp_yn_xp_xn_00_00_zp_zn little endian
    NO_CONNECTIONS: Final[int] = 0b00_00_00_00_00_00
    ALL_CONNECTIONS: Final[int] = 0b11_11_11_11_11_11
    NO_TOP: Final[int] = 0b00_11_11_11_11_11

    @staticmethod
    def serialize(
        v: int,
        version: int,
        ref_to_idx: dict[str, int]
    ) -> bytearray:
        return bytearray(_STRUCT_UINT16.pack(v))

    @staticmethod
    def deserialize(v: bytearray, version: int) -> int:
        return _STRUCT_UINT16.unpack(v)[0]

    @staticmethod
    def create(xp: int, yp: int, zp: int, xn: int, yn: int, zn: int) -> int:
        """Builds the integer corresponding to this connector spacing.
        p → postive, n → negative. Requirement: 0 <= arg <= 3"""
        return xn + xp << 2 + yn << 4 + yp << 6 + zn << 8 + zp << 10


COUPLING_MODE: Final[str] = 'CouplingMode'

@_b.register(COUPLING_MODE)
class CouplingMode(_m.EnumMeta):
    """Coupling mode of a male coupler brick"""
    DEFAULT: Final[str] = 'Default'
    STATIC: Final[str] = 'Static'


DISPLAY_COLOR: Final[str] = 'DisplayColor'

@_b.register(DISPLAY_COLOR)
class DisplayColor(_m.UInteger24):
    """Digit display color for display bricks"""


EXHAUST_EFFECT: Final[str] = 'ExhaustEffect'

@_b.register(EXHAUST_EFFECT)
class ExhaustEffect(_m.EnumMeta):
    """Exhaust brick effect type"""
    SMOKE: Final[str] = 'Smoke'
    TRAIL: Final[str] = 'Trail'


GEAR_RATIO: Final[str] = 'GearRatioScale'

@_b.register(B_TANK_DRIVE)
class GearRatio(_m.Float32Meta):
    """Gear Ratio Scale property"""
    BASE: Final[float] = 1.0


HORN_PITCH: Final[str] = 'HornPitch'

@_b.register(HORN_PITCH)
class HornPitch(_m.Float32Meta):
    """Horn pitch"""
    DEFAULT_VALUE: Final[float] = 1.0


IMAGE: Final[str] = 'Image'

@_b.register(IMAGE)
class Image(_m.EnumMeta):
    """Image displayed on image bricks"""
    ARROW: Final[str] = 'Arrow'
    BIOHAZARD: Final[str] = 'Biohazard'
    BRAF: Final[str] = 'BRAF'

    BRICK_RIGS: Final[str] = 'BrickRigs'
    BRICK_RIGS_ARMS: Final[str] = 'BrickRigsArms'
    CAUTION: Final[str] = 'Caution'

    CRIMINALS: Final[str] = 'Criminals'
    CROSSHAIR: Final[str] = 'Crosshair'
    DESERT_WORMS: Final[str] = 'DesertWorms'

    DUMMY: Final[str] = 'Dummy'
    ELECTRICAL_HAZARD: Final[str] = 'ElectricalHazard'
    EXPLOSIVE: Final[str] = 'Explosive'

    FIRE_DEPT: Final[str] = 'FireDept'
    FIRE_HAZARD: Final[str] = 'FireHazard'
    GAUGE: Final[str] = 'Gauge'

    LIMIT_80: Final[str] = 'Limit80'
    NO_ENTRANCE: Final[str] = 'NoEntrance'
    ONE_WAY: Final[str] = 'OneWay'

    PHONE: Final[str] = 'Phone'
    POLICE: Final[str] = 'Police'
    RADIOACTIVE: Final[str] = 'Radioactive'

    STAR: Final[str] = 'Star'
    STOP: Final[str] = 'Stop'
    TANK: Final[str] = 'Tank'

    VIRUS: Final[str] = 'Virus'


IMAGE_COLOR: Final[str] = 'ImageColor'

@_b.register(IMAGE_COLOR)
class ImageColor(_m.UInteger24):
    """Color of the image of an image brick"""
    DEFAULT_COLOR: Final[str] = 0xffffff


INPUT_CNL_INPUT_AXIS: Final[str] = 'InputChannel.InputAxis'
INPUT_CNL_SOURCE_BRICKS: Final[str] = 'InputChannel.SourceBricks'
INPUT_CNL_VALUE: Final[str] = 'InputChannel.Value'

# Math bricks...
INPUT_CNL_A_INPUT_AXIS: Final[str] = 'InputChannelA.InputAxis'
INPUT_CNL_A_SOURCE_BRICKS: Final[str] = 'InputChannelA.SourceBricks'
INPUT_CNL_A_VALUE: Final[str] = 'InputChannelA.Value'

INPUT_CNL_B_INPUT_AXIS: Final[str] = 'InputChannelB.InputAxis'
INPUT_CNL_B_SOURCE_BRICKS: Final[str] = 'InputChannelB.SourceBricks'
INPUT_CNL_B_VALUE: Final[str] = 'InputChannelB.Value'

@_b.register(INPUT_CNL_INPUT_AXIS)
class InputCnl_InputAxis(_m.InputAxisMeta):
    """Input type for InputChannel"""

@_b.register(INPUT_CNL_SOURCE_BRICKS)
class InputCnl_SourceBricks(_m.SourceBricksMeta):
    """Source bricks for InputChannel"""

@_b.register(INPUT_CNL_VALUE)
class InputCnl_Value(_m.ValueMeta):
    """Constant value for InputChannel"""




# why
@_b.register(INPUT_CNL_A_INPUT_AXIS)
class InputCnl_A_InputAxis(_m.InputAxisMeta):
    """Input type for InputChannelA"""

@_b.register(INPUT_CNL_A_SOURCE_BRICKS)
class InputCnl_A_SourceBricks(_m.SourceBricksMeta):
    """Source bricks for InputChannelA"""

@_b.register(INPUT_CNL_A_VALUE)
class InputCnl_A_Value(_m.ValueMeta):
    """Constant value for InputChannelA"""


@_b.register(INPUT_CNL_B_INPUT_AXIS)
class InputCnl_B_InputAxis(_m.InputAxisMeta):
    """Input type for InputChannelB"""

@_b.register(INPUT_CNL_B_SOURCE_BRICKS)
class InputCnl_B_SourceBricks(_m.SourceBricksMeta):
    """Source bricks for InputChannelB"""

@_b.register(INPUT_CNL_B_VALUE)
class InputCnl_B_Value(_m.ValueMeta):
    """Constant value for InputChannelB"""




INPUT_SCALE: Final[str] = 'InputScale'

@_b.register(INPUT_SCALE)
class InputScale(_m.Float32Meta):
    """Input scale property"""
    BASE: Final[float] = 1


MIN_LIMIT: Final[str] = 'MinLimit'

@_b.register(MIN_LIMIT)
class MinLimit(_m.Float32Meta):
    """Minimum limit of an actuator's angle or distance in degrees or centimeters"""


MIN_ANGLE: Final[str] = 'MinAngle'

@_b.register(MIN_ANGLE)
class MinAngle(_m.Float32Meta):
    """Minimum angle of a flap"""


MAX_LIMIT: Final[str] = 'MaxLimit'

@_b.register(MAX_LIMIT)
class MaxLimit(_m.Float32Meta):
    """Maximum limit of an actuator's angle or distance in degrees or centimeters"""


MAX_ANGLE: Final[str] = 'MaxAngle'

@_b.register(MAX_ANGLE)
class MaxAngle(_m.Float32Meta):
    """Maximum angle of a flap"""


NUM_FRACTIONAL_DIGITS: Final[str] = 'NumFractionalDigits'

@_b.register(NUM_FRACTIONAL_DIGITS)
class NumFractionalDigits(_b.PropertyMeta[int]):
    """Number of fractional digits displayed on the display"""

    @staticmethod
    def serialize(
        v: int,
        version: int,
        ref_to_idx: dict[str, int]
    ) -> bytearray:
        return bytearray(_STRUCT_INT8.pack(v))

    @staticmethod
    def deserialize(v: bytearray, version: int) -> int:
        return _STRUCT_INT8.unpack(v)[0]


OWNING_SEAT: Final[str] = 'OwningSeat'

@_b.register(OWNING_SEAT)
class OwningSeat(_m.SingleSourceBrickMeta):
    """Seat owning the brick (camera, ...)"""


SIREN_TYPE: Final[str] = 'SirenType'

@_b.register(SIREN_TYPE)
class SirenType(_m.EnumMeta):
    """Siren sound property"""
    CAR_HORN: Final[str] = 'CarHorn'
    EMS_US: Final[str] = 'EmsUS'
    FIRE_DEPT_GERMAN: Final[str] = 'FireDeptGerman'
    POLICE_GERMAN: Final[str] = 'PoliceGerman'
    TRUCK_HORN: Final[str] = 'TruckHorn'


SIZE_SCALE: Final[str] = 'SizeScale'

@_b.register(SIZE_SCALE)
class SizeScale(_m.Float32Meta):
    """Exhaust brick particle size scale"""


SPAWN_SCALE: Final[str] = 'SpawnScale'

@_b.register(SPAWN_SCALE)
class SpawnScale(_m.Float32Meta):
    """Exhaust brick particle spawn scale"""


SMOKE_COLOR: Final[str] = 'SmokeColor'

@_b.register(SMOKE_COLOR)
class SmokeColor(_m.UInteger24):
    """Exhaust effect color"""


STEERING_INPUT_CNL_INPUT_AXIS: Final[str] = 'SteeringInputChannel.InputAxis'
STEERING_INPUT_CNL_SOURCE_BRICKS: Final[str] = 'SteeringInputChannel.SourceBricks'
STEERING_INPUT_CNL_VALUE: Final[str] = 'SteeringInputChannel.Value'

@_b.register(STEERING_INPUT_CNL_INPUT_AXIS)
class SteeringInputCnl_InputAxis(_m.InputAxisMeta):
    """Input type for SteeringInputChannel"""

@_b.register(STEERING_INPUT_CNL_SOURCE_BRICKS)
class SteeringInputCnl_SourceBricks(_m.SourceBricksMeta):
    """Source bricks for SteeringInputChannel"""

@_b.register(STEERING_INPUT_CNL_VALUE)
class SteeringInputCnl_Value(_m.ValueMeta):
    """Constant value for SteeringInputChannel"""


SUSPENSION_LENGTH: Final[str] = 'SuspensionLength'

@_b.register(SUSPENSION_LENGTH)
class SuspensionLength(_m.Float32Meta):
    """Suspension length property"""


SUSPENSION_STIFFNESS: Final[str] = 'SuspensionStiffness'

@_b.register(SUSPENSION_STIFFNESS)
class SuspensionStiffness(_m.Float32Meta):
    """Suspension stiffness property"""


SUSPENSION_DAMPING: Final[str] = 'SuspensionDamping'

@_b.register(SUSPENSION_DAMPING)
class SuspensionDamping(_m.Float32Meta):
    """Suspension daming property"""


TIRE_PRESSURE: Final[str] = 'TirePressureRatio'

@_b.register(TIRE_PRESSURE)
class TirePressure(_m.Float32Meta):
    """Tire pressure ratio"""
    DEFAULT_VALUE: Final[float] = 0.8


TIRE_WIDTH: Final[str] = 'TireThickness'

@_b.register(TIRE_WIDTH)
class TireWidth(_m.Float32Meta):
    """Width (thickness) of the tire for wheels"""


THROTTLE_INPUT_CNL_INPUT_AXIS: Final[str] = 'ThrottleInputChannel.InputAxis'
THROTTLE_INPUT_CNL_SOURCE_BRICKS: Final[str] = 'ThrottleInputChannel.SourceBricks'
THROTTLE_INPUT_CNL_VALUE: Final[str] = 'ThrottleInputChannel.Value'

@_b.register(THROTTLE_INPUT_CNL_INPUT_AXIS)
class ThrottleInputCnl_InputAxis(_m.InputAxisMeta):
    """Input type for ThrottleInputChannel"""

@_b.register(THROTTLE_INPUT_CNL_SOURCE_BRICKS)
class ThrottleInputCnl_SourceBricks(_m.SourceBricksMeta):
    """Source bricks for ThrottleInputChannel"""

@_b.register(THROTTLE_INPUT_CNL_VALUE)
class ThrottleInputCnl_Value(_m.ValueMeta):
    """Constant value for ThrottleInputChannel"""


WHEEL_DIAMETER: Final[str] = 'WheelDiameter'

@_b.register(WHEEL_DIAMETER)
class WheelDiameter(_m.Float32Meta):
    """Diameter of the wheel in centimeters"""


WHEEL_WIDTH: Final[str] = 'WheelWidth'

@_b.register(WHEEL_WIDTH)
class WheelWidth(_m.Float32Meta):
    """Width of the wheel in centimeters"""

SWITCH_NAME: Final[str] = 'SwitchName'
@_b.register(SWITCH_NAME)
class SwitchName(_m.TextMeta):
    """Name attributed to the switch"""
    EMPTY: Final[str] = ''

B_RETURN_TO_ZERO = 'bReturnToZero'
@_b.register(B_RETURN_TO_ZERO)
class BReturnToZero(_m.Boolean):
    """Return to zero property"""

OUTPUT_CNL_MIN_IN = 'OutputChannel.MinIn'
OUTPUT_CNL_MAX_IN = 'OutputChannel.MaxIn'
OUTPUT_CNL_MIN_OUT = 'OutputChannel.MinOut'
OUTPUT_CNL_MAX_OUT = 'OutputChannel.MaxOut'

@_b.register(OUTPUT_CNL_MIN_IN)
class OutputCnl_MinIn(_m.Float32Meta):
    """Minimum input value for OutputChannel"""

@_b.register(OUTPUT_CNL_MAX_IN)
class OutputCnl_MaxIn(_m.Float32Meta):
    """Maximum input value for OutputChannel"""

@_b.register(OUTPUT_CNL_MIN_OUT)
class OutputCnl_MinOut(_m.Float32Meta):
    """Minimum output value for OutputChannel"""

@_b.register(OUTPUT_CNL_MAX_OUT)
class OutputCnl_MaxOut(_m.Float32Meta):
    """Maximum output value for OutputChannel"""

OPERATION = "Operation"

@_b.register(OPERATION)
class Operation(_m.EnumMeta):
    """Math brick operation property"""
    ADD = 'Add'
    SUBTRACT = 'Subtract'
    MULTIPLY = 'Multiply'
    DIVIDE = 'Divide'
    MODULO = 'Fmod'
    POWER = 'Power'
    GREATER = 'Greater'
    LESS = 'Less'
    MIN = 'Min'
    MAX = 'Max'
    ABS = 'Abs'
    SIGN = 'Sign'
    ROUND = 'Round'
    CEIL = 'Ceil'
    FLOOR = 'Floor'
    SQUARE_ROOT = 'Sqrt'

    SIN_DEG = 'SinDeg'
    SIN_RAD = 'Sin'
    ASIN_DEG = 'AsinDeg'
    ASIN_RAD = 'Asin'
    COS_DEG = 'CosDeg'
    COS_RAD = 'Cos'
    ACOS_DEG = 'AcosDeg'
    ACOS_RAD = 'Acos'
    TAN_DEG = 'TanDeg'
    TAN_RAD = 'Tan'
    ATAN_DEG = 'AtanDeg'
    ATAN_RAD = 'Atan'


    SUB = SUBTRACT
    MUL = MULTIPLY
    DIV = DIVIDE
    MOD = MODULO
    POW = POWER
    EXPONENT = POWER
    GT = GREATER
    LT = LESS
    MINIMUM = MIN
    MAXIMUM = MAX
    ABSOLUTE = ABS
    CEILING = CEIL
    SQRT = SQUARE_ROOT
