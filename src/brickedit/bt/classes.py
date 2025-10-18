from typing import Final
from collections.abc import Hashable

from .. import p as _p
from .. import vec as _v
from . import base as _b


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
            _p.INPUT_CNL_VALUE: _p.InputCnl_Value.DEFAULT_VALUE
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
        return _base_properties.copy()

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


AXLE_1SX1SX1S = AxleBrickMeta('Axle_1sx1sx1s', 1000, 50)
AXLE_1X1X1S = AxleBrickMeta('Axle_1x1x1s', 1000, 50)
AXLE_1X1X1S_02 = AxleBrickMeta('Axle_1x1x1s_02', 1000, 50)
AXLE_1X2X1S = AxleBrickMeta('Axle_1x2x1s', 1000, 50)
AXLE_2X2X1 = AxleBrickMeta('Axle_2x2x1', 5000, 250)
AXLE_2X2X1S = AxleBrickMeta('Axle_2X2X1S', 1000, 50)
AXLE_2X4X1S = AxleBrickMeta('Axle_2x4x1s', 3000, 150)
AXLE_2X6X1S = AxleBrickMeta('Axle_2x6x1s', 4000, 200)



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

AIRCRAFTR4 = MotorBrickMeta('AircraftR4', .5, 3, (1e3, 1e4), (0, .05), (.65, .95), (.1, .3), .85,
                            .5, 2, 1, 1, 5500,  10, 1e-3)
