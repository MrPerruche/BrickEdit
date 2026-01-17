from typing import Self
from math import sqrt
from dataclasses import dataclass
from abc import ABC, abstractmethod


class Vec(ABC):

    """Abstract base class for vector types."""


    @abstractmethod
    def as_tuple(self) -> tuple[float, ...]:
        """Convert the vector to a tuple of floats.
        Returns:
            tuple[float, ...]: The vector as a tuple of floats."""

    def magnitude(self) -> float:
        """Calculate the magnitude (length) of the vector.
        Uses a slower, general implementation for vectors of any dimension provided in class Vec.
        
        Returns:
            float: The magnitude of the vector.
        """
        return sqrt(sum((n ** 2 for n in self.as_tuple())))

    def normalize(self) -> Self:
        """Normalize the vector to have a magnitude of 1.
        Uses a slower, general implementation for vectors of any dimension provided in class Vec.

        Returns:
            Self: A new vector with the same direction but a magnitude of 1.
        """
        mag = self.magnitude()
        if mag == 0:
            return self.__class__(*(0 for _ in range(len(self))))
        return self.__class__(*(n / mag for n in self.as_tuple()))

    @abstractmethod
    def __len__(self) -> int:
        """Number of dimensions in the vector."""

    def __add__(self, other) -> Self:
        """Add two vectors.
        Uses a slower, general implementation for vectors of any dimension provided in class Vec."""
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.__class__(*(a + b for (a, b) in zip(self.as_tuple(), other.as_tuple())))

    def __sub__(self, other) -> Self:
        """Subtract two vectors.
        Uses a slower, general implementation for vectors of any dimension provided in class Vec."""
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.__class__(*(a - b for (a, b) in zip(self.as_tuple(), other.as_tuple())))

    def __mul__(self, other: float) -> Self:
        """Multiply vector by a scalar.
        Uses a slower, general implementation for vectors of any dimension provided in class Vec."""
        return self.__class__(*(a * other for a in self.as_tuple()))

    def __rmul__(self, other: float) -> Self:
        """Right multiplication to support scalar * vector."""
        return self.__mul__(other)

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({", ".join(str(n) for n in self.as_tuple())})'



@dataclass(frozen=True, slots=True)
class Vec2(Vec):

    """
    A 2D vector class with basic operations.
    Used to store scales, etc.
    
    Attributes:
        x (float): The x component of the vector.
        y (float): The y component of the vector.
    """

    x: float
    y: float

    def as_tuple(self) -> tuple[float, float]:
        return (self.x, self.y)

    def magnitude(self) -> float:
        """
        Calculate the magnitude (length) of the vector.

        Returns:
            float: The magnitude of the vector.
        """
        return sqrt(self.x**2 + self.y**2)

    def normalize(self) -> Self:
        """
        Normalize the vector to have a magnitude of 1.

        Returns:
            Self: A new vector with the same direction but a magnitude of 1.
        """
        mag = self.magnitude()
        if mag == 0:
            return self.__class__(0, 0)
        return self.__class__(self.x / mag, self.y / mag)

    def __len__(self):
        return 2

    def __add__(self, other: Self) -> Self:
        """Add two vectors."""
        return self.__class__(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Self) -> Self:
        """Subtract two vectors."""
        return self.__class__(self.x - other.x, self.y - other.y)

    def __mul__(self, other: float) -> Self:
        """Multiply vector by a scalar."""
        return self.__class__(self.x * other, self.y * other)

    def __rmul__(self, other: float) -> Self:
        return self.__mul__(other)


@dataclass(frozen=True, slots=True)
class Vec3(Vec):

    """
    A 3D vector class with basic operations.
    Used to store coordinates, scales, colors, etc.
    
    Attributes:
        x (float): The x component of the vector.
        y (float): The y component of the vector.
        z (float): The z component of the vector.
    """

    x: float
    y: float
    z: float

    def as_tuple(self) -> tuple[float, float, float]:
        return (self.x, self.y, self.z)

    def magnitude(self) -> float:
        """
        Calculate the magnitude (length) of the vector.

        Returns:
            float: The magnitude of the vector.
        """
        return sqrt(self.x**2 + self.y**2 + self.z**2)

    def normalize(self) -> Self:
        """
        Normalize the vector to have a magnitude of 1.

        Returns:
            Self: A new vector with the same direction but a magnitude of 1.
        """
        mag = self.magnitude()
        if mag == 0:
            return self.__class__(0, 0, 0)
        return self.__class__(self.x / mag, self.y / mag, self.z / mag)

    def __len__(self):
        return 3

    def __add__(self, other: Self) -> Self:
        """Add two vectors."""
        return self.__class__(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: Self) -> Self:
        """Subtract two vectors."""
        return self.__class__(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other: float) -> Self:
        """Multiply vector by a scalar."""
        return self.__class__(self.x * other, self.y * other, self.z * other)

    def __rmul__(self, other: float) -> Self:
        return self.__mul__(other)



@dataclass(frozen=True, slots=True)
class Vec4(Vec):

    """
    A 4D vector class with basic operations.
    Used to store colors, etc.

    Attributes:
        x (float): The x component of the vector.
        y (float): The y component of the vector.
        z (float): The z component of the vector.
        w (float): The w component of the vector.
    """

    x: float
    y: float
    z: float
    w: float

    def as_tuple(self) -> tuple[float, float, float, float]:
        return (self.x, self.y, self.z, self.w)

    def magnitude(self) -> float:
        """
        Calculate the magnitude (length) of the vector.

        Returns:
            float: The magnitude of the vector.
        """
        return sqrt(self.x**2 + self.y**2 + self.z**2 + self.w**2)

    def normalize(self) -> Self:
        """
        Normalize the vector to have a magnitude of 1.

        Returns:
            Self: A new vector with the same direction but a magnitude of 1.
        """
        mag = self.magnitude()
        if mag == 0:
            return self.__class__(0, 0, 0, 0)
        return self.__class__(self.x / mag, self.y / mag, self.z / mag, self.w / mag)

    def __len__(self):
        return 4

    def __add__(self, other: Self) -> Self:
        """Add two vectors."""
        return self.__class__(self.x + other.x, self.y + other.y, self.z + other.z, self.w + other.w)

    def __sub__(self, other: Self) -> Self:
        """Subtract two vectors."""
        return self.__class__(self.x - other.x, self.y - other.y, self.z - other.z, self.w - other.w)

    def __mul__(self, other: float) -> Self:
        """Multiply vector by a scalar."""
        return self.__class__(self.x * other, self.y * other, self.z * other, self.w * other)

    def __rmul__(self, other: float) -> Self:
        return self.__mul__(other)
