from datetime import datetime
from functools import wraps
from time import time
from typing import Tuple, AnyStr


def time_it(func):
    """Measure function execution time"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time()
        result = func(*args, **kwargs)
        elapsed_time = int(time() - start_time)
        print("Done in {}".format(pretty_relative_time(elapsed_time)))

        return result

    return wrapper


def pretty_relative_time(time_diff_secs: int) -> AnyStr:
    """Returns seconds as a friendly readable string.
    Source: https://stackoverflow.com/a/18421524"""
    weeks_per_month = 365.242 / 12 / 7
    intervals = [
        ("minute", 60),
        ("hour", 60),
        ("day", 24),
        ("week", 7),
        ("month", 365.242 / 12 / 7),
        ("year", 12),
    ]

    unit, number = "second", abs(time_diff_secs)
    for new_unit, ratio in intervals:
        new_number = float(number) / ratio
        # If the new number is too small, don't go to the next unit.
        if new_number < 1:
            break
        unit, number = new_unit, new_number
    shown_num = int(number)

    return f"{shown_num} {unit + ('' if shown_num == 1 else 's')}"


def seconds_to_units(seconds: int) -> Tuple[int, int, int, int]:
    """Returns day, hour, minute, seconds tuple calculated from given seconds count"""
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)

    return d, h, m, s


def pretty_seconds(seconds: int) -> AnyStr:
    """Returns given seconds number as nicely formatted string"""
    units = {
        0: "day",
        1: "hour",
        2: "minute",
        3: "second",
    }
    result = ''
    for i, x in enumerate(seconds_to_units(seconds)):
        if x == 0 or (i == 3 and seconds >= 3600):
            continue
        result += f" {x} {units[i] if x == 1 else units[i] + 's'}"

    return result.strip()


def seconds_since_midnight() -> int:
    """Returns number of seconds since midnight
    https://stackoverflow.com/a/15971505
    """
    now = datetime.now()
    seconds = int(
        (now - now.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()
    )

    return seconds
