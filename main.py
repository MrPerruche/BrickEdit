from typing import Final

from src.brickedit import *

# Internal name variable
MY_PROPERTY: Final[str] = 'MyProperty'

# Registration decorator required for be to detect and use this data type
@p.register(MY_PROPERTY)
class MyPropertyMeta(p.PropertyMeta[str]):

    # Our made up property type is an enum with 3 possible states
    FIRST_OPTION: Final[str] = 'FirstOption'
    SECOND_OPTION: Final[str] = 'SecondOption'
    THIRD_OPTION: Final[str] = 'ThirdOption'

    @staticmethod
    def serialize(v: str, version: int) -> bytearray:
        # Enums are often stored as a utf-8 string prefixed by its length as a UInteger8
        return serialization.UInteger8.serialize(len(v)) + serialization.String.serialize(v)

    @staticmethod
    def deserialize(v: bytearray, version: int) -> str:
        # Enums are often stored as a utf-8 string prefixed by its length as a UInteger8
        # Given be already slices the bytearray to only contain the property value, we can skip the first byte
        return serialization.String.deserialize(v[1: ])