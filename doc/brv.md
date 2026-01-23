# `brickedit`: BRV (Brick Rigs Vehicle)


## Having trouble understanding this?

<details>
<summary>Having trouble understanding this?</summary>

Are you a beginner in computer science or unfamiliar with Python? This short section will give some information to go back to if you need help reading:
- "Deserialization" refers to the process of converting something expressed in a specific format (binary) back into a data structure that a program can use.
- "Serialization" is the opposite of deserialization. It is the process of converting a data structure into a specific format (binary) for storage or transmission.

</details>

-----


## Working with vehicles: `BRVFile`

The `BRVFile` class contains all necessary methods to work with vehicle files. They contain two attributes:
- `version` (`int`): The version of the Brick Rigs Vehicle format to use.
- `bricks` (`list[Brick]`): A (mutable) list of all bricks in the vehicle.


## Methods of `BRVFile`

Here are all the methods of `BRVFile` outside and (de)serialization:

- `__add__` (`BRVFile() + BRVFile()`): Merges two `BRVFile`s into one, combining their bricks. Both must be of the same version, otherwise they will raise a `ValueError`. Returns a new `BRVFile` instance.
- `add(self, brick: Brick) -> Self`: Adds a brick to the vehicle. Returns self.
- `update(self, bricks: Iterable[Brick]) -> Self`: Updates the vehicle by adding all bricks from any given iterable. Returns self.
- `update_from_brvfile(self, other: BRVFile) -> Self`: Updates the vehicle by adding all bricks from another `BRVFile`. Returns self.


## (De)serialization of vehicle files

### Serialization

Serialization is done using the `BRVFile.serialize` method. It takes does not take any arguments and returns the serialized bytes of the vehicle file.

### Deserialization

Deserialization is done using the `BRVFile.deserialize` class method. It is not a static method because it requires the file version. It takes one argument:

- `buffer` (`bytes | bytearray`): The bytes of the vehicle file to deserialize.

When deserializing, the bricks will be named as such:
- `id` is set to `brick_{i}` where `{i}` is the index of the brick, starting at 0.
- `weld` is set to `weld_{weld_idx}` where `{weld_idx}` is the index of the weld group, starting at 1. If it is not part of a weld group, it is set to `None`.
- `editor` is set to `editor_{editor_idx}` where `{editor_idx}` is the index of the editor group, starting at 1. If it is not part of an editor group, it is set to `None`.


## Example usage

```py
from brickedit import *

# Deserialize a BRV file
with open('Vehicle.brv', 'rb') as f:
    brv_data = f.read()
brv: BRVFile = BRVFile(FILE_MAIN_VERSION)  # First, create an instance
brv.deserialize(brv_data)  # Then call deserialize

# Do something on the brv. For example, add a brick:
brv.add(Brick(
    ID('custom_brick'),
    bt.SCALABLE_BRICK
))

# Serialize the BRV file back to bytes
new_brv_data: bytes = brv.serialize()
with open('Vehicle.brv', 'wb') as f:
    f.write(new_brv_data)
```
