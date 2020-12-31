from enum import Enum
from re import search, DOTALL, IGNORECASE

try:
    from libs.my.core.network.ip_address import IPAddress
except ModuleNotFoundError:
    from core.network.ip_address import IPAddress


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
        proxy_type, ip, port, username, password = None, None, None, None, None
        if '@' in proxy_string:
            # matches = search(r"(http|https)://([^:]+):([^:]+)@(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}):(\d{2,})", proxy_string)
            matches = search(r"(http|https)://([^:]+):([^:]+)@([^.]+.[^.]+.[^.]+.[^:]+):(\d{2,})", proxy_string)
            if matches:
                proxy_type = matches.group(1)
                username = matches.group(2)
                password = matches.group(3)
                ip = matches.group(4)
                port = matches.group(5)
        else:
            # matches = search(r"(http|https)://(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}):(\d{2,})", proxy_string)
            matches = search(r"(http|https)://([^.]+.[^.]+.[^.]+.[^:]+):(\d{2,})", proxy_string)
            if matches:
                proxy_type = matches.group(1)
                ip = matches.group(2)
                port = matches.group(3)
        try:
            proxy = Proxy(ip, int(port), username, password)
            proxy.type = (
                ProxyType.HTTPS if proxy_type == "https" else ProxyType.HTTP
            )
        except Exception:
            pass

        return proxy

    @classmethod
    def validate(cls, ip, port):
        """Raises exception if proxy is not valid"""
        # if not IPAddress.validate(ip):
        #     raise ValueError("Invalid ip address format")
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
