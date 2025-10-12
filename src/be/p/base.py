from typing import Any, Generic, Type, TypeVar
from abc import ABC, abstractmethod

T = TypeVar("T")

class PropertyMeta(Generic[T], ABC):
    
    @abstractmethod
    @staticmethod
    def serialize(v: T, version: int) -> bytearray:
        pass
    
    @abstractmethod
    @staticmethod
    def deserialize(v: bytearray, version: int) -> T:
        pass
    

pmeta_registry: dict[str, Type[PropertyMeta[Any]]] = {}

def register(name: str, registry: dict[str, Type[PropertyMeta[Any]]] = pmeta_registry):
    """
    Decorator to register a PropertyMeta subclass under `name` in `registry`.
    """
    def _decorator(class_: Type[PropertyMeta[Any]]):
        registry[name] = class_
        return class_
    return _decorator