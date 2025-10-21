# pylint: disable=missing-module-docstring # im just disabling globally at this point. fuck this
import math
import numpy as np

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

def _srgb_transfer(x: float) -> float:
    """8-bit sRGB channel → linear light (0-1)"""
    x = x / 255.0
    return x / 12.92 if x <= 0.04045 else math.pow((x + 0.055) / 1.055, 2.4)

def _gamma_correct(x: float) -> float:
    """linear light (0-1) → 8-bit sRGB channel"""
    x = 12.92 * x if x <= 0.0031308 else 1.055 * math.pow(x, 1.0/2.4) - 0.055
    return max(0.0, min(1.0, x)) * 255.0


M1_XYZ_2_LMS_N = np.array(
    [
        (0.8189330101, 0.3618667424, -0.1288597137),
        (0.0329845436, 0.9293118715,  0.0361456387),
        (0.0482003018, 0.2643662691,  0.6338517070),
    ]
)

M2_LMS_2_LAB_N = np.array(
    [
        (0.2104542553, 0.7936177850, -0.0040720468),
        (1.9779984951, -2.4285922050, 0.4505937099),
        (0.0259040371, 0.7827717662, -0.8086757660),
    ]
)

M1_LMS_2_XYZ_I = np.linalg.inv(M1_XYZ_2_LMS_N)
M2_LAB_2_LMS_I = np.linalg.inv(M2_LMS_2_LAB_N)

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



def srgb_to_oklab(r, g, b):
    """Input: 0-1 floats.  Output: (L, a, b) floats."""

    # linearise
    rl, gl, bl = _srgb_transfer(r*255), _srgb_transfer(g*255), _srgb_transfer(b*255)

    #rl, gl, bl = np.dot(SRGB_TO_CIE_XYZ, np.array([rl, gl, bl])) # ???

    # Applying the linear map which converts the XYZ values into a space analogous to the LMS color space:[b]
    l, m, s = np.dot(M1_XYZ_2_LMS_N, np.array([rl, gl, bl]))
    # Applying a cube root non-linearity:
    ll, mm, ss = l**(1/3), m**(1/3), s**(1/3)

    L, a, b = np.dot(M2_LMS_2_LAB_N, np.array([ll, mm, ss])) # pylint: disable=invalid-name

    return L, a, b

def oklab_to_srgb(L, a, b): # pylint: disable=invalid-name
    """Input: (L,a,b) floats.  Output: (r,g,b) 0-255 integers."""
    # inverse Oklab → LMS
    ll, mm, ss = np.dot(M2_LAB_2_LMS_I, np.array([L, a, b]))

    l, m, s = ll**3, mm**3, ss**3

    # inverse linear map
    rl, gl, bl = np.dot(M1_LMS_2_XYZ_I, np.array([l, m, s]))

    #rl, gl, bl = np.dot(SRGB_FROM_CIE_XYZ, np.array([rl, gl, bl])) # ???????

    # gamma-encode
    r = int(round(_gamma_correct(rl)))
    g = int(round(_gamma_correct(gl)))
    b = int(round(_gamma_correct(bl)))
    return max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b))



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
