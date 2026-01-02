# pylint: disable=invalid-name
# pylint: disable=too-many-lines
from typing import Final
import struct

from . import base as _b
from . import meta as _m
from .. import var as _v
from .. import vec as _vec


_STRUCT_INT8 = struct.Struct('b')
_STRUCT_UINT16 = struct.Struct('<H')
_STRUCT_UINT32 = struct.Struct('<I')
_STRUCT_UINT32_BIGENDIAN = struct.Struct('>I')
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
    ) -> bytes | _b.InvalidVersionType:

        if version <= _v.FILE_LEGACY_VERSION:
            return _b.InvalidVersion
        return _STRUCT_UINT32_BIGENDIAN.pack(v)  # Technically it's little-endian but brickedit
                                                 # represent colors the other way around so...

    @staticmethod
    def deserialize(v: bytes, version: int) -> int:
        if version <= _v.FILE_LEGACY_VERSION:
            return _b.InvalidVersion
        return _STRUCT_UINT32_BIGENDIAN.unpack(v)[0]


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
    ) -> bytes:
        return _STRUCT_3SPFLOAT.pack(*v.as_tuple())

    @staticmethod
    def deserialize(v: bytes, version: int) -> _vec.Vec3:
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


AUTO_HOVER_INPUT_CNL_INPUT_AXIS: Final[str] = 'AutoHoverInputChannel.InputAxis'
AUTO_HOVER_INPUT_CNL_SOURCE_BRICKS: Final[str] = 'AutoHoverInputChannel.SourceBricks'
AUTO_HOVER_INPUT_CNL_VALUE: Final[str] = 'AutoHoverInputChannel.Value'

@_b.register(AUTO_HOVER_INPUT_CNL_INPUT_AXIS)
class AutoHoverInputCnl_InputAxis(_m.InputAxisMeta):
    """Input type for AutoHoverInputChannel"""

@_b.register(AUTO_HOVER_INPUT_CNL_SOURCE_BRICKS)
class AutoHoverInputCnl_SourceBricks(_m.SourceBricksMeta):
    """Source type for AutoHoverInputChannel"""

@_b.register(AUTO_HOVER_INPUT_CNL_VALUE)
class AutoHoverInputCnl_Value(_m.ValueMeta):
    """Value type for AutoHoverInputChannel"""


B_ACCUMULATED: Final[str] = 'bAccumulated'

@_b.register(B_ACCUMULATED)
class BAccumulated(_m.BooleanMeta):
    """Thruster input accumulates"""


B_ACCUMULATE_INPUT: Final[str] = 'bAccumulateInput'

@_b.register(B_ACCUMULATE_INPUT)
class BAccumulateInput(_m.BooleanMeta):
    """Flap input is accumulated property"""


B_CAN_DISABLE_STEERING: Final[str] = 'bCanDisableSteering'

@_b.register(B_CAN_DISABLE_STEERING)
class BCanDisableSteering(_m.BooleanMeta):
    """Axle can disable steering property"""


B_CAN_INVERT_STEERING: Final[str] = 'bCanInvertSteering'

@_b.register(B_CAN_INVERT_STEERING)
class BCanInvertSteering(_m.BooleanMeta):
    """Axle can invert steering property"""


B_DRIVEN: Final[str] = 'bDriven'

@_b.register(B_DRIVEN)
class BDriven(_m.BooleanMeta):
    """Axle is driven property"""


B_FLUID_DYNAMIC: Final[str] = 'bGenerateLift'

@_b.register(B_DRIVEN)
class BFluidDynamic(_m.BooleanMeta):
    """Brick fluid dynamics (generate lift / aero) property"""


B_HAS_BRAKE: Final[str] = 'bHasBrake'

@_b.register(B_HAS_BRAKE)
class BHasBrake(_m.BooleanMeta):
    """Axle has brake property"""


B_HAS_HANDBRAKE: Final[str] = 'bHasHandBrake'

@_b.register(B_HAS_HANDBRAKE)
class BHasHandbrake(_m.BooleanMeta):
    """Axle has handbrake property"""


