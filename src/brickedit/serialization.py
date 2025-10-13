from typing import Generic, TypeVar
from abc import ABC, abstractmethod
import struct

T = TypeVar("T")

class Serializer(Generic[T], ABC): # pylint: disable=missing-class-docstring

    @staticmethod
    @abstractmethod
    def serialize(v: T) -> bytearray:
        pass

    @staticmethod
    @abstractmethod
    def deserialize(v: bytearray) -> T:
        pass


class EnumValue(Serializer[str]): # pylint: disable=missing-class-docstring

    @staticmethod
    def serialize(v: str) -> bytearray:
        return bytearray(v.encode('ascii'))

    @staticmethod
    def deserialize(v: bytearray) -> str:
        return v.decode('ascii')


class UInteger8(Serializer[int]): # pylint: disable=missing-class-docstring

    @staticmethod
    def serialize(v: int) -> bytearray:
        return bytearray(int(v).to_bytes(1, 'little'))

    @staticmethod
    def deserialize(v: bytearray) -> int:
        return int.from_bytes(v, 'little')
