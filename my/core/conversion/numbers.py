from re import match
from typing import Any, AnyStr, Optional

SECOND = 1000


def try_to_int(value: Any, default: Optional[int] = None) -> Optional[int]:
    """Returns integer if conversion from input value to integer is successful
    otherwise None"""
    result = default
    if value is not None:
        try:
            result = int(value)
        except (TypeError, ValueError):
            pass

    return result


def pretty_bytes(num_bytes: int) -> AnyStr:
    """Returns string description of rounded number of bytes to closest size
    unit (MB, GB ...)
    https://stackoverflow.com/a/52379087
    """
    step_unit = 1000.0  # 1024 bad the size

    for x in ["bytes", "KB", "MB", "GB", "TB"]:
        if num_bytes < step_unit:
            return "%3.1f %s" % (num_bytes, x)
        num_bytes /= step_unit


def string_to_float(value: AnyStr) -> Optional[float]:
    """Returns floating point number from given input if successfully converted otherwise None"""
    result = None
    if isinstance(value, str) and match(r"[+-]?([0-9]*[.])?[0-9]+", value):
        try:
            result = float(value)
        except ValueError:
            pass

    return result


def try_to_float(value: Any) -> Optional[float]:
    """Returns floating point number from given input if successfully converted otherwise None"""
    result = None
    if value is not None:
        try:
            result = float(value)
        except (TypeError, ValueError):
            pass

    return result
