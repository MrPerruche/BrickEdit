"""Value helper."""

from typing import Final

from . import units as _u
from . import color as _col
from . import time as _time
from .. import vec as _vec
from .. import var as _var


_INV_255: Final[float] = 1.0/255.0


class ValueHelper:
    """A helper for converting values between different units."""
    def __init__(self, version: int,
                 default_physical_unit=_u.METER,
                 default_rotational_unit=_u.DEGREE,
                 default_force_unit=_u.NEWTON):
        self.version = version
        self.default_physical_unit = default_physical_unit
        self.default_rotational_unit = default_rotational_unit
        self.default_force_unit = default_force_unit


    def current_time(self):
        """Returns time formatted for metadata folders"""
        return _time.net_ticks_now()

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
            unit *= _u.DECI  # CENTI = 1, division is useless

        return _vec.Vec3(x * unit, y * unit, z * unit)

    def brick_size_vec(self, vec: _vec.Vec3, unit=None) -> _vec.Vec3:
        """Alias for ValueHelper.brick_size() for Vec3 objects."""
        return self.brick_size(vec.x, vec.y, vec.z, unit)



    def p_rgba(self, rgba: int) -> int:
        """Converts a packed RGBA value into Brick Rigs' format
        
        Args:
            rgba (int): The packed RGBA value
            to_srgb (bool, optional): Convert to sRGB first
        """
        # Unpack
        r = ((rgba >> 24) & 0xff) * _INV_255
        g = ((rgba >> 16) & 0xff) * _INV_255
        b = ((rgba >> 8)  & 0xff) * _INV_255
        a = (rgba         & 0xff) * _INV_255
        return self.rgba(r, g, b, a)


    def rgba(self, r: int, g: int, b: int, a: int = 0xFF) -> int:
        """Convert an RGBA value to Brick Rigs' format"""
        # To HSV / RGB depending on update
        if self.version >= _var.FILE_UNIT_UPDATE:
            return _col.pack_float_to_int(r, g, b, a)
        else:
            h, s, v = _col.rgb_to_hsv(r, g, b)
            return _col.pack_float_to_int(h, s, v, a)



    def hsva(self, h: float, s: float, v: float, a: float = 1.0) -> int:
        """Convert an HSVA value to Brick Rigs' format"""
        # Keep check in memory
        is_post_file_unit_update = self.version >= _var.FILE_UNIT_UPDATE

        # Do we have to go through RGB?
        if is_post_file_unit_update:
            r, g, b = _col.hsv_to_rgb(h, s, v)
            # Pack RGB
            return _col.pack_float_to_int(r, g, b, a)

        # Pack HSV
        return _col.pack_float_to_int(h, s, v, a)



    def oklab(self, l: float, a: float, b: float, alpha: float = 1.0) -> int:
        """Convert OKLAB colors into RGBA.

        Args:
            l (float): The lightness component of the color.
            a (float): The green-red component of the color.
            b (float): The blue-yellow component of the color.

        Returns:
            int: The RGBA value, as a hexadecimal integer.
        """

        # sRGB or linear RGB?
        r, g, b = _col.oklab_to_linear(l, a, b)
        # HSV/RGB depending on version
        if self.version >= _var.FILE_UNIT_UPDATE:
            return _col.pack_float_to_int(*_col.multi_clamp(r, g, b, min_val=0, max_val=1), alpha)
        else:
            h, s, v = _col.rgb_to_hsv(r, g, b)
            return _col.pack_float_to_int(_col.clamp(h, 0, 360), *_col.multi_clamp(s, v, min_val=0, max_val=1), alpha)

    def oklch(self, L: float, C: float, h: float, alpha: float = 1.0) -> int: # pylint: disable=invalid-name
        """Convert OKLCH colors into RGBA.

        Args:
            L (float): The lightness component of the color.
            C (float): The chroma component of the color.
            h (float): The hue component of the color.

        Returns:
            int: The RGBA value, as a hexadecimal integer.
        """
        r, g, b = _col.oklch_to_linear_fitted(L, C, h)

        return _col.pack_float_to_int(
            *_col.multi_clamp(r, g, b, min_val=0, max_val=1),
            alpha
        )

    def cmyk(self, c: float, y: float, m: float, k: float, a: float = 1.0) -> int:
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
        if self.version >= _var.FILE_UNIT_UPDATE:
            return _col.pack_float_to_int(r, g, b, a)
        else:
            h, s, v = _col.rgb_to_hsv(r, g, b)
            return _col.pack_float_to_int(h, s, v, a)

    def force(self, value: float, unit=None) -> float:
        """A helper method for physical force units.

        Args:
            value (float): The force value.
            unit (int, optional): The unit of the value. Defaults to None, for the default force
                unit of this instance.

        Returns:
            float: The force value, taking into account the desired force unit.
        """

        if unit is None:
            unit = self.default_physical_unit

        return value * unit
