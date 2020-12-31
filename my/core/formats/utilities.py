from json import loads, JSONDecodeError
from typing import AnyStr, Dict, Optional


def try_json(text: AnyStr) -> Optional[Dict]:
    """Returns JSON dictionary from given JSON text on parse success otherwise None"""
    try:
        result = loads(text)
    except JSONDecodeError:
        result = None

    return result