B_INVERT_DRIVE: Final[str] = 'bInvertDrive'

@_b.register(B_INVERT_DRIVE)
class BInvertDrive(_m.BooleanMeta):
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


BRIGHTNESS: Final[str] = 'Brightness'

@_b.register(BRIGHTNESS)
class Brightness(_m.Float32Meta):
    """Brightness of a light brick"""
    DEFAULT: Final[float] = 1.0
    PERCENT: Final[float] = 0.01


B_INVERT_TANK_STEERING: Final[str] = 'bInvertTankSteering'

@_b.register(B_INVERT_TANK_STEERING)
class BInvertTankSteering(_m.BooleanMeta):
    """Invert tank steering on wheels property"""


B_TANK_DRIVE: Final[str] = 'bTankDrive'

@_b.register(B_TANK_DRIVE)
class BTankDrive(_m.BooleanMeta):
    """Tank drive style property"""


CAMERA_NAME: Final[str] = 'CameraName'

@_b.register(CAMERA_NAME)
class CameraName(_m.TextMeta):
    """Name attributed to the camera"""
    EMPTY: Final[str] = ''


CONE_ANGLE: Final[str] = 'LightConeAngle'

@_b.register(CONE_ANGLE)
class ConeAngle(_m.Float32Meta):
    """Cone angle of a light brick"""
    DEFAULT: Final[float] = 45.0


CONNECTOR_SPACING: Final[str] = 'ConnectorSpacing'

@_b.register(CONNECTOR_SPACING)
class ConnectorSpacing(_b.PropertyMeta[int]):

    # Format: zp_zn_yp_yn_xp_xn big endian / yp_yn_xp_xn_00_00_zp_zn little endian
    NO_CONNECTIONS: Final[int] = 0b00_00_00_00_00_00
    ALL_CONNECTIONS: Final[int] = 0b11_11_11_11_11_11
    SPINNER_CONNECTIONS: Final[int]= 0b00_00_00_00_11_11
    NO_TOP: Final[int] = 0b00_11_11_11_11_11

    @staticmethod
    def serialize(
        v: int,
        version: int,
        ref_to_idx: dict[str, int]
    ) -> bytes:
        return _STRUCT_UINT16.pack(v)

    @staticmethod
    def deserialize(v: bytes, version: int) -> int:
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
class DisplayColor(_m.UInteger24Meta):
    """Digit display color for display bricks"""


EXIT_LOCATION: Final[str] = 'ExitLocation'

@_b.register(EXIT_LOCATION)
class ExitLocation(_b.PropertyMeta[_vec.Vec3]):
    """Exit location of a light brick"""

    @staticmethod
    def serialize(
        v: _vec.Vec3,
        version: int,
        ref_to_idx: dict[str, int]
    ) -> bytes:
        return _STRUCT_3SPFLOAT.pack(*v.as_tuple())

    @staticmethod
    def deserialize(v: bytes, version: int) -> _vec.Vec3:
        return _vec.Vec3(*_STRUCT_3SPFLOAT.unpack_from(v))



EXHAUST_EFFECT: Final[str] = 'ExhaustEffect'

@_b.register(EXHAUST_EFFECT)
class ExhaustEffect(_m.EnumMeta):
    """Exhaust brick effect type"""
    SMOKE: Final[str] = 'Smoke'
    TRAIL: Final[str] = 'Trail'


FLASH_SEQUENCE: Final[str] = 'FlashSequence'

