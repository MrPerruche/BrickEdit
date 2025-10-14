# `brickedit.bt`: Brick Types


## Having trouble understanding this?

<details>
<summary>Having trouble understanding this?</summary>

Are you a beginner in computer science or unfamiliar with Python? This short section will give some information to go back to if you need help reading:

- Decorators are things that wrap around functions and classes to easily add additional code. You can see them as a special kind of function. They are placed above a class or function and start with `@`. They can take arguments in parentheses. For example: `@staticmethod`, `@p.register(BRICK_MATERIAL)`.
- While somewhat uncommon in Python, there are generic types. A concise note: TypeVars and Generic are used by type checkers (mypy, IDEs) and are not enforced at runtime. `T` is a common name for a type variable. Example usage: `class MyClass(ParentClass[str])` tells type checkers that all `T`s in `ParentClass`'s are `str`.

</details>


This module contains all brick types and their classes in brickedit:
- `BrickMeta`: Class defining how brick types must be defined. Its subclasses are the different brick classes instanciated by individual bricks.
- Class of each brick type. For example, `GunBrick`, `ScalableBrick`,... .


## Structure as a graph

```mermaid
flowchart TB
    subgraph BASE[base.py]
        META["class BrickMeta"]
    end
    subgraph CLASSES[classes.py]

        %% CLASSES
        CE1["**class ScalableBrickMeta(BrickMeta)**"]
        CE2["**class GunBrickMeta(BrickMeta); where base_properties take arguments**"]
        CE3["..."]

        %% INSTANCES
        subgraph CE1T["Instances:"]
            CE1T1["SCALABLE_BRICK = ScalableBrickMeta('ScalableBrick')"]
            CE1T2["SCALABLE_WEDGE = ScalableBrickMeta('ScalableWedge')"]
            CE1T3["..."]
        end
        subgraph CE2T["Instances:"]
            CE2T1["GUN_2x1x1 = GunBrickMeta('Gun_2x1x1')"]
            CE2T2["GUN_2x2x2 = GunBrickMeta('Gun_2x2x2', ammo_type=p.AmmoType.EXPLOSIVE)"]
            CE2T3["..."]
        end
        CE3T["..."]
        
    end

    META ---> CE1 & CE2 & CE3
    CE1 -.-> CE1T
    CE2 -.-> CE2T
    CE3 -.-> CE3T
```

## Defining new brick types: `BrickMeta(ABC)`

`BrickMeta` is the base class for all brick types.

Each subclass of `BrickMeta` must define the following:
- `@abstractmethod base_properties(self, *args, **kwargs) -> dict[str, object]` which creates a new object holding the default properties for each individual brick type. Anything may be added to args and kwargs and be used to determine the outputted dictionary.