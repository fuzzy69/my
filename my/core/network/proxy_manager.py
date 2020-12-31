from typing import Union

try:
    from libs.my.core.meta.dummy_object import DummyObject
    from libs.my.core.network.proxy import Proxy
    from libs.my.core.network.proxy_pool import ProxyPool, ProxyPoolDepletedError
except ModuleNotFoundError:
    from core.meta.dummy_object import DummyObject
    from core.network.proxy import Proxy
    from core.network.proxy_pool import ProxyPool, ProxyPoolDepletedError


class ProxyManager:
    """Manages proxy pool, tracks proxy failures, removes burned ones from pool
    and ensures that one proxy is  always used by just one consumer"""

    def __init__(
        self, proxy_pool: Union[ProxyPool, DummyObject], max_wait_time: float = 30
    ):
        self._proxy_pool = proxy_pool
        self._max_wait_time = max_wait_time
        self._proxy = None
        self._proxy_retries = 0

    def add_failure(self):
        """Increases failure count for proxy"""
        self._proxy_retries += 1

    def get(self) -> Proxy:
        """Returns proxy from proxy pool"""
        if isinstance(self._proxy, Proxy):
            self._proxy_pool.return_proxy(self._proxy, self._proxy_retries)
        self._proxy, self._proxy_retries = self._proxy_pool.get_proxy(
            self._max_wait_time
        )

        return self._proxy

    def __enter__(self):
        """Override"""

        return self

    def __exit__(self, *args):
        """Override"""
        if isinstance(self._proxy, Proxy):
            self._proxy_pool.return_proxy(self._proxy, self._proxy_retries)
