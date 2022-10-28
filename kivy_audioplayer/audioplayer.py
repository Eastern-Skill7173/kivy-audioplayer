"""
In order to integrate and utilize every platform's native media player,
before importing the module you must set the
"NATIVE_AUDIO_PLAYER" environmental variable
to a list of platforms separated with a comma.
As an example, to integrate the player with android and windows:

    import os

    os.environ["PLATFORM_AUDIO_PLAYER_INTEGRATION"] = "android,windows"

    # You must do this before importing the audio player module

    from utils.audioplayer import AudioPlayer
    ...

Currently supported platforms are:
    android: `android`

Soon to be integrated:
    windows: `win`
    linux: `linux`
"""

import os
from typing import Iterable
from kivy_audioplayer.type_aliases import Number, SoundType
from kivy_audioplayer._conversions import (
    NumberConversion,
    SoundTypeConversion,
)
from kivy_audioplayer._utils import (
    humanize_duration,
    normalize_index,
)
from kivy.utils import platform
from kivy.clock import Clock
from kivy.core.audio import SoundLoader, Sound

__all__ = (
    "AudioPlayer",
)


# TODO: integrate player with windows and linux
if platform in os.getenv("NATIVE_AUDIO_PLAYER", '').split(','):
    if platform == "android":
        from kivy_audioplayer._os_integration.\
            _android_player import AndroidSoundPlayer
        SoundLoader.register(AndroidSoundPlayer)
    elif platform == "linux":
        from kivy_audioplayer._os_integration.\
            _linux_player import LinuxSoundPlayer
        SoundLoader.register(LinuxSoundPlayer)
    elif platform == "win":
        from kivy_audioplayer._os_integration.\
            _windows_player import WindowsSoundPlayer
        SoundLoader.register(WindowsSoundPlayer)


