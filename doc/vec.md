# `brickedit`: Vectors

## Structure as a graph

```mermaid

flowchart TB

    ACLS_VEC["class Vec(ABC)"]

    CLS_VEC2["class Vec2"]
    CLS_VEC3["class Vec3"]
    CLS_VEC4["class Vec4"]

    ACLS_VEC --> CLS_VEC2 & CLS_VEC3 & CLS_VEC4

```

-----

This module contains vector-related classes used throughout brickedit.

## Base vector: `Vec(ABC)`

`Vec` is the abstract base class for all vector types in brickedit. It defines common methods and properties that all vector types must implement, such as addition, subtraction, scalar multiplication, and dot product.

It features generic implementations for most methods. These generic implementations are slower, and should be replaced by more efficient ones in subclasses when possible.

You must define the following abstract methods in subclasses:

- `@abstractmethod as_tuple(self) -> tuple[float, ...]`: Converts the vector to a tuple of floats.
- `@abstractmethod __len__(self) -> int`: Returns the number of dimensions in the vector.

You should also override the following methods in subclasses for better performance:
- `magnitude(self) -> float`: Calculates the magnitude (length) of the vector.
- `normalize(self) -> Self`: Normalizes the vector to have a magnitude of 1.
- `__add__(self, other) -> Self`: Adds two vectors.
- `__sub__(self, other) -> Self`: Subtracts two vectors.
- `__mul__(self, other: float) -> Self`: Multiplies the vector by a scalar.
- `__repr__(self) -> str`: Returns a string representation of the vector.

Vectors also contains the following methods of which their generic implementation already are fast enough and do not need to be overridden:
- `__rmul__(self, other: float) -> Self`: Right multiplication to support scalar * vector.


## Available vector types

BrickEdit implements 3 vectors: `Vec2`, `Vec3` and `Vec4`, representing 2D, 3D and 4D vectors respectively. Each of these classes inherit from the `Vec` base class and implement the required abstract methods as well as overriding the necessary methods for better performance. The attributes are named `x`, `y`, `z` and `w` respectively for each dimension.
