from datetime import datetime

"""Integer subclass to represent naive time since epoch.

TimeInt values are only good for the time between
   Jan 1, 1970 -> Apr 2, 2016
These limits are available as TimeInt.MIN and TimeInt.MAX
Within this range time is rounded to the nearest second.

The idea is to have the time small for storage while making
sort comparisons quick and easy.

Also provides a method to represent the time as a string
without extraneous parts (like including time of day when
value falls on midnight, or including seconds when value
falls on a minute etc).

NOTE: although TimeInt is naive about time zone, in the
regular use of the oanda_candles package all times will
be in UTC.

"""


class TimeInt(int):
    """Integer that represents a naive time since epoch."""

    MIN = None  # Jan 1, 1970, start of epoch
    MAX = None  # Apr 2, 2106, end of epoch in 32bit

    @classmethod
    def from_unix(cls, epoch: str) -> "TimeInt":
        """TimeInt from string like "1590177600.000000000"""
        return cls(round(float(epoch)))

    @classmethod
    def utcnow(cls) -> "TimeInt":
        """Get the TimeInt for right now."""
        return TimeInt(round(datetime.utcnow().timestamp()))

    def get_datetime(self) -> datetime:
        return datetime.fromtimestamp(int(self))

    def get_pretty(self) -> str:
        """Get as formatted string leaving off parts that are 0 on end.

        For example, if the time lands on the hour, leave off minutes
        and seconds. If it happens to fall right on the second where
        a year changes, just give the year number etc.
        """
        dt = datetime.fromtimestamp(int(self))
        if dt.second:
            form = "%Y-%m-%d %I:%M:%S %p"
        elif dt.minute:
            form = "%Y-%m-%d %I:%M %p"
        elif dt.hour:
            form = "%Y-%m-%d %I %p"
        elif dt.day:
            form = "%Y-%m-%d"
        elif dt.month:
            form = "%Y-%m"
        else:
            form = "%Y"
        return dt.strftime(form)


TimeInt.MIN = TimeInt(0)
TimeInt.MAX = TimeInt(4_294_967_294)