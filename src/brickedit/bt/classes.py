from typing import Final
from collections.abc import Hashable

from .. import p as _p
from .. import vec as _v
from . import base as _b
from . import meta as _m
from . import inner_properties as _ip


_base_properties: dict[str, Hashable] = {
    _p.BRICK_COLOR: _p.BrickColor.DEFAULT_COLOR,
    _p.BRICK_PATTERN: _p.BrickPattern.NONE,
    _p.BRICK_MATERIAL: _p.BrickMaterial.PLASTIC
}



class ActuatorBrickBaseMeta(_b.BrickMeta):

    def __init__(
        self,
        name: str,
        linear_actuation_offset: float,
        linear_actuation_range: float,
        *args,
        **kwargs):
        super().__init__(name, *args, **kwargs)
        self._linear_actuation_offset = linear_actuation_offset
        self._linear_actuation_range = linear_actuation_range

    def linear_actuation_offset(self):
        """Returns the range of the actuator in centimeters"""
        return self._linear_actuation_offset

    def linear_actuation_range(self):
        """Returns the range of the actuator in centimeters"""
        return self._linear_actuation_range

    def base_properties(self, *args, **kwargs) -> dict[str, Hashable]:
        return _base_properties.copy()

ACTUATOR_1SX1SX1S_02_TOP: Final = ActuatorBrickBaseMeta('Actuator_1sx1sx1s_02_Top', 0, 0)
ACTUATOR_1SX1SX1S_MALE: Final = ActuatorBrickBaseMeta('Actuator_1sx1sx1s_Male', -10, 0)
ACTUATOR_1SX1SX1S_TOP: Final = ActuatorBrickBaseMeta('Actuator_1sx1sx1s_Top', 0, 0)
ACTUATOR_1SX1SX2S_BOTTOM: Final = ActuatorBrickBaseMeta('Actuator_1sx1sx2s_Top', -19, 0)
ACTUATOR_1X1X1_TOP: Final = ActuatorBrickBaseMeta('Actuator_1x1x1_Top', 0, 0)
ACTUATOR_1X1X1S_TOP: Final = ActuatorBrickBaseMeta('Actuator_1x1x1s_Top', 0, 0)
ACTUATOR_1X1X3_TOP: Final = ActuatorBrickBaseMeta('Actuator_1x1x3_Top', -70, 0)
ACTUATOR_1X1X6_TOP: Final = ActuatorBrickBaseMeta('Actuator_1x1x6_Top', -160, 0)
ACTUATOR_20X2X1S_TOP: Final = ActuatorBrickBaseMeta('Actuator_20x2x1s_Top', -285, 570)
ACTUATOR_2X1X1S_02_TOP: Final = ActuatorBrickBaseMeta('Actuator_2x1x1s_02_Top', -30, 0)
ACTUATOR_2X1X1S_MALE: Final = ActuatorBrickBaseMeta('Actuator_2x2x1s_Male', -45, 0)
ACTUATOR_2X1X1S_TOP: Final = ActuatorBrickBaseMeta('Actuator_2x2x1s_Top', 45, 0)
ACTUATOR_2X2X15_TOP: Final = ActuatorBrickBaseMeta('Actuator_2x2x15_Top', -410, 0)
ACTUATOR_2X2X1S_ANGULAR_TOP: Final = ActuatorBrickBaseMeta('Actuator_2x2x1s_Angular_Top', 0, 0)
ACTUATOR_2X2X1S_TOP: Final = ActuatorBrickBaseMeta('Actuator_2x2x1s_Top', 45, 0)
ACTUATOR_2X2X2_TOP: Final = ActuatorBrickBaseMeta('Actuator_2x2x2_Top', 0, 0)
ACTUATOR_4X1X1S_TOP: Final = ActuatorBrickBaseMeta('Actuator_4x1x1s_Top', -45, 90)
ACTUATOR_4X4X1S_TOP: Final = ActuatorBrickBaseMeta('Actuator_4x4x1s_Top', 0, 0)
ACTUATOR_6X2X1S_TOP: Final = ActuatorBrickBaseMeta('Actuator_6x2x1s_Top', 5, 0)
ACTUATOR_8X8X1_TOP: Final = ActuatorBrickBaseMeta('Actuator_8x8x1_Top', 0, 0)


class ActuatorBrickMeta(_b.BrickMeta):

    def __init__(
        self,
        name: str,
        actuation_speed: float,
        is_anglar_actuator: bool,
        linear_actuation_offset: float,
        linear_actuation_range: float,
        *args, **kwargs
    ):
        super().__init__(name, *args, **kwargs)
        self._actuation_speed = actuation_speed
        self._is_anglar_actuator = is_anglar_actuator
        self._linear_actuation_offset = linear_actuation_offset
        self._linear_actuation_range = linear_actuation_range

    def base_properties(self, *args, **kwargs) -> dict[str, Hashable]:
        return _base_properties | {
            _p.ACTUATOR_MODE: _p.ActuatorMode.ACCUMULATED,
            _p.INPUT_CNL_INPUT_AXIS: _p.InputCnl_InputAxis.CUSTOM,
            _p.INPUT_CNL_SOURCE_BRICKS: _p.InputCnl_SourceBricks.EMPTY,
            _p.INPUT_CNL_VALUE: _p.InputCnl_Value.DEFAULT_VALUE,
            _p.SPEED_FACTOR: 1.0
        }

    def actuation_speed(self):
        """Returns the speed of the actuator in degrees or cm per second"""
        return self._actuation_speed

    def is_anglar_actuator(self):
        """Returns whether or not it is an anglair actuator (spins or push)"""
        return self._is_anglar_actuator

    def linear_actuation_offset(self):
        """Returns the range of the actuator in centimeters"""
        return self._linear_actuation_offset

    def linear_actuation_range(self):
        """Returns linear actuation range (centimeters)"""
        return self._linear_actuation_range

