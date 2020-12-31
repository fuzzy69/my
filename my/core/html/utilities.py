from re import findall, IGNORECASE
from typing import Any, AnyStr, Dict, Iterable, Optional, Tuple, Union
from urllib.parse import urlparse

from lxml import etree
from lxml.html import fromstring
from lxml.html.clean import Cleaner

try:
    from libs.my.core.text.utilities import trim_whitespaces
except ModuleNotFoundError:
    from core.text.utilities import trim_whitespaces


def get_first(dom: Any, xpath: AnyStr, default: Optional[Any] = None) -> Optional[Any]:
    """Returns first matched element from DOM by xpath expression otherwise 
    default value"""
    elements = dom.xpath(xpath)
    if len(elements) == 0:
        return None if default is None else default

    return elements[0]


def get_last(dom: Any, xpath: AnyStr, default: Optional[Any] = None) -> Optional[Any]:
    """Returns last element matched by given XPATH query otherwise None"""
    element = default
    elements = dom.xpath(xpath)
    for element in elements:
        pass

    return element


def get_all(dom: Any, xpath: AnyStr) -> Iterable[Any]:
    """Yields all matched elements from DOM by xpath expression"""
    elements = dom.xpath(xpath)
    if len(elements) == 0:
        yield from []
    for element in elements:
        yield element


def extract_links(html: str, base_url: str = None) -> Iterable[Tuple[str, str]]:
    """Yields link URL and link text tuple"""
    urls = set()
    dom = fromstring(html)
    if base_url is not None:
        dom.make_links_absolute(base_url)
    for link in dom.xpath("//a"):
        url = link.attrib.get("href")
        if url is not None:
            if url not in urls:
                text = link.text_content().strip()
                urls.add(url)
                yield url, text


def extract_internal_links(html: AnyStr, base_url: AnyStr) -> Iterable[Tuple[AnyStr, AnyStr]]:
    """Yields pair of link url and link text of all links from given HML text"""
    for url, text in extract_links(html, base_url):
        if urlparse(url).netloc == urlparse(base_url).netloc:
            yield url, text


def extract_inbound_links(html: str, base_url: str) -> Iterable[Tuple[str, str]]:
    """Yields pair of link url and link text of all links from given HML text"""
    for url, text in extract_links(html, base_url):
        if urlparse(url).netloc == urlparse(base_url).netloc:
            yield url, text


def extract_keywords_frequency(
    text: str, keywords: set, result: dict
) -> Dict[str, int]:
    """Returns dictionary where key is a keyword and value is keyword frequency"""
    text = (
        " " + text + " "
    )  # Prepend and append non-alphanumeric character to enable matching of first and last word
    for keyword in keywords:
        matches = findall(
            r"\W+{keyword}\W+".format(keyword=trim_whitespaces(keyword)),
            text,
            IGNORECASE,
        )
        matches_count = len(matches)
        if matches_count > 0:
            result[keyword] += matches_count

    return result


def extract_text_from_html(html: Any) -> AnyStr:
    """Returns inner text of all tags from given HTML code"""
    if isinstance(html, str):
        dom = fromstring(html)
    else:
        dom = html
    cleaner = Cleaner()
    cleaner.javascript = True
    cleaner.style = True
    dom = cleaner.clean_html(dom)
    els = dom.xpath("//body")
    if len(els) == 0:
        return ""
    text = " ".join(el for el in els[0].itertext())
    text = trim_whitespaces(text)

    return text


def parse_sitemap(text: AnyStr, unique: bool=True) -> Iterable[AnyStr]:
    """Yields URLs from sitemap file text, skips duplicate URLs if unique is set to True"""
    text = text.encode("utf-8")
    root = etree.fromstring(text)
    urls = set()
    for sitemap in root:
        for child in sitemap.getchildren():
            if "loc" in child.tag:
                url = child.text.strip()
                if unique:
                    if url in urls:  # Duplicate URL, skip it
                        continue
                    else:
                        urls.add(url)
                yield child.text.strip()
