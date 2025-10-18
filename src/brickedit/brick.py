from copy import deepcopy
from typing import Optional, Self, Callable, Hashable

from . import bt
from .exceptions import BrickError
from .vec import Vec3, Vec4


class Brick:

    __slots__ = ('_meta', 'ref', 'pos', 'rot', 'ppatch')

    def __init__(self,
                 ref: str,
                 meta: bt.BrickMeta,
                 pos: Optional[Vec3] = None,
                 rot: Optional[Vec3] = None,
                 ppatch: Optional[dict[str, Hashable]] = None
                 ):
        self.ref = ref
        self._meta = meta
        self.pos = pos if pos is not None else Vec3(0, 0, 0)
        self.rot = rot if rot is not None else Vec3(0, 0, 0)
        self.ppatch: dict[str, Hashable] = {} if ppatch is None else ppatch

    def meta(self) -> bt.BrickMeta:
        """Returns the BrickMeta of this brick."""
        return self._meta

    def get_property(self, p: str) -> Hashable:
        """Gets a property of the brick. If it has been modified, returns the modified value.
        Otherwise, returns a deepcopy of the default value from the BrickMeta.

        Args:
            p (str): The name of the property to get.

        Returns:
            object: The value of the property.
        """
        pobj = self.ppatch.get(p)
        if pobj is None:
            pobj = self._meta.p.get(p)
            if pobj is None:
                raise BrickError(f"Property '{p}' does not exist on brick type '{self._meta.name}'")
            return deepcopy(pobj)

    def set_property(self, p: str, v: Hashable) -> Self:
        """Sets a property of the brick.

        Args:
            p (str): The name of the property to set.
            v (object): The value to set the property to.

        Returns:
            Self: The Brick instance.
        """
        self.ppatch[p] = v
        return self

    def edit_property(self, p: str, lf: Callable[[Hashable], Hashable]) -> Self:
        """
        Edits a property of a brick using a lambda function.
        BrickEdit counts None properties as not set -> ignored, goes to default.
        You may use this to reset a property, however Brick.reset_property is usually preferred.
        """
        self.ppatch[p] = lf(self.get_property(p))
        return self

    def reset_property(self, p: str) -> Self:
        """Resets a property of the brick to its default value.

        Args:
            p (str): The name of the property to reset.

        Returns:
            Self: The Brick instance.
        """
        if p in self.ppatch:
            del self.ppatch[p]
        return self
