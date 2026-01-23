# BrickEdit
BrickEdit is a library to interact with `.brv` and `.brm` files, the vehicle and metadata files used in the game Brick Rigs.

## Installation

To install the library, run `pip install brickedit`.

## Requirements

- Python 3.13 or later

## Basic Usage

Example of how to create a single brick using brickedit:
```python
from brickedit import *

brv = BRVFile(FILE_MAIN_VERSION)

brv.add(Brick(
    ID("my_brick"),
    bt.SCALABLE_BRICK
))

with open("Vehicle.brv", "wb") as f:
    f.write(brv.serialize())
```

## License

See the [`LICENSE`](LICENSE) file for details.
