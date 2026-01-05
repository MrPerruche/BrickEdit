# pylint: disable=missing-module-docstring # im just disabling globally at this point. fuck this
import math
from typing import Final
from . import mat as _mat


# Math / bitwise functions

def cbrt_copysign(x: float) -> float:
    """math.copysign(abs(x) ** (1/3), x)"""
    return math.copysign(abs(x) ** (1/3), x)

def float_to_int(v: float):
    """Converts a float [0, 1] to an int [0, 255] with epsilon for FPA accuracy issues.
    Example: 1 → 255"""
    return int(v * 255 + 1e-10)  # 1e-10 (epsilon) for FPA issues

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

def clamp(v: float, min_val: float, max_val: float) -> float:
    return max(min(v, max_val), min_val)

def multi_clamp(*args: float, min_val: float, max_val: float) -> tuple[float, ...]:
    return tuple(clamp(v, min_val, max_val) for v in args)



# Color space shifting functions

def srgb_to_linear(x: float) -> float:
    """sRGB (0-1) → linear rgb (0-1)"""
    return x / 12.92 if x <= 0.04045 else math.pow((x + 0.055) / 1.055, 2.4)

def multi_srgb_to_linear(*args: float) -> tuple[float, ...]:
    """sRGB (0-1) → linear rgb (0-1)"""
    return (srgb_to_linear(x) for x in args)

def linear_to_srgb(x: float) -> float:
    """linear rgb (0-1) → sRGB (0-1). Clamps to 0-1 if linear rgb out of range."""
    if x <= 0.0:
        return 0.0
    if x >= 1.0:
        return 1.0
    return (
        12.92 * x
        if x <= 0.0031308
        else 1.055 * math.pow(x, 1.0 / 2.4) - 0.055
    )

def multi_linear_to_srgb(*args: float) -> tuple[float, ...]:
    """linear rgb (0-1) → sRGB (0-1)"""
    return (linear_to_srgb(x) for x in args)


# HSV Color Space

def hsv_to_rgb(h: float, s: float, v: float) -> tuple[float, float, float]:
    """Convert HSV colors into RGB.

    Args:
        h (float): The hue component of the color.
        s (float): The saturation component of the color.
        v (float): The value component of the color.

    Returns:
        tuple[float, float, float]: The RGB components of the color.
    """

    c = v * s
    h_prime = h / 60
    x = c * (1 - abs((h_prime % 2) - 1))
    m = v - c

    r, g, b = 0, 0, 0

    if 0 <= h_prime < 1:
        r, g, b = c, x, 0

    elif 1 <= h_prime < 2:
        r, g, b = x, c, 0

    elif 2 <= h_prime < 3:
        r, g, b = 0, c, x

    elif 3 <= h_prime < 4:
        r, g, b = 0, x, c

    elif 4 <= h_prime < 5:
        r, g, b = x, 0, c

    elif 5 <= h_prime < 6:
        r, g, b = c, 0, x

    return r+m, g+m, b+m


def rgb_to_hsv(r: float, g: float, b: float) -> tuple[float, float, float]:
    """Convert RGB colors into HSV.

    Args:
        r (float): The red component of the color.
        g (float): The green component of the color.
        b (float): The blue component of the color.

    Returns:
        tuple[float, float, float]: The HSV components of the color.
    """

    cmax = max(r, g, b)
    cmin = min(r, g, b)
    diff = cmax - cmin

    h = 0
    if diff == 0:
        h = 0
    elif cmax == r:
        h = 60 * (((g - b) / diff) % 6)
    elif cmax == g:
        h = 60 * (((b - r) / diff) + 2)
    elif cmax == b:
        h = 60 * (((r - g) / diff) + 4)

    if cmax == 0:
        s = 0
    else:
        s = diff / cmax

    v = cmax

    return h, s, v



# OKLAB and OKLCH Color Space

M1_XYZ_2_LMS_N: Final[_mat.Matrix3] = (
    (0.8189330101, 0.3618667424, -0.1288597137),
    (0.0329845436, 0.9293118715,  0.0361456387),
    (0.0482003018, 0.2643662691,  0.6338517070),
)

M2_LMS_2_LAB_N: Final[_mat.Matrix3] = (
    (0.2104542553, 0.7936177850, -0.0040720468),
    (1.9779984951, -2.4285922050, 0.4505937099),
    (0.0259040371, 0.7827717662, -0.8086757660),
)

M1_LMS_2_XYZ_I = _mat.inv_mat3(M1_XYZ_2_LMS_N)
M2_LAB_2_LMS_I = _mat.inv_mat3(M2_LMS_2_LAB_N)

def oklab_to_oklch(L: float, a: float, b: float) -> tuple[float, float, float]: # pylint: disable=invalid-name
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

def oklch_to_oklab(L: float, C: float, h: float) -> tuple[float, float, float]: # pylint: disable=invalid-name
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



def srgb_to_oklab(r: float, g: float, b: float):
    """Converts sRGB (0-1) to OKLAB."""
    return linear_to_oklab(srgb_to_linear(r), srgb_to_linear(g), srgb_to_linear(b))


def linear_to_oklab(r: float, g: float, b: float):
    """Convert linear RGB (0–1) to OKLAB."""

        # linear RGB → LMS (via XYZ baked into matrix)
    l, m, s = _mat.mul_mat3_vec3(M1_XYZ_2_LMS_N, (r, g, b))

    # nonlinearity
    ll = cbrt_copysign(l)
    mm = cbrt_copysign(m)
    ss = cbrt_copysign(s)

    return _mat.mul_mat3_vec3(M2_LMS_2_LAB_N, (ll, mm, ss))



def oklab_to_linear(L: float, a: float, b: float): # pylint: disable=invalid-name
    """Convert OKLAB to linear rgb (unbounded float)."""
    ll, mm, ss = _mat.mul_mat3_vec3(M2_LAB_2_LMS_I, (L, a, b))

    l = ll * ll * ll
    m = mm * mm * mm
    s = ss * ss * ss

    rl, gl, bl = _mat.mul_mat3_vec3(M1_LMS_2_XYZ_I, (l, m, s))

    return rl, gl, bl

def oklab_to_srgb(L: float, a: float, b: float): # pylint: disable=invalid-name
    """Convert OKLAB to sRGB (0-1)."""
    rl, gl, bl = oklab_to_linear(L, a, b)
    return linear_to_srgb(rl), linear_to_srgb(gl), linear_to_srgb(bl)



# CMYK Color space

def rgb_to_cmyk(r: int, g: int, b: int) -> tuple[float, float, float, float]:
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

def cmyk_to_rgb(c: float, m: float, y: float, k: float) -> tuple[float, float, float]:
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
