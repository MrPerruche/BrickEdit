"""Value helper."""

import math
from .units import *
from . import color as _col
from .. import vec as _vec
from .. import var as _var


_INV_255: Final[float] = 1.0/255.0

def float_to_int(v: float):
    """Converts a float [0, 1] to an int [0, 255] with epsilon for FPA accuracy issues.
    Example: 1 → 255"""
    return int(v * 255 + 1e-10)  # 1e-10 for FPA issu

def pack(*args):
    """Pack 8-bit integers into a single integer.
    Example: pack(1, 2, 3) -> 0x010203"""
    shift_offset = len(args) - 1
    packed = 0
    for i, v in enumerate(args):
        packed |= v << ((shift_offset - i) * 8)
    return packed

def pack_float_to_int(*args):
    """Pack floats converted to 8-bit integers with float_to_int into a single integer
    Example; pack_float_to_int(0, 0.5, 1) -> 0x007fff"""
    shift_offset = len(args) - 1
    packed = 0
    for i, v in enumerate(args):
        packed |= int(v * 255 + 1e-10) << ((shift_offset - i) * 8)
    return packed


class ValueHelper:
    """A helper for converting values between different units."""
    def __init__(self, version: int,
                 default_physical_unit=METER,
                 default_rotational_unit=DEGREE,
                 default_force_unit=NEWTON):
        self.version = version
        self.default_physical_unit = default_physical_unit
        self.default_rotational_unit = default_rotational_unit
        self.default_force_unit = default_force_unit


    def pos(self, x: float, y: float, z: float, unit=None) -> _vec.Vec3:
        """A helper method for physical positioning.

        Args:
            x (float): The x component of the vector.
            y (float): The y component of the vector.
            z (float): The z component of the vector.
            unit (int, optional): The unit of the vector.

        Returns:
            Vec3: 3D vector of the physical position, in the desired unit
        """

        if unit is None:
            unit = self.default_physical_unit

        # Pos was expressed in centimeters before update; no change

        return _vec.Vec3(x * unit, y * unit, z * unit)

    def pos_vec(self, v: _vec.Vec3, unit=None) -> _vec.Vec3:
        """Alias for ValueHelper.pos() for Vec3 objects."""
        return self.pos(v.x, v.y, v.z, unit)



    def rot(self, x: float, y: float, z: float, unit=None) -> _vec.Vec3:
        """A helper method for rotational positioning.

        Args:
            x (float): The x component of the vector.
            y (float): The y component of the vector.
            z (float): The z component of the vector.
            unit (int, optional): The unit of the vector if different from the instance.

        Returns:
            Vec3: A 3D vector representing the rotational position.
        """

        if unit is None:
            unit = self.default_rotational_unit

        return _vec.Vec3(x * unit, y * unit, z * unit)

    def rot_vec(self, v: _vec.Vec3, unit=None) -> _vec.Vec3:
        """Alias for ValueHelper.pos() for Vec3 objects."""
        return self.rot(v.x, v.y, v.z, unit)



    def brick_size(self, x: float, y: float, z: float, unit=None) -> _vec.Vec3:
        """A helper method for physical scale.

        Args:
            x (float): The x component of the vector.
            y (float): The y component of the vector.
            z (float): The z component of the vector.
            unit (int, optional): The unit of the vector if different from the instance.

        Returns:
            Vec3: A 3D vector representing the physical scale.
        """

        if unit is None:
            unit = self.default_physical_unit

        if self.version < _var.FILE_UNIT_UPDATE:
            unit *= DECI  # CENTI = 1, division is useless

        return _vec.Vec3(x * unit, y * unit, z * unit)

    def brick_size_vec(self, vec: _vec.Vec3, unit=None) -> _vec.Vec3:
        """Alias for ValueHelper.brick_size() for Vec3 objects."""
        return self.brick_size(vec.x, vec.y, vec.z, unit)



    def p_rgba(self, rgba: int) -> int:
        """Converts a packed RGBA value into Brick Rigs' format"""
        if self.version >= _var.FILE_UNIT_UPDATE:
            return rgba
        r = (rgba >> 24) & 0xff
        g = (rgba >> 16) & 0xff
        b = (rgba >> 8)  & 0xff
        a = rgba         & 0xff
        h, s, v = _col.rgb_to_hsv(r * _INV_255, g * _INV_255, b * _INV_255)
        return pack_float_to_int(h, s, v, a)


    def rgba(self, r: int, g: int, b: int, a: int = 0xFF) -> int:
        """Convert an RGBA value to Brick Rigs' format"""
        if self.version >= _var.FILE_UNIT_UPDATE:
            return pack(r, g, b, a)
        h, s, v = _col.rgb_to_hsv(r * _INV_255, g * _INV_255, b * _INV_255)
        return pack_float_to_int(h, s, v, a)



    def p_rgb(self, rgb: int) -> int:
        """Converts a packed RGB value into Brick Rigs' format"""
        if self.version >= _var.FILE_UNIT_UPDATE:
            return rgb
        r = (rgb >> 16) & 0xff
        g = (rgb >> 8)  & 0xff
        b = rgb         & 0xff
        h, s, v = _col.rgb_to_hsv(r * _INV_255, g * _INV_255, b * _INV_255)
        return pack_float_to_int(h, s, v)

    def rgb(self, r: int, g: int, b: int) -> int:
        """Convert an RGB value to Brick Rigs' format"""
        if self.version >= _var.FILE_UNIT_UPDATE:
            return pack(r, g, b)
        h, s, v = _col.rgb_to_hsv(r * _INV_255, g * _INV_255, b * _INV_255)
        return pack_float_to_int(h, s, v)



    def hsva(self, h: float, s: float, v: float, a: float = 1.0) -> int:
        """Convert an HSVA value to Brick Rigs' format"""
        if self.version >= _var.FILE_UNIT_UPDATE:
            r, g, b = _col.hsv_to_rgb(h, s, v)
            return pack_float_to_int(r, g, b, a)
        return pack_float_to_int(h, s, v, a)



    def hsv(self, h: float, s: float, v: float) -> int:
        """Convert an HSV value to Brick Rigs' format"""
        if self.version >= _var.FILE_UNIT_UPDATE:
            r, g, b = _col.hsv_to_rgb(h, s, v)
            return pack_float_to_int(r, g, b)
        return pack_float_to_int(h, s, v)



    def oklab(self, l: float, a: float, b: float) -> int:
        """Convert OKLAB colors into RGBA.

        Args:
            l (float): The lightness component of the color.
            a (float): The green-red component of the color.
            b (float): The blue-yellow component of the color.

        Returns:
            int: The RGBA value, as a hexadecimal integer.
        """

        r, g, b = _col.oklab_to_srgb(l, a, b)
        return r << 24 | b << 16 | g << 8 | 0xFF

    def oklch(self, L: float, C: float, h: float) -> int: # pylint: disable=invalid-name
        """Convert OKLCH colors into RGBA.

        Args:
            L (float): The lightness component of the color.
            C (float): The chroma component of the color.
            h (float): The hue component of the color.

        Returns:
            int: The RGBA value, as a hexadecimal integer.
        """
        return self.oklab(*_col.oklch_to_oklab(L, C, h))

    def cmyk(self, c: float, y: float, m: float, k: float) -> int:
        """Convert CMYK colors into RGBA.

        Args:
            c (float): The cyan component of the color.
            y (float): The yellow component of the color.
            m (float): The magenta component of the color.
            k (float): The black component of the color.

        Returns:
            int: The RGBA value, as a hexadecimal integer.
        """
        r, g, b = _col.cmyk_to_rgb(c, m, y, k)
        return r << 24 | g << 16 | b << 8 | 0xFF

    def force(self, value: float, unit=None) -> float:
        """A helper method for physical force units.

        Args:
            value (float): The force value.
            unit (int, optional): The unit of the value. Defaults to None, for the default force unit of this instance.

        Returns:
            float: The force value, taking into account the desired force unit.
        """

        if unit is None:
            unit = self.default_physical_unit

        return value * unit
