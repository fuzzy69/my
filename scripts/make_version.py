from datetime import datetime
from os.path import abspath, basename, dirname, join
from pathlib import Path
from time import strftime, time


def seconds_since_midnight() -> int:
    """Returns number of seconds since midnight
    https://stackoverflow.com/a/15971505
    """
    now = datetime.now()
    seconds = int(
        (now - now.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()
    )

    return seconds


CURRENT_DIR = abspath(dirname(__file__))
PROJECT_DIR = Path(CURRENT_DIR).parent
PROJECT_NAME = basename(PROJECT_DIR)
SOURCES_DIR = join(PROJECT_DIR, PROJECT_NAME)
# VERSION_FORMAT = "%Y, %-m, %-d, %-H%M%S"
VERSION_FORMAT = "%Y, %-m, %-d"
SECONDS_SINCE_MIDNIGHT = seconds_since_midnight()


code = f"""__version__ = ({strftime(VERSION_FORMAT)}, {SECONDS_SINCE_MIDNIGHT if SECONDS_SINCE_MIDNIGHT > 0 else 1})

version_string = '.'.join(str(x) for x in __version__)


if __name__ == "__main__":
    print(version_string)
"""

VERSION_FILE = join(SOURCES_DIR, "version.py")
with open(VERSION_FILE, 'w') as f:
    f.write(code)
