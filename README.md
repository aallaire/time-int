# time-int
Integer subclass for number of seconds since the epoch in UTC

### The Idea
UNIX has a venerable tradition of representing time as seconds since the
start of 1970. This has its limitations, but it is sometimes desirably
simple. This package sub-classes int to give a little handy functionality
to this simple approach.

#### More robust resources
For uses beyond this rather specific functionality, the standard python
distribution includes powerful time related packages such as `datetime`,
`time` and `calendar`. Also other packages installable time related
packages such as `pytz` and `timeutil`.

### Important Limitations of TimeInt objects.
* Values are always treated as relative to UTC.
* Values are rounded down to the second.
* Supported range starts at Jan 1, 1970 (UTC): 0
* Supported range ends at Jan 1, 3000 (UTC): 32,503,680,000
* The supported range might need to be different on other systems, have only tested on windows.
* This package is not far enough along in development to be safe from errors or major feature changes.

### Quick Example
```python
from time_int import TimeInt

start_time = TimeInt.utcnow()
some_slow_operation()
end_time = TimeInt.utcnow()

print(f"Operation started at {start_time.get_pretty()}")
print(f"Operation ended  at  {end_time.get_pretty()}")
print(f"Operation took {end_time - start_time} seconds")
```

### The trunc_\<unit\> Methods
Some trunc_\<unit\> methods are available for rounding down times to the
year, month, week, day, hour, or minute. One can also round down to units based
on some number of these units. For example to round a time int to the fifteen
minute period it falls in:
```python
from time_int import TimeInt
from datetime import datetime

dt = datetime(year=2001, month=5, day=16, hour=10, minute=53)
time = TimeInt.from_datetime(dt)

quarter_hour_time = time.trunc_minute(num=15)
``` 
The `quater_hour_time` will round down 10:53am to 10:45am.
Note that the 15 minute periods rounded to are based on when the hour started, as
one might intuitively suspect. For numbers of hours the `trunc_day` method is based
on start of the day. Such that if you round down to units of 6 hours, you will round
down to ether midnight, 6am, noon, or 6pm. Weeks do not have this grouping feature because
there is no obvious place I can see to start counting groups of weeks from. For
days they are based on start of month. For months on start of year, and for years
on a fictional year 0 (which technically does not exist). Sometimes there will be
oddly sized groups with less than the number of units, for example if you choose to
round to units of 7 hours, you will get either midnight, 7am, 2pm, or 9pm. With 9pm
to midnight only being the left over 3 hours. When the time unit is groups of 2 or
more days, this is bound to happen due to the way months vary from 28 to 31 days.

##### trunc method
There is a generic `trunc` method that wraps all the `trunc_<unit>` methods so
one can specify the basic time unit as an argument. For example to find the start
of the start of the current quarter year in UTC:

```python
from time_int import TimeInt, TimeTruncUnit

current_time = TimeInt.utcnow()
start_of_quarter = current_time.trunc(TimeTruncUnit.MONTH, num=3)
```
Of course in this example one would probably just use `trunc_month(num=3)` which
does the same thing.




