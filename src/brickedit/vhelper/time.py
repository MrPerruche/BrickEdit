from datetime import datetime as _datetime, timezone as _timezone, timedelta as _timedelta


DOTNET_EPOCH = _datetime(1, 1, 1, tzinfo=_timezone.utc)

def net_ticks_now() -> int:
    """Provides the current time in the .NET DateTime ticks format.

    Returns:
        int: .NET DateTime ticks (100s of nanoseconds since 0001-01-01 00:00:00)
    """
    return to_net_ticks(_datetime.now(_timezone.utc))


def to_net_ticks(dt: _datetime) -> int:
    """
    Converts the given datetime to .NET DateTime ticks.

    Args:
        dt (datetime): Time to convert

    Returns:
        int: .NET DateTime ticks (100 ns since 0001-01-01 00:00:00)
    """

    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=_timezone.utc)

    delta = dt - DOTNET_EPOCH

    return (
        delta.days * 86400 * 10_000_000 +
        delta.seconds * 10_000_000 +
        delta.microseconds * 10
    )

def from_net_ticks(time: int) -> _datetime:
    """
    Converts the given .NET DateTime ticks to a datetime object.

    Args:
        time (int): .NET DateTime ticks (100s of nanoseconds since 0001-01-01 00:00:00)

    Returns:
        datetime: Converted datetime object
    """
    
    return DOTNET_EPOCH + _timedelta(microseconds=time // 10)