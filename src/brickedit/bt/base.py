from collections.abc import Hashable
from abc import ABC, abstractmethod

class BrickMeta(ABC):

    __slots__ = ('_name', 'p')

    def __init__(self, name: str, *args, **kwargs):
        """
        BrickMeta is a meta class for brick types:
        each brick type is an instance of a class inheriting BrickMeta.
        It holds the name of the brick type and its default properties.
        Args and kwargs are passed to base_properties and allow you to 
        """
        self._name: str = name
        self.p: dict[str, Hashable] = self.base_properties(*args, **kwargs)

    def name(self) -> str:
        return self._name

    @abstractmethod
    def base_properties(self, *args, **kwargs) -> dict[str, Hashable]:
        """
        Default properties of a brick class.
        It creates a new dictionary each time to avoid shared mutable state.
        Only ran once by brickedit to initialize self.p in __init__ of BrickMeta.
        May be used to reinitialize modded properties or inspect original properties.
        """
