"""Units for the value helper."""
from typing import Final
from math import pi as _pi

# Multipliers (SI)
QUETTA: Final[float] = 1e30
RONNA: Final[float] = 1e27
YOTTA: Final[float] = 1e24
ZETTA: Final[float] = 1e21
EXA: Final[float] = 1e18
PETA: Final[float] = 1e15
TERA: Final[float] = 1e12
GIGA: Final[float] = 1e9
MEGA: Final[float] = 1e6
KILO: Final[float] = 1e3
HECTO: Final[float] = 1e2
DECA: Final[float] = 1e1
DECI: Final[float] = 1e-1
CENTI: Final[float] = 1e-2
MILLI: Final[float] = 1e-3
MICRO: Final[float] = 1e-6
NANO: Final[float] = 1e-9
PICO: Final[float] = 1e-12
FEMTO: Final[float] = 1e-15
ATTO: Final[float] = 1e-18
ZEPTO: Final[float] = 1e-21
YOCTO: Final[float] = 1e-24
RONTO: Final[float] = 1e-27
QUECTO: Final[float] = 1e-30

# Default positional unit is in CENTIMETERS
KILOMETER: Final[float] = 100_000.0
METER: Final[float] = 100.0
DECIMETER: Final[float] = 10.0
CENTIMETER: Final[float] = 1.0
MILLIMETER: Final[float] = 0.1
KM, M, CM, MM = KILOMETER, METER, CENTIMETER, MILLIMETER

INCH: Final[float] = 2.54
FOOT: Final[float] = INCH * 12
YARD: Final[float] = FOOT * 3
MILE: Final[float] = YARD * 1760
IN, FT, YD, MI = INCH, FOOT, YARD, MILE

# Default rotational unit is in DEGREES
DEGREE: Final[float] = 1.0
RADIAN: Final[float] = 180 / _pi
DEG, RAD = DEGREE, RADIAN

# Default force unit is in NEWTONS
NEWTON: Final[float] = 1.0
KILO_NEWTON: Final[float] = 1e3
MEGA_NEWTON: Final[float] = 1e6
