from functools import reduce
import operator
from typing import Any, List, Iterable, Dict, Optional


def split_list(li: List, n: int) -> List:
    """Split list into n lists

    :param list li: list to split
    :param int n: split chunks count
    :return: list of n lists
    """
    k, m = divmod(len(li), n)

    return [li[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n)]


def to_n_lists(li: List, n: int) -> Iterable:
    """Split list into n lists

    :param list li: list to split
    :param int n: split chunks count
    :return: list of n lists
    """
    k, m = divmod(len(li), n)
    for i in range(n):
        yield li[i * k + min(i, m):(i + 1) * k + min(i + 1, m)]


def to_n_length_lists(li: List, n: int) -> Iterable:
    """Yields each list chunk from given list split to n chunks"""
    for i in range(0, len(li), n):
        yield li[i:i + n]


def try_key(data: Dict, keys: List, default: Any = None, rtype: Optional[type] = None) -> Optional[Any]:
    """Returns value of nested item in dictionary"""
    result = default
    try:
        result = reduce(operator.getitem, keys, data)
    except KeyError:
        pass

    # Result type doesn't match defaults, try to force conversion
    if result is not None and rtype is not None and not isinstance(result, rtype):
        try:
            result = rtype(result)
        except (TypeError, ValueError):
            pass

    return result
