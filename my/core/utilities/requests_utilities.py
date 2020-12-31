from typing import AnyStr, Dict, Optional

try:
    from libs.my.core.defaults import USER_AGENT, TIMEOUT
    from libs.my.core.network.proxy import Proxy
except ModuleNotFoundError:
    from core.defaults import USER_AGENT, TIMEOUT
    from core.network.proxy import Proxy


def set_kwargs(
    headers: Optional[Dict] = None,
    user_agent: AnyStr = USER_AGENT,
    proxy: Optional[Proxy] = None,
    timeout: int = TIMEOUT,
    **kwargs,
) -> Dict:
    """Returns constructed arguments dictionary for requests"""
    if not kwargs:
        kwargs = {}
    if headers is None:  # Add default headers
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-US,en;q=0.5",
            "Cache-Control": "max-age=0",
        }
    if "headers" not in kwargs:  # Use default headers
        kwargs["headers"] = headers
    if proxy is not None:
        auth = (
            f"{proxy.username}:{proxy.password}@"
            if proxy.username and proxy.password
            else ""
        )
        kwargs["proxies"] = {
            "http": f"http://{auth}{proxy.ip}:{proxy.port}/",
            "https": f"https://{auth}{proxy.ip}:{proxy.port}/",
        }
    kwargs["headers"]["User-Agent"] = user_agent
    kwargs["timeout"] = timeout

    return kwargs
