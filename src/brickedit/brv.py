"""BRV file handling."""
import struct
from typing import Self, Optional, Iterable
#from ..brick import Brick
from . import brick as _brick
from . import var as _var
#from ..var import FILE_EXP_VERSION

class BRVFile:
    """A Brick Rigs vehicle file.
    
    Properties:
        todo"""

    def __init__(
        self,
        version: int = _var.FILE_EXP_VERSION,
        bricks: Optional[list[_brick.Brick]] = None
    ):
        self.version: int = version
        self.bricks: list[_brick.Brick] = [] if bricks is None else bricks


    def __add__(self, other: Self) -> Self:
        """Merges two BRVFiles into a new instance. Use .update() when possible.

        Args:
            other (BRVFile): The vehicle to add from.

        Returns:
            BRVFile: New instance
        """
        return self.__class__().update_from_brvfile(self).update_from_brvfile(other)


    def add(self, brick: _brick.Brick) -> Self:
        """
        Add a new brick to the vehicle.

        Arguments:
            brick (Brick): The brick to add.
        
        Returns:
            Self
        """
        self.bricks.append(brick)
        return self


    def update(self, bricks: Iterable[_brick.Brick]) -> Self:
        """
        Updates (extend) the list of bricks

        Args:
            bricks (Iterable[Brick]): List of bricks to update.
            
        Returns:
            Self
        """
        self.bricks.extend(bricks)
        return self


    def update_from_brvfile(self, other: Self) -> Self:
        """
        Updates (extend) the list of bricks from another instance's list, effectively concatenating them.
        Edits the original instance.

        Args:
            other (BRVFile): The vehicle file to update from.
        
        Returns:
            Self: The concatenated vehicle file.
        """

        self.bricks.extend(other.bricks)
        return self




    def serialize(self) -> bytearray:
        """Serialize the vehicle file into a bytearray.

        Returns:
            bytearray: The serialized vehicle file."""

        # Let's start by writing the version byte.
        buffer = bytearray(struct.pack("B", self.version))

        # Next, at offset 0x01, the number of bricks. (uint16)
        buffer.extend(struct.pack("<H", len(self.bricks)))

        # At 0x03, we write the number of unique brick types.
        unique_types = set(brick.meta() for brick in self.bricks)
        unique_types_mapping = {
            bt: i for i, bt in enumerate(unique_types)
        }
        # TODO: Defaults
        default_props: dict = dict()
        buffer.extend(struct.pack("<H", len(unique_types)))

        # 0x05: Number of unique properties.
        # This, along with the stuff at 0x03, is for an atlas system.
        # Let's count how many unique properties there are.

        unique_properties = set(brick.p for brick in self.bricks)
        # Let's just hope that works.
        # FIXME: That almost certainly doesn't.

        buffer.extend(struct.pack("<H", len(unique_properties)))

        # Brick types
        # For each brick type...
        for bt in unique_types:
            # Write the length of the following string.
            buffer.extend(struct.pack("B", len(bt.name())))
            # The string itself.
            buffer.extend(bt.name().encode("ascii"))

        # Properties
        for prop in unique_properties:
            # Write the length of the following string.
            buffer.extend(struct.pack("B", len(prop.name())))
            # The string itself.
            buffer.extend(prop.name().encode("ascii"))

            # Number of property values.
            buffer.extend(struct.pack())