@_b.register(FLASH_SEQUENCE)
class FlashSequence(_m.EnumMeta):
    """Flash pattern of a light brick"""
    STATIC: Final[str] = 'Static'
    BLINKER: Final[str] = 'Blinker_Sequence'
    BLINKER_INVERTED: Final[str] = 'Blinker_Sequence_Inverted'
    DOUBLE_FLASH_INVERTED: Final[str] = 'DoubleFlash_Inverted_Sequence'
    DOUBLE_FLASH: Final[str] = 'DoubleFlash_Sequence'
    RUNNING_LIGHT_01_INVERTED: Final[str] = 'RunningLight_01_Inverted_Sequence'
    RUNNING_LIGHT_01: Final[str] = 'RunningLight_01_Sequence'
    RUNNING_LIGHT_02_INVERTED: Final[str] = 'RunningLight_02_Inverted_Sequence'
    RUNNING_LIGHT_02: Final[str] = 'RunningLight_02_Sequence'
    RUNNING_LIGHT_03_INVERTED: Final[str] = 'RunningLight_03_Inverted_Sequence'
    RUNNING_LIGHT_03: Final[str] = 'RunningLight_03_Sequence'
    RUNNING_LIGHT_04_INVERTED: Final[str] = 'RunningLight_04_Inverted_Sequence'
    RUNNING_LIGHT_04: Final[str] = 'RunningLight_04_Sequence'
    STROBE: Final[str] = 'Strobe_Sequence'


FUEL_TYPE: Final[str] = 'FuelType'

@_b.register(FUEL_TYPE)
class FuelType(_m.EnumMeta):
    """Fuel type of a fuel brick"""
    PETROL: Final[str] = 'Petrol'
    NITRO: Final[str] = 'Nitro'
    ROCKET_FUEL: Final[str] = 'RocketFuel'
    C4: Final[str] = 'C4'


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


IDLER_WHEELS: Final[str] = 'IdlerWheels'

@_b.register(IDLER_WHEELS)
class IdlerWheels(_m.SourceBricksMeta):
    """Idler wheels connected to a sprocket (for tracks)"""


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
class ImageColor(_m.UInteger24Meta):
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

ENABLED_INPUT_CNL_INPUT_AXIS: Final[str] = 'EnabledInputChannel.InputAxis'
ENABLED_INPUT_CNL_SOURCE_BRICKS: Final[str] = 'EnabledInputChannel.SourceBricks'
ENABLED_INPUT_CNL_VALUE: Final[str] = 'EnabledInputChannel.Value'

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

@_b.register(ENABLED_INPUT_CNL_INPUT_AXIS)
class EnabledInputCnl_InputAxis(_m.InputAxisMeta):
    """Input type for EnabledInputChannel"""

@_b.register(ENABLED_INPUT_CNL_SOURCE_BRICKS)
class EnabledInputCnl_SourceBricks(_m.SourceBricksMeta):
    """Source bricks for EnabledInputChannel"""

@_b.register(ENABLED_INPUT_CNL_VALUE)
class EnabledInputCnl_Value(_m.ValueMeta):
    """Constant value for EnabledInputChannel"""


LIGHT_DIRECTION: Final[str] = 'LightDirection'

@_b.register(LIGHT_DIRECTION)
class LightDirection(_m.EnumMeta):
    """Light direction"""
    OFF: Final[str] = 'Off'
    OMNIDIRECTIONAL: Final[str] = 'Omnidirectional'
    X: Final[str] = 'X'
    X_NEG: Final[str] = 'XNeg'
    Y: Final[str] = 'Y'
    Y_NEG: Final[str] = 'YNeg'
    Z: Final[str] = 'Z'
    Z_NEG: Final[str] = 'ZNeg'


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
    ) -> bytes:
        return _STRUCT_INT8.pack(v)

    @staticmethod
    def deserialize(v: bytes, version: int) -> int:
        return _STRUCT_INT8.unpack(v)[0]


OWNING_SEAT: Final[str] = 'OwningSeat'

@_b.register(OWNING_SEAT)
class OwningSeat(_m.SingleSourceBrickMeta):
    """Seat owning the brick (camera, ...)"""


PITCH_INPUT_CNL_INPUT_AXIS: Final[str] = 'PitchInputChannel.InputAxis'
PITCH_INPUT_CNL_SOURCE_BRICKS: Final[str] = 'PitchInputChannel.SourceBricks'
PITCH_INPUT_CNL_VALUE: Final[str] = 'PitchInputChannel.Value'

