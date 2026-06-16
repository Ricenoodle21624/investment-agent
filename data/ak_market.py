import akshare as ak
import requests
import json
import re
import pandas as pd

def get_gold():

    url = (
        "https://stock2.finance.sina.com.cn/"
        "futures/api/jsonp.php/"
        "var%20_AU0=/"
        "InnerFuturesNewService.getDailyKLine"
    )

    params = {
        "symbol": "AU0",
        "_": int(pd.Timestamp.now().timestamp() * 1000)
    }

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:

        session = requests.Session()

        # 禁止读取系统代理
        session.trust_env = False

        resp = session.get(
            url,
            params=params,
            headers=headers,
            timeout=15
        )

        resp.raise_for_status()

        text = resp.text

        match = re.search(
            r'var _AU0=\(?(.*?)\)?;?\s*$',
            text,
            re.DOTALL
        )

        if not match:
            print("[gold] no jsonp match")
            return None

        json_str = match.group(1).strip()

        if not json_str or json_str == "null":
            print("[gold] empty")
            return None

        data = json.loads(json_str)

        if isinstance(data, dict):
            data = [data]

        df = pd.DataFrame(data)

        if "c" not in df.columns:
            print("[gold] no close")
            return None

        return float(df.iloc[-1]["c"])

    except Exception as e:

        print("[gold]", e)

        return None

def get_hstech():

    try:

        import os

        # 防止继承系统代理
        os.environ["HTTP_PROXY"] = ""
        os.environ["HTTPS_PROXY"] = ""
        os.environ["http_proxy"] = ""
        os.environ["https_proxy"] = ""

        df = ak.stock_hk_index_daily_sina(
            symbol="HSTECH"
        )

        if df is None or df.empty:
            print("[hstech] empty dataframe")
            return None

        return float(
            df.iloc[-1]["close"]
        )

    except Exception as e:

        print("[hstech]", e)

        return None

def get_shanghai():

    try:

        df = ak.stock_zh_index_daily(
            symbol="sh000001"
        )

        return float(
            df.iloc[-1]["close"]
        )

    except Exception as e:

        print("[shanghai]", e)

        return None


def get_chinext():

    try:

        df = ak.stock_zh_index_daily(
            symbol="sz399006"
        )

        return float(
            df.iloc[-1]["close"]
        )

    except Exception as e:

        print("[chinext]", e)

        return None