ACTUATOR_1SX1SX1S_BOTTOM: Final = ActuatorBrickMeta('Actuator_1sx1sx1s_Bottom', 90, True, 5, 0)
ACTUATOR_1SX1SX1S_FEMALE: Final = ActuatorBrickMeta('Actuator_1sx1sx1s_Female', 90, True, 0, 0)
ACTUATOR_1SX1SX2S_BOTTOM: Final = ActuatorBrickMeta('Actuator_1sx1sx2s_Bottom', 50, True, 1e-6, 20)
ACTUATOR_1X1SX1S_BOTTOM: Final = ActuatorBrickMeta('Actuator_1x1sx1s_Bottom', 50, False, -10, -20)
ACTUATOR_1X1X1_BOTTOM: Final = ActuatorBrickMeta('Actuator_1x1x1_Bottom', 90, True, 0, 0)
ACTUATOR_1X1X1S_BOTTOM: Final = ActuatorBrickMeta('Actuator_1x1x1s_Bottom', 120, True, 10, 0)
ACTUATOR_1X1X3_BOTTOM: Final = ActuatorBrickMeta('Actuator_1x1x3_Bottom', 50, False, 10+4e-6, 70)
ACTUATOR_1X1X6_BOTTOM: Final = ActuatorBrickMeta('Actuator_1x1x6_Bottom', 100, False, 10+8e-6, 160)
ACTUATOR_20X2X1S_BOTTOM: Final = ActuatorBrickMeta('Actuator_20x2x1s_Bottom', 60, False, -285, 570)
ACTUATOR_2X1SX1S_BOTTOM: Final = ActuatorBrickMeta('Actuator_2x1sx1s_Bottom', 50, False, -25, 50)
ACTUATOR_2X1X1S_02_BOTTOM: Final = ActuatorBrickMeta('Actuator_2x1x1s_02_Bottom', 60, False, 5, 0)
ACTUATOR_2X1X1S_BOTTOM: Final = ActuatorBrickMeta('Actuator_2x1x1s_Bottom', 60, True, 0, 0)
ACTUATOR_2X1X1S_FEMALE: Final = ActuatorBrickMeta('Actuator_2x1x1s_Female', 60, False, 0, 0)
ACTUATOR_2X2X15_BOTTOM: Final = ActuatorBrickMeta('Actuator_2x2x15_Bottom', 200,False,10+15e-6, 410)
ACTUATOR_2X2X1S_ANGULAR: Final = ActuatorBrickMeta('Actuator_2x2x1s_Angular', 75, True, 10, 0)
ACTUATOR_2X2X1S_BOTTOM: Final = ActuatorBrickMeta('Actuator_2x2x1s_Bottom', 40, True, 0, 0)
ACTUATOR_2X2X2_BOTTOM: Final = ActuatorBrickMeta('Actuator_2x2x2_Bottom', 40, True, 0, 0)
ACTUATOR_4X1X1S_BOTTOM: Final = ActuatorBrickMeta('Actuator_4x1x1s_Bottom', 50, False, -45, 90)
ACTUATOR_4X4X1S_BOTTOM: Final = ActuatorBrickMeta('Actuator_4x4x1s_Bottom', 50, False, 10, 0)
ACTUATOR_6X2X1S_BOTTOM: Final = ActuatorBrickMeta('Actuator_6x2x1s_Bottom', 30, True, 0, 0)
ACTUATOR_8X8X1_BOTTOM: Final = ActuatorBrickMeta('Actuator_8x8x1_Bottom', 40, True, 20, 0)



class AntennaBrickMeta(_b.BrickMeta):

    def base_properties(self, *args, **kwargs):
        return _base_properties.copy()

ANTENNA_1X1X8: Final = AntennaBrickMeta('Antenna_1x1x8')
ANTENNA_2X1X1S: Final = AntennaBrickMeta('Antenna_2x1x1s')



class ArchBrickMeta(_b.BrickMeta):

    def base_properties(self, *args, **kwargs):
        return _base_properties | {
            _p.B_FLUID_DYNAMIC: False
        }

ARCH_2X1X2: Final = ArchBrickMeta('Arch_2x1x2')
ARCH_4X1X4: Final = ArchBrickMeta('Arch_4x1x4')
ARCH_6X1X1: Final = ArchBrickMeta('Arch_6x1x1')
ARCH_8X1X8: Final = ArchBrickMeta('Arch_8x1x8')



class AxleBrickMeta(_b.BrickMeta):

    def __init__(
        self,
        name: str,
        suspension_stiffness: float,
        suspension_damping: float,
        *args, **kwargs
    ):
        super().__init__(name, *args, **kwargs)
        self._suspension_stiffness = suspension_stiffness
        self._suspension_damping = suspension_damping

    def suspension_stiffness(self):
        """Suspension stiffness multiplier"""
        return self._suspension_stiffness

    def suspension_damping(self):
        """Suspension damping multiplier"""
        return self._suspension_damping

    def base_properties(self, *args, **kwargs):
        return _base_properties | {
            _p.SUSPENSION_LENGTH: 0,
            _p.SUSPENSION_STIFFNESS: 2,
            _p.SUSPENSION_DAMPING: 1,
            _p.B_DRIVEN: True,
            _p.B_INVERT_DRIVE: False,
            _p.B_HAS_BRAKE: True,
            _p.B_HAS_HANDBRAKE: True,
            _p.BRAKE_STRENGTH: _p.BrakeStrength.BASE,
            _p.STEERING_INPUT_CNL_INPUT_AXIS: _p.SteeringInputCnl_InputAxis.STEERING,
            _p.STEERING_INPUT_CNL_SOURCE_BRICKS: _p.SteeringInputCnl_SourceBricks.EMPTY,
            _p.STEERING_INPUT_CNL_VALUE: _p.SteeringInputCnl_Value.DEFAULT_VALUE,
            _p.BRAKE_INPUT_CNL_INPUT_AXIS: _p.BrakeInputCnl_InputAxis.STEERING,
            _p.BRAKE_INPUT_CNL_SOURCE_BRICKS: _p.BrakeInputCnl_SourceBricks.EMPTY,
            _p.BRAKE_INPUT_CNL_VALUE: _p.BrakeInputCnl_Value.DEFAULT_VALUE,
            _p.B_CAN_DISABLE_STEERING: False,
            _p.B_CAN_INVERT_STEERING: False
        }


AXLE_1SX1SX1S: Final = AxleBrickMeta('Axle_1sx1sx1s', 1000, 50)
AXLE_1X1X1S: Final = AxleBrickMeta('Axle_1x1x1s', 1000, 50)
AXLE_1X1X1S_02: Final = AxleBrickMeta('Axle_1x1x1s_02', 1000, 50)
AXLE_1X2X1S: Final = AxleBrickMeta('Axle_1x2x1s', 1000, 50)
AXLE_2X2X1: Final = AxleBrickMeta('Axle_2x2x1', 5000, 250)
AXLE_2X2X1S: Final = AxleBrickMeta('Axle_2X2X1S', 1000, 50)
AXLE_2X4X1S: Final = AxleBrickMeta('Axle_2x4x1s', 3000, 150)
AXLE_2X6X1S: Final = AxleBrickMeta('Axle_2x6x1s', 4000, 200)



class BarrelBrickMeta(_b.BrickMeta):

    def base_properties(self, *args, **kwargs):
        return _base_properties.copy()

BARREL_1SX1SX3: Final = BarrelBrickMeta('Barrel_1sx1sx3')
BARREL_1X1X4: Final = BarrelBrickMeta('Barrel_1x1x4')
BARREL_1X1X4_FLAT: Final = BarrelBrickMeta('Barrel_1x1x4_Flat')



class BladeBrickMeta(_b.BrickMeta):

    def base_properties(self, *args, **kwargs):
        return _base_properties.copy()

BLADE_20X2: Final = BladeBrickMeta('Blade_20x2')
BLADE_26X2: Final = BladeBrickMeta('Blade_26x2')



class BladeHolderBrickMeta(_b.BrickMeta):

    def base_properties(self, *args, **kwargs):
        return _base_properties.copy()

BLADE_HOLDER_2X1: Final = BladeHolderBrickMeta('BladeHolder_2x1')