@_b.register(PITCH_INPUT_CNL_INPUT_AXIS)
class PitchInputCnl_InputAxis(_m.InputAxisMeta):
    """Input type for PitchInputChannel"""

@_b.register(PITCH_INPUT_CNL_SOURCE_BRICKS)
class PitchInputCnl_SourceBricks(_m.SourceBricksMeta):
    """Source bricks for PitchInputChannel"""

@_b.register(PITCH_INPUT_CNL_VALUE)
class PitchInputCnl_Value(_m.ValueMeta):
    """Constant value for PitchInputChannel"""


POWER_INPUT_CNL_INPUT_AXIS: Final[str] = 'PowerInputChannel.InputAxis'
POWER_INPUT_CNL_SOURCE_BRICKS: Final[str] = 'PowerInputChannel.SourceBricks'
POWER_INPUT_CNL_VALUE: Final[str] = 'PowerInputChannel.Value'

@_b.register(POWER_INPUT_CNL_INPUT_AXIS)
class PowerInputCnl_InputAxis(_m.InputAxisMeta):
    """Input type for PowerInputChannel"""

@_b.register(POWER_INPUT_CNL_SOURCE_BRICKS)
class PowerInputCnl_SourceBricks(_m.SourceBricksMeta):
    """Source bricks for PowerInputChannel"""

@_b.register(POWER_INPUT_CNL_VALUE)
class PowerInputCnl_Value(_m.ValueMeta):
    """Constant value for PowerInputChannel"""


ROLL_INPUT_CNL_INPUT_AXIS: Final[str] = 'RollInputChannel.InputAxis'
ROLL_INPUT_CNL_SOURCE_BRICKS: Final[str] = 'RollInputChannel.SourceBricks'
ROLL_INPUT_CNL_VALUE: Final[str] = 'RollInputChannel.Value'

@_b.register(ROLL_INPUT_CNL_INPUT_AXIS)
class RollInputCnl_InputAxis(_m.InputAxisMeta):
    """Input type for RollInputChannel"""

@_b.register(ROLL_INPUT_CNL_SOURCE_BRICKS)
class RollInputCnl_SourceBricks(_m.SourceBricksMeta):
    """Source bricks for RollInputChannel"""

@_b.register(ROLL_INPUT_CNL_VALUE)
class RollInputCnl_Value(_m.ValueMeta):
    """Constant value for RollInputChannel"""


SEAT_NAME: Final[str] = 'SeatName'

@_b.register(SEAT_NAME)
class SeatName(_m.TextMeta):
    """Name of the seat"""


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

SPEED_FACTOR: Final[str] = 'SpeedFactor'

@_b.register(SPEED_FACTOR)
class SpeedFactor(_m.Float32Meta):
    """Actuator speed factor"""
    DEFAULT_VALUE: Final[float] = 1.0


SPINNER_ANGLE: Final[str] = 'SpinnerAngle'

@_b.register(SPINNER_ANGLE)
class SpinnerAngle(_m.Float32Meta):
    """Angle of a spinner brick"""


SPINNER_RADIUS: Final[str] = 'SpinnerRadius'

@_b.register(SPINNER_RADIUS)
class SpinnerRadius(_m.Vec2Meta):
    """Radius of a spinner brick"""


SPINNER_SHAPE: Final[str] = 'SpinnerShape'

@_b.register(SPINNER_SHAPE)
class SpinnerShape(_m.EnumMeta):
    """Shape of a spinner brick"""
    SQUARE: Final[str] = 'Square'
    TRIANGLE_IN: Final[str] = 'TriangleIn'
    TRIANGLE_OUT: Final[str] = 'TriangleOut'
    ISOSCELES_TRIANGLE_IN: Final[str] = 'IsoscelesTriangleIn'
    ISOSCELES_TRIANGLE_OUT: Final[str] = 'IsoscelesTriangleOut'
    ISOSCELES_TRIANGLE_UP: Final[str] = 'IsoscelesTriangleUp'
    CIRCLE: Final[str] = 'Circle'
    HALF_CIRCLE_IN: Final[str] = 'HalfCircleIn'
    HALF_CIRCLE_OUT: Final[str] = 'HalfCircleOut'
    HALF_CIRCLE_UP: Final[str] = 'HalfCircleUp'
    QUARTER_CIRCLE_IN: Final[str] = 'QuarterCircleIn'
    QUARTER_CIRCLE_OUT: Final[str] = 'QuarterCircleOut'
    DIAMOND: Final[str] = 'Diamond'


