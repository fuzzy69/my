TIMEOUT = 30
RETRIES = 2
DELAY = 1
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/71.0"
)
LOG_FORMAT = (
    "%(asctime)s [%(name)s] <%(threadName)s> %(levelname)s: %(message)s",
    "%Y-%m-%d %H:%M:%S",
)

HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    "Cache-Control": "max-age=0",
    "User-Agent": USER_AGENT,
}

SCREEN_WIDTH = 1366
SCREEN_HEIGHT = 768
CHROME_PATH = "/usr/bin/google-chrome"
CHROME_DRIVER_PATH = "/usr/bin/chromedriver"