class CarWheelBrickMeta(_b.BrickMeta):

    def __init__(
        self,
        name: str,
        rim_radius: float,
        min_tire_thickness: float,
        min_tire_pop_damage: float,
        wheel_radius: float,
        min_wheel_radius: float,
        max_wheel_radius_scale: float,
        min_wheel_width: float,
        max_wheel_width_scale: float,
        *args, **kwargs
    ):
        super().__init__(name, *args, **kwargs)
        self._rim_radius = rim_radius
        self._min_tire_thickness = min_tire_thickness
        self._min_tire_pop_damage = min_tire_pop_damage
        self._wheel_radius = wheel_radius
        self._min_wheel_radius = min_wheel_radius
        self._max_wheel_radius_scale = max_wheel_radius_scale
        self._min_wheel_width = min_wheel_width
        self._max_wheel_width_scale = max_wheel_width_scale

    def rim_radius(self):
        """Radius of the rim only"""
        return self._rim_radius

    def min_tire_thickness(self):
        """Minimum thickness the tire is allowed to be scaled to"""
        return self._min_tire_thickness

    def min_tire_pop_damage(self):
        """Min damage needed to pop the tire"""
        return self._min_tire_pop_damage

    def wheel_radius(self):
        """Radius of the wheel"""
        return self._wheel_radius

    def min_wheel_radius(self):
        """Minimum wheel radius"""
        return self._min_wheel_radius

    def max_wheel_radius_scale(self):
        """Max wheel radius scale"""
        return self._max_wheel_radius_scale

    def min_wheel_width(self):
        """Min wheel width"""
        return self._min_wheel_width

    def max_wheel_width_scale(self):
        """Max wheel width scale"""
        return self._max_wheel_width_scale

    def base_properties(self, *args, **kwargs):

        wheel_diameter = kwargs.get('wd')
        assert wheel_diameter is not None, f"wheel_diameter is not set for brick type {self._name}"
        wheel_width = kwargs.get('ww')
        assert wheel_width is not None, f"wheel_width is not set for brick type {self._name}"
        tire_width = kwargs.get('tw')
        assert tire_width is not None, f"tire_width is not set for brick type {self._name}"

        return _base_properties | {
            _p.B_INVERT_TANK_STEERING: False,
            _p.WHEEL_DIAMETER: wheel_diameter,
            _p.WHEEL_WIDTH: wheel_width,
            _p.TIRE_WIDTH: tire_width,
            _p.TIRE_PRESSURE: _p.TirePressure.DEFAULT_VALUE
        }

DRAG_WHEEL_4X2: Final = CarWheelBrickMeta('DragWheel_4x2', 30, 10, 0.1, 60, 37.5, 2, 55, 4,
                                          wd=120, ww=70, tw=30)


class ExhaustBrickMeta(_b.BrickMeta):

    def base_properties(self, *args, **kwargs):
        return _base_properties | {
            _p.BRICK_SIZE: _v.Vec3(30, 30, 30),
            _p.CONNECTOR_SPACING: _p.ConnectorSpacing.ALL_CONNECTIONS,
            _p.INPUT_CNL_INPUT_AXIS: _p.InputCnl_InputAxis.NONE,
            _p.INPUT_CNL_SOURCE_BRICKS: _p.InputCnl_SourceBricks.EMPTY,
            _p.INPUT_CNL_VALUE: _p.InputCnl_Value.DEFAULT_VALUE,
            _p.SPAWN_SCALE: 1,
            _p.SIZE_SCALE: 1,
            _p.EXHAUST_EFFECT: _p.ExhaustEffect.SMOKE,
            _p.SMOKE_COLOR: 0xffffff
        }

EXHAUST_BRICK: Final = ExhaustBrickMeta('ExhaustBrick')
EXHAUST_CYLINDER: Final = ExhaustBrickMeta('ExhaustCylinder')



class LegoBrickMeta(_b.BrickMeta):  # Not the same name as in BRMK.

    def base_properties(self, *args, **kwargs):
        return _base_properties | {
            _p.B_FLUID_DYNAMIC: False
        }