SPINNER_SIZE: Final[str] = 'SpinnerSize'

@_b.register(SPINNER_SIZE)
class SpinnerSize(_m.Vec2Meta):
    """Size of a spinner brick"""


SMOKE_COLOR: Final[str] = 'SmokeColor'

@_b.register(SMOKE_COLOR)
class SmokeColor(_m.UInteger24Meta):
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


TRACK_COLOR: Final[str] = 'TrackColor'

@_b.register(TRACK_COLOR)
class TrackColor(_m.UInteger32Meta):
    """Track color"""
    DEFAULT: Final[int] = 0x595959ff


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
class BReturnToZero(_m.BooleanMeta):
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
    EMPTY: Final[str] = ''
    DEFAULT: Final[str] = 'Add'

    ADD: Final[str] = 'Add'
    SUBTRACT: Final[str] = 'Subtract'
    MULTIPLY: Final[str] = 'Multiply'
    DIVIDE: Final[str] = 'Divide'
    MODULO: Final[str] = 'Fmod'
    POWER: Final[str] = 'Power'
    GREATER: Final[str] = 'Greater'
    LESS: Final[str] = 'Less'
    MIN: Final[str] = 'Min'
    MAX: Final[str] = 'Max'
    ABS: Final[str] = 'Abs'
    SIGN: Final[str] = 'Sign'
    ROUND: Final[str] = 'Round'
    CEIL: Final[str] = 'Ceil'
    FLOOR: Final[str] = 'Floor'
    SQUARE_ROOT: Final[str] = 'Sqrt'

    SIN_DEG: Final[str] = 'SinDeg'
    SIN_RAD: Final[str] = 'Sin'
    ASIN_DEG: Final[str] = 'AsinDeg'
    ASIN_RAD: Final[str] = 'Asin'
    COS_DEG: Final[str] = 'CosDeg'
    COS_RAD: Final[str] = 'Cos'
    ACOS_DEG: Final[str] = 'AcosDeg'
    ACOS_RAD: Final[str] = 'Acos'
    TAN_DEG: Final[str] = 'TanDeg'
    TAN_RAD: Final[str] = 'Tan'
    ATAN_DEG: Final[str] = 'AtanDeg'
    ATAN_RAD: Final[str] = 'Atan'

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


TEXT = 'Text'
@_b.register(TEXT)
class Text(_m.TextMeta):
    """Text property for text bricks."""
    EMPTY: Final[str] = ''
    DEFAULT: Final[str] = 'Text'


FONT = 'Font'
@_b.register(FONT)
class Font(_m.EnumMeta):
    """Font property for text bricks."""

    EMPTY: Final[str] = ''
    DEFAULT: Final[str] = 'Roboto'

    ROBOTO: Final[str] = 'Roboto'
    ROBOTO_SERIF: Final[str] = 'RobotoSerif'
    SILKSCREEN: Final[str] = 'Silkscreen'
    PERMANENT_MARKER: Final[str] = 'PermanentMarker'
    ORBITRON: Final[str] = 'Orbitron'
    BIG_SHOULDERS_STENCIL: Final[str] = 'BigShouldersStencil'
    NOTO_EMOJI: Final[str] = 'NotoEmoji'


FONT_SIZE = 'FontSize'
@_b.register(FONT_SIZE)
class FontSize(_m.Float32Meta):
    """Font size property for text bricks."""
    DEFAULT_VALUE: Final[float] = 60.0


