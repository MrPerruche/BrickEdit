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

        r, g, b = self.linear_srgb_to_rgb(*self.oklab_to_linear_srgb(l, a, b))
        return r << 24 | b << 16 | g << 8 | 0xFF



    def oklab_to_linear_srgb(self, L: float, a: float, b: float) -> tuple[int, int, int]: # pylint: disable=invalid-name
        """Convert OKLAB colors into linear sRGB.

        Args:
            l (float): The lightness component of the color.
            a (float): The green-red component of the color.
            b (float): The blue-yellow component of the color.

        Returns:
            tuple[int, int, int]: The linear sRGB components of the color.
        """

        l_ = L + 0.3963377774 * a + 0.2158037573 * b
        m_ = L - 0.1055613458 * a - 0.0638541728 * b
        s_ = L - 0.0894841775 * a - 1.2914855480 * b
        l = l_ ** 3
        m = m_ ** 3
        s = s_ ** 3
        r = +4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s
        g = -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s
        b = -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s
        return r, g, b

    def oklch_to_oklab(self, L: float, C: float, h: float) -> tuple[float, float, float]: # pylint: disable=invalid-name
        """Convert OKLCH colors into OKLAB.

        Args:
            L (float): The lightness component of the color.
            C (float): The chroma component of the color.
            h (float): The hue component of the color.

        Returns:
            tuple[float, float, float]: The OKLAB components of the color.
        """
        a = math.cos(math.radians(h)) * C
        b = math.sin(math.radians(h)) * C
        return L, a, b

    def linear_srgb_to_rgb(self, r: int, g: int, b: int) -> tuple[int, int, int]: # pylint: disable=invalid-name
        """Convert linear sRGB colors into RGB.

        Args:
            r (int): The red component of the color.
            g (int): The green component of the color.
            b (int): The blue component of the color.

        Returns:
            tuple[int, int, int]: The RGB components of the color.
        """
        def _lin_to_rgb(v: float) -> float:
            # Clamp first – linear values can slightly exceed [0,1]
            v = max(0.0, min(1.0, v))
            return 12.92 * v if v <= 0.0031308 else 1.055 * (v ** (1.0 / 2.4)) - 0.055

        return int(_lin_to_rgb(r/255)*255), int(_lin_to_rgb(g/255)*255), int(_lin_to_rgb(b/255)*255)


    def oklch(self, L: float, C: float, h: float) -> int: # pylint: disable=invalid-name
        """Convert OKLCH colors into RGBA.

        Args:
            L (float): The lightness component of the color.
            C (float): The chroma component of the color.
            h (float): The hue component of the color.

        Returns:
            int: The RGBA value, as a hexadecimal integer.
        """
        return self.oklab(*self.oklch_to_oklab(L, C, h))

    def linear_srgb_to_oklab(self, r, g, b) -> tuple[float, float, float]:
        """Convert linear sRGB colors into OKLAB.

        Args:
            r (int): The red component of the color.
            g (int): The green component of the color.
            b (int): The blue component of the color.

        Returns:
            tuple[float, float, float]: The OKLAB components of the color.
        """
        # linear sRGB → OKLab
        l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
        m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
        s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b

        l_ = l ** (1 / 3)
        m_ = m ** (1 / 3)
        s_ = s ** (1 / 3)

        L = 0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_ # pylint: disable=invalid-name
        a = 1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_
        b = 0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_

        return L, a, b

    def oklab_to_oklch(self, L: float, a: float, b: float) -> tuple[float, float, float]: # pylint: disable=invalid-name
        """Convert OKLAB colors into OKLCH.

        Args:
            L (float): The lightness component of the color.
            a (float): The green-red component of the color.
            b (float): The blue-yellow component of the color.

        Returns:
            tuple[float, float, float]: The OKLCH components of the color.
        """
        C = math.sqrt(a * a + b * b) # pylint: disable=invalid-name
        h = math.degrees(math.atan2(b, a)) % 360
        return L, C, h

    def srgb_to_linear_channel(self, c):
        """Convert a single sRGB channel into linear light."""
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

    def srgb_to_linear(self, rgb):
        """Convert sRGB colors into linear light."""
        return tuple(self.srgb_to_linear_channel(c) for c in rgb)

    def rgb_to_cmyk(self, r: int, g: int, b: int) -> tuple[float, float, float, float]:
        """Convert RGB colors into CMYK.

        Args:
            r (int): The red component of the color.
            g (int): The green component of the color.
            b (int): The blue component of the color.

        Returns:
            tuple[float]: The CMYK components of the color.
        """
        rn = r / 255
        gn = g / 255
        bn = b / 255

        k = 1 - max(rn, gn, bn)

        if k == 1:
            return 0, 0, 0, 1

        c = (1 - rn - k) / (1 - k)
        m = (1 - gn - k) / (1 - k)
        y = (1 - bn - k) / (1 - k)

        return c, m, y, k

    def cmyk_to_rgb(self, c: float, m: float, y: float, k: float) -> tuple[float, float, float]:
        """Convert CMYK colors into RGB.

        Args:
            c (float): The cyan component of the color.
            m (float): The magenta component of the color.
            y (float): The yellow component of the color.
            k (float): The black component of the color.

        Returns:
            tuple[float, float, float]: The RGB components of the color.
        """
        c = max(0.0, min(1.0, c))
        m = max(0.0, min(1.0, m))
        y = max(0.0, min(1.0, y))
        k = max(0.0, min(1.0, k))

        rn = (1 - c) * (1 - k)
        gn = (1 - m) * (1 - k)
        bn = (1 - y) * (1 - k)

        return int(rn*255), int(gn*255), int(bn*255)

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
        r, g, b = self.cmyk_to_rgb(c, m, y, k)
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
