from collections.abc import Hashable

from .. import p as _p
from . import base as _b
from . import inner_properties as _ip


_base_properties: dict[str, Hashable] = {
    _p.BRICK_COLOR: _p.BrickColor.DEFAULT_COLOR,
    _p.BRICK_PATTERN: _p.BrickPattern.NONE,
    _p.BRICK_MATERIAL: _p.BrickMaterial.PLASTIC
}


class BaseGunBrickMeta(_b.BrickMeta):

    def __init__(
        self,
        name: str,
        firearm_properties: _ip.FirearmProperties,
        reload_time: float,
        recoil_impulse: float,
        max_barrel_length: float,
        min_spread_radius_scale: float,
        min_muzzle_velocity_scale: float,
        min_damage_scale: float,
        *args, **kwargs
    ):
        super().__init__(name, *args, **kwargs)
        self._firearm_properties = firearm_properties
        self._reload_time = reload_time
        self._recoil_impulse = recoil_impulse
        self._max_barrel_length = max_barrel_length
        self._min_spread_radius_scale = min_spread_radius_scale
        self._min_muzzle_velocity_scale = min_muzzle_velocity_scale
        self._min_damage_scale = min_damage_scale

    def firearm_properties(self) -> _ip.FirearmProperties:
        """Firearm properties"""
        return self._firearm_properties

    def reload_time(self):
        """How long it takes to reload the gun"""
        return self._reload_time

    def recoil_impulse(self):
        """Impulse to add to the gun for every shot"""
        return self._recoil_impulse

    def max_barrel_length(self):
        """Max length at which barrels have an impact"""
        return self._max_barrel_length

    def min_spread_radius_scale(self):
        """Spread factor applied at the maximum barrel length, interpolated between"""
        return self._min_spread_radius_scale

    def min_muzzle_velocity_scale(self):
        """Projectile speed factor applied at the minimum barrel length,
        interpolated up to the max barrel length"""
        return self._min_muzzle_velocity_scale

    def min_damage_scale(self):
        """Projectile damage factor applied at the minimum barrel length,
        interpolated up to the max barrel length"""
        return self._min_damage_scale

    def base_properties(self, *args, **kwargs):
        ammo_type = kwargs.get('at')
        assert ammo_type is not None, f"Missing parameter ammo_type (at) for brick {self._name}"
        return _base_properties | {
            _p.INPUT_CNL_INPUT_AXIS: _p.InputCnl_InputAxis.FIRE_ACTION_1,
            _p.INPUT_CNL_SOURCE_BRICKS: _p.InputCnl_SourceBricks.EMPTY,
            _p.INPUT_CNL_VALUE: _p.InputCnl_Value.DEFAULT_VALUE,
            _p.AMMO_TYPE: _p.AmmoType.DEFAULT
        }
