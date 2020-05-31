from time_int import __version__, TimeInt


def test_version():
    assert __version__ == '0.0.1'


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
    assert time_int.get_pretty() == "2020-05-31 11:13:03 PM"
    assert on_the_minute.get_pretty() == "2020-05-31 11:13 PM"
    assert on_the_hour.get_pretty() == "2020-05-31 11 PM"
    assert on_the_day.get_pretty() == "2020-05-31"

