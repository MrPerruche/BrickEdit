"""BRV file handling."""
from ..brick import Brick
from ..var import FILE_EXP_VERSION

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
