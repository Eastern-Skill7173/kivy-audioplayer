from pathlib import Path
from kivy.core.audio import Sound
from typing import Union

__all__ = (
    "Number",
    "PathType",
    "SoundType",
)


Number = Union[int, float]
PathType = Union[str, Path]
SoundType = Union[PathType, Sound]
