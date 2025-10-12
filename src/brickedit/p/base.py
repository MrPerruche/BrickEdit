from typing import Any, Generic, Type, TypeVar
from abc import ABC, abstractmethod

T = TypeVar("T")

# Todo: Make the setup more robust later, (enforce the singleton).
class InvalidVersionType:
    def __repr__(self):
        return 'InvalidVersion'

InvalidVersion = InvalidVersionType()


class PropertyMeta(Generic[T], ABC):

    @staticmethod
    @abstractmethod
    def serialize(v: T, version: int) -> bytearray | InvalidVersionType:
        pass

    @staticmethod
    @abstractmethod
    def deserialize(v: bytearray, version: int) -> T | InvalidVersionType:
        pass


pmeta_registry: dict[str, Type[PropertyMeta[Any]]] = {}

def register(name: str, registry: dict[str, Type[PropertyMeta[Any]]] | None = None):
    """
    Decorator to register a PropertyMeta subclass under `name` in `registry`.
    If registry is none, will use BrickEdit's default registry pmeta_registry.
    """
    if registry is None:
        registry = pmeta_registry
    def _decorator(class_: Type[PropertyMeta[Any]]):
        registry[name] = class_
        return class_
    return _decorator
