from enum import Enum
from random import choice, randrange
from threading import Lock
from time import sleep, time
from typing import Iterable, Optional, Tuple

try:
    from libs.my.core.defaults import RETRIES
    from libs.my.core.meta.dummy_object import DummyObject
    from libs.my.core.network.proxy import Proxy
except ModuleNotFoundError:
    from core.defaults import RETRIES
    from core.meta.dummy_object import DummyObject
    from core.network.proxy import Proxy


class ProxyPoolError(Exception):
    """Proxy pool base error"""

    pass


class ProxyPoolTimeoutError(ProxyPoolError):
    """Raised when proxy pool can't return requests proxy after wait time
    exceeded"""

    pass


class ProxyPoolDepletedError(ProxyPoolError):
    """Raised when proxy pool has no more live proxies"""

    pass


class ProxyRotationStrategy(Enum):
    """Proxy rotation strategies"""

    RANDOM = 0  # Picks random proxy, can pick the same proxy subsequently, no rules
    RANDOM_UNIQUE = 1  # Picks random proxy once until every proxy is picked once and then repeats it in different order
    CYCLE = 2  # Goes from first to last proxy on and on
    CHOICE = 3  # Picks random proxy, doesn't care if proxy is already in use, doesn't track failures
    DUMMY = 4  # Do not return proxy (used)


class ProxyPool:
    """Proxy pool, thread-safe class for managing multiple proxies"""

    def __init__(self, proxies: Iterable[Proxy], max_retries: int = RETRIES):
        self._lock = Lock()
        self._max_retries = max_retries
        self._rotation_strategy = ProxyRotationStrategy.RANDOM
        self._available_proxies = []
        self._in_use_proxies = {}
        self._dead_proxies = []

        self._available_count = 0
        self._in_use_count = 0
        self._live_count = 0
        self._dead_count = 0
        self._total_count = 0

        for proxy in proxies:
            self.add_proxy(proxy)

    def _update_counts(self):
        """Updates all tracking proxy count numbers"""
        self._available_count = len(self._available_proxies)
        self._in_use_count = len(self._in_use_proxies)
        self._live_count = self._available_count + self._in_use_count
        self._dead_count = len(self._dead_proxies)
        self._total_count = self._live_count + self._dead_count

    def add_proxy(self, proxy: Proxy):
        """Adds valid proxy to available list, associates an user agent to a proxy"""
        if isinstance(proxy, Proxy):
            self._available_proxies.append((proxy, 0))
            self._update_counts()

    def get_proxy(self, max_wait_time: float = 30) -> Tuple[Optional[Proxy], int]:
        """Returns random proxy from list of available ones"""
        if self.rotation_strategy == ProxyRotationStrategy.CHOICE:
            return choice(self._available_proxies)
        elif self.rotation_strategy == ProxyRotationStrategy.DUMMY:
            return None, 0
        if self.live_count == 0:
            raise ProxyPoolDepletedError()
        start_time = int(time())
        proxy, retries = None, 0
        i = 0
        while True:
            if int(time()) - start_time > max_wait_time:
                raise ProxyPoolTimeoutError
            if i > 0:
                sleep(3)
            i += 1
            with self._lock:
                if not self.has_available_proxies():
                    continue
                # FIXME: resizing lists is slow, find other approach
                if self._rotation_strategy == ProxyRotationStrategy.CYCLE:
                    proxy, retries = self._available_proxies.pop(0)
                # TODO: implement random unique strategy
                elif self._rotation_strategy == ProxyRotationStrategy.RANDOM_UNIQUE:
                    proxy, retries = self._available_proxies.pop(
                        randrange(self._available_count)
                    )
                else:
                    proxy, retries = self._available_proxies.pop(
                        randrange(self._available_count)
                    )
                self._in_use_proxies[str(proxy)] = (proxy, retries)
                self._update_counts()
                if proxy is not None:
                    break

        return proxy, retries

    def return_proxy(self, proxy: Proxy, retries: int) -> bool:
        """Removes proxy from "in use" list, puts it back to "available" list or skips if proxy exceeds maximum retries
         count"""
        if self.rotation_strategy in (ProxyRotationStrategy.CHOICE, ProxyRotationStrategy.DUMMY):
            return True
        with self._lock:
            proxy_string = str(proxy)
            proxy_data = self._in_use_proxies.get(proxy_string)
            del self._in_use_proxies[proxy_string]
            _proxy, _retries = proxy_data
            _retries += retries
            if _retries < self._max_retries:
                self._available_proxies.append((_proxy, _retries))
            else:
                self._dead_proxies.append((_proxy, _retries))
            self._update_counts()

        return True

    @property
    def available_count(self) -> int:
        """Returns number of available proxies in proxy pool"""
        return self._available_count

    @property
    def in_use_count(self) -> int:
        """Returns number of in use proxies in proxy pool"""
        return self._in_use_count

    @property
    def live_count(self) -> int:
        """Returns number of live proxies in proxy pool"""
        return self._live_count

    @property
    def dead_count(self) -> int:
        """Returns number of dead proxies in proxy pool"""
        return self._dead_count

    @property
    def total_count(self) -> int:
        """Returns total number of proxies in proxy pool"""
        return self._total_count

    def has_available_proxies(self) -> bool:
        """Returns True if proxy pool has available proxies otherwise False"""
        return self.available_count > 0

    @property
    def rotation_strategy(self) -> ProxyRotationStrategy:
        """Returns proxy rotation strategy"""
        return self._rotation_strategy

    @rotation_strategy.setter
    def rotation_strategy(self, rotation_strategy: ProxyRotationStrategy):
        """Sets proxy rotation strategy"""
        self._rotation_strategy = rotation_strategy
