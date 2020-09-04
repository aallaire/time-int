from time_int import __version__, TimeInt


def test_version():
    assert __version__ == "0.0.5"


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


def test_trunc_month():
    time_int = TimeInt(1590984783)
    month_time_int = time_int.trunc_month()
    assert month_time_int.get_pretty() == "2020-05"


def test_trunc_day():
    time_int = TimeInt(1590984783)
    day_time_int = time_int.trunc_day()
    assert day_time_int.get_pretty() == "2020-05-31"


def test_trunc_hour():
    time_int = TimeInt(1590984783)
    hour_time_int = time_int.trunc_hour()
    assert hour_time_int.get_pretty() == "2020-05-31 11 PM"


def test_trunc_minute():
    time_int = TimeInt(1590984783)
    minute_time_int = time_int.trunc_minute()
    assert minute_time_int.get_pretty() == "2020-05-31 11:13 PM"


def test_trunc_week():
    time_int = TimeInt(1591287183)
    week_time_int = time_int.trunc_week()
    assert week_time_int.get_pretty() == "2020-05-31"
