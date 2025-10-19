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
