from typing import Any, AnyStr, Callable, Optional

from requests import Response, Session
from requests.cookies import RequestsCookieJar
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

try:
    from libs.my.core.defaults import USER_AGENT, TIMEOUT, RETRIES, HEADERS
    from libs.my.core.network.proxy import Proxy
except ModuleNotFoundError:
    from core.defaults import USER_AGENT, TIMEOUT, RETRIES, HEADERS
    from core.network.proxy import Proxy


class TimeoutHTTPAdapter(HTTPAdapter):
    """Request library timeout HTTP adapter"""

    def __init__(self, *args, **kwargs):
        self.timeout = TIMEOUT
        if "timeout" in kwargs:
            self.timeout = kwargs["timeout"]
            del kwargs["timeout"]
        super().__init__(*args, **kwargs)

    def send(self, request, **kwargs):
        """Sets request timeout value"""
        timeout = kwargs.get("timeout")
        if timeout is None:
            kwargs["timeout"] = self.timeout

        return super().send(request, **kwargs)


class HttpClient:
    """HTTP client class"""

    def __init__(self, logging_callback: Optional[Callable] = None):
        self._session = Session()
        self._user_agent = USER_AGENT
        self._timeout = TIMEOUT
        self._retries = RETRIES
        self._headers = HEADERS
        self._proxy = None
        self._referrer_url = None
        self._timeout_adapter = None

        if logging_callback is not None:
            self._session.hooks["response"] = [self._logging_hook]
            self._logging_callback = logging_callback

    def __enter__(self):
        self._session.__enter__()

        return self

    def __exit__(self, type, value, traceback):
        self._session.__exit__(self, type, value, traceback)

    def _init(self):
        self._retry_strategy = Retry(
            total=self.retries,
            status_forcelist=[413, 429, 500, 502, 503, 504],
            method_whitelist=["HEAD", "GET", "OPTIONS"],
            backoff_factor=2,
        )

        self._timeout_adapter = TimeoutHTTPAdapter(
            timeout=5, max_retries=self._retry_strategy
        )
        self._session.mount("https://", self._timeout_adapter)
        self._session.mount("http://", self._timeout_adapter)

    @property
    def user_agent(self) -> AnyStr:
        """Returns user agent string"""
        return self._headers.get("User-Agent", "")

    @user_agent.setter
    def user_agent(self, user_agent: AnyStr):
        """Sets user agent string"""
        self._headers["User-Agent"] = user_agent

    @property
    def proxy(self) -> Proxy:
        """Returns current proxy"""
        return self._proxy

    @proxy.setter
    def proxy(self, proxy: Proxy):
        """Sets current proxy"""
        self._proxy = proxy

    @property
    def timeout(self) -> float:
        """Returns timeout value"""
        return self._timeout

    @timeout.setter
    def timeout(self, timeout: float):
        """Sets timeout"""
        self._timeout = timeout

    @property
    def retries(self) -> int:
        """Return current retries count"""
        return self._retries

    @retries.setter
    def retries(self, retries: int):
        """Sets retries count"""
        self._retries = retries

    @property
    def referrer_url(self) -> AnyStr:
        """Returns current referrer URL"""
        return self._referrer_url

    @referrer_url.setter
    def referrer_url(self, referrer_url: AnyStr):
        """Sets current referrer URL"""
        self._referrer_url = referrer_url

    @property
    def cookies(self) -> RequestsCookieJar:
        """Returns cookie jar"""
        return self._session.cookies

    def _process_kwargs(self, kwargs: Any) -> Any:
        """Sets request arguments"""
        if self._timeout_adapter is None:
            self._init()
        if kwargs is None:
            kwargs = {}
        if "headers" not in kwargs:
            kwargs["headers"] = self._headers
        if "proxies" not in kwargs and self._proxy is not None:
            auth = ""
            if all((self.proxy.username, self.proxy.password)):
                auth = f"{self.proxy.username}:{self.proxy.password}@"
            kwargs["proxies"] = {
                "http": f"http://{auth}{self._proxy.ip}:{self._proxy.port}/",
                "https": f"https://{auth}{self._proxy.ip}:{self._proxy.port}/",
            }
        if "timeout" not in kwargs:
            kwargs["timeout"] = self.timeout
        if "referrer_url" in kwargs:
            kwargs["headers"]["Referer"] = kwargs["referrer_url"]
            del kwargs["referrer_url"]

        return kwargs

    def get(self, url: AnyStr, **kwargs: Any) -> Response:
        """Performs GET request and returns response instance"""
        kwargs = self._process_kwargs(kwargs)

        return self._session.get(url, **kwargs)

    def try_get(self, url: AnyStr, **kwargs: Any) -> Optional[Response]:
        """Tries to perform GET request, returns response instance on success otherwise None"""
        try:
            return self.get(url, **kwargs)
        except Exception as e:
            return None

    def _logging_hook(self, response: Response, *args, **kwargs):
        """Adds logging callback function to a response instance"""
        self._logging_callback(response, *args, **kwargs)
