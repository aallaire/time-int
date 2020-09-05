from time_int import __version__, TimeInt
from datetime import datetime


def test_version():
    assert __version__ == "0.0.6"


def test_time_int():
    time_int = TimeInt(1590984783)
    assert isinstance(time_int, int)
    assert isinstance(time_int, TimeInt)
    date_time = time_int.get_datetime()
    assert date_time.year == 2020
    assert date_time.month == 5
    assert date_time.day == 31
    assert date_time.hour == 23
    assert date_time.minute == 13
    assert date_time.second == 3
    assert time_int > TimeInt.MIN
    assert time_int < TimeInt.MAX


def test_get_pretty():
    time_int = TimeInt(1590984783)
    on_the_minute = TimeInt(time_int - 3)
    on_the_hour = TimeInt(time_int - 783)
    on_the_day = TimeInt(time_int - 83583)
    on_the_month = TimeInt(time_int - 2675583)
    on_the_year = TimeInt(1577858400)
    assert time_int.get_pretty() == "2020-05-31 11:13:03 PM"
    assert on_the_minute.get_pretty() == "2020-05-31 11:13 PM"
    assert on_the_hour.get_pretty() == "2020-05-31 11 PM"
    assert on_the_day.get_pretty() == "2020-05-31"
    assert on_the_month.get_pretty() == "2020-05"
    assert on_the_year.get_pretty() == "2020"


def test_from_datetime():
    time_int = TimeInt(1590984783)
    date_time = time_int.get_datetime()
    time_int2 = TimeInt.from_datetime(date_time)
    assert isinstance(time_int2, TimeInt)
    assert time_int == time_int2


def test_trunc_year():
    time_int = TimeInt(1590984783)
    year_time_int = time_int.trunc_year()
    assert year_time_int.get_pretty() == "2020"
    time = time_int.trunc_year(num=2)
    assert time.get_pretty() == "2020"
    time = time_int.trunc_year(num=3)
    assert time.get_pretty() == "2019"
    time = time_int.trunc_year(num=4)
    assert time.get_pretty() == "2020"
    time = time_int.trunc_year(num=5)
    assert time.get_pretty() == "2020"
    time = time_int.trunc_year(num=6)
    assert time.get_pretty() == "2016"
    time = time_int.trunc_year(num=10)
    assert time.get_pretty() == "2020"
    time = time_int.trunc_year(num=17)
    assert time.get_pretty() == "2006"


def test_trunc_month():
    time_int = TimeInt(1590984783)
    month_time_int = time_int.trunc_month()
    assert month_time_int.get_pretty() == "2020-05"
    time = time_int.trunc_month(num=2)
    assert time.get_pretty() == "2020-05"
    time = time_int.trunc_month(num=3)
    assert time.get_pretty() == "2020-04"
    time = time_int.trunc_month(num=4)
    assert time.get_pretty() == "2020-05"
    time = time_int.trunc_month(num=5)
    assert time.get_pretty() == "2020"


def test_trunc_day():
    time_int = TimeInt(1590984783)
    day_time_int = time_int.trunc_day()
    assert day_time_int.get_pretty() == "2020-05-31"
    day_time_int = time_int.trunc_day(num=2)
    assert day_time_int.get_pretty() == "2020-05-31"
    day_time_int = time_int.trunc_day(num=3)
    assert day_time_int.get_pretty() == "2020-05-31"
    day_time_int = time_int.trunc_day(num=4)
    assert day_time_int.get_pretty() == "2020-05-29"
    day_time_int = time_int.trunc_day(num=5)
    assert day_time_int.get_pretty() == "2020-05-31"
    day_time_int = time_int.trunc_day(num=6)
    assert day_time_int.get_pretty() == "2020-05-31"
    day_time_int = time_int.trunc_day(num=7)
    assert day_time_int.get_pretty() == "2020-05-29"
    start_of_month = time_int.trunc_month()
    assert start_of_month.get_pretty() == "2020-05"
    start_of_day = start_of_month.trunc_day()
    assert start_of_day.get_pretty() == "2020-05"
    start_of_day = start_of_month.trunc_day(2)
    assert start_of_day.get_pretty() == "2020-05"
    start_of_day = start_of_month.trunc_day(3)
    assert start_of_day.get_pretty() == "2020-05"
    start_of_day = start_of_month.trunc_day(4)
    assert start_of_day.get_pretty() == "2020-05"
    day_5 = TimeInt.from_datetime(datetime(year=2020, month=5, day=5, hour=11))
    assert day_5.get_pretty() == "2020-05-05 11 AM"
    time = day_5.trunc_day()
    assert time.get_pretty() == "2020-05-05"
    time = day_5.trunc_day(num=2)
    assert time.get_pretty() == "2020-05-05"
    time = day_5.trunc_day(num=3)
    assert time.get_pretty() == "2020-05-04"
    time = day_5.trunc_day(num=4)
    assert time.get_pretty() == "2020-05-05"


def test_trunc_hour():
    time_int = TimeInt(1590984783)
    hour_time_int = time_int.trunc_hour()
    assert hour_time_int.get_pretty() == "2020-05-31 11 PM"
    time = time_int.trunc_hour(num=2)
    assert time.get_pretty() == "2020-05-31 10 PM"
    time = time_int.trunc_hour(num=3)
    assert time.get_pretty() == "2020-05-31 09 PM"
    time = time_int.trunc_hour(num=4)
    assert time.get_pretty() == "2020-05-31 08 PM"
    time = time_int.trunc_hour(num=5)
    assert time.get_pretty() == "2020-05-31 08 PM"
    time = time_int.trunc_hour(num=6)
    assert time.get_pretty() == "2020-05-31 06 PM"
    time = time_int.trunc_hour(num=12)
    assert time.get_pretty() == "2020-05-31 12 PM"


def test_trunc_minute():
    time_int = TimeInt(1590984783)
    minute_time_int = time_int.trunc_minute()
    assert minute_time_int.get_pretty() == "2020-05-31 11:13 PM"
    time = time_int.trunc_minute(num=2)
    assert time.get_pretty() == "2020-05-31 11:12 PM"
    time = time_int.trunc_minute(num=3)
    assert time.get_pretty() == "2020-05-31 11:12 PM"
    time = time_int.trunc_minute(num=4)
    assert time.get_pretty() == "2020-05-31 11:12 PM"
    time = time_int.trunc_minute(num=5)
    assert time.get_pretty() == "2020-05-31 11:10 PM"
    time = time_int.trunc_minute(num=6)
    assert time.get_pretty() == "2020-05-31 11:12 PM"
    time = time_int.trunc_minute(num=7)
    assert time.get_pretty() == "2020-05-31 11:07 PM"


def test_trunc_week():
    time_int = TimeInt(1591287183)
    week_time_int = time_int.trunc_week()
    assert week_time_int.get_pretty() == "2020-05-31"
