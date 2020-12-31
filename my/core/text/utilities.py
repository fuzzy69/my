from re import escape, findall, search, sub, IGNORECASE, Pattern, split, I
from typing import AnyStr, Dict, List, Optional, Union, Iterable
from unicodedata import normalize

try:
    from libs.my.core.collection.utilities import split_list
except ModuleNotFoundError:
    from core.collection.utilities import split_list


def slugify(text: AnyStr, delimiter: AnyStr='-', lowercase: bool=True) -> AnyStr:
    """Normalizes string, converts to lowercase, removes non-alpha characters, and converts spaces to hyphens.
    Source: https://stackoverflow.com/a/295466"""
    text = normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    text = sub("[^\w\s-]", "", text).strip()
    if lowercase:
        text = text.lower()
    text = sub(f"[{delimiter}\s]+", delimiter, text)

    return text


def trim_whitespaces(text: AnyStr) -> AnyStr:
    """Returns string without multiple whitespace characters"""
    return sub("\\s+", " ", text)


def string_contains(haystack: AnyStr, needles: AnyStr, ignore_case: bool = False) -> bool:
    """Returns True if string contains at least one string needle otherwise False"""
    haystack = haystack.lower() if ignore_case else haystack
    for needle in needles:
        if not ignore_case:
            needle = needle.lower()
        if needle in haystack:
            return True

    return False


def string_endswith(haystack: AnyStr, needles: List, ignore_case: bool = False) -> bool:
    """Returns True if string ends with one of given needles otherwise False"""
    haystack = haystack.lower() if ignore_case else haystack
    for needle in needles:
        if not ignore_case:
            needle = needle.lower()
        if haystack.endswith(needle):
            return True

    return False


def get_match(regex: Union[AnyStr, Pattern], text: AnyStr, rtype: type = None):
    """
    Return first regex match group
    :param str regex: regex pattern
    :param str text: text to match
    :param type rtype: optionally convert to return type
    :return: matched string or None
    """
    if isinstance(regex, Pattern):
        match = search(regex, text)
    else:
        match = search(regex, text, IGNORECASE)
    if not match:
        return None
    match = match.group(1)
    if rtype is not None:
        try:
            match = rtype.__call__(match)
        except ValueError:
            return None

    return match


def multi_replace(text: AnyStr, dic: Dict) -> AnyStr:
    """
    Replaces multiple different strings at once
    :param str text: original string
    :param dict dic: dictionary of key (find) => value (replace) strings
    :return: new string with replaced values
    """
    pattern = "|".join(map(escape, dic.keys()))

    return sub(pattern, lambda m: dic[m.group()], text)


def count_words(text: AnyStr) -> int:
    """Returns number of tokens (words) longer than 1 character"""
    words = findall(r"\w{2,}", text)

    return len(words)


def get_between(text: AnyStr, start_token: AnyStr, end_token: AnyStr) -> Optional[AnyStr]:
    """Returns the text without text from start to end token (including tokens)
    otherwise just returns input text."""
    result = None
    try:
        start_index = text.index(start_token)
        end_index = text.index(end_token)
        result = text[start_index + len(start_token):end_index]
    except ValueError:
        pass

    return result


def remove_between(text: AnyStr, start_token: AnyStr, end_token: AnyStr) -> AnyStr:
    """Returns the text without text from start to end token (including tokens)
    otherwise just returns input text."""
    try:
        start_index = text.index(start_token)
        end_index = text.index(end_token)
        text = text[:start_index] + text[end_index + len(end_token):]
    except ValueError:
        pass

    return text


def text_between(text: AnyStr, start_token: AnyStr, end_token: AnyStr, keep_tokens: bool = False) -> Optional[AnyStr]:
    """Returns the text without text from start to end token (including tokens)
    otherwise just returns input text."""
    if start_token not in text:
        return None
    start_index = text.index(start_token)
    if not keep_tokens:
        start_index += len(start_token)
    text = text[start_index:]
    if end_token not in text:
        return None
    end_index = text.index(end_token)
    if keep_tokens:
        end_index += len(end_token)
    return text[:end_index]


def remove_text_between(text: AnyStr, start_token: AnyStr, end_token: AnyStr, keep_tokens: bool = False) -> AnyStr:
    """Returns the text without text from start to end token (including tokens)
    otherwise just returns input text."""
    if not all((start_token in text, end_token in text)):
        return text
    start_index = text.index(start_token)
    end_index = text.index(end_token)
    if not start_index < end_index:
        return text

    if keep_tokens:
        start_index += len(start_token)
    else:
        end_index += len(end_token)

    return text[:start_index] + text[end_index:]


def text_contains(text: AnyStr, tokens: Iterable[AnyStr]) -> Optional[AnyStr]:
    """Returns the first token that text contains otherwise None"""
    text = text.lower()
    for token in tokens:
        if token.lower() in text:
            return token

    return None


def text_to_sentences(text: AnyStr) -> Iterable[AnyStr]:
    """Yields sentence strings after splitting given text string to sentences"""
    for sentence in split(r"\.\s+", text):
        yield sentence.strip() + '.'


def text_words_only(text: AnyStr) -> AnyStr:
    """Returns formatted text string after removing excess characters
    https://stackabuse.com/python-for-nlp-working-with-facebook-fasttext-library/
    """
    stop_words = set()
    # Remove all the special characters
    text = sub(r"\W", " ", text)
    # Remove all single characters
    text = sub(r"\s+[a-zA-Z]\s+", " ", text)
    # Remove single characters from the start
    text = sub(r"\^[a-zA-Z]\s+", " ", text)
    # Replace multiple spaces with single space
    text = sub(r"\s+", " ", text, flags=I)
    # Remove prefixed 'b'
    text = sub(r"^b\s+", "", text)

    text = text.lower()
    tokens = text.split()
    tokens = [word for word in tokens if word not in stop_words]
    tokens = [word for word in tokens if len(word) > 3]
    text = " ".join(tokens)

    return text


def preprocess_text(text: AnyStr) -> AnyStr:
    """Returns formatted text string"""
    text = sub(r"\n{2,}", "\n\n", text)  # Allow max 2 consecutive new lines

    return text


def split_text(text: AnyStr, max_words: int) -> Iterable[AnyStr]:
    """Yields text chunks split from given text when each chunk has less or equal number of words than given maximum
    words count"""
    words = split(r"\s+", text)
    # https://stackoverflow.com/a/312464
    for i in range(0, len(words), max_words):
        yield ' '.join(words[i:i + max_words])


def text_intersection(text1: AnyStr, text2: AnyStr) -> AnyStr:
    """Returns intersection string part of two given strings of text
    https://stackoverflow.com/a/55638470"""
    result = ''
    for i in range(len(text1)):
        for j in range(i + 1, len(text1)):
            chunk = text1[i:j]
            if chunk in text2 and len(chunk) > len(result):
                result = chunk

    return result