class AudioPlayer:
    """
    Audio player class for extending standard `SoundLoader` functionalities,
    including:
    queuing, fast forwarding, rewinding, global volume, extended states...
    This class has the most integration with ffmpeg & the `ffpyplayer` package.
    In order to switch your audio provider, check out:
    https://kivy.org/doc/stable/guide/environment.html#restrict-core-to-specific-implementation

    BUG:
        In kivy 2.1.0, calling `.stop()` on an audio file and then `.play()`
        causes audio to restart from beginning. When tested on 2.0.0, the error
        was not there.
    """
    _aliases = {}
    """
    Private dictionary containing aliases
    """

    def __init__(self,
                 queue: Iterable = (),
                 volume: Number = 1,
                 loop: bool = False,
                 estimate_position: bool = True,
                 interval: Number = 1):
        self._external_stop_call = False
        self._queue_progress_index = -1
        self._queue = []
        self._volume = volume
        self.load(*queue)
        self._loop = loop
        self._estimate_position = estimate_position
        self._interval = interval
        self._pos_estimate = 0
        self._state = "queue empty"
        self._clock_event = None
        self._current_sound_obj = None

    def __repr__(self) -> str:
        return "{0}(length={1}, loop={2}".format(
            type(self).__name__,
            self.__len__(),
            self._loop,
        )

    def __iter__(self):
        for sound_obj in self._queue[self._queue_progress_index + 1:]:
            yield sound_obj

    def __len__(self) -> int:
        return len(self._queue[self._queue_progress_index + 1:])

    def __contains__(self, item) -> bool:
        return item in self._queue[self._queue_progress_index + 1:]

    @classmethod
    def aliases(cls) -> dict:
        """
        Class-method to return the currently registered aliases

        Returns
        -------
        dict
            A dictionary containing containing the registered aliases as
            keys (Any) and holding the respective value (Sound, str or Path)
        """
        return cls._aliases.copy()

    @classmethod
    def register(cls, alias, value: SoundType) -> None:
        """
        Class-method to register a sound object or a string
        as an easily accessible alias

        Parameters
        ----------
        alias : Any
            Alias to be used for the value
        value : SoundType
            The value to be registered with the given alias

        Returns
        -------
        None
        """
        SoundTypeConversion.is_allowed(value)
        cls._aliases[alias] = value

    @classmethod
    def get_alias(cls, alias, default_value=None):
        """
        Class-method to get a registered alias's value

        Parameters
        ----------
        alias : Any
            Alias that is registered with the value
        default_value : Any
            Value to return if the given alias could not be found
            (default is None)

        Returns
        -------
        Any
            Returns the sound type (Sound, str or Path) associated
            with the registered alias if found else return the
            previously passed `default_value`
        """
        return cls._aliases.get(alias, default_value)

    def _update_pos_estimate(self, position: Number) -> None:
        """
        Private method to update the position estimate
        with the given position in seconds

        Parameters
        ----------
        position : Number
            New position of the current audio file in seconds

        Returns
        -------
        None
        """
        self._pos_estimate = position

    def _cancel_clock(self) -> None:
        """
        Private method to cancel `self._clock_event`

        Returns
        -------
        None
        """
        self._clock_event.cancel()

    def _start_clock(self) -> None:
        """
        Private method to start a clock for updating the position estimate
        every `self._interval`

        Returns
        -------
        None
        """
        self._clock_event = Clock.schedule_interval(
            lambda dt: self._update_pos_estimate(
                self._pos_estimate + self._interval
            ),
            self._interval
        )

    def _initialize_estimation(self) -> None:
        """
        Private method to be bound to every sound object's `on_play` event
        to initialize the clock for position estimation if enabled

        Returns
        -------
        None
        """
        if self._estimate_position:
            self._start_clock()

    def _cancel_estimation(self) -> None:
        """
        Private method to be bound to every sound object's `on_stop` event
        to cancel the clock to prevent inaccurate position estimation
        (if enabled during initialization)

        Returns
        -------
        None
        """
        if self._estimate_position:
            self._cancel_clock()
        if not self._external_stop_call:
            self._update_pos_estimate(0)
            self.skip_to_next(stop_current_playback=False)

    def _set_current_sound_obj(self) -> None:
        """
        Private method to set the current sound object to
        the queue progression element retrieved using its index from the queue

        Returns
        -------
        None
        """
        self._current_sound_obj = self._queue[self._queue_progress_index]

    def _jump_to_index(self, index: int) -> None:
        """
        Private method to jump to the given index in the queue

        Parameters
        ----------
        index : int
            Index of the queue to jump to

        Returns
        -------
        None
        """
        try:
            self._queue_progress_index = index
            self._set_current_sound_obj()
        except IndexError:
            self._queue_progress_index = -1
            self._current_sound_obj = None
            if self._loop:
                self.play()

    def _configure_sound_obj(self, sound_obj: Sound) -> None:
        """
        Private method to configure a sound object to match player behavior.
        (Set its volume to globally declared volume,
        Bind `on_play` & `on_stop` methods...)

        Parameters
        ----------
        sound_obj : Sound
            The sound object to be configured

        Returns
        -------
        None
        """
        sound_obj.volume = self._volume
        sound_obj.bind(
            on_play=lambda sound: self._initialize_estimation()
        )
        sound_obj.bind(
            on_stop=lambda sound: self._cancel_estimation()
        )

    def clear_queue(self) -> None:
        """
        Method to clear what is in the queue

        Returns
        -------
        None
        """
        self._queue.clear()

    def load(self,
             *args: SoundType,
             clear_previous_queue: bool = False,
             ignore_aliases: bool = False) -> None:
        """
        Method to add audio files to queue

        Parameters
        ----------
        *args : SoundType
            List of strings representing individual paths
            to audio files or pre-initialized sound objects
        clear_previous_queue : bool
            Clear whatever is in the queue before loading new files
            (default is False)
        ignore_aliases : bool
            Whether to avoid fetching given values from registered aliases
            (default is False)

        Returns
        -------
        None
        """
        if clear_previous_queue:
            self.clear_queue()
        for audio_file in args:
            if not ignore_aliases:
                found_alias = self.get_alias(audio_file)
                if found_alias:
                    audio_file = found_alias
            sound_obj = SoundTypeConversion.as_sound_obj(audio_file)
            self._configure_sound_obj(sound_obj)
            self._queue.append(sound_obj)
        if self._queue:
            self._state = "queue loaded"

    def unload(self) -> None:
        """
        Method to de-activate and shutdown the audio player

        Returns
        -------
        None
        """
        if self._current_sound_obj:
            self._current_sound_obj.unload()
        self._queue.clear()
        self._state = "queue empty"

    def play(self) -> None:
        """
        Method to start playing the current audio file.
        If none, then advance in queue to load the next

        Returns
        -------
        None
        """
        if not self._current_sound_obj:
            self._jump_to_index(0)
        self._current_sound_obj.play()
        self._state = "play"

    def stop(self) -> None:
        """
        Method to pause the current audio file.
        This method will set `self._external_stop_call` to `True`
        when called to indicate that the stopping was from the wrapper class

        Returns
        -------
        None
        """
        self._external_stop_call = True
        self._current_sound_obj.stop()
        self._state = "stop"
        self._external_stop_call = False

    def get_pos(self) -> Number:
        """
        Method to get the position of the current audio file

        Returns
        -------
        Number
            The position of the current audio file in numeric format
        """
        return self._current_sound_obj.get_pos()

    def seek(self, position: Number) -> None:
        """
        Method to jump to the given position in the current audio file

        Parameters
        ----------
        position : Number
            Position to jump to in seconds

        Returns
        -------
        None
        """
        self._current_sound_obj.seek(position)

    def fast_forward(self, seconds: Number = 10) -> None:
        """
        Method to skip the next given seconds in the current audio file

        Parameters
        ----------
        seconds : Number
            Jump/Skip duration in seconds (int or float)

        Returns
        -------
        None
        """
        current_song_position = self.get_pos()
        current_song_length = self.length
        if current_song_length - current_song_position > seconds:
            new_position = current_song_position + seconds
        else:
            new_position = current_song_length
        self.seek(new_position)
        if self._estimate_position:
            self._update_pos_estimate(new_position)

    def rewind(self, seconds: Number = 10) -> None:
        """
        Method to go back in the next given seconds in the current audio file

        Parameters
        ----------
        seconds : Number
            Duration to rewind/jump back to in seconds (int or float)

        Returns
        -------
        None
        """
        current_song_position = self.get_pos()
        if current_song_position > seconds:
            new_position = current_song_position - seconds
        else:
            new_position = 0
        self.seek(new_position)
        if self._estimate_position:
            self._update_pos_estimate(new_position)

    def skip_to_next(self,
                     play_immediately: bool = True,
                     stop_current_playback: bool = True,
                     restart_audio_position: bool = True) -> None:
        """
        Method to load the next audio file in the queue

        Parameters
        ----------
        play_immediately : bool
            Whether to play the next track immediately or just load it
            (default is True)
        stop_current_playback : bool
            Whether to call `self.stop` on the current audio file
            (default is True)
        restart_audio_position : bool
            Whether to reset the position of the current audio file
            (default is True)

        Returns
        -------
        None
        """
        if stop_current_playback:
            self.stop()
        self._jump_to_index(self._queue_progress_index + 1)
        if restart_audio_position:
            self.seek(0)
        if play_immediately:
            self.play()

    def skip_to_previous(self,
                         play_immediately: bool = True,
                         stop_current_playback: bool = True,
                         restart_audio_position: bool = True) -> None:
        """
        Method to load the previous audio file in the queue

        Parameters
        ----------
        play_immediately : bool
            Whether to play the previous track immediately or just load it
            (default is True)
        stop_current_playback : bool
            Whether to call `self.stop` on the current audio file
            (default is True)
        restart_audio_position : bool
            Whether to reset the position of the current audio file
            (default is True)

        Returns
        -------
        None
        """
        if stop_current_playback:
            self.stop()
        self._jump_to_index(
            normalize_index(self._queue, self._queue_progress_index - 1)
        )
        if restart_audio_position:
            self.seek(0)
        if play_immediately:
            self.play()

    @property
    def queue_progress_index(self) -> int:
        return self._queue_progress_index

    @property
    def state(self) -> str:
        return self._state

    @property
    def source(self) -> str:
        return self._current_sound_obj.source

    @property
    def length(self) -> float:
        return self._current_sound_obj.length

    @property
    def human_readable_length(self) -> str:
        return humanize_duration(self.length)

    @property
    def volume(self) -> Number:
        return self._volume

    @volume.setter
    def volume(self, new_volume: Number) -> None:
        NumberConversion.is_allowed(new_volume)
        if 0 > new_volume > 1:
            raise ValueError("volume can only be from 0-1")
        self._volume = new_volume
        for sound_obj in self._queue:
            sound_obj.volume = self._volume

    @property
    def pos_estimate(self) -> Number:
        return self._pos_estimate

    @property
    def human_readable_pos_estimate(self) -> str:
        return humanize_duration(self._pos_estimate)
