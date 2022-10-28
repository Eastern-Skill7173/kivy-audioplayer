from pathlib import Path
from typing import Tuple
from kivy.core.audio import Sound, SoundLoader
from kivy_audioplayer.type_hints import (
    Number,
    PathType,
    SoundType,
)

__all__ = (
    "NumberConversion",
    "PathTypeConversion",
    "SoundTypeConversion",
)


class _TypeHintConversion:
    """
    Class for storing information about a type (hint)
    such as:

        * the allowed types (can be accessed by `cls.allowed_types()`)
        * the conversion methods between the allowed types
        (defined by the subclasses not this base class)

    This base class does not define the conversion methods itself
    the extra methods must be declared inside of each individual subclass
    """
    _allowed_types = ()

    @classmethod
    def allowed_types(cls) -> Tuple[type, ...]:
        """
        Classmethod to return the designated allowd types

        Returns
        -------
        Tuple[type, ....]
            A tuple containing the allowed/designated types
        """
        return cls._allowed_types

    @classmethod
    def is_allowed(cls, obj):
        """
        Checker classmethod to see if the passed object
        is of the previously declared types

        Parameters
        ----------
        obj : Any
            object to check its type against the allowed types of the class

        Returns
        -------
        None
        
        Raises
        ------
        TypeError
            If the given object is not of the acceptable types
            then a TypeError is raised
        """
        if not isinstance(obj, cls._allowed_types):
            raise TypeError(
                "only {0} types are accepted".format(cls._allowed_types)
            )


class NumberConversion(_TypeHintConversion):
    """
    Class for storing information about the `Number` type hint,
    containing the conversion methods:

        * `as_int` classmethod to convert a number type to an int
        * `as_float` classmethod to convert a number type to a float

    """
    _allowed_types = (int, float)

    @classmethod
    def as_int(cls, number: Number) -> int:
        """
        Classmethod to convert any number type (eiter `int` or `float`)
        to the converted integer

        Parameters
        ----------
        number : Number
            Number type (`int` or `float`) to be converted

        Returns
        -------
        int
            An integer representing the converted number
        """
        return int(number)

    @classmethod
    def as_float(cls, number: Number) -> float:
        """
        Classmethod to convert any number type (eiter `int` or `float`)
        to the float equivalent value

        Parameters
        ----------
        number : Number
            Number type (`int` or `float`) to be converted

        Returns
        -------
        float
            A float representing the converted number
        """
        return float(number)


class PathTypeConversion(_TypeHintConversion):
    """
    Class for storing information about the `PathType` type hint,
    containing the conversion methods:

        * `as_str` classmethod to convert a path type to a string
        * `as_path_obj` classmethod to convert a path type to a path obj

    """
    _allowed_types = (str, Path)

    @classmethod
    def as_str(cls, path: PathType) -> str:
        """
        Classmethod to convert any path type (eiter `str` or `pathlib.Path`)
        to the equivalent string

        Parameters
        ----------
        path : PathType
            path type (`str` or `pathlib.Path`) to be converted

        Returns
        -------
        str
            A string representing the equivalent path
        """
        return str(path)

    @classmethod
    def as_path_obj(cls, path: PathType) -> Path:
        """
        Classmethod to convert any path type (either `str` or `pathlib.Path`)
        to the equivalent path object

        Parameters
        ----------
        path : PathType
            path type (`str` or `pathlib.Path`) to be converted

        Returns
        -------
        pathlib.Path
            A pathlib.Path object representing the equivalent path
        """
        return Path(path)


class SoundTypeConversion(_TypeHintConversion):
    """
    Class for storing information about the `SoundType` type hint,
    containing the conversion methods:

        * `as_str` classmethod to convert a sound type to a string
        * `as_path_obj` classmethod to convert a sound type to a path obj
        * `as_sound_obj` classmethod to convert a sound type
        to a kivy sound obj

    """
    _allowed_types = (str, Path, Sound)

    @classmethod
    def as_str(cls, sound: SoundType) -> str:
        """
        Classmethod to convert any sound type (`str`, `pathlib.Path`
        or `kivy.core.audio.Sound`) to the equivalent audio path

        Parameters
        ----------
        sound : SoundType
            sound type (`str`, `pathlib.Path` or `kivy.core.audio.Sound`)
            to be converted

        Returns
        -------
        str
            A string representing the audio file path
        """
        if isinstance(sound, Sound):
            return sound.source
        return str(sound)

    @classmethod
    def as_path_obj(cls, sound: SoundType) -> Path:
        """
        Classmethod to convert any sound type (`str`, `pathlib.Path`
        or `kivy.core.audio.Sound`) to the equivalent audio file path object

        Parameters
        ----------
        sound : SoundType
            sound type (`str`, `pathlib.Path` or `kivy.core.audio.Sound`)
            to be converted

        Returns
        -------
        pathlib.Path
            A pathlib.Path object representing the
            equivalent audio file path object
        """
        if isinstance(sound, Sound):
            return Path(sound.source)
        return Path(sound)

    @classmethod
    def as_sound_obj(cls, sound: SoundType) -> Sound:
        """
        Classmethod to convert any sound type (`str`, `pathlib.Path`
        or `kivy.core.audio.Sound`) to the loaded sound object

        Parameters
        ----------
        sound : SoundType
            sound type (`str`, `pathlib.Path` or `kivy.core.audio.Sound`)
            to be converted

        Returns
        -------
        kivy.core.audio.Sound
            A loaded sound object referring to the audio path
        """
        if isinstance(sound, Sound):
            return sound
        return SoundLoader.load(cls.as_str(sound))
