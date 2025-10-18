# Preferred conventions in the brickedit codebase:


The brickedit codebase must follow Python conventions, and:


## Documentation and docstrings:

### BrickEdit, Brickedit, brickedit, BE, be,... ?

Use `BrickEdit` when capitalized (e.g., at the beginning of a sentence or title). Otherwise, use `brickedit`.

### Docstring format

Docstrings must preferably be formatted in the most appropriate of the following styles:

<details>
<summary>Examples</summary>

```py
def my_obvious_and_simple_function_or_method() -> ...:
    """
    <Description>.
    """
```

```py
def my_function_or_method(arg1: ..., arg2: Optional[...] = None) -> ...:
    """
    <Description>.

    Args:
        <Arg1> (<type>): <Arg1 description>;
        <Arg2> (<type>) (optional): <Arg2 description>.

    Returns:
        <Type>: <Return value description>.
    """
```

```py
def my_function_or_method(arg1: ..., arg2: Optional[...] = None) -> ...:
    """
    <Description>.

    Args:
        <Arg1> (<type>): <Arg1 description>;
        <Arg2> (<type>) (optional): <Arg2 description>.

    Raises:
        <Exc1> (<type>) (<contents>): ...;
        <Exc2> (<type>) (<contents>): ....

    Returns:
        <Type>: <Return value description>.
    """
```

</details>

<details>
<summary>Rationale</summary>

This format is well supported by most IDEs that provide custom formatting to docstrings. Picking a specific format is key for consistency.

</details>


### Terminology

Remember:
- "parameter" → `arg1` in `def my_function_or_method(arg1: ...) -> ...:`
- "argument" → `arg1` → `"test_value"` in `my_function_or_method("test_value")`


### Type annotation

Type annotation must be complete. When applicable, work with generics to provide more helpful type annotation.

If None is used as a default to trigger the same behavior as another argument value, write it as:
`arg: Optional[...] = None`

Otherwise if, default or not, None is a valid argument that results in unique behavior, write it as:
`arg: ... | None = ...`

<details>
<summary>Rationale</summary>

This help clearly distinguish when `None` indicates a default value or has genuine consequences to the outcome of functions and methods.

</details>


## Function and method declaration

See "Docstring format" to learn more.

If a function or method declaration exceeds 100 characters, split it by placing each parameter on a new line, aligned with the indentation level of the function body and docstring.

<details>
<summary>Example</summary>

```py
def my_ridiculously_long_function_definition(
    first_argument: ...,
    second_argument: ...,
    third_argument: ...,
    fourth_argument: ...
    ...
) -> ...:
    """
    ...
    """  # Docstring here

    ...  # Code here
```

</details>


## Imports

Imports must preferably be handled as such:

- Users should be encouraged to write:
  - `from brickedit import *` or at least
  - `import brickedit as be`

- In `__init__.py`, for the sake of structure, it's acceptable to expose essential modules using:
  - `from . import bt, p`

- Within the codebase, internal imports should be kept private for structure:
  - `from . import brick as _brick`

In brickedit, import things privately to keep the code organised: `from . import brick as _brick`,... .


## Linting

We use Pylint on default settings.


## Naming

A few names for essential parts of brickedit (which are isolated behind a module such as `bt`, `p`,...) may be reduced to short initials.

<details>
<summary>Rationale</summary>

Such design drastically reduces verbosity. For example, here are two examples using (`bt`, `vh`, `p`) and (`brick_type`, `value_helper` and `properties`):

#### With long module names
```py
from brickedit import *

v: value_helper.ValueHelper = value_helper.ValueHelper(FILE_MAIN_VERSION, default_unit=units.METER)

brv: BRVFile = BRVFile(FILE_MAIN_VERSION)

brv.add(Brick(
    "my_brick",
    brick_type.SCALABLE_BRICK,
    pos=v.pos(2.0, 5.0, 0.0),
    ppatch={
        properties.BRICK_MATERIAL: properties.BrickMaterial.PLASTIC,
        properties.BRICK_COLOR: v.rgba(0xff000000)
    }
))

brv.write(FILE_MAIN_VERSION)
```

#### With short module names
```py
from brickedit import *

v: vh.ValueHelper = vh.ValueHelper(FILE_MAIN_VERSION, default_unit=units.METER)

brv: BRVFile = BRVFile(FILE_MAIN_VERSION)

brv.add(Brick(
    "my_brick",
    bt.SCALABLE_BRICK,
    pos=v.pos(2.0, 5.0, 0.0),
    ppatch={
        p.BRICK_MATERIAL: p.BrickMaterial.PLASTIC,
        p.BRICK_COLOR: v.rgba(0xff000000)
    }
))

brv.write(FILE_MAIN_VERSION)
```
</details>
