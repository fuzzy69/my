from re import findall
from typing import AnyStr, Optional, Set, Tuple

try:
    from libs.my.core.defaults import USER_AGENT, SCREEN_WIDTH, SCREEN_HEIGHT
    from libs.my.core.html.utilities import extract_text_from_html
    from libs.my.core.network.ip_address import IPAddress
    from libs.my.core.network.utilities import regex_proxy
    from libs.my.extra.selenium.utilities import WebDriver
except ModuleNotFoundError:
    from core.defaults import USER_AGENT, SCREEN_WIDTH, SCREEN_HEIGHT
    from core.html.utilities import extract_text_from_html
    from core.network.ip_address import IPAddress
    from core.network.utilities import regex_proxy
    from extra.selenium.utilities import WebDriver


def scrape_proxies(url: AnyStr, timeout: int) -> Tuple[Set, Optional[AnyStr]]:
    """Returns a set of proxies scraped from proxy source URL"""
    results = set()
    error = None
    try:
        with WebDriver(
            user_agent=USER_AGENT,
            window_width=SCREEN_WIDTH,
            window_height=SCREEN_HEIGHT,
            timeout=timeout,
        ) as wd:
            wd.get(url)
            element = wd.find_element_by_xpath("//html")
            if element:
                html = element.get_attribute("innerHTML")
                text = extract_text_from_html(html)
                matches = findall(regex_proxy, text)
                for ip, port in matches:
                    if IPAddress.validate(ip):
                        results.add((ip, port))
    except Exception as e:
        error = str(e)

    return results, error