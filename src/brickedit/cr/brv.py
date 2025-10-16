"""BRV file handling."""
from ..brick import Brick
from ..var import FILE_EXP_VERSION
from typing import Self

class BRVFile:
    """A Brick Rigs vehicle file.
    
    Properties:
        todo"""

    def __init__(self):
        self.version: int = FILE_EXP_VERSION
        self.bricks: list = []



    def add(self, brick: Brick) -> None:
        """Add a new brick to the vehicle.

        Arguments:
            brick (Brick): The brick to add.
        
        Returns:
            None"""

        self.bricks.append(brick)



    def paste(self, other: Self) -> Self:
        """Paste this vehicle file instance onto another, effectively concatenating them.
        Does not modify either of the original files.

        Arguments:
            other (BRVFile): The vehicle file to paste onto.
        
        Returns:
            Self: The concatenated vehicle file."""

        if self.version != other.version:
            raise ValueError("Cannot paste BRV files with different versions.")

        new = self.__class__()
        new.version = self.version

        new.bricks.extend(other.bricks)
        new.bricks.extend(self.bricks)
        return new

    def __add__(self, other):
        return other.paste(self) # Paste onto *us*.
