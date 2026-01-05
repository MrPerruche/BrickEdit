from datetime import datetime as _datetime, timezone as _timezone


def net_ticks_now() -> int:
    """Provides the current time in the .NET DateTime ticks format.

    Returns:
        int: .NET DateTime ticks (100s of nanoseconds since 0001-01-01 00:00:00)
    """
    return to_net_ticks(_datetime.now(_timezone.utc))

def to_net_ticks(time: _datetime) -> int:
    """
    Converts the given time to .NET DateTime ticks.
    
    Args:
        time (datetime): Time to convert

    Returns:
        int: .NET DateTime Ticks (100s of nanoseconds since 0001-01-01 00:00:00)
    """

    # Get current UTC time
    time_delta = time - _datetime(1, 1, 1, tzinfo=_timezone.utc)
    return int(time_delta.total_seconds() * 1e7)