BRICK_10X1X1: Final = LegoBrickMeta('Brick_10x1x1')
BRICK_10X1X1S: Final = LegoBrickMeta('Brick_10x1x1s')
BRICK_10X2X1: Final = LegoBrickMeta('Brick_10x2x1')
BRICK_10X2X1S: Final = LegoBrickMeta('Brick_10x2x1s')
BRICK_10X2X1S_FLAT: Final = LegoBrickMeta('Brick_10x2x1s_Flat')
BRICK_10X4X1S: Final = LegoBrickMeta('Brick_10x4x1s')
BRICK_10X4X1S_FLAT: Final = LegoBrickMeta('Brick_10x4x1s_Flat')
BRICK_10X6X1S: Final = LegoBrickMeta('Brick_10x6x1s')
BRICK_10X6X1S_FLAT: Final = LegoBrickMeta('Brick_10x6x1s_Flat')
BRICK_10X8X1S: Final = LegoBrickMeta('Brick_10x8x1s')
BRICK_10X8X1S_FLAT: Final = LegoBrickMeta('Brick_10x8x1s_Flat')
BRICK_12X1X1: Final = LegoBrickMeta('Brick_12x1x1')
BRICK_12X1X1S: Final = LegoBrickMeta('Brick_12x1x1s')
BRICK_12X6X1S: Final = LegoBrickMeta('Brick_12x6x1s')
BRICK_12X6X1S_FLAT: Final = LegoBrickMeta('Brick_12x6x1s_Flat')
BRICK_12X8X1S: Final = LegoBrickMeta('Brick_12x8x1s')
BRICK_12X8X1S_FLAT: Final = LegoBrickMeta('Brick_12x8x1s_Flat')
BRICK_16X1X1: Final = LegoBrickMeta('Brick_16x1x1')
BRICK_16X8X1S: Final = LegoBrickMeta('Brick_16x8x1s')
BRICK_16X8X1S_FLAT: Final = LegoBrickMeta('Brick_16x8x1s_Flat')
BRICK_1X1X1: Final = LegoBrickMeta('Brick_1x1x1')
BRICK_1X1X1S: Final = LegoBrickMeta('Brick_1x1x1s')
BRICK_1X1X1S_FLAT: Final = LegoBrickMeta('Brick_1x1x1s_Flat')
BRICK_20X1X1: Final = LegoBrickMeta('Brick_20x1x1')
BRICK_2X1X1: Final = LegoBrickMeta('Brick_2x1x1')
BRICK_2X1X1S: Final = LegoBrickMeta('Brick_2x1x1s')
BRICK_2X1X1S_FLAT: Final = LegoBrickMeta('Brick_2x1x1s_Flat')
BRICK_2X2X1: Final = LegoBrickMeta('Brick_2x2x1')
BRICK_2X2X1S: Final = LegoBrickMeta('Brick_2x2x1s')
BRICK_2X2X1S_FLAT: Final = LegoBrickMeta('Brick_2x2x1s_Flat')
BRICK_3X1X1: Final = LegoBrickMeta('Brick_3x1x1')
BRICK_3X1X1S: Final = LegoBrickMeta('Brick_3x1x1s')
BRICK_3X1X1S_FLAT: Final = LegoBrickMeta('Brick_3x1x1s_Flat')
BRICK_3X2X1: Final = LegoBrickMeta('Brick_3x2x1')
BRICK_3X2X1S: Final = LegoBrickMeta('Brick_3x2x1s')
BRICK_3X2X1S_FLAT: Final = LegoBrickMeta('Brick_3x2x1s_Flat')
BRICK_4X1X1: Final = LegoBrickMeta('Brick_4x1x1')
BRICK_4X1X1S: Final = LegoBrickMeta('Brick_4x1x1s')
BRICK_4X1X1S_FLAT: Final = LegoBrickMeta('Brick_4x1x1s_Flat')
BRICK_4X2X1: Final = LegoBrickMeta('Brick_4x2x1')
BRICK_4X2X1S: Final = LegoBrickMeta('Brick_4x2x1s')
BRICK_4X2X1S_FLAT: Final = LegoBrickMeta('Brick_4x2x1s_Flat')
BRICK_4X4X1S: Final = LegoBrickMeta('Brick_4x4x1s')
BRICK_4X4X1S_FLAT: Final = LegoBrickMeta('Brick_4x4x1s_Flat')
BRICK_5X1X1: Final = LegoBrickMeta('Brick_5x1x1')
BRICK_5X1X1S: Final = LegoBrickMeta('Brick_5x1x1s')
BRICK_5X1X1S_FLAT: Final = LegoBrickMeta('Brick_5x1x1s_Flat')
BRICK_5X2X1: Final = LegoBrickMeta('Brick_5x2x1')
BRICK_5X2X1S: Final = LegoBrickMeta('Brick_5x2x1s')
BRICK_5X2X1S_FLAT: Final = LegoBrickMeta('Brick_5x2x1s_Flat')
BRICK_6X1X1: Final = LegoBrickMeta('Brick_6x1x1')
BRICK_6X1X1S: Final = LegoBrickMeta('Brick_6x1x1s')
BRICK_6X1X1S_FLAT: Final = LegoBrickMeta('Brick_6x1x1s_Flat')
BRICK_6X2X1: Final = LegoBrickMeta('Brick_6x2x1')
BRICK_6X2X1S: Final = LegoBrickMeta('Brick_6x2x1s')
BRICK_6X2X1S_FLAT: Final = LegoBrickMeta('Brick_6x2x1s_Flat')
BRICK_6X4X1S: Final = LegoBrickMeta('Brick_6x4x1s')
BRICK_6X4X1S_FLAT: Final = LegoBrickMeta('Brick_6x4x1s_Flat')
BRICK_6X6X1S: Final = LegoBrickMeta('Brick_6x6x1s')
BRICK_6X6X1S_FLAT: Final = LegoBrickMeta('Brick_6x6x1s_Flat')
BRICK_8X1X1: Final = LegoBrickMeta('Brick_8x1x1')
BRICK_8X1X1S: Final = LegoBrickMeta('Brick_8x1x1s')
BRICK_8X1X1S_FLAT: Final = LegoBrickMeta('Brick_8x1x1s_Flat')
BRICK_8X2X1: Final = LegoBrickMeta('Brick_8x2x1')
BRICK_8X2X1S: Final = LegoBrickMeta('Brick_8x2x1s')
BRICK_8X2X1S_FLAT: Final = LegoBrickMeta('Brick_8x2x1s_Flat')
BRICK_8X4X1S: Final = LegoBrickMeta('Brick_8x4x1s')
BRICK_8X4X1S_FLAT: Final = LegoBrickMeta('Brick_8x4x1s_Flat')
BRICK_8X6X1S: Final = LegoBrickMeta('Brick_8x6x1s')
BRICK_8X6X1S_FLAT: Final = LegoBrickMeta('Brick_8x6x1s_Flat')
BRICK_8X8X1S: Final = LegoBrickMeta('Brick_8x8x1s')
BRICK_8X8X1S_FLAT: Final = LegoBrickMeta('Brick_8x8x1s_Flat')
BRICK_ROUNDED_2X1X1S: Final = LegoBrickMeta('BrickRounded_2x1x1s')
BRICK_ROUNDED_2X1X1S_FLAT: Final = LegoBrickMeta('BrickRounded_2x1x1s_Flat')
BRICK_ROUNDED_3X1X1S: Final = LegoBrickMeta('BrickRounded_3x1x1s')
BRICK_ROUNDED_3X1X1S_FLAT: Final = LegoBrickMeta('BrickRounded_3x1x1s_Flat')
BRICK_ROUNDED_4X1X1S: Final = LegoBrickMeta('BrickRounded_4x1x1s')
BRICK_ROUNDED_4X1X1S_FLAT: Final = LegoBrickMeta('BrickRounded_4x1x1s_Flat')
BRICK_ROUNDED_5X1X1S: Final = LegoBrickMeta('BrickRounded_5x1x1s')
BRICK_ROUNDED_5X1X1S_FLAT: Final = LegoBrickMeta('BrickRounded_5x1x1s_Flat')
BRICK_ROUNDED_6X1X1S: Final = LegoBrickMeta('BrickRounded_6x1x1s')
BRICK_ROUNDED_6X1X1S_FLAT: Final = LegoBrickMeta('BrickRounded_6x1x1s_Flat')
BRICK_ROUNDED_8X1X1S: Final = LegoBrickMeta('BrickRounded_8x1x1s')
BRICK_ROUNDED_8X1X1S_FLAT: Final = LegoBrickMeta('BrickRounded_8x1x1s_Flat')
BRICK_ROUNDED_CORNER_2X2X1S: Final = LegoBrickMeta('BrickRoundedCorner_2x2x1s')

CORNER_BRICK_2X2X1: Final = LegoBrickMeta('CornerBrick_2x2x1')
CORNER_BRICK_2X2X1S: Final = LegoBrickMeta('CornerBrick_2x2x1s')



class BumperBrickMeta(_b.BrickMeta):

    def base_properties(self, *args, **kwargs):
        return _base_properties | {
            _p.B_FLUID_DYNAMIC: False
        }

BUMPER_4SX6X2: Final = BumperBrickMeta('Bumper_4sx6x2')
BUMPER_4SX8X7S: Final = BumperBrickMeta('Bumper_4x8x7s')



class CameraBrickMeta(_b.BrickMeta):

    def base_properties(self, *args, **kwargs):
        return _base_properties | {
            _p.CAMERA_NAME: _p.CameraName.EMPTY,
            _p.OWNING_SEAT: _p.OwningSeat.EMPTY
        }

CAMERA_1SX1SX1S: Final = CameraBrickMeta('Camera_2x1x1')
CAMERA_2X1X1: Final = CameraBrickMeta('Camera_2x1x1')



class CompressorBrickMeta(_b.BrickMeta):

    def __init__(self, name: str, boost_factor: float, *args, **kwargs):
        super().__init__(name, *args, **kwargs)
        self._boost_factor = boost_factor

    def boost_factor(self):
        """Compressor's boost factor"""
        return self._boost_factor

    def base_properties(self, *args, **kwargs):
        return _base_properties | {
            _p.B_FLUID_DYNAMIC: False
        }

COMPRESSOR_4X1X4S: Final = CompressorBrickMeta('Compressor_4x1x4s', 1)



class ConeBrickMeta(_b.BrickMeta):

    def base_properties(self, *args, **kwargs):
        return _base_properties | {
            _p.B_FLUID_DYNAMIC: False
        }

