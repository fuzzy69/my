# NOTE: This module will soon be deprecated and removed
import ipaddress
import json
from enum import Enum
from random import choice
from re import compile, search

import requests

try:
    from libs.my.core.defaults import HEADERS, TIMEOUT
    from libs.my.core.meta.dummy_object import DummyObject
except ModuleNotFoundError:
    from core.defaults import HEADERS, TIMEOUT
    from core.meta.dummy_object import DummyObject


MATCH_WHITESPACE = "\s+"
MATCH_PROXY = "((\d{1,3})(\.\d{1,3}){3})(?:\s)*(?::)?(\d{2,5})"

regex_whitespace = compile(MATCH_WHITESPACE)
regex_proxy = compile(MATCH_PROXY)


class IPAddress:
    """IP address class"""

    def __init__(self, ip):
        self._ip = ip

    @property
    def ip(self):
        """Returns IP address"""
        return self._ip

    @staticmethod
    def validate(ip):
        """Returns True if IP address is valid otherwise False"""
        try:
            ipaddress.IPv4Address(ip)
        except ipaddress.AddressValueError:
            return False
        else:
            return True

    @staticmethod
    def geo_info(ip):
        """TBI"""
        pass

    @staticmethod
    def external_ip(ip):
        """TBI"""
        pass


class ProxyError(Exception):
    """Proxy error class"""

    pass


class ProxyType(Enum):
    """Proxy connection types"""

    HTTP = "http"
    HTTPS = "https"


class Proxy:
    """Proxy class"""

    def __init__(self, ip, port, username=None, password=None, timeout=10, ssl=False):
        Proxy.validate(ip, port)
        self._ip = ip
        self._port = port
        self._username = username
        self._password = password
        self._timeout = timeout
        self._type = ProxyType.HTTPS if ssl else ProxyType.HTTP

    def __repr__(self):
        """Returns Proxy class representation"""
        return "<Proxy [{}] ({}:{})>".format(self.type.name, self.ip, self.port)

    def __str__(self):
        """Returns Proxy class as string"""
        if self.username and self.password:
            return "{}://{}:{}@{}:{}".format(
                self.type.value, self.username, self.password, self.ip, self.port
            )
        else:
            return "{}://{}:{}".format(self.type.value, self.ip, self.port)

    def __eq__(self, other):
        """Returns true if current proxy object is equal to given other proxy"""
        return self.ip == other.ip and self.port == other.port

    def __hash__(self):
        """Returns uniques hash value for current proxy object"""
        return hash((self.ip, self.port))

    @staticmethod
    def from_string(proxy_string: str):
        """Returns new Proxy object from given proxy string otherwise None"""
        proxy = None
        matches = search(r"(http|https)://(.*?):(\d{1,})", proxy_string)
        if matches:
            proxy_type = matches.group(1)
            ip = matches.group(2)
            port = matches.group(3)
            try:
                proxy = Proxy(ip, int(port))
                proxy.type = (
                    ProxyType.HTTPS if proxy_type == "https" else ProxyType.HTTP
                )
            except (ValueError, ProxyError):
                pass

        return proxy

    @classmethod
    def validate(cls, ip, port):
        """Raises exception if proxy is not valid"""
        if not IPAddress.validate(ip):
            raise ValueError("Invalid ip address format")
        if type(port) is not int:
            raise ValueError("Invalid port value type, int required")
        if not (0 <= port <= 65535):
            raise ValueError("Invalid port number")

    @property
    def ip(self):
        """Returns proxy IP address"""
        return self._ip

    @property
    def port(self):
        """Returns proxy port number"""
        return self._port

    @property
    def username(self):
        """Returns proxy auth username"""
        return self._username

    @property
    def password(self):
        """Returns proxy auth password"""
        return self._password

    @property
    def type(self) -> ProxyType:
        """Returns proxy type"""
        return self._type

    @type.setter
    def type(self, proxy_type: ProxyType):
        """Sets proxy type"""
        self._type = proxy_type


def get_real_ip():
    """Returns current host IP address or None"""
    ip = None
    try:
        r = requests.get(
            "http://httpbin.org/get?show_env", headers=HEADERS, timeout=TIMEOUT
        )
        if r.status_code == 200:
            data = json.loads(r.text)
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
            r = requests.get(url, proxies=proxies, headers=HEADERS, timeout=timeout)
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
