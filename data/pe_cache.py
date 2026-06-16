import os
import json
from datetime import datetime, timedelta

CACHE_FILE = "cache/pe_cache.json"
CACHE_DAYS = 7


def load_cache():

    if not os.path.exists(CACHE_FILE):
        return {}

    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}


def save_cache(cache):

    os.makedirs("cache", exist_ok=True)

    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=2)


def is_expired(date_str):

    try:
        cache_date = datetime.strptime(
            date_str,
            "%Y-%m-%d"
        )

        return (
            datetime.now()
            - cache_date
        ) > timedelta(days=CACHE_DAYS)

    except:
        return True