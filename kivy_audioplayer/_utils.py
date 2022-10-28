import datetime
from typing import Sequence

__all__ = (
    "humanize_duration",
    "normalize_index",
)


def humanize_duration(
    seconds: int,
    remove_leading_zero: bool = True
) -> str:
    """
    Utility function to return a humanized version of a
    duration in seconds through a string

    Parameters
    ----------
    remove_leading_zeros : bool
        Whether to remove leading zeros if the position
        estimate is less than an hour or is less than 10
        minutes (default is True)

    Returns
    -------
    str
        A string indicating the passed duration
        through a human readable format (H:M:S)
    """
    human_readable_duration = str(
        datetime.timedelta(seconds=seconds)
    )
    if remove_leading_zero:
        if seconds < 3600:
            _, string_minutes, string_seconds = \
                human_readable_duration.split(':')
            if seconds < 10 * 60:
                parsed_minutes = string_minutes[1]
            else:
                parsed_minutes = string_minutes
            human_readable_duration = "{0}:{1}".format(
                parsed_minutes, string_seconds
            )
    return human_readable_duration


def normalize_index(
    sequence: Sequence,
    index: int,
) -> int:
    """
    Utility function to convert a reverse index to a standard one

    Parameters
    ----------
    index : int
        Index to be checked then converted

    Returns
    -------
    int
        The normalized version of the index if index is
        not reversed (index > 0) else returns the original index

    Raises
    ------
    IndexError
        If the given index is out of the sequence's range
        (whether reversed or normal) then an IndexError is raised
    """
    sequence_length = len(sequence)
    if index < 0:
        if abs(index) > sequence_length:
            raise IndexError("sequnece index is out of range")
        return sequence_length + index
    else:
        if index > sequence_length - 1:
            raise IndexError("sequence index is out of range")
        return index
