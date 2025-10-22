"""BRV file handling."""
import struct
from typing import Self, Optional, Iterable, Any
#from ..brick import Brick
from . import brick as _brick
from . import var as _var
from . import bt as _bt
from . import p as _p
from . import exceptions as _e
#from ..var import FILE_EXP_VERSION

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

        # --------1. HEADER

        # Version Byte
        buffer = bytearray(struct.pack('B', self.version))  # B → uint8

        # Number of bricks
        buffer.extend(struct.pack('<H', len(self.bricks)))  # <H → LE uint16

        # Number of unique brick types. No .name, strings are larger objects
        types: set[_bt.BrickMeta] = set(brick.meta() for brick in self.bricks)
        types_to_index: dict[_bt.BrickMeta, int] = {
            bt: i for i, bt in enumerate(types)
        }
        buffer.extend(struct.pack('<H', len(types)))  # <H → LE uint16

        # ---- Building property dicts (hardest part, I NEED comments yet I hate commenting)


        # A dictionary that will for each property give us its index
        prop_to_index: dict[str, int] = {}
        # A list that for each property index will give us the dict of values : index
        value_to_index: list[dict[Any, int]] = [{}]
        # A list that for each prop gives {for each value index gives us its serialized version}
        indexes_to_serialized: list[list[bytearray]] = []
        # A list of reference to brick index for source brick properties
        reference_to_brick_index: dict[str, int] = {b.ref: i+1 for i, b in enumerate(self.bricks)}

        # Exploring all bricks
        for brick in self.bricks:

            # Exploring all properties
            for prop, value in brick.ppatch.items():

                if value is None:
                    continue

                # Get the serialization class and make sure it's valid
                prop_serialization_class = _p.pmeta_registry.get(prop)
                if prop_serialization_class is None:
                    raise _e.BrickError(f"Property {prop!r} from brick {brick!r}"
                                        "does not have any serialization class registered.")

                # Put in the lists if it's not already
                if prop not in prop_to_index:
                    prop_to_index[prop] = len(prop_to_index)
                    value_to_index.append({})
                    indexes_to_serialized.append([])

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
                    raise _e.BrickError(f'Unhashable value {value!r} for property {prop!r}'
                                        f'of brick {brick!r}. Do not use lists. Use Vec or tuples.')


        # ---- Back to header!
        buffer.extend(struct.pack('<H', len(prop_to_index)))  # <H → LE uint16


        # --------2. BRICK TYPES
        for t in types:
            # Len of t then t
            buffer.extend(struct.pack('B', len(t.name())))  # B → uint8
            buffer.extend(t.name().encode('ascii'))


        # --------3. PROPERTIES
        for prop, prop_index in prop_to_index.items():

            # Encode the property -- Len of prop then prop
            buffer.extend(struct.pack('B', len(prop)))  # B → uint8
            buffer.extend(prop.encode('ascii'))

            # Number of properties
            num_values = len(value_to_index[prop_index])
            buffer.extend(struct.pack('<H', num_values)) # <H → LE uint16

            # Write the properties:
            # Get the sum of all properties
            binaries = indexes_to_serialized[prop_index]
            sum_binaries = bytearray()
            for binary in binaries:
                sum_binaries.extend(binary)
            # Write the length
            buffer.extend(struct.pack('<I', len(sum_binaries)))  # <I → LE uint32
            # Write the values
            buffer.extend(sum_binaries)

            # Property footer
            # If 1 element, no footer
            if num_values > 1:
                # If all elements are of the same length, only show the length of one (the 1st)
                if all(b == binaries[0] for b in binaries):
                    buffer.extend(struct.pack('<H', len(binaries[0])))
                # Else elements have different lenghts, write 0 then length of each element
                else:
                    buffer.extend(b'\x00\x00')  # (LE uint16) 0
                    for binary in binaries:
                        buffer.extend(struct.pack('<H', len(binary)))


        # --------4. BRICKS

        # Remember. Index starts at 1 here because fluppi
        for brick in self.bricks:

            # 1. Brick Type
            brick_type_index = types_to_index[brick.meta()]
            buffer.extend(struct.pack('<H', brick_type_index))  # <H → LE uint16

            subbuffer = bytearray()

            # 2. Properties
            # Num of properties
            num_properties = len(brick.ppatch)
            subbuffer.extend(struct.pack('B', num_properties))  # B → uint8
            # Each property
            for prop, value in brick.ppatch.items():
                prop_index = prop_to_index[prop]  # Key index
                sub_list = value_to_index[prop_index]  # Where to get vals → index of this property
                value_index = sub_list[value]  # Value index
                # Add key and value to subbuffer
                subbuffer.extend(struct.pack('<H', prop_index))  # <H → LE uint16
                subbuffer.extend(struct.pack('<H', value_index))  # <H → LE uint16

            # 3. Position and rotation
            # For loop to reduce code repetition
            for v in (brick.pos.x, brick.pos.y, brick.pos.z, brick.rot.y, brick.rot.z, brick.rot.x):
                subbuffer.extend(struct.pack('<f', v))  # <f → Single-precision LE float
            # 4. Write len and write to buffer
            buffer.extend(struct.pack('<I', len(subbuffer)))  # <I → LE uint32
            buffer.extend(subbuffer)

        return buffer



    def deserialize(self, buffer: bytes) -> None:
        """Deserialize a bytearray into this vehicle.

        Args:
            buffer (bytes): Bytearray to deserialize
        """

        self.bricks.clear()

        self.version = struct.unpack('B', buffer[0:1])[0]

        num_bricks = struct.unpack('<H', buffer[1:3])[0]

        print(f"{self.version=}")
        print(f"{num_bricks=}")

        types = set()
        index_to_type = {} # proceeds to not even use this
        index_to_prop = {}
        index_to_value = [{}]
        serialized_to_indexes = []

        num_types = struct.unpack('<H', buffer[3:5])[0]
        print(f"{num_types=}")
        num_properties = struct.unpack('<H', buffer[5:7])[0]
        print(f"{num_properties=}")

        pointer = 7
        tmp_pointer = pointer

        for _ in range(num_types):
            type_name_len = struct.unpack('B', buffer[pointer: pointer + 1])[0]
            pointer += 1
            type_name = buffer[pointer : pointer + type_name_len].decode('ascii')
            types.add(type_name)
            pointer += type_name_len

        print(f"{types=}")

        #property_index = 0
        for _ in range(num_properties):
            print(f"\nproperty... {pointer=}, {tmp_pointer=}, {pointer-tmp_pointer=}\n")
            # one byte for how long the property name is
            prop_name_len = struct.unpack('B', buffer[pointer: pointer + 1])[0]
            pointer += 1
            # the actual name of this property
            prop_name = buffer[pointer : pointer + prop_name_len].decode('ascii')
            # i have no idea what im doing with index_to_xyz anymore...! just trying to reverse serialize
            index_to_prop[len(index_to_prop)] = prop_name
            index_to_value.append({})
            pointer += prop_name_len

            # property class that we need to use
            prop_serialization_class = _p.pmeta_registry.get(prop_name)
            if prop_serialization_class is None:
                raise _e.BrickError(f"Property '{prop_name}' does not exist in the registry.")

            print(f"{prop_serialization_class=}")

            # the number of values the header tells us to expect.
            num_values_expected = struct.unpack('<H', buffer[pointer: pointer + 2])[0]
            pointer += 2

            print(f"{num_values_expected=}")

            # total length of all of the values.
            total_len_values = struct.unpack('<I', buffer[pointer: pointer + 4])[0]
            pointer += 4

            print(f"{total_len_values=}")

            # read way past that to get to the actual uint16[] of their lengths

            value_lens = []

            if num_values_expected > 1:
                tmp_pointer = pointer + total_len_values
                # we currently have no idea how long the values are
                # we can ... probably ... assume that no value is 0 bytes long, therefore,
                # we can make an easy check to see if the next 2 bytes == \x00\x00
                print(f"{buffer[tmp_pointer:tmp_pointer+2]=}")
                if buffer[tmp_pointer:tmp_pointer+2] == b'\x00\x00':
                    # if so, we can just start at the next 2 bytes and read num_values_expected uint16s...
                    tmp_pointer += 2
                    for _ in range(num_values_expected):
                        value_lens.append(struct.unpack('<H', buffer[tmp_pointer:tmp_pointer + 2])[0])
                        tmp_pointer += 2
                else:
                    # if not, then everyone is the same length. become an int.
                    value_lens = struct.unpack('<H', buffer[tmp_pointer:tmp_pointer + 2])[0]
                    tmp_pointer += 2

            else:
                value_lens = total_len_values # The optimized nature of a BRV file
                # means the uint16 array simply DOESN'T EXIST if there is only one value.

            print(f"{value_lens=}")


            # i took it that im not supposed to iterate over values here, so i commented it. this is what i *was* doing though.
            #for i in range(num_values_expected):
            #    if isinstance(value_lens, int):
            #        buffer_slice = buffer[pointer: pointer + value_lens]
            #        pointer += value_lens
            #    else:
            #        buffer_slice = buffer[pointer: pointer + value_lens[i]]
            #        pointer += value_lens[i]
            #    deserialized_value = prop_serialization_class.deserialize(buffer_slice, self.version)
            #    print(f"{deserialized_value=}")
            #    if prop_name not in index_to_value[-1]:
            #        index_to_value[-1][prop_name] = deserialized_value
            #    else:
            #        # ... assume we're adding to a list
            #        if not isinstance(index_to_value[-1][prop_name], list):
            #            index_to_value[-1][prop_name] = [index_to_value[-1][prop_name]]
            #        index_to_value[-1][prop_name].append(deserialized_value)
            print(f"moving tm {pointer=} {tmp_pointer=}")
            pointer = tmp_pointer if num_values_expected > 1 else pointer

            print(f"{index_to_value=}")

