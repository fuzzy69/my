from platform import system
from typing import AnyStr

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

try:
    from libs.my.core.defaults import (
        USER_AGENT,
        CHROME_PATH,
        CHROME_DRIVER_PATH,
        SCREEN_WIDTH,
        SCREEN_HEIGHT,
        TIMEOUT,
    )
except ModuleNotFoundError:
    from core.defaults import (
        USER_AGENT,
        CHROME_PATH,
        CHROME_DRIVER_PATH,
        SCREEN_WIDTH,
        SCREEN_HEIGHT,
        TIMEOUT,
    )


class WebDriver:
    """WebDriver context manager class
    https://stackoverflow.com/a/48630668"""

    def __init__(
        self,
        chrome_path: AnyStr = CHROME_PATH,
        chrome_driver_path: AnyStr = CHROME_DRIVER_PATH,
        user_agent: AnyStr = USER_AGENT,
        window_width: int = SCREEN_WIDTH,
        window_height: int = SCREEN_HEIGHT,
        timeout: float = TIMEOUT,
    ):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument(f"--window-size={window_width},{window_height}")
        chrome_options.add_argument(f"--user-agent={user_agent}")
        if system() == "Linux":
            chrome_options.binary_location = chrome_path
            driver = webdriver.Chrome(
                executable_path=chrome_driver_path, chrome_options=chrome_options
            )
        else:
            driver = webdriver.Chrome(chrome_options=chrome_options)
        driver.set_page_load_timeout(timeout)
        self._driver = driver

    def __enter__(self):
        return self._driver

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._driver.quit()
