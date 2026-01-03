from copy import deepcopy
from typing import Optional, Self, Callable
from collections.abc import Hashable

from . import bt
from .id import ID as _ID
from .exceptions import BrickError
from .vec import Vec3


class Brick:

    __slots__ = ('_meta', 'ref', 'pos', 'rot', 'ppatch')

    def __init__(self,
                 ref: _ID,
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
        # If the property key exists in the patch, return its stored value
        # (including explicit None). Otherwise return a deepcopy of the
        # default value from the BrickMeta.
        if p in self.ppatch:
            return self.ppatch[p]
        if p not in self._meta.p:
            raise BrickError(f"Property '{p}' does not exist on brick type '{self._meta.name()}'")
        pobj = self._meta.p.get(p)
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
        
        Args:
            p (str): The name of the property to edit.
            lf (Callable[[Hashable], Hashable]): A lambda function that takes the current property
                value and returns the new property value.

        Returns:
            Self: The Brick instance.
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

    def get_all_properties(self) -> dict[str, Hashable]:
        """Returns a dictionary of all properties of the brick, including modified and default values.

        Returns:
            dict[str, Hashable]: A dictionary of all properties of the brick.
        """
        props = {}
        for p in self._meta.p.keys():
            props[p] = self.get_property(p)
        return props