CONE_1X1X1: Final = ConeBrickMeta('Cone_1x1x1')
CONE_2X2X2: Final = ConeBrickMeta('Cone_2x2x2')
CONE_4X4X4: Final = ConeBrickMeta('Cone_4x4x4')



class CouplingBrickMeta(_b.BrickMeta):

    def __init__(self, name: str, angular_limits: _v.Vec3, *args, **kwargs):
        super().__init__(name, *args, **kwargs)
        self._angular_limits: _v.Vec3 = angular_limits

    def angular_limits(self):
        """Angular limits of the coupler"""
        return _v.Vec3(*self._angular_limits.as_tuple())

    def base_properties(self, *args, **kwargs):
        return _base_properties | {
            _p.COUPLING_MODE: _p.CouplingMode.DEFAULT,
            _p.INPUT_CNL_INPUT_AXIS: _p.InputCnl_InputAxis.NONE,
            _p.INPUT_CNL_SOURCE_BRICKS: _p.InputCnl_SourceBricks.EMPTY,
            _p.INPUT_CNL_VALUE: _p.InputCnl_Value.DEFAULT_VALUE
        }

COUPLING_1SX1SX1S_FRONT_MALE: Final = CouplingBrickMeta('Coupling_1sx1sx1s_Front_Male',
                                                        _v.Vec3(0, 15, 15))
COUPLING_1X1X1S_FRONT_MALE: Final = CouplingBrickMeta('Coupling_1x1x1s_Front_Male',
                                                      _v.Vec3(0, 15, 15))
COUPLING_2X2X1S_FRONT_MALE: Final = CouplingBrickMeta('Coupling_2x2x1s_Front_Male',
                                                      _v.Vec3(0, 15, 15))
COUPLING_2X2X1S_MALE: Final = CouplingBrickMeta('Coupling_2x2x1s_Male', _v.Vec3(15, 0, 15))
COUPLING_4X1X2S_BOTTOM: Final = CouplingBrickMeta('Coupling_4x1x2s_Bottom', _v.Vec3(0, 0, 0))
COUPLING_6X2X1S_MALE: Final = CouplingBrickMeta('Coupling_6x2x1s_Male', _v.Vec3(0, 15, 15))



class CouplingBrickBaseMeta(_b.BrickMeta):

    def base_properties(self, *args, **kwargs):
        return _base_properties

COUPLING_1SX1SX1S_FRONT_FEMALE: Final = CouplingBrickBaseMeta('Coupling_1sx1sx1s_Front_Female')
COUPLING_1X1X1S_FRONT_FEMALE: Final = CouplingBrickBaseMeta('Coupling_1x1x1s_Front_Female')
COUPLING_2X2X1S_FEMALE: Final = CouplingBrickBaseMeta('Coupling_2x2x1s_Female')
COUPLING_2X2X1S_FRONT_FEMALE: Final = CouplingBrickBaseMeta('Coupling_2x2x1s_Front_Female')
COUPLING_4X1X2S_TOP: Final = CouplingBrickBaseMeta('Coupling_4x1x2s_Top')



class CylinderBrickMeta(_b.BrickMeta):

    def base_properties(self, *args, **kwargs):
        return _base_properties | {
            _p.B_FLUID_DYNAMIC: False
        }

HALF_CYLINDER_4X2X4: Final = CylinderBrickMeta('HalfZylinder_4x2x4')



class DetonatorBrickMeta(_b.BrickMeta):

    def __init__(self, name: str, damage: float, *args, **kwargs):
        super().__init__(name, *args, **kwargs)
        self._damage = damage

    def damage(self):
        """Damage applied upon detonation"""
        return self._damage

    def base_properties(self, *args, **kwargs):
        return _base_properties | {
            _p.BRICK_SIZE: _v.Vec3(30, 30, 30),
            _p.CONNECTOR_SPACING: _p.ConnectorSpacing.ALL_CONNECTIONS
        }

DETONATOR_BRICK: Final = DetonatorBrickMeta('DetonatorBrick', 1.0)
DETONATOR_CYLINDER: Final = DetonatorBrickMeta('DetonatorCylinder', 1.0)



class DisplayBrickMeta(_b.BrickMeta):

    def base_properties(self, *args, **kwargs):
        return _base_properties | {
            _p.BRICK_SIZE: _v.Vec3(60, 30, 10),
            _p.CONNECTOR_SPACING: _p.ConnectorSpacing.NO_TOP,
            _p.INPUT_CNL_INPUT_AXIS: _p.InputCnl_InputAxis.CUSTOM,
            _p.INPUT_CNL_SOURCE_BRICKS: _p.InputCnl_SourceBricks.EMPTY,
            _p.INPUT_CNL_VALUE: _p.InputCnl_Value.DEFAULT_VALUE,
            _p.NUM_FRACTIONAL_DIGITS: 1,
            _p.DISPLAY_COLOR: 0xbc5959
        }

DISPLAY_BRICK: Final = DisplayBrickMeta('DisplayBrick')



class DoorBrickMeta(_b.BrickMeta):

    def base_properties(self, *args, **kwargs):
        return _base_properties | {
            _p.B_FLUID_DYNAMIC: False
        }

DOOR_L_3X1X1: Final = DoorBrickMeta('Door_L_3x1x1')
DOOR_L_3X1X2: Final = DoorBrickMeta('Door_L_3x1x2')
DOOR_R_3X1X1: Final = DoorBrickMeta('Door_R_3x1x1')
DOOR_R_3X1X2: Final = DoorBrickMeta('Door_R_3x1x2')



class FlamethrowerBrickMeta(_b.BrickMeta):

    def __init__(
        self,
        name: str,
        flame_length: float,
        flame_radius: float,
        flame_damage: float,
        damage_interval: float,
        fuel_capacity: float,
        fuel_consumption: float,
        *args, **kwargs
    ):
        super().__init__(name, *args, **kwargs)
        self._flame_length = flame_length
        self._flame_radius = flame_radius
        self._flame_damage = flame_damage
        self._damage_interval = damage_interval
        self._fuel_capacity = fuel_capacity
        self._fuel_consumption = fuel_consumption

    def flame_length(self):
        """How far the flame reaches"""
        return self._flame_length

    def flame_radius(self):
        """The maximum radius of the flame"""
        return self._flame_radius

    def flame_damage(self):
        """The damage to apply to objects being hit by the flame"""
        return self._flame_damage

    def damage_interval(self):
        """How often damage is applied and stuff is ignited"""
        return self._damage_interval

    def fuel_capacity(self):
        """Fuel capacity"""
        return self._fuel_capacity

    def fuel_consumption(self):
        """Amount of fuel in liters to consume per second"""
        return self._fuel_consumption

    def base_properties(self, *args, **kwargs):
        return _base_properties | {
            _p.INPUT_CNL_INPUT_AXIS: _p.InputCnl_InputAxis.FIRE_ACTION_1,
            _p.INPUT_CNL_SOURCE_BRICKS: _p.InputCnl_SourceBricks.EMPTY,
            _p.INPUT_CNL_VALUE: _p.InputCnl_Value.DEFAULT_VALUE
        }

FLAMETHROWER_2X2X2: Final = FlamethrowerBrickMeta('Flamethrower_2x2x2', 1000, 100, .25, .25, 10, 1)



