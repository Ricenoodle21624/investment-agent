from datetime import datetime

from config_loader import load_watchlist

from data.pe_cache import (
    load_cache,
    save_cache
)

from data.valuation_us import (
    get_stock_pe
)

from data.valuation_cn import (
    get_cn_stock_pe
)


def is_valid_pe(pe):

    if not pe:
        return False

    return any([
        pe.get("trailing_pe") is not None,
        pe.get("forward_pe") is not None,
        pe.get("peg") is not None
    ])


def cache_expired(
    cache_item,
    days=7
):

    if not cache_item:
        return True

    timestamp = cache_item.get(
        "timestamp"
    )

    if not timestamp:
        return True

    try:

        cache_date = datetime.strptime(
            timestamp,
            "%Y-%m-%d"
        )

        age = (
            datetime.now()
            -
            cache_date
        ).days

        return age >= days

    except Exception:

        return True


def get_cached_or_fetch(
    symbol,
    name,
    cache,
    fetch_func,
    source="unknown"
):

    cache_item = cache.get(symbol)

    cached = None

    if cache_item:

        cached = cache_item.get(
            "data"
        )

    # ==========================
    # Cache Hit
    # ==========================

    if (
        is_valid_pe(cached)
        and
        not cache_expired(cache_item)
    ):

        age = (
            datetime.now()
            -
            datetime.strptime(
                cache_item["timestamp"],
                "%Y-%m-%d"
            )
        ).days

        print(
            f"[CACHE HIT] "
            f"{symbol} "
            f"({name}) "
            f"source="
            f"{cache_item.get('source', 'unknown')} "
            f"age={age}d"
        )

        return cached

    # ==========================
    # Cache Expired
    # ==========================

    if cache_item:

        print(
            f"[CACHE EXPIRED] "
            f"{symbol} "
            f"({name}) "
            f"{cache_item.get('timestamp')}"
        )

    else:

        print(
            f"[CACHE MISS] "
            f"{symbol} "
            f"({name})"
        )

    print(
        f"[API FETCH] "
        f"{symbol}"
    )

    pe_data = fetch_func()

    if is_valid_pe(pe_data):

        print(
            f"[API OK] "
            f"{symbol}"
        )

    else:

        print(
            f"[API FAIL] "
            f"{symbol}"
        )

    cache[symbol] = {

        "source": source,

        "data": pe_data,

        "timestamp":
            datetime.now()
            .strftime("%Y-%m-%d")
    }

    return pe_data


def get_valuation_data():

    watchlist = load_watchlist()

    cache = load_cache()

    result = {

        "us": {},

        "hk": {},

        "a": {}
    }

    print(
        "\n========== PE START ==========\n"
    )

    # ==========================
    # US
    # ==========================

    for symbol, name in watchlist.get(
        "us",
        {}
    ).items():

        pe_data = get_cached_or_fetch(

            symbol,

            name,

            cache,

            lambda:
                get_stock_pe(symbol),

            source="alphavantage"
        )

        result["us"][symbol] = {

            "name": name,

            "data": pe_data
        }

    # ==========================
    # HK
    # ==========================

    for symbol, name in watchlist.get(
        "hk",
        {}
    ).items():

        code = symbol.replace(
            ".HK",
            ""
        )

        pe_data = get_cached_or_fetch(

            symbol,

            name,

            cache,

            lambda:
                get_cn_stock_pe(
                    code,
                    "hk"
                ),

            source="sina/tencent"
        )

        result["hk"][symbol] = {

            "name": name,

            "data": pe_data
        }

    # ==========================
    # A Share
    # ==========================

    for symbol, name in watchlist.get(
        "a",
        {}
    ).items():

        market = symbol[:2]

        code = symbol[2:]

        pe_data = get_cached_or_fetch(

            symbol,

            name,

            cache,

            lambda:
                get_cn_stock_pe(
                    code,
                    market
                ),

            source="sina/tencent"
        )

        result["a"][symbol] = {

            "name": name,

            "data": pe_data
        }

    save_cache(cache)

    print(
        "\n========== PE END ==========\n"
    )

    return result