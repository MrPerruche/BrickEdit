"""
Minimal 3x3 matrix utilities.

This module intentionally avoids general-purpose linear algebra.
All operations are specialized for 3x3 matrices and 3-element vectors
for performance and simplicity.
"""


TupleVec3 = tuple[float, float, float]
Matrix3 = tuple[TupleVec3, TupleVec3, TupleVec3]


def mul_mat3_vec3(m: Matrix3, v: TupleVec3) -> TupleVec3:
    """Multiply a 3x3 matrix by a 3-element vector.

    Args:
        m (Matrix3): Matrix.
        v (Vector3): Vector.

    Returns:
        Vector3: Resulting vector.
    """
    return (
        m[0][0] * v[0] + m[0][1] * v[1] + m[0][2] * v[2],
        m[1][0] * v[0] + m[1][1] * v[1] + m[1][2] * v[2],
        m[2][0] * v[0] + m[2][1] * v[1] + m[2][2] * v[2],
    )

def det_mat3(m: Matrix3) -> float:
    """Computes the determinant of a 3x3 matrix."""
    return (
        m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
        - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
        + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0])
    )

def inv_mat3(m: Matrix3) -> Matrix3:
    """Computes the inverse of a 3x3 matrix.

    Args:
        m (Matrix3): The matrix to invert.

    Returns:
        Matrix3: The inverted matrix.
    """
    det = det_mat3(m)
    if det == 0.0:
        raise ValueError("Matrix is singular and cannot be inverted")

    inv_det = 1.0 / det

    return (
        (
            (m[1][1] * m[2][2] - m[1][2] * m[2][1]) * inv_det,
            (m[0][2] * m[2][1] - m[0][1] * m[2][2]) * inv_det,
            (m[0][1] * m[1][2] - m[0][2] * m[1][1]) * inv_det,
        ),
        (
            (m[1][2] * m[2][0] - m[1][0] * m[2][2]) * inv_det,
            (m[0][0] * m[2][2] - m[0][2] * m[2][0]) * inv_det,
            (m[0][2] * m[1][0] - m[0][0] * m[1][2]) * inv_det,
        ),
        (
            (m[1][0] * m[2][1] - m[1][1] * m[2][0]) * inv_det,
            (m[0][1] * m[2][0] - m[0][0] * m[2][1]) * inv_det,
            (m[0][0] * m[1][1] - m[0][1] * m[1][0]) * inv_det,
        ),
    )