class FlapBrickMeta(_b.BrickMeta):

    def __init__(self, name: str, flap_interp_speed: float, *args, **kwargs):
        super().__init__(name, *args, **kwargs)
        self._flap_interp_speed = flap_interp_speed

    def flap_interp_speed(self):
        """Rate at which the flap is moved"""
        return self._flap_interp_speed

    def base_properties(self, *args, **kwargs):
        return _base_properties | {
            _p.B_FLUID_DYNAMIC: True,
            _p.BRICK_SIZE: _v.Vec3(60, 120, 10),
            _p.CONNECTOR_SPACING: _p.ConnectorSpacing.ALL_CONNECTIONS,
            _p.INPUT_CNL_INPUT_AXIS: _p.InputCnl_InputAxis.NONE,
            _p.INPUT_CNL_SOURCE_BRICKS: _p.InputCnl_SourceBricks.EMPTY,
            _p.INPUT_CNL_VALUE: _p.InputCnl_Value.DEFAULT_VALUE,
            _p.INPUT_SCALE: _p.InputScale.BASE,
            _p.MIN_ANGLE: -22.5,
            _p.MAX_ANGLE: 22.5,
            _p.B_ACCUMULATE_INPUT: False
        }

FLAP_BRICK: Final = FlapBrickMeta('FlapBrick', 256)
FLAP_WEDGE: Final = FlapBrickMeta('FlapWedge', 256)



class FlareBrickMeta(_m.BaseGunBrickMeta):
    pass

FLARE_GUN_1X1X1: Final = FlareBrickMeta('FlareGun_1x1x1', _ip.FirearmProperties(
    9, _p.AmmoType.FLARE, _ip.ProjectileParams(5e3, .1, .05, 1e3, 1e4, 1e4), 1, 500, .25, True,
    False, 0), 15, 1e3, 240, .1, .35, .5, at=_p.AmmoType.FLARE)



class FloatBrickMeta(_b.BrickMeta):

    def base_properties(self, *args, **kwargs):
        return _base_properties | {
            _p.BRICK_SIZE: _v.Vec3(30, 30, 30),
            _p.CONNECTOR_SPACING: _p.ConnectorSpacing.ALL_CONNECTIONS
        }

FLOAT: Final = FloatBrickMeta('Float')



class GrilleBrickMeta(_b.BrickMeta):

    def base_properties(self, *args, **kwargs):
        return _base_properties | {
            _p.B_FLUID_DYNAMIC: False
        }

GRID_2X1X1S: Final = GrilleBrickMeta('Grid_2x1x1s')
GRID_2X1X1S_02: Final = GrilleBrickMeta('Grid_2x1x1s_02')
GRID_CYLINDER_2X1X1S: Final = GrilleBrickMeta('GridZylinder_2x1x1s')



class GunBrickMeta(_m.BaseGunBrickMeta):
    pass

GUN_2X1X1: Final = GunBrickMeta('Gun_2x1x1', _ip.FirearmProperties(100, _p.AmmoType.DEFAULT,
    _ip.ProjectileParams(74000, 0.3, 0.15, 2e3, 5e4, 5e5), 1, 40, 0.1, False, True, 0), 2, 2500, 90,
    0.1, 0.35, 0.5, at=_p.AmmoType.DEFAULT)
GUN_2X2X2: Final = GunBrickMeta('Gun_2x2x2', _ip.FirearmProperties(1, _p.AmmoType.HIGH_EXPLOSIVE,
    _ip.ProjectileParams(5e5, 10, 1, 5e4, 1e6, 1e6), 1, 10, 0.5, True, False, 0), 1.5, 1e5, 240,
    0.1, 0.35, 0.5, at=_p.AmmoType.HIGH_EXPLOSIVE)
# Parent class of GUN_2X2X2_BALLISTIC is actually GUN_2X2X2... But you didn't see anything. Did you?
GUN_2X2X2_BALLISTIC: Final = GunBrickMeta('Gun_2x2x2_Ballistic', _ip.FirearmProperties(1,
    _p.AmmoType.DEFAULT, _ip.ProjectileParams(65000, 15, 15, 2e4, 8e5, 1e6), 1, 10, 0.5, True,
    False, 0), 1.5, 1e5, 240, 0.1, 0.35, 0.5, at=_p.AmmoType.DEFAULT)
GUN_4X2X2: Final = GunBrickMeta('Gun_4x2x2', _ip.FirearmProperties(100, _p.AmmoType.DEFAULT,
    _ip.ProjectileParams(88000, 2, 1, 2500, 5e4, 5e5), 1, 20, 0.15, False, True, 0), 2, 5e3, 180,
    0.1, 0.35, 0.5, at=_p.AmmoType.DEFAULT)



class HandleBrickMeta(_b.BrickMeta):

    def base_properties(self, *args, **kwargs):
        return _base_properties.copy()

HANDLE_1X2X4S: Final = HandleBrickMeta('Handle_1x2x4s')
HANDLE_4X1X1: Final = HandleBrickMeta('Handle_4x1x1')



class IdlerWheelMeta(_b.BrickMeta):

    def __init__(
        self,
        name: str,
        wheel_radius: float,
        min_wheel_radius: float,
        max_wheel_radius_scale: float,
        min_wheel_width: float,
        max_wheel_width_scale: float,
        *args, **kwargs
    ):
        super().__init__(name, *args, **kwargs)
        self._wheel_radius = wheel_radius
        self._min_wheel_radius = min_wheel_radius
        self._max_wheel_radius_scale = max_wheel_radius_scale
        self._min_wheel_width = min_wheel_width
        self._max_wheel_width_scale = max_wheel_width_scale

    def wheel_radius(self):
        """Radius of the idler wheel"""
        return self._wheel_radius

    def min_wheel_radius(self):
        """Min Wheel Radius"""
        return self._min_wheel_radius

    def max_wheel_radius_scale(self):
        """Max Wheel Radius"""
        return self._max_wheel_radius_scale

    def min_wheel_width(self):
        """Min Wheel Width"""
        return self._min_wheel_width

    def max_wheel_width_scale(self):
        """Max Wheel Width Scale"""
        return self._max_wheel_width_scale

    def base_properties(self, *args, **kwargs):
        return _base_properties | {
            _p.B_INVERT_TANK_STEERING: False,
            _p.WHEEL_DIAMETER: 90,
            _p.WHEEL_WIDTH: 30
        }

IDLER_WHEEL: Final = IdlerWheelMeta('IdlerWheel', 45, 20, 2, 25, 4)



class ImageBrickMeta(_b.BrickMeta):

    def __init__(
            self,
            name: str,
            image_margin: float,
            *args, **kwargs
        ):
        super().__init__(name, *args, **kwargs)
        self._image_margin = image_margin

    def image_margin(self):
        """Size of the margin to keep around the image"""
        return self._image_margin

    def base_properties(self, *args, **kwargs):
        size = kwargs.get("size")
        assert size is not None, "size is not set for brick type " + self._name
        spacing = kwargs.get("spacing")
        assert spacing is not None, "spacing is not set for brick type " + self._name
        return _base_properties | {
            _p.BRICK_SIZE: size,
            _p.CONNECTOR_SPACING: spacing,
            _p.B_FLUID_DYNAMIC: False,
            _p.IMAGE: _p.Image.CAUTION,
            _p.IMAGE_COLOR: _p.ImageColor.DEFAULT_COLOR,
        }

