"""BRV file handling."""
import struct
from typing import Self, Optional, Iterable
from collections import defaultdict
from collections.abc import Hashable
import io

from . import brick as _brick
from . import vec as _vec
from . import var as _var
from . import bt as _bt
from . import p as _p
from . import exceptions as _e


class BRVFile:
    """A Brick Rigs vehicle file.
    
    Properties:
        todo"""

    def __init__(
        self,
        version: int = _var.FILE_EXP_VERSION,
        bricks: Optional[list[_brick.Brick]] = None
    ):
        self.version: int = version
        self.bricks: list[_brick.Brick] = [] if bricks is None else bricks


    def __add__(self, other: Self) -> Self:
        """Merges two BRVFiles into a new instance. Use .update() when possible.

        Args:
            other (BRVFile): The vehicle to add from.

        Returns:
            BRVFile: New instance
        """
        return self.__class__().update_from_brvfile(self).update_from_brvfile(other)


    def add(self, brick: _brick.Brick) -> Self:
        """
        Add a new brick to the vehicle.

        Arguments:
            brick (Brick): The brick to add.
        
        Returns:
            Self
        """
        self.bricks.append(brick)
        return self


    def update(self, bricks: Iterable[_brick.Brick]) -> Self:
        """
        Updates (extend) the list of bricks

        Args:
            bricks (Iterable[Brick]): List of bricks to update.
            
        Returns:
            Self
        """
        self.bricks.extend(bricks)
        return self


    def update_from_brvfile(self, other: Self) -> Self:
        """
        Updates (extend) the list of bricks from another instance's list,
        effectively concatenating them. Edits the original instance self.

        Args:
            other (BRVFile): The vehicle file to update from.
        
        Returns:
            Self: The concatenated vehicle file.
        """

        self.bricks.extend(other.bricks)
        return self




    def serialize(self) -> bytearray:
        """
        Serialize the vehicle file into a bytearray.

        Returns:
            bytearray: The serialized vehicle file."""

        assert len(self.bricks) <= 65_534, "Too many bricks! Max: 65,534"

        # Init buffer
        buffer = io.BytesIO()

        # No repeated global lookups
        pmeta_registry_get = _p.pmeta_registry.get
        BrickError = _e.BrickError
        write = buffer.write

        # Precompile struct
        pack_B = struct.Struct('B').pack   # 'B'  → uint8
        pack_H = struct.Struct('<H').pack  # '<H' → uint16 LE
        pack_I = struct.Struct('<I').pack  # '<I' → uint32 LE
        pack_f = struct.Struct('<f').pack  # '<f' → sp float LE

        # --------1. HEADER

        # Version Byte
        write(pack_B(self.version))

        # Number of bricks
        write(pack_H(len(self.bricks)))

        # Number of unique brick types. No .name, strings are larger objects
        types = []
        types_to_index = {}
        for brick in self.bricks:
            meta = brick.meta()
            if meta not in types_to_index:
                types_to_index[meta] = len(types)
                types.append(meta)
        write(pack_H(len(types)))

        # ---- Building property dicts (hardest part, I NEED comments yet I hate commenting)


        # A dictionary that will for each property give us its index
        prop_to_index: dict[str, int] = {}
        # A list that for each property index will give us the dict of values : index
        value_to_index = defaultdict(dict)
        # A list that for each prop gives {for each value index gives us its serialized version}
        indexes_to_serialized = defaultdict(list)
        # A list of reference to brick index for source brick properties
        reference_to_brick_index: dict[str, int] = {b.ref: i+1 for i, b in enumerate(self.bricks)}

        # Exploring all bricks
        for brick in self.bricks:

            # Exploring all properties
            for prop, value in brick.ppatch.items():

                if value is None:
                    continue

                # Get the serialization class and make sure it's valid
                prop_serialization_class = pmeta_registry_get(prop)
                if prop_serialization_class is None:
                    raise BrickError(f"Property {prop!r} from brick {brick!r}"
                                        "does not have any serialization class registered.")

                # Put in the lists if it's not already
                if prop not in prop_to_index:
                    prop_to_index[prop] = len(prop_to_index)
                    # value_to_index and indexes_to_serialized are defaultdicts,
                    # no need to init with an empty object.

                # Keep what property index we're at
                prop_index = prop_to_index[prop]

                # Handing the value:
                try:
                    # Serialize
                    binary = prop_serialization_class.serialize(value, self.version, reference_to_brick_index)
                    # print(f'{prop} > {value} : {binary=}')
                    # If version is invalid, skip
                    if binary is _p.InvalidVersion:
                        # If this invalid is alone in the list of properties, kill it!
                        if len(value_to_index[prop_index]) == 0:
                            prop_to_index.pop(prop)  # This one use property name as key
                            value_to_index.pop(prop_index)  # Uses index
                            indexes_to_serialized.pop(prop_index)  # Uses index
                        continue

                    # Put value in property → value → index. Cannot be None because value_to_index
                    # is handled when a new property is discovered: value_to_index.append({})
                    sub_dict = value_to_index[prop_index]
                    sub_dict_len = len(sub_dict)  # Remember the length for later, see if it changes
                    sub_dict.setdefault(value, sub_dict_len)

                    # If it's new, put the binary:
                    if sub_dict_len != len(sub_dict):  # len(sub_dict) changed → something added
                        indexes_to_serialized[prop_index].append(binary)

                except TypeError as e:
                    if 'unhashable' not in str(e):
                        raise
                    raise BrickError(f'Unhashable value {value!r} for property {prop!r} of brick '
                                        f'{brick!r}. Do not use lists. Use Vec or tuples.') from e


        # ---- Back to header!
        write(pack_H(len(prop_to_index)))


        # --------2. BRICK TYPES
        for t in types:
            # Len of t then t
            write(pack_B(len(t.name())))
            write(t.name().encode('ascii'))


        # --------3. PROPERTIES
        for prop, prop_index in prop_to_index.items():

            # Encode the property -- Len of prop then prop
            write(pack_B(len(prop)))
            write(prop.encode('ascii'))

            # Number of properties
            num_values = len(value_to_index[prop_index])
            write(pack_H(num_values))

            # Write the properties:
            # Get the sum of all properties
            binaries = indexes_to_serialized[prop_index]
            # Write the length
            total_len = sum(len(b) for b in binaries)
            write(pack_I(total_len))
            for binary in binaries:
                # Write the values
                write(binary)

            # Property footer
            # If 1 element, no footer
            if num_values > 1:
                # If all elements are of the same length, only show the length of one (the 1st)
                len_first_binaries = len(binaries[0])
                if all(len(b) == len_first_binaries for b in binaries):
                    write(pack_H(len(binaries[0])))
                # Else elements have different lenghts, write 0 then length of each element
                else:
                    write(b'\x00\x00')
                    for binary in binaries:
                        write(pack_H(len(binary)))


        # --------4. BRICKS

        # Remember. Index starts at 1 here because fluppi
        for brick in self.bricks:

            # 1. Brick Type
            brick_type_index = types_to_index[brick.meta()]
            write(pack_H(brick_type_index))

            subbuffer = bytearray()

            # 2. Properties
            # Num of properties
            num_properties = len(brick.ppatch)
            subbuffer.extend(pack_B(num_properties))  # B → uint8
            # Each property
            ppatch_items = brick.ppatch.items()
            for prop, value in ppatch_items:
                prop_index = prop_to_index[prop]  # Key index
                sub_list = value_to_index[prop_index]  # Where to get vals → index of this property
                value_index = sub_list[value]  # Value index
                # Add key and value to subbuffer
                subbuffer.extend(pack_H(prop_index))  # <H → LE uint16
                subbuffer.extend(pack_H(value_index))  # <H → LE uint16

            # 3. Position and rotation
            # For loop to reduce code repetition
            for v in (brick.pos.x, brick.pos.y, brick.pos.z, brick.rot.y, brick.rot.z, brick.rot.x):
                subbuffer.extend(pack_f(v))  # <f → Single-precision LE float
            # 4. Write len and write to buffer
            write(pack_I(len(subbuffer)))  # <I → LE uint32
            write(subbuffer)

        return bytearray(buffer.getvalue())



    def deserialize(self, buffer: bytes | bytearray | io.BytesIO) -> None:
        """Deserialize a bytearray into this vehicle.

        Args:
            buffer (bytes): Bytearray to deserialize
        """

        # Change the type of the buffer to something we want
        if not isinstance(buffer, io.BytesIO):
            buffer = io.BytesIO(buffer)

        # No repeated global lookups and stuff
        read = buffer.read
        pmeta_registry_get = _p.pmeta_registry.get
        BrickError = _e.BrickError
        unpack_B = struct.Struct('B').unpack
        unpack_H = struct.Struct('<H').unpack
        unpack_I = struct.Struct('<I').unpack
        unpack_6f = struct.Struct('<6f').unpack


        # --------1. HEADER
        self.bricks.clear()
        self.version, = unpack_B(read(1))

        num_bricks, = unpack_H(read(2))
        num_brick_types, = unpack_H(read(2))
        num_properties, = unpack_H(read(2))

        # --------2. BRICK TYPES
        # print(buffer.getvalue()[buffer.tell():])
        brick_types_list = [read(unpack_B(read(1))[0]).decode('ascii') for _ in range(num_brick_types)]


        # --------3. PROPERTIES
        # This will bind to each property a list,
        # where for each index
        # we can find its corresponding value.
        # defaultdict will make sure we can append values to keys yet to be added
        property_names_list = []
        prop_to_index_to_value = defaultdict(list)

        for i in range(num_properties):
            # print(buffer.getvalue()[buffer.tell():])
            # Property name
            prop_len, = unpack_B(read(1))
            prop = read(prop_len).decode('ascii')
            # Add it to the list of index → property
            property_names_list.append(prop)
            # Get property's deserializer for later
            prop_deserialization_class = pmeta_registry_get(prop)
            if prop_deserialization_class is None:
                raise BrickError(f"Unknown property '{prop}'")

            # Number of values for this property
            num_values, = unpack_H(read(2))
            # Byte length of the property's values
            len_binaries, = unpack_I(read(4))

            # Get properties in a separate buffer
            property_buffer = io.BytesIO(read(len_binaries))
            read_property = property_buffer.read

            # print(f'{num_values=}, {len_binaries=},'
            #       f'{property_buffer.getvalue()[property_buffer.tell():]},
            #       f'\n{buffer.getvalue()[buffer.tell():]}')

            # Figure out the length of each element
            if num_values > 1:

                # Read the length of the first probable element
                first_element_length, = unpack_H(read(2))
                # print(f'{first_element_length=}')
                # If it's zero, then it means each element has a different length
                if first_element_length == 0:
                    elements_length = tuple((unpack_H(read(2))[0] for _ in range(num_values)))
                # Else all elements have the same length
                else:
                    elements_length = tuple((first_element_length for _ in range(num_values)))

            # If there is only one value, brick rigs does not indicate it → no read_property here
            else:
                elements_length = (len_binaries,)

            for elem_length in elements_length:
                # Read the value
                # print(f'{elements_length=}, {elem_length=}')
                value = read_property(elem_length)
                deserialized_value = prop_deserialization_class.deserialize(bytearray(value), self.version)
                if deserialized_value is _p.InvalidVersion:
                    raise BrickError(f"Invalid version for property '{prop}'")
                prop_to_index_to_value[prop].append(deserialized_value)

        # -------- 4. BRICKS

        # For each brick
        for i in range(num_bricks):
            # Brick type
            # print(f'{brick_types_list=}, {buffer.getvalue()[buffer.tell()-30:buffer.tell()]}'
            #       f'|  {buffer.getvalue()[buffer.tell():]}')
            brick_type_index = unpack_H(read(2))[0]
            # print(f'{brick_type_index=}')
            brick_type_name = brick_types_list[brick_type_index]
            brick_meta = _bt.bt_registry.get(brick_type_name)
            if brick_meta is None:
                raise BrickError(f"Unknown brick type '{brick_type_name}'")

            # Properties
            # Byte length of the properties part of this brick. We do not need it
            read(4)
            # Get the number of properties
            num_properties, = unpack_B(read(1))

            # Unpack the properties
            properties: dict[str, Hashable] = {}
            for _ in range(num_properties):
                # Get the type
                type_index, = unpack_H(read(2))
                type_name = property_names_list[type_index]
                # Get the value
                value_index, = unpack_H(read(2))
                value_deserialized = prop_to_index_to_value[type_name][value_index]
                # Add the value to the list of found properties
                properties[type_name] = value_deserialized

            # Position and rotation
            pos_x, pos_y, pos_z, rot_y, rot_z, rot_x = unpack_6f(read(6 * 4))

            # Create the brick
            self.add(_brick.Brick(
                ref=f'brick_{i}',
                meta=brick_meta,
                pos=_vec.Vec3(pos_x, pos_y, pos_z),
                rot=_vec.Vec3(rot_x, rot_y, rot_z),
                ppatch=properties
            ))
