import logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SHORTS_URLS_STORAGE_FILEPATH = BASE_DIR / "short-urls.json"

LOG_LEVEL = logging.INFO
LOG_FORMAT: str = (
    "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
)
API_TOKENS: frozenset[str] = frozenset(
    {
        "EdaUF6NX0--OrT10f-oBIQ",
        "5qTHyP5pQLIoVaQ9gPjJow",
    }
)
# Only for demo!
# no real users in code!!
USER_DB: dict[str, str] = {
    # username: password
    "sam": "password",
    "bob": "qwerty",
}


REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0
