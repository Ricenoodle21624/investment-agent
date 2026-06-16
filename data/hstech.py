import requests


def get_hstech():

    url = "https://push2his.eastmoney.com/api/qt/stock/kline/get"
    params = {
        "fields1": "f1,f2,f3,f4,f5,f6",
        "fields2": "f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61",
        "secid": "124.HSTECH",   # 恒生科技指数代码
        "klt": "101",           # 日线
        "fqt": "1",            # 前复权
        "end": "20500101",
        "lmt": "10000",        # 最大返回条数
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": "https://quote.eastmoney.com/",
    }

    try:

        r = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=15,
            proxies={}
        )

        r.raise_for_status()

        data = r.json()

        if not data.get("data"):
            return None

        klines = data["data"].get(
            "klines"
        )

        if not klines:
            return None

        latest = klines[-1]

        close_price = float(
            latest.split(",")[2]
        )

        return close_price

    except Exception as e:

        print("[hstech]", e)

        return None