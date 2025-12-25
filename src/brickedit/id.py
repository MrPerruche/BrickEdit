from typing import Optional

class ID:

    __slots__ = ('id', 'weld', 'editor')

    def __init__(self, id: str, weld: Optional[str] = None, editor: Optional[str] = None):
        self.id: str = id
        self.weld: Optional[str] = weld
        self.editor: Optional[str] = editor

    def __repr__(self):
        return f'ID({self.id}, {self.weld}, {self.editor})'

    def __eq__(self, other):
        return self.id == other.id and self.weld == other.weld and self.editor == other.editor