SENSOR_TYPE = 'SensorType'
@_b.register(SENSOR_TYPE)
class SensorType(_m.EnumMeta):
    SPEED: Final[str] = 'Speed'
    NORMAL_SPEED: Final[str] = 'NormalSpeed'
    ACCELERATION: Final[str] = 'Acceleration'
    NORMAL_ACCELERATION: Final[str] = 'NormalAcceleration'
    ANGULAR_SPEED: Final[str] = 'AngularSpeed'
    NORMAL_ANGULAR_SPEED: Final[str] = 'NormalAngularSpeed'
    DISTANCE: Final[str] = 'Distance'
    TIME: Final[str] = 'Time'
    PROXIMITY: Final[str] = 'Proximity'
    DISTANCE_TO_GROUND: Final[str] = 'DistanceToGround'
    ALTITUDE: Final[str] = 'Altitude'
    ABSOLUTE_ALTITUDE: Final[str] = 'AbsAltitude'
    PITCH: Final[str] = 'Pitch'
    YAW: Final[str] = 'Yaw'
    ROLL: Final[str] = 'Roll'
    NUM_SEEKING_PROJECTILES: Final[str] = 'NumSeekingProjectiles'
    SEEKING_PROJECTILE_DISTANCE: Final[str] = 'SeekingProjectileDistance'
    DELTA_TIME: Final[str] = 'DeltaTime'
    FRAMERATE: Final[str] = 'Framerate'
    TIME_OF_DAY: Final[str] = 'TimeOfDay'
    WIND_SPEED: Final[str] = 'WindSpeed'
    WIND_DIRECTION_DEGREES: Final[str] = 'WindDirectionDeg'
    WIND_DIRECTION: Final[str] = 'WindDirection'

    # Ingame display names, and some other aliases such as _DEG instead of _DEGREES
    GROUND_DISTANCE = DISTANCE_TO_GROUND
    RELATIVE_ALTITUDE = ALTITUDE
    NUMBER_OF_TRACKING_MISSILES = NUM_SEEKING_PROJECTILES
    TRACKING_MISSILE_DISTANCE = SEEKING_PROJECTILE_DISTANCE
    WIND_DIRECTION_DEG = WIND_DIRECTION_DEGREES
    WIND_DIRECTION_RADIANS = WIND_DIRECTION
    WIND_DIRECTION_RAD = WIND_DIRECTION


TEXT_COLOR = 'TextColor'
@_b.register(TEXT_COLOR)
class TextColor(_m.UInteger24Meta):
    """Text color property for text bricks."""
    DEFAULT_COLOR: Final[int] = 0x000000

OUTLINE_THICKNESS = 'OutlineThickness'
@_b.register(OUTLINE_THICKNESS)
class OutlineThickness(_m.Float32Meta):
    """Outline thickness property for text bricks."""
    DEFAULT_VALUE: Final[float] = 0.0


WINCH_SPEED: Final[str] = 'WinchSpeed'

@_b.register(WINCH_SPEED)
class WinchSpeed(_m.Float32Meta):
    """Winch speed in centimeters per second"""
    DEFAULT_VALUE: Final[float] = 100.0


YAW_INPUT_CNL_INPUT_AXIS: Final[str] = 'YawInputChannel.InputAxis'
YAW_INPUT_CNL_SOURCE_BRICKS: Final[str] = 'YawInputChannel.SourceBricks'
YAW_INPUT_CNL_VALUE: Final[str] = 'YawInputChannel.Value'

@_b.register(YAW_INPUT_CNL_INPUT_AXIS)
class YawInputCnl_InputAxis(_m.InputAxisMeta):
    """Input type for YawInputChannel"""

@_b.register(YAW_INPUT_CNL_SOURCE_BRICKS)
class YawInputCnl_SourceBricks(_m.SourceBricksMeta):
    """Source bricks for YawInputChannel"""

@_b.register(YAW_INPUT_CNL_VALUE)
class YawInputCnl_Value(_m.ValueMeta):
    """Constant value for YawInputChannel"""
