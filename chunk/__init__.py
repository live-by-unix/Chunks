import sys
import types
from .core import chunk, set_chunk_size

_module = sys.modules[__name__]

class _ChunkModule(types.ModuleType):
    def __setattr__(self, name, value):
        if name == "chunk_size":
            set_chunk_size(value)
        else:
            super().__setattr__(name, value)

_module.__class__ = _ChunkModule
_module.chunk = chunk
