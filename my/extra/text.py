from typing import AnyStr

from pycld2 import detect


def is_text_english(text: AnyStr) -> bool:
    """Returns True if given text is English otherwise False"""
    is_reliable, _, details = detect(text)
    return is_reliable and details[0][1] == "en"
