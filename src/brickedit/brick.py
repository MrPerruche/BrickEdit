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

    def __repr__(self) -> str:
        return f'Brick({self.ref}, {self._meta.name()}, {self.pos!r}, {self.rot!r}, {self.ppatch})'

    def __format__(self, spec) -> str:
        """Format the Brick instance. Each character adds a "flag" that affects the output. Order does not matter.
        
        'f' for full: also display properties set to default values.
        'h' for human: represents as a human-readable list instead of the programmer-readable dict.
        'r' for repr: represent values using repr() instead of using str().

        Args:
            spec (str): The format specifier.

        Example:
            f'{b:fh}' → Complete human readable format that could be displayed to the user

        Returns:
            str: The formatted Brick instance.
        """
        # ppatch formatting
        displayed_properties = self.get_all_properties() if 'f' in spec else self.ppatch
        display = repr if 'r' in spec else str

        valid = {'f', 'h', 'r'}
        invalid = set(spec) - valid
        if invalid:
            raise ValueError(f"Unknown format specifier(s): {''.join(sorted(invalid))}. Valid flags: {''.join(sorted(valid))}")

        if 'h' in spec:
            return (f"Identifier:"
                  f"\n  Ref → {display(self.ref.id)}"
                  f"\n  Weld group → {display(self.ref.weld)}"
                  f"\n  Editor group → {display(self.ref.editor)}"
                  f"\nInternal name → {display(self.meta().name())}"
                  f"\nPosition → {display(self.pos)}"
                  f"\nRotation → {display(self.rot)}"
                  f"\nProperties:" +
                ''.join(f"\n  {i+1:02d}. {display(k)} → {display(v)}" for i, (k, v) in enumerate(displayed_properties.items()))
                )
        else:
            return f"Brick({display(self.ref)}, {display(self.meta().name())}, {display(self.pos)}, {display(self.rot)}, {display(displayed_properties)})"