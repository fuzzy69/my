import operator
from functools import reduce
from os import scandir
from os.path import basename, isdir, isfile
from platform import system
from re import compile as re_compile, findall, IGNORECASE
from subprocess import Popen, PIPE
from typing import Any, AnyStr, Dict, Iterable, List, Optional, Tuple

try:
    from libs.my.core.network.proxy import Proxy
    from libs.my.core.text.utilities import get_match
except ModuleNotFoundError:
    from core.network.proxy import Proxy
    from core.text.utilities import get_match


MATCH_WHITESPACE = "\s+"
# MATCH_PROXY = "((\d{1,3})(\.\d{1,3}){3})(?:\s)*(?::)?(\d{2,5})"
MATCH_PROXY = "(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s*:?\s*(\d{2,5})"

if system() == "Windows":
    MATCH_CHROME = r"google\s+chrome\s+(\d+)\."
    MATCH_CHROME_DRIVER = r"chromedriver\s+(\d+)\."
else:
    MATCH_CHROME = r"google\s+chrome\s+(\d+)\."
    MATCH_CHROME_DRIVER = r"chromedriver\s+(\d+)\."

regex_chrome = re_compile(MATCH_CHROME, IGNORECASE)
regex_chrome_driver = re_compile(MATCH_CHROME_DRIVER, IGNORECASE)


def try_get_key(data: Dict, keys: List) -> Tuple[bool, Optional[Any]]:
    """Returns value of nested item in dictionary"""
    ok, result = False, None
    try:
        result = reduce(operator.getitem, keys, data)
        ok = True
    except KeyError:
        pass

    return ok, result


def get_chrome_version(chrome_dir: Optional[AnyStr] = None) -> Optional[int]:
    """Returns Chrome major version """
    result = None
    if system() == "Windows":
        for dir_ in scandir(chrome_dir):
            if isdir(dir_):
                match = get_match(r"(\d+)\.\d+", basename(dir_.path))
                if match:
                    result = int(match)
                    break
    else:
        binary_path = "chromedriver"
        p = Popen([binary_path, "--version"], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        std_out, std_err = p.communicate()
        if not std_err:
            match = get_match(regex_chrome, str(std_out))
            if match is not None:
                result = int(match)

    return result


def get_chrome_driver_version(binary_path: Optional[AnyStr] = None) -> Optional[int]:
    """Returns Chrome driver major version"""
    result = None
    if binary_path is None:
        binary_path = "chromedriver.exe" if system() == "Windows" else "chromedriver"
    if not isfile(binary_path):
        return None
    p = Popen([binary_path, "-v"], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    std_out, std_err = p.communicate()
    if not std_err:
        match = get_match(regex_chrome_driver, str(std_out))
        if match is not None:
            result = int(match)

    return result


def extract_proxies(text: AnyStr) -> Iterable[Proxy]:
    """Returns collection of network proxy objects from parsed text"""
    results = set()
    matches = findall(MATCH_PROXY, text)
    for ip, port in matches:
        proxy = Proxy.from_string(f"https://{ip}:{port}/")
        if proxy is not None:
            results.add(proxy)

    return results


def increase(obj: Any, field: AnyStr):
    """Increase object integer field by one"""
    if hasattr(obj, field):
        value = getattr(obj, field)
        if isinstance(value, int):
            setattr(obj, field, value + 1)


def decrease(obj: Any, field: AnyStr):
    """Increase object integer field by one"""
    if hasattr(obj, field):
        value = getattr(obj, field)
        if isinstance(value, int):
            setattr(obj, field, value - 1)