IMAGE_BRICK: Final = ImageBrickMeta('ImageBrick', 0.5, size=_v.Vec3(60, 60, 10), spacing=_p.ConnectorSpacing.NO_TOP)
IMAGE_CYLINDER: Final = ImageBrickMeta('ImageCylinder', 0.5, size=_v.Vec3(60, 60, 10), spacing=_p.ConnectorSpacing.NO_TOP)
FLAG_3X1X2: Final = ImageBrickMeta('Flag_3x1x2', 0.5, size=_v.Vec3(60, 10, 60), spacing=_p.ConnectorSpacing.ALL_CONNECTIONS)



class LedgeBrickMeta(_b.BrickMeta):

    def base_properties(self, *args, **kwargs):
        return _base_properties | {
            _p.B_FLUID_DYNAMIC: False
        }

CORNER_LEDGE_1X1X1: Final = LedgeBrickMeta('CornerLedge_1x1x1')



class MotorBrickMeta(_b.BrickMeta):

    def __init__(
        self,

        startup_time: float,
        acceleration: float,
        rpm_range: tuple[float, float],
        clutch_rpm_range: tuple[float, float],
        shiftup_rpm_range: tuple[float, float],
        shiftdown_rpm_range: tuple[float, float],
        backfire_rpm: float,

        shift_delay: float,
        min_auto_shift_delay: float,
        num_forward_gears: int,
        num_reverse_gears: int,
        last_gear_speed: int,

        fuel_capacity: float,
        fuel_consumption: float,

        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)

        self._startup_time = startup_time
        self._acceleration = acceleration
        self._rpm_range = rpm_range
        self._clutch_rpm_range = clutch_rpm_range
        self._shiftup_rpm_range = shiftup_rpm_range
        self._shiftdown_rpm_range = shiftdown_rpm_range
        self._backfire_rpm = backfire_rpm

        self._shift_delay = shift_delay
        self._min_auto_shift_delay = min_auto_shift_delay
        self._num_forward_gears = num_forward_gears
        self._num_reverse_gears = num_reverse_gears
        self._last_gear_speed = last_gear_speed

        self._fuel_capacity = fuel_capacity
        self._fuel_consumption = fuel_consumption

    def startup_time(self):
        """Time it takes until the motor is started"""
        return self._startup_time

    def acceleration(self):
        """Angular acceleration in the first gear"""
        return self._acceleration

    def rpm_range(self):
        """Min (idle) and max RPM"""
        return self._rpm_range

    def clutch_rpm_range(self):
        """Relative RPM at which the clutch starts to grip and is fully engaged"""
        return self._clutch_rpm_range

    def shiftup_rpm_range(self):
        """RPM ratio to shift up at 0 and 100% throttle"""
        return self._shiftup_rpm_range

    def shiftdown_rpm_range(self):
        """RPM ratio to shift down at 0 and 100% throttle"""
        return self._shiftdown_rpm_range

    def backfire_rpm(self):
        """RPM at which the backfire effect is spawned"""
        return self._backfire_rpm

    def shift_delay(self):
        """Time a gear shift takes"""
        return self._shift_delay

    def min_auto_shift_delay(self):
        """Minimum time to wait between automatic shifts"""
        return self._min_auto_shift_delay

    def num_forward_gears(self):
        """Num Forward Gears"""
        return self._num_forward_gears

    def num_reverse_gears(self):
        """Num Reverse Gears"""
        return self._num_reverse_gears

    def last_gear_speed(self):
        """Last Gear Speed (cm/s)"""
        return self._last_gear_speed

    def fuel_capacity(self):
        """Fuel capacity"""
        return self._fuel_capacity

    def fuel_consumption(self):
        """Amount of fuel in liters to consume per second"""
        return self._fuel_consumption


    def base_properties(self, *args, **kwargs):
        return _base_properties | {
            _p.THROTTLE_INPUT_CNL_INPUT_AXIS: _p.ThrottleInputCnl_InputAxis.THROTTLE,
            _p.THROTTLE_INPUT_CNL_SOURCE_BRICKS: _p.ThrottleInputCnl_SourceBricks.EMPTY,
            _p.THROTTLE_INPUT_CNL_VALUE: _p.ThrottleInputCnl_Value.DEFAULT_VALUE,
            _p.GEAR_RATIO: _p.GearRatio.BASE,
            _p.B_TANK_DRIVE: False,
        }

AIRCRAFTR4: Final = MotorBrickMeta('AircraftR4', 0.5, 3, (1000, 10000), (0, 0.05), (0.65, 0.95),
                                   (0.1, 0.3), 0.85, .5, 2, 1, 1, 5500,  10, 1e-3)
DIESELV12: Final = MotorBrickMeta('DieselV12', 2, 1.2, (200, 2000), (0, 0.05), (0.65, 0.95),
                                  (0.1, 0.3), 0.85, 0.5, 2, 5, 3, 2500, 40, 0.05)
DRAGV8: Final = MotorBrickMeta('DragV8', 1, 4, (1000, 10000), (0, 0.05), (0.65, 0.95), (0.1, 0.3),
                               0.85, 0.1, 2, 5, 1, 14000, 20, 0.5)
EMOTOR_2X2X2: Final = MotorBrickMeta('EMotor_2x2x2', 0, 5, (0, 10000), (0, 0.05), (0.65, 0.95),
                                     (0.1, 0.3), 0.85, 0.2, 2, 3, 1, 8300, 10, 0.001)



class RampBrickMeta(_b.BrickMeta):

    def base_properties(self, *args, **kwargs):
        return _base_properties.copy()

CORNER_RAMP_1X1X1: Final = RampBrickMeta('CornerRamp_1x1x1')
CORNER_RAMP_2X2X1: Final = RampBrickMeta('CornerRamp_2x2x1')
CORNER_RAMP_2X2X1_02: Final = RampBrickMeta('CornerRamp_2x2x1_02')
CORNER_RAMP_3X2X1_L: Final = RampBrickMeta('CornerRamp_3x2x1_L')
CORNER_RAMP_3X2X1_R: Final = RampBrickMeta('CornerRamp_3x2x1_R')
CORNER_RAMP_3X3X1: Final = RampBrickMeta('CornerRamp_3x3x1')
CORNER_RAMP_4X3X1_L: Final = RampBrickMeta('CornerRamp_4x3x1_L')
CORNER_RAMP_4X3X1_R: Final = RampBrickMeta('CornerRamp_4x3x1_R')
CORNER_RAMP_4X4X1: Final = RampBrickMeta('CornerRamp_4x4x1')
CORNER_RAMP_5X3X1_L: Final = RampBrickMeta('CornerRamp_5x3x1_L')
CORNER_RAMP_5X3X1_R: Final = RampBrickMeta('CornerRamp_5x3x1_R')
CORNER_RAMPN_2X2X1: Final = RampBrickMeta('CornerRampN_2x2x1')
CORNER_ROUNDED_2X2X1: Final = RampBrickMeta('CornerRounded_2x2x1')
CORNER_ROUNDED_2X2X1_02: Final = RampBrickMeta('CornerRounded_2x2x1_02')

