from typing import Generic, TypeVar
from abc import ABC, abstractmethod

T = TypeVar("T")

class Serializer(Generic[T], ABC):

    @staticmethod
    @abstractmethod
    def serialize(v: T) -> bytearray:
        pass

    @staticmethod
    @abstractmethod
    def deserialize(v: bytearray) -> T:
        pass


class EnumValue(Serializer[str]):

    @staticmethod
    def serialize(v: str) -> bytearray:
        return bytearray(v.encode('ascii'))

    @staticmethod
    def deserialize(v: bytearray) -> str:
        return v.decode('ascii')


class UInteger8(Serializer[int]):

    @staticmethod
    def serialize(v: int) -> bytearray:
        return bytearray(b'\x00') # TODO

    @staticmethod
    def deserialize(v: bytearray) -> int:
        return 0 # TODO