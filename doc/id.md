# `brickedit`: ID

Bricks are identified using IDs. An ID is represented using the `ID` class. They contain 3 attributes:

- `id` (`str`): The string ID of the brick. For example: `"my_brick"`. This string is used to identify bricks for input channels.
- `weld` (`str`): The weld ID of the brick. All bricks with the same weld attribute will be in the same weld group.
- `editor` (`str`): The editor ID of the brick. All bricks with the same editor attribute will be in the same editor group.

The `ID` class has a repr and supports equality checks with another ID. Equality checks compare all 3 attributes.


## Example of an equality check between different IDs

```py
from brickedit import *

id1 = ID("brick_1", weld="group_1", editor="editor_1")
id2 = ID("brick_1", weld="group_1", editor="editor_1")
id3 = ID("brick_2", weld="group_1", editor="editor_1")

assert id1 == id2  # True, all attributes are the same
assert id1 != id3  # True, id attribute is different
```
