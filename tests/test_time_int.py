from time_int import __version__, TimeInt, TimeTruncUnit
from calendar import timegm
from datetime import datetime, timezone
from time import struct_time, gmtime
import pytest


def test_version():
    assert __version__ == "0.0.8"


def test_end_of_week_stamp():
    """Testing specific stamp Friday evening at 8:59 pm."""
    # This specific time is to give me confidence that values are really UAC and
    # not my local timezone. Got int from the last 1 minute candle downloaded
    # from the forex broker Oanda for a trading week. Forex trading weeks
    # end when it is 5pm in New York thus the last 1 minute candle would
    # start at 4:59 pm in New York, which means 8:59 pm in UTC.
    stamp_9_11_8_59_pm = 1599857940
    ti = TimeInt(stamp_9_11_8_59_pm)
    assert ti.year == 2020
    assert ti.month == 9
    assert ti.day == 11
    assert ti.weekday == 5
    assert ti.hour == 20
    assert ti.minute == 59
    assert ti.second == 0
    assert ti.get_pretty() == "2020-09-11 08:59 PM"


@pytest.mark.parametrize(
    "year,month,day,hour,minute,second",
    [
        (1970, 1, 1, 0, 0, 0),
        (2999, 12, 31, 23, 59, 59),
        (3000, 1, 1, 0, 0, 0),
        (2018, 5, 4, 4, 32, 49),
        (2020, 9, 11, 0, 0, 4),
        (2099, 12, 31, 11, 59, 59),
        (2299, 12, 31, 11, 59, 59),
    ],
)
def test_time(year, month, day, hour, minute, second):
    dt = datetime(
        year=year,
        month=month,
        day=day,
        hour=hour,
        minute=minute,
        second=second,
        tzinfo=timezone.utc,
    )
    dt_minute = datetime(
        year=year,
        month=month,
        day=day,
        hour=hour,
        minute=minute,
        second=0,
        tzinfo=timezone.utc,
    )
    dt_hour = datetime(
        year=year,
        month=month,
        day=day,
        hour=hour,
        minute=0,
        second=0,
        tzinfo=timezone.utc,
    )
    dt_day = datetime(
        year=year, month=month, day=day, hour=0, minute=0, second=0, tzinfo=timezone.utc
    )
    dt_month = datetime(
        year=year, month=month, day=1, hour=0, minute=0, second=0, tzinfo=timezone.utc
    )
    dt_year = datetime(
        year=year, month=1, day=1, hour=0, minute=0, second=0, tzinfo=timezone.utc
    )
    time_minute = TimeInt(dt_minute.timestamp())
    time_hour = TimeInt(dt_hour.timestamp())
    time_day = TimeInt(dt_day.timestamp())
    time_month = TimeInt(dt_month.timestamp())
    time_year = TimeInt(dt_year.timestamp())
    time = TimeInt(dt.timestamp())
    # time attrs equal to dt counterpart
    dt2 = time.get_datetime()
    assert time.year == dt.year == dt2.year
    assert time.month == dt.month == dt2.month
    assert time.day == dt.day == dt2.day
    assert time.hour == dt.hour == dt2.hour
    assert time.minute == dt.minute == dt2.minute
    assert time.second == dt.second == dt2.second
    assert dt == dt2
    # For TimeInt week starts at Sunday, for datetime its Monday.
    assert time.weekday == (dt.weekday() + 1) % 7
    # times greater than their truncated parts
    assert time >= time_minute
    assert time >= time_hour
    assert time >= time_day
    assert time >= time_month
    assert time >= time_year
    # time attrs
    assert time.second == second
    assert time.minute == minute
    assert time.hour == hour
    assert time.day == day
    assert time.month == month
    assert time.year == year
    # time_minute attrs
    assert time_minute.second == 0
    assert time_minute.minute == minute
    assert time_minute.hour == hour
    assert time_minute.day == day
    assert time_minute.month == month
    assert time_minute.year == year
    # time_hour attrs
    assert time_hour.second == 0
    assert time_hour.minute == 0
    assert time_hour.hour == hour
    assert time_hour.month == month
    assert time_hour.year == year
    # time_day attrs
    assert time_day.second == 0
    assert time_day.minute == 0
    assert time_day.hour == 0
    assert time_day.day == day
    assert time_day.month == month
    assert time_day.year == year
    # time_month attrs
    assert time_month.second == 0
    assert time_month.minute == 0
    assert time_month.hour == 0
    assert time_month.day == 1
    assert time_month.month == month
    assert time_month.year == year
    # time_year attrs
    assert time_year.second == 0
    assert time_year.minute == 0
    assert time_year.hour == 0
    assert time_year.day == 1
    assert time_year.month == 1
    assert time_year.year == year

    assert time.trunc_minute() == time_minute
    assert time.trunc_hour() == time_hour
    assert time.trunc_day() == time_day
    assert time.trunc_month() == time_month
    assert time.trunc_year() == time_year
    assert time.trunc(TimeTruncUnit.MINUTE) == time_minute
    assert time.trunc(TimeTruncUnit.HOUR) == time_hour
    assert time.trunc(TimeTruncUnit.DAY) == time_day
    assert time.trunc(TimeTruncUnit.MONTH) == time_month
    assert time.trunc(TimeTruncUnit.YEAR) == time_year


