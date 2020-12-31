from random import choice
from typing import AnyStr, Iterable, Optional

try:
    from libs.my.core.filesystem.file import read_text_file_lines
    from libs.my.core.network.proxy import Proxy
except ModuleNotFoundError:
    from core.filesystem.file import read_text_file_lines
    from core.network.proxy import Proxy


class UserAgentManager:
    """Binds random user agents to proxies"""

    def __init__(self, proxies: Iterable[Proxy], user_agents: Iterable[AnyStr]):
        self._proxy_user_agent_map = dict()
        self._user_agents = list(user_agents)
        for proxy in proxies:
            if proxy not in self._proxy_user_agent_map:
                self._proxy_user_agent_map[proxy] = choice(self._user_agents)

    def get(self, proxy: Optional[Proxy], default: AnyStr) -> AnyStr:
        """Returns user agent for chosen proxy"""
        if proxy is None:
            return default
        else:
            return self._proxy_user_agent_map.get(proxy)

    def random(self) -> AnyStr:
        """Returns random user agent string"""
        return choice(self._user_agents)


if __name__ == "__main__":
    USER_AGENTS_FILE = "../data/user_agents.txt"
    USER_AGENTS = read_text_file_lines(USER_AGENTS_FILE, unique=True)
    proxies = []
    proxies.append(Proxy.from_string("http://127.0.0.1:80"))
    proxies.append(Proxy.from_string("https://127.0.0.2:80"))
    proxies.append(Proxy.from_string("https://127.0.0.3:80"))
    uam = UserAgentManager(proxies, USER_AGENTS)
    for proxy in proxies:
        for _ in range(3):
            print(proxy, uam.get(proxy))
