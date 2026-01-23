# `brickedit`: Brick

Bricks are represented using the `Brick` class.

The `Brick` class has the following attributes, which you will learn more about below the list:
- `ref` (`ID`): The ID of the brick.
- `_meta` (`BrickMeta`): The brick type of the brick.
- `pos` (`Vec3`): The position of the brick.
- `rot` (`Vec3`): The rotation of the brick.
- `ppatch` (`dict[str, Hashable]`): The property patch of the brick, mapping property IDs to their values.

Bricks are added to `BRVFile`s using the `BRVFile.add` method. Learn more about `BRVFile`s in the [BRV file documentation](/doc/brv.md).

## Attributes

### `ref` attribute

The `ref` attribute is an instance of the `ID` class, which uniquely identifies the brick. It contains information such as the brick's ID string, weld group, and editor group.

Learn more about the `ID` class in the [ID documentation](/doc/id.md).


### `_meta` attribute

The `_meta` attribute is an instance of the `BrickMeta` class.

The attribute is named `_meta` to discourage direct mutation; you should treat it as read-only and access it via meta().

Each brick type in brickedit is represented by an instance of a subclass of `BrickMeta`. You do not have to worry about creating your own brick type instances. BrickEdit provides by default every vanilla brick type in the `bt` module. For example, `bt.SCALABLE_BRICK` is the brick type of scalable bricks (cube). It is an instance of the `ScalableBrickMeta` class, which is a subclass of `BrickMeta`.

Learn more about the technicalities of brick types and `BrickMeta` in the [brick types documentation](/doc/bt.md).


### `pos` and `rot` attributes

The two vectors represent the position and rotation of the brick in 3D space, respectively. Both attributes are instances of the `Vec3` class, which represents a 3D vector with `x`, `y`, and `z` components.

Learn more about vectors in BrickEdit in the [vectors documentation](/doc/vec3.md).


### `ppatch` attribute

The `ppatch` attribute is a dictionary that stores the properties of a brick. More specifically, it stores every property that differs from the brick type's default properties. It is fine to include properties set to their default values in the `ppatch` dictionary, but this will increase the file size, memory usage and processing time.

Methods are made available (and documented later here) to help you manage the `ppatch` attribute optimally and easily.

Learn more about the technicalities of properties in BrickEdit in the [properties documentation](/doc/p.md).


## Methods

The `Brick` class provides several methods to interact with and manipulate bricks:

- `meta() -> BrickMeta`: Returns the brick type (`BrickMeta` subclass instance) of the brick.
- `get_property(p: str) -> Hashable | None`: Returns the value of a property (deepcopied to avoid mutability issues). If the property does not exist for this brick, it raises a `BrickError`.
- `set_property(p: str, v: Hashable) -> Self`: Sets the value of a property, regardless of if it is the default value or not, and regardless of it this property exists for this brick. Returns self.
- `edit_property(self, p: str, lf: Callable[[Hashable], Hashable]) -> Self`: Edits the value of a property using a lambda function. The lambda function takes the current value of the property and returns the new value. Returns self.
- `reset_property(self, p: str) -> Self`: Resets the value of a property to its default value as defined by the brick type. Returns self.
- `get_all_properties(self) -> dict[str, Hashable]`: Returns a dictionary containing all properties of the brick, including those set to their default values.


## Representation

The `Brick` class has a `__repr__` method that provides an evaluable string representation of the object.

It also contains a `format` method that allows you to customize the string representation of the brick using format specifiers. Each character in the format is considered as "flag" that affects the output. The available flags are:

- `r`: Uses `repr()` instead of `str()` for values.
- `f`: Includes properties set to their default values.
- `h`: Outputs a drastically different, human-friendly format.


## Examples of bricks

When working with bricks, we recommend you use a value helper. Learn more about value helpers in the [value helper documentation](/doc/vhelper.md).

```py
from brickedit import *


# The basic grey default scalable with no non-default properties
brick1 = Brick(ID("brick_1"),
    bt.SCALABLE_BRICK,
    pos=Vec3(0.0, 0.0, 0.0),
    rot=Vec3(0.0, 0.0, 0.0)
)

# Usage of a value helper. See /doc/vhelper.md for more information
vh: ValueHelper = ValueHelper(FILE_MAIN_VERSION, default_unit=units.METER)

# Creation of a red or green wedge scalable brick at position (1m, 2m, 3m) with rotation (45°, 90°, 180°) of scale (4m, 5m, 6m)
# Using the .set_property method to set properties
brick2 = Brick(ID("brick_2"),
    bt.SCALABLE_WEDGE,
    pos=Vec3(1.0, 2.0, 3.0),
    rot=Vec3(45.0, 90.0, 180.0)
)
brick2.set_property(p.BRICK_COLOR, vh.rgba(0xff0000ff))  # Red color
brick2.set_property(p.BRICK_SIZE, vh.pos(4.0, 5.0, 6.0))  # Scale of (4m, 5m, 6m)

# By directly setting ppatch
brick3 = Brick(ID("brick_3"),
    bt.SCALABLE_WEDGE,
    pos=Vec3(1.0, 2.0, 3.0),
    rot=Vec3(45.0, 90.0, 180.0),
    ppatch={
        p.BRICK_COLOR: vh.rgba(0x00ff00ff),  # Green color
        p.BRICK_SIZE: vh.pos(4.0, 5.0, 6.0)  # Scale of (4m, 5m, 6m)
    }
)

# Create two basic scalables welded together
brick4 = Brick(ID("brick_4", weld="example_weld_group"),
    bt.SCALABLE_BRICK
)
brick5 = Brick(ID("brick_5", weld="example_weld_group"),
    bt.SCALABLE_BRICK,
    pos=Vec3(50.0, 0.0, 0.0)  # Positioned 50 centimeters along the X axis for BRVFile versions >= 15.
)
```
