# Structure of brickedit

**If flowchards are not supported by your IDE, consider installing a plugin to add Mermaid support.**

## Base class

`base.py` files contains the essentials for the rest of the module if fair for all to be put in a single file. For example in the case of `p` (properties), is defined the main class all other classes inherit from, `InvalidVersion` (sentinel),  

## File structure 
```mermaid
flowchart LR

    %%{init: {"flowchart": {"defaultRenderer": "elk"}}}%%

    %% Nodes
    SRC[brickedit]
    subgraph BT[bt: Brick Types]
        BT_B[base: Base]
        BT_C["classes: All brick classes initialized and instanced"]
        BT_I["inner_properties: All dataclasses related to BRMK properties"]
    end
    subgraph P[p: Properties]
        P_B[base: Base]
        P_C["classes: All property classes are initialized and finals declared"]
        P_M["meta: All kinds of common property classes to be initialized and inherited from"]
    end
    BRICK["brick: Holds the Brick class, a container for each brick's type, id,... with related methods"]
    EXC["exceptions: Custom Exceptions from brickedit"]
    SRZ["serialization: Classes being an abstraction of struct module"]
    VAR["var: Commmon variables (brickedit version, Brick Rigs version,...)"]
    VEC["vec: Custom implementation of vectors"]

    %% LINKS
    SRC --> BT
    SRC --> P
    SRC --> BRICK
    SRC --> EXC
    SRC --> SRZ
    SRC --> VAR
    SRC --> VEC
```
