# Welcome to the BrickEdit documentation!

BrickEdit is a Python library for creating and manipulating Brick Rigs files (vehicle and metadata). It provides both tools to read, write, and modify these files programmatically, and utils to help you work with bricks, properties, and vectors.

BrickEdit is meant to be fast and in-depth, while being easy to use. We aim to be beginner-friendly and provide a wide range of features to help you create and modify vehicle files efficiently, without having to worry much about low-level details.

## Installation

You can install BrickEdit using pip:

```bash
pip install brickedit
```

Or you can download new releases' source code from [GitHub](https://github.com/MrPerruche/BrickEditInterface/releases).


## Before getting started

To reduce verbosity, BrickEdit has a few abbreviated names that are hard to guess and you must learn:
- `bt` refers to "Brick Type". This is a module name.
- `p` refers to "Property". This is a module name.
- `vhelper` refers to "Value Helper". This is a module name.
- `.brv` and `.brm` are Brick Rigs' vehicle and metadata files extensions.

## Making your first vehicle

### Setup: creating a new BRVFile

You must first import brickedit. We recommend you use `from brickedit import *` or `import brickedit as be`.

After importing brickedit, you must create an instance of the `BRVFile` class. It is a class that will contain the file version you are using and the bricks in this vehicle. When it comes to the file version, you can use the constants `FILE_MAIN_VERSION` or `FILE_EXP_VERSION` depending on the branch you're using.

```py
from brickedit import *

brv = BRVFile(FILE_MAIN_VERSION)
```

### Adding a brick

BrickEdit represents bricks using the `Brick` class. To create a basic brick with no non-default properties, you may do something like this:; We will go over each argument after the example.

```py
from brickedit import *

brv = BRVFile(FILE_MAIN_VERSION)

brick = Brick(
    ID("my_brick"),
    bt.SCALABLE_BRICK,
    pos=Vec3(0, 0, 0),  # Optional argument. Default value: Vec3(0, 0, 0)
    rot=Vec3(0, 0, 0),  # Optional argument. Default value: Vec3(0, 0, 0)
    ppatch={}  # Optional argument. Default value: {}
)
```

- Parameter 1: `id` (`ID`) (`ID("my_brick")` in this example): ID is a class that holds 3 attributes (1 mandatory and 2 optional). It is used to identify bricks for input channels. You may learn more in the [ID documentation](/doc/id.md).
- Parameter 2: `_meta` (`BrickMeta`) (`bt.SCALABLE_BRICK` in this example): Brick Types are a complicated topic. What you must understand is each brick type is a constant variable, and brickedit provide constants for every brick type in vanilla Brick Rigs. You may learn more in the [brick types documentation](/doc/bt.md), but we do not advise you get into these technicalities just yet.
- Parameter 3: `pos` (`Vec3`): Position of the brick in the vehicle. The unit depends on the version, and we will learn more about it later. You may learn more about vectors in the [vector documentation](/doc/vec.md).
- Parameter 4: `rot` (`Vec3`): Rotation of the brick in the vehicle. You may learn more in the [vector documentation](/doc/vec.md).
- Parameter 5: `ppatch` (`dict[str, Hashable]`): Property patch: this is a dictionary of properties that are different from the default ones. We will learn about it later.


### Working with units

As previously mentioned, units are messy, because they depend on the version. Instead of letting you deal with these technicalities, we created the `vhelper` module to help you work with values. You will use it with the `ValueHelper` class.

The `ValueHelper` class must be instantiated with the file version you are working with.

Here is how you can use `ValueHelper` to work with units:

```py
from brickedit import *

brv = BRVFile(FILE_MAIN_VERSION)
vh = vhelper.ValueHelper(FILE_MAIN_VERSION)  # By default, ValueHelper uses meters. You can change the unit by setting the default_physical_unit argument. For example, vh = ValueHelper(FILE_MAIN_VERSION, default_physical_unit=vhelper.CENTIMETER)

brick = Brick(
    ID("my_brick"),
    bt.SCALABLE_BRICK,
    pos=vh.pos(0, 0, 0),
    rot=Vec3(0, 0, 0),
    ppatch={}
)
```

You may learn more about the `ValueHelper` class in the [value helper documentation](/doc/vhelper.md).


### Working with properties

Properties are essential to builds, but they are not an obvious topic. They are handled via the `p` module.

The internal names of properties are not very clear. We made constant variables for every property, that are their name's or a similar name in screaming snake case, so instead of writing for example `"BrickSize"`, you can write for example `p.BRICK_SIZE` (and make use of your IDE's suggestions).

The same goes for their values. Depending on the property, you may either use value helpers to get the right unit, or use constant values stored by brickedit. Stored values (for enums etc.) are available in the property's class, that are their name's or a similar same in pascal case. For example, you may get the value for the plastic material via `p.BrickMaterial.PLASTIC`.

To show both vehicle helper and the `p` module in action, here is an example of what properties you want to use to make a glowing red brick:

```py
my_properties = {
    p.BRICK_MATERIAL: p.BrickMaterial.GLOW,
    p.BRICK_COLOR: vh.p_rgba(0xff0000ff)
    # Note: vh.p_rgba is packed rgba. It takes as input 0xrrggbbaa
    # Instead of vh.p_rgba, you may use vh.rgba(255, 0, 0, 255), vh.hsva(0, 1, 1, 1), etc.
    # Reminder: you can learn more about vhelper in /doc/vhelper.md
}
```

