from typing import Any, Callable, Generic, Type, TypeVar
from abc import ABC, abstractmethod

T = TypeVar("T")

class InvalidVersionType:
    """Class of InvalidVersion singleton (sentinel)."""

    __slots__ = ()
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(InvalidVersionType, cls).__new__(cls)
        return cls._instance

    def __repr__(self):
        return 'InvalidVersion'

InvalidVersion: InvalidVersionType = InvalidVersionType()


class PropertyMeta(Generic[T], ABC):
    """Base class for property metadata."""

    @staticmethod
    @abstractmethod
    def serialize(v: T, version: int) -> bytearray | InvalidVersionType:
        """Serializes the value `v`.

        Args:
            v (T): Value to serialize
            version (int): Version of the property

        Returns:
            bytearray | InvalidVersionType: Result as bytearray or InvalidVersion sentinel
            if the property does not support this version.
        """
    @staticmethod
    @abstractmethod
    def deserialize(v: bytearray, version: int) -> T | InvalidVersionType:
        """Deserializes the value `v` for the given `version`.

        Args:
            v (bytearray): Value to deserialize
            version (int): Version of the property

        Returns:
            T | InvalidVersionType: Result as deserialized value or InvalidVersion sentinel
            if the property does not support this version.
        """


pmeta_registry: dict[str, Type[PropertyMeta[Any]]] = {}

_T = TypeVar('_T', bound=Type[PropertyMeta[Any]])

def register(
    name: str,
    registry: dict[str, Type[PropertyMeta]] | None = None
) -> Callable[[_T], _T]:
    """
    Decorator to register a PropertyMeta subclasses.
    If registry is none, will use BrickEdit's default registry pmeta_registry.
    
    Args:
        name (str): Name of the property type.
        registry (dict[str, Type[PropertyMeta]]), optional: Registry to use. Defaults to None.
    """

    if registry is None:
        registry = pmeta_registry

    def _decorator(class_: _T) -> _T:
        registry[name] = class_
        return class_
    return _decorator