def test_time_int():
    value = 1590984783
    st = gmtime(value)
    ti = TimeInt(value)
    dt = ti.get_datetime()
    assert st.tm_zone == "UTC"
    assert dt.tzinfo == timezone.utc
    assert isinstance(ti, int)
    assert isinstance(ti, TimeInt)
    assert ti.year == st.tm_year == dt.year == 2020
    assert ti.month == st.tm_mon == dt.month == 6
    assert ti.day == st.tm_mday == dt.day == 1
    assert ti.hour == st.tm_hour == dt.hour == 4
    assert ti.minute == st.tm_min == dt.minute == 13
    assert ti.second == st.tm_sec == dt.second == 3
    assert ti > TimeInt.MIN
    assert ti < TimeInt.MAX


@pytest.mark.parametrize(
    "year,month,day,hour,minute,second,pretty",
    [
        (1970, 1, 1, 0, 0, 0, "1970"),
        (2999, 12, 31, 23, 59, 59, "2999-12-31 11:59:59 PM"),
        (3000, 1, 1, 0, 0, 0, "3000"),
        (2018, 5, 4, 0, 0, 0, "2018-05-04"),
        (2018, 5, 4, 4, 0, 0, "2018-05-04 04 AM"),
        (2018, 5, 4, 4, 32, 0, "2018-05-04 04:32 AM"),
        (2018, 5, 4, 4, 32, 49, "2018-05-04 04:32:49 AM"),
        (2020, 9, 11, 0, 0, 4, "2020-09-11 12:00:04 AM"),
        (2099, 12, 31, 11, 59, 59, "2099-12-31 11:59:59 AM"),
        (2299, 12, 31, 12, 0, 0, "2299-12-31 12 PM"),
    ],
)
def test_get_pretty(
    year: int, month: int, day: int, hour: int, minute: int, second: int, pretty: str
):
    values = (year, month, day, hour, minute, second, 0, 0, 0)
    st = struct_time(values)
    epoch = timegm(st)
    ti = TimeInt(epoch)
    assert ti.get_pretty() == pretty


def test_trunc_year():
    values = (2020, 6, 1, 4, 13, 3, 0, 0, 0)
    epoch = timegm(values)
    raw_ti = TimeInt(epoch)
    year_ti = raw_ti.trunc_year()
    assert year_ti.get_pretty() == "2020"
    ti = raw_ti.trunc_year(num=2)
    assert ti.get_pretty() == "2020"
    ti = raw_ti.trunc_year(num=3)
    assert ti.get_pretty() == "2019"
    ti = raw_ti.trunc_year(num=4)
    assert ti.get_pretty() == "2020"
    ti = raw_ti.trunc_year(num=5)
    assert ti.get_pretty() == "2020"
    ti = raw_ti.trunc_year(num=6)
    assert ti.get_pretty() == "2016"
    ti = raw_ti.trunc_year(num=10)
    assert ti.get_pretty() == "2020"
    ti = raw_ti.trunc_year(num=17)
    assert ti.get_pretty() == "2006"