Properties are stored in the `ppatch` dictionary. Any property that is not included in the ppatch will be left to its default values.

**Note:** without getting into the technicalities, we recommend you do not include properties that are left to their default values. Doing this will reduce the file size, memory usage and processing time.

Here is an example of how to create a glowing red brick:

```py
from brickedit import *

brv = BRVFile(FILE_MAIN_VERSION)
vh = vhelper.ValueHelper(FILE_MAIN_VERSION)

brick = Brick(
    ID("my_glowing_brick"),
    bt.SCALABLE_BRICK,
    pos=vh.pos(0, 0, 0),
    rot=Vec3(0, 0, 0),
    ppatch={  # See my_properties in the previous example
        p.BRICK_MATERIAL: p.BrickMaterial.GLOW,
        p.BRICK_COLOR: vh.p_rgba(0xff0000ff)
    }
)
```

You may learn more about properties (mostly how to create custom properties) in the [property documentation](/doc/p.md).


### Adding a brick to a vehicle

Adding bricks to a vehicle is very simple. There are two ways to do it:

You can directly edit the `bricks` attribute of `BRVFile`:

```py
from brickedit import *

brv = BRVFile(FILE_MAIN_VERSION)
vh = vhelper.ValueHelper(FILE_MAIN_VERSION)

brick = Brick(
    ID("my_glowing_brick"),
    bt.SCALABLE_BRICK,
    pos=vh.pos(0, 0, 0),
    rot=Vec3(0, 0, 0),
    ppatch={
        p.BRICK_MATERIAL: p.BrickMaterial.GLOW,
        p.BRICK_COLOR: vh.p_rgba(0xff0000ff)
    }
)

brv.bricks.append(brick)
```

Or you can directly use the `add` method (which we recommend). While we're there, we are also going to directly add the brick instead of making it a variable to make the code shorter:

```py
from brickedit import *

brv = BRVFile(FILE_MAIN_VERSION)
vh = vhelper.ValueHelper(FILE_MAIN_VERSION)

brv.add(Brick(
    ID("my_glowing_brick"),
    bt.SCALABLE_BRICK,
    pos=vh.pos(0, 0, 0),
    rot=Vec3(0, 0, 0),
    ppatch={
        p.BRICK_MATERIAL: p.BrickMaterial.GLOW,
        p.BRICK_COLOR: vh.p_rgba(0xff0000ff)
    }
))
```


### Saving the vehicle

Saving is easy. First, we must serialize the vehicle (serialization is the process of converting something into bytes to store or transmit it) using `BRVFile.serialize()`. Then, we can write the bytes to a file.

**Note:** Brick Rigs will only read the vehicle file that is named `Vehicle.brv` (case-sensitive). Any other file name will be ignored.

Here is an example:

```py
from brickedit import *

brv = BRVFile(FILE_MAIN_VERSION)
vh = vhelper.ValueHelper(FILE_MAIN_VERSION)

brv.add(Brick(
    ID("my_glowing_brick"),
    bt.SCALABLE_BRICK,
    pos=vh.pos(0, 0, 0),
    rot=Vec3(0, 0, 0),
    ppatch={
        p.BRICK_MATERIAL: p.BrickMaterial.GLOW,
        p.BRICK_COLOR: vh.p_rgba(0xff0000ff)
    }
))

serialized: bytearray = brv.serialize()
with open("Vehicle.brv", "wb") as f:
    f.write(serialized)
```

Congratulations! You have created your first vehicle file! Next, we will learn how to add metadata to this vehicle.

If you wish to train more, here is a few build ideas to create programmatically:
- Easy: a pyramid of height n, similar to the *, **, etc. pyramids in tutorials;
- Fair: a cube made of glowing scalable cubes;
- Medium: a rainbow circle made of spinners.


## Creating a metadata file

BrickRigs vehicles have a `MetaData.brm` file alongside them, that stores information such as the name, description, author, etc. You can create a metadata file using the `BRMFile` class.

First, you must create an instance of `BRMFile`. Here is an example:

```py
from brickedit import *

brm = BRMFile(FILE_MAIN_VERSION)
```

Then, you will directly serialize the file using the `serialize` method. You will pass the name, description, and other information using arguments. Here is an example:

```py
from brickedit import *

brm = BRMFile(FILE_MAIN_VERSION)
serialized: bytearray = brm.serialize(
    name="My Vehicle",
    description="This is a description",
    author=76561199130146863,  # Steam64 ID of perru_. You can put your own!
    creation_time=vhelper.net_ticks_now(),  # vhelper.net_ticks_now() is a function to get the current time in .NET ticks, which BrickRigs use.
    last_update_time=vhelper.net_ticks_now(),
    visibility=VISIBILITY_PUBLIC,  # Constant variable from brickedit
    tags=["tag1", "tag2"]
)
with open("MetaData.brm", "wb") as f:
    f.write(serialized)
```


## Deserialization (Loading a file)

Deserialization is a little more complicated, and out of the scope of this documentation. We suggest you learn more about it in their respective documentations:

- [`BRVFile` documentation](/doc/brv.md)
- [`BRMFile` documentation](/doc/brm.md)
