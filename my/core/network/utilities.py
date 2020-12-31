from json import loads
from random import choice
from re import compile as re_compile, findall, IGNORECASE
from typing import AnyStr, Optional, Set, Tuple
from urllib.parse import parse_qs, urlparse

from requests import get

try:
    from libs.my.core.defaults import USER_AGENT, HEADERS, TIMEOUT
    from libs.my.core.network.ip_address import IPAddress
    from libs.my.core.network.proxy import Proxy, ProxyType
    from libs.my.core.html.utilities import extract_text_from_html
    from libs.my.core.defaults import SCREEN_HEIGHT, SCREEN_WIDTH, USER_AGENT
except ModuleNotFoundError:
    from core.defaults import USER_AGENT, HEADERS, TIMEOUT
    from core.network.ip_address import IPAddress
    from core.network.proxy import Proxy, ProxyType
    from core.text.utilities import extract_text_from_html
    from core.defaults import SCREEN_HEIGHT, SCREEN_WIDTH, USER_AGENT


MATCH_WHITESPACE = "\s+"
MATCH_PROXY = "(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s*:?\s*(\d{2,5})"

regex_whitespace = re_compile(MATCH_WHITESPACE)
regex_proxy = re_compile(MATCH_PROXY)


def get_real_ip() -> Optional[AnyStr]:
    """Returns current host IP address or None"""
    ip = None
    try:
        r = get("http://httpbin.org/get?show_env", headers=HEADERS, timeout=TIMEOUT)
        if r.status_code == 200:
            data = loads(r.text)
            ip = data["origin"].split(",")[0].strip()
    except Exception as e:
        pass

    return ip


def check_anonymity(ip, port, real_ip, timeout):
    """Returns Proxy object if proxy is working otherwise None"""
    http_proxy_judges = (
        "http://httpbin.org/ip",
        "http://api.ipify.org",
        "http://icanhazip.com/",
    )
    https_proxy_judges = (
        "https://httpbin.org/ip",
        "https://api.ipify.org",
        "https://icanhazip.com/",
    )
    http_proxy = None
    https_proxy = None
    for proxy_judges in [
        (ProxyType.HTTP, http_proxy_judges),
        (ProxyType.HTTPS, https_proxy_judges),
    ]:
        try:
            proxy_type, proxy_judges = proxy_judges
            port = int(port)
            url = choice(proxy_judges)
            proxies = {
                "http": "http://{}:{}/".format(ip, port),
                "https": "https://{}:{}/".format(ip, port),
            }
            # r = requests.get(url, proxies=proxies, headers=HEADERS, timeout=TIMEOUT)
            r = get(url, proxies=proxies, headers=HEADERS, timeout=timeout)
            if r.status_code == 200:
                if str(real_ip) not in r.text:
                    if proxy_type == ProxyType.HTTP:
                        http_proxy = Proxy(ip, port)
                    elif proxy_type == ProxyType.HTTPS:
                        https_proxy = Proxy(ip, port, ssl=True)
        except Exception as e:
            pass
    proxy = https_proxy if http_proxy is not None and https_proxy is not None else None

    return proxy


def _try_get_qs(url: AnyStr, name: AnyStr) -> Tuple[bool, Optional[AnyStr]]:
    """Returns pair of True and query string value for selected key otherwise pair of False and None"""
    ok, result = False, None
    try:
        result = parse_qs(urlparse(url).query).get(name)[0]
        ok = True
    except (IndexError, TypeError, ValueError):
        pass

    return ok, result


def try_get_qs(url: AnyStr, name: AnyStr) -> Optional[AnyStr]:
    """Returns query string value for selected key otherwise None"""
    try:
        result = parse_qs(urlparse(url).query).get(name)[0]
    except (IndexError, TypeError, ValueError):
        result = None

    return result


def try_qs_key(url: AnyStr, name: AnyStr) -> Optional[AnyStr]:
    """Returns query string value for selected key otherwise None"""
    try:
        result = parse_qs(urlparse(url).query).get(name)[0]
    except (IndexError, TypeError, ValueError):
        result = None

    return result


def is_valid_url(url: AnyStr) -> bool:
    """Returns True if given URL is valid otherwise False
    https://stackoverflow.com/a/7995979"""
    regex = re_compile(
        r"^https?://"  # http:// or https://
        r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|"  # domain...
        r"localhost|"  # localhost...
        r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # ...or ip
        r"(?::\d+)?"  # optional port
        r"(?:/?|[/?]\S+)$",
        IGNORECASE,
    )

    return url is not None and regex.search(url)


def is_root_url(url: AnyStr) -> bool:
    """Returns True if given URL is root otherwise False"""
    if not url.startswith("http"):
        url = "http://" + url
    url = url.rstrip("/")

    return len(urlparse(url).path) == 0


def extract_domain(url: AnyStr) -> Optional[AnyStr]:
    """Returns domain from given URL on success otherwise None"""
    url = url.strip()
    if not url.startswith("http"):
        url = f"http://{url}"
    if not is_valid_url(url):
        return None
    try:
        domain = urlparse(url).netloc
    except ValueError:
        return None
    if domain == "":
        return None

    return domain.lstrip("www.")