def test_trunc_month():
    values = (2020, 6, 1, 4, 13, 3, 0, 0, 0)
    epoch = timegm(values)
    raw_ti = TimeInt(epoch)

    ti = raw_ti.trunc_month()
    assert ti.get_pretty() == "2020-06"
    ti = raw_ti.trunc_month(num=2)
    assert ti.get_pretty() == "2020-05"
    ti = raw_ti.trunc_month(num=3)
    assert ti.get_pretty() == "2020-04"
    ti = raw_ti.trunc_month(num=4)
    assert ti.get_pretty() == "2020-05"
    ti = raw_ti.trunc_month(num=5)
    assert ti.get_pretty() == "2020-06"
    ti = raw_ti.trunc_month(num=6)
    assert ti.get_pretty() == "2020"
    ti = raw_ti.trunc_month(num=7)
    assert ti.get_pretty() == "2020"


def test_trunc_day():
    values = (2012, 3, 11, 14, 18, 13, 0, 0, 0)
    epoch = timegm(values)
    raw_ti = TimeInt(epoch)

    ti = raw_ti.trunc_day()
    assert ti.get_pretty() == "2012-03-11"
    ti = raw_ti.trunc_day(num=2)
    assert ti.get_pretty() == "2012-03-11"
    ti = raw_ti.trunc_day(num=3)
    assert ti.get_pretty() == "2012-03-10"
    ti = raw_ti.trunc_day(num=4)
    assert ti.get_pretty() == "2012-03-09"
    ti = raw_ti.trunc_day(num=5)
    assert ti.get_pretty() == "2012-03-11"
    ti = raw_ti.trunc_day(num=6)
    assert ti.get_pretty() == "2012-03-07"
    ti = raw_ti.trunc_day(num=7)
    assert ti.get_pretty() == "2012-03-08"
    ti = raw_ti.trunc_day(num=11)
    assert ti.get_pretty() == "2012-03"
    ti = raw_ti.trunc_day(num=15)
    assert ti.get_pretty() == "2012-03"


def test_trunc_hour():
    values = (2012, 3, 31, 14, 18, 13, 0, 0, 0)
    epoch = timegm(values)
    raw_ti = TimeInt(epoch)
    ti = raw_ti.trunc_hour()
    assert ti.get_pretty() == "2012-03-31 02 PM"
    ti = raw_ti.trunc_hour(num=2)
    assert ti.get_pretty() == "2012-03-31 02 PM"
    ti = raw_ti.trunc_hour(num=3)
    assert ti.get_pretty() == "2012-03-31 12 PM"
    ti = raw_ti.trunc_hour(num=4)
    assert ti.get_pretty() == "2012-03-31 12 PM"
    ti = raw_ti.trunc_hour(num=5)
    assert ti.get_pretty() == "2012-03-31 10 AM"
    ti = raw_ti.trunc_hour(num=6)
    assert ti.get_pretty() == "2012-03-31 12 PM"
    ti = raw_ti.trunc_hour(num=12)
    assert ti.get_pretty() == "2012-03-31 12 PM"
    ti = raw_ti.trunc_hour(num=13)
    assert ti.get_pretty() == "2012-03-31 01 PM"
    ti = raw_ti.trunc_hour(num=14)
    assert ti.get_pretty() == "2012-03-31 02 PM"
    ti = raw_ti.trunc_hour(num=15)
    assert ti.get_pretty() == "2012-03-31"