DOUBLE_RAMP_3X1X1: Final = RampBrickMeta('DoubleRamp_3x1x1')
DOUBLE_RAMP_N_3X1X1: Final = RampBrickMeta('DoubleRampN_3x1x1')



class RedirectorBrickMeta(_b.BrickMeta):

    def base_properties(self, *args, **kwargs):
        return _base_properties | {
            _p.B_FLUID_DYNAMIC: False
        }

CORNER_BRICK_1X1X1S_FLAT: Final = RedirectorBrickMeta('CornerBrick_1x1x1s_Flat')



class RotorBladeBrickMeta(_b.BrickMeta):

    def base_properties(self, *args, **kwargs):
        return _base_properties.copy()

BARREL_1SX1SX3 = BarrelBrickMeta('Barrel_1sx1sx3')



class TrussBrickMeta(_b.BrickMeta):

    def base_properties(self, *args, **kwargs):
        return _base_properties | {
            _p.B_FLUID_DYNAMIC: False
        }

CRANE_SUPPORT_6X6X20: Final = TrussBrickMeta('CraneSupport_6x6x20')



class ScalableBrickMeta(_b.BrickMeta):

    def base_properties(self, *args, **kwargs):
        return _base_properties | {
            _p.BRICK_SIZE: _v.Vec3(30, 30, 30),
            _p.CONNECTOR_SPACING: _p.ConnectorSpacing.ALL_CONNECTIONS,
            _p.B_FLUID_DYNAMIC: False
        }

SCALABLE_BRICK: Final = ScalableBrickMeta('ScalableBrick')



class SirenBrickMeta(_b.BrickMeta):

    def base_properties(self, *args, **kwargs):
        return _base_properties | {
            _p.SIREN_TYPE: _p.SirenType.CAR_HORN,
            _p.HORN_PITCH: _p.HornPitch.DEFAULT_VALUE,
            _p.INPUT_CNL_INPUT_AXIS: _p.InputCnl_InputAxis.HORN,
            _p.INPUT_CNL_SOURCE_BRICKS: _p.InputCnl_SourceBricks.EMPTY,
            _p.INPUT_CNL_VALUE: _p.InputCnl_Value.DEFAULT_VALUE
        }

DOUBLE_SIREN_1X2X1S: Final = SirenBrickMeta('DoubleSiren_1x2x1s')

# FIXME: This has BRMK properties missing.
class TextBrickMeta(_b.BrickMeta):

    def base_properties(self, *args, **kwargs):
        return _base_properties | {
            _p.BRICK_SIZE: _v.Vec3(60, 60, 10),
            _p.CONNECTOR_SPACING: _p.ConnectorSpacing.ALL_CONNECTIONS,
            _p.B_FLUID_DYNAMIC: False,
            _p.TEXT: _p.Text.DEFAULT,
            _p.FONT: _p.Font.DEFAULT,
            _p.FONT_SIZE: _p.FontSize.DEFAULT_VALUE,
            _p.TEXT_COLOR: _p.TextColor.DEFAULT_COLOR,
            _p.OUTLINE_THICKNESS: _p.OutlineThickness.DEFAULT_VALUE
        }

TEXT_BRICK: Final = TextBrickMeta('TextBrick')
TEXT_CYLINDER: Final = TextBrickMeta('TextCylinder')

# FIXME: This (probably) has BRMK properties missing.
class SwitchBrickMeta(_b.BrickMeta):

    def base_properties(self, *args, **kwargs):
        return _base_properties | {
            _p.INPUT_CNL_INPUT_AXIS: _p.InputCnl_InputAxis.NONE,
            _p.INPUT_CNL_SOURCE_BRICKS: _p.InputCnl_SourceBricks.EMPTY,
            _p.INPUT_CNL_VALUE: _p.InputCnl_Value.DEFAULT_VALUE,
            _p.SWITCH_NAME: _p.SwitchName.EMPTY,
            _p.BRICK_SIZE: _v.Vec3(10, 10, 10),
            _p.CONNECTOR_SPACING: _p.ConnectorSpacing.NO_TOP,
            _p.B_RETURN_TO_ZERO: True,
            _p.OUTPUT_CNL_MIN_IN: -1.0,
            _p.OUTPUT_CNL_MAX_IN: 1.0,
            _p.OUTPUT_CNL_MIN_OUT: -1.0,
            _p.OUTPUT_CNL_MAX_OUT: 1.0
        }

SWITCH_BRICK: Final = SwitchBrickMeta('SwitchBrick')
# other switches need to be implemented, beware

# FIXME: This (probably) has BRMK properties missing.
class MathBrickMeta(_b.BrickMeta):

    def base_properties(self, *args, **kwargs):
        return _base_properties | {
            _p.BRICK_SIZE: _v.Vec3(10, 10, 10),
            _p.CONNECTOR_SPACING: _p.ConnectorSpacing.ALL_CONNECTIONS,
            _p.OPERATION: _p.Operation.ADD,
            _p.INPUT_CNL_A_INPUT_AXIS: _p.InputCnl_A_InputAxis.NONE,
            _p.INPUT_CNL_A_SOURCE_BRICKS: _p.InputCnl_A_SourceBricks.EMPTY,
            _p.INPUT_CNL_A_VALUE: _p.InputCnl_A_Value.DEFAULT_VALUE,
            _p.INPUT_CNL_B_INPUT_AXIS: _p.InputCnl_B_InputAxis.NONE,
            _p.INPUT_CNL_B_SOURCE_BRICKS: _p.InputCnl_B_SourceBricks.EMPTY,
            _p.INPUT_CNL_B_VALUE: _p.InputCnl_B_Value.DEFAULT_VALUE
        }

MATH_BRICK: Final = MathBrickMeta('MathBrick')

# FIXME: This has BRMK properties missing.
class SensorBrickMeta(_b.BrickMeta):

    def base_properties(self, *args, **kwargs):
        return _base_properties | {
            _p.ENABLED_INPUT_CNL_INPUT_AXIS: _p.EnabledInputCnl_InputAxis.ALWAYS_ON,
            _p.ENABLED_INPUT_CNL_SOURCE_BRICKS: _p.EnabledInputCnl_SourceBricks.EMPTY,
            _p.INPUT_CNL_VALUE: _p.InputCnl_Value.DEFAULT_VALUE,
            _p.BRICK_SIZE: _v.Vec3(10, 10, 10),
            _p.CONNECTOR_SPACING: _p.ConnectorSpacing.NO_TOP,
            _p.B_RETURN_TO_ZERO: False,
            _p.SENSOR_TYPE: _p.SensorType.SPEED,
            _p.OUTPUT_CNL_MIN_IN: -1.0,
            _p.OUTPUT_CNL_MAX_IN: 1.0,
            _p.OUTPUT_CNL_MIN_OUT: -1.0,
            _p.OUTPUT_CNL_MAX_OUT: 1.0
        }

SENSOR_BRICK: Final = SensorBrickMeta('SensorBrick')
# other sensors need to be implemented too