def test_trunc_minute():
    values = (1994, 8, 14, 7, 19, 12, 0, 0, 0)
    epoch = timegm(values)
    raw_ti = TimeInt(epoch)
    ti = raw_ti.trunc_minute()
    assert ti.get_pretty() == "1994-08-14 07:19 AM"
    ti = raw_ti.trunc_minute(num=2)
    assert ti.get_pretty() == "1994-08-14 07:18 AM"
    ti = raw_ti.trunc_minute(num=3)
    assert ti.get_pretty() == "1994-08-14 07:18 AM"
    ti = raw_ti.trunc_minute(num=4)
    assert ti.get_pretty() == "1994-08-14 07:16 AM"
    ti = raw_ti.trunc_minute(num=5)
    assert ti.get_pretty() == "1994-08-14 07:15 AM"
    ti = raw_ti.trunc_minute(num=6)
    assert ti.get_pretty() == "1994-08-14 07:18 AM"
    ti = raw_ti.trunc_minute(num=7)
    assert ti.get_pretty() == "1994-08-14 07:14 AM"
    ti = raw_ti.trunc_minute(num=15)
    assert ti.get_pretty() == "1994-08-14 07:15 AM"
    ti = raw_ti.trunc_minute(num=18)
    assert ti.get_pretty() == "1994-08-14 07:18 AM"
    ti = raw_ti.trunc_minute(num=19)
    assert ti.get_pretty() == "1994-08-14 07:19 AM"
    ti = raw_ti.trunc_minute(num=20)
    assert ti.get_pretty() == "1994-08-14 07 AM"
    ti = raw_ti.trunc_minute(num=30)
    assert ti.get_pretty() == "1994-08-14 07 AM"


def test_trunc_week():
    values = (2018, 8, 18, 12, 0, 1, 0, 0, 0)
    epoch = timegm(values)
    raw_ti = TimeInt(epoch)
    ti = raw_ti.trunc_week()
    assert ti.get_pretty() == "2018-08-12"
    values = (2018, 8, 3, 3, 0, 1, 0, 0, 0)
    epoch = timegm(values)
    raw_ti = TimeInt(epoch)
    ti = raw_ti.trunc_week()
    assert ti.get_pretty() == "2018-07-29"


def test_errors():
    with pytest.raises(ValueError):
        TimeInt(-1)
    with pytest.raises(ValueError):
        TimeInt(TimeInt.MAX + 1)
    with pytest.raises(ValueError):
        TimeInt("bogus")
    TimeInt(0)
    TimeInt(TimeInt.MAX)
    ti = TimeInt(49299112)
    with pytest.raises(ValueError):
        ti.trunc("bogus")
    with pytest.raises(ValueError):
        ti.trunc(TimeTruncUnit.DAY, num=-2)
    with pytest.raises(ValueError):
        ti.trunc(TimeTruncUnit.WEEK, num=2)
    with pytest.raises(ValueError):
        ti.trunc(TimeTruncUnit.MONTH, num=0)


def test_trunc():
    values = (2018, 8, 18, 12, 0, 1, 0, 0, 0)
    epoch = timegm(values)
    raw_ti = TimeInt(epoch)

    ti = raw_ti.trunc(TimeTruncUnit.YEAR, num=6)
    assert ti.get_pretty() == "2016"
    ti = raw_ti.trunc(TimeTruncUnit.MONTH, num=3)
    assert ti.get_pretty() == "2018-07"
    ti = raw_ti.trunc(TimeTruncUnit.WEEK)
    assert ti.get_pretty() == "2018-08-12"
    ti = raw_ti.trunc(TimeTruncUnit.DAY, num=7)
    assert ti.get_pretty() == "2018-08-15"
    ti = raw_ti.trunc(TimeTruncUnit.HOUR, num=5)
    assert ti.get_pretty() == "2018-08-18 10 AM"
    ti = raw_ti.trunc(TimeTruncUnit.MINUTE, num=2)
    assert ti.get_pretty() == "2018-08-18 12 PM"
