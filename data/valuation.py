import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")


def get_stock_pe(symbol):

    url = "https://www.alphavantage.co/query"

    params = {
        "function": "OVERVIEW",
        "symbol": symbol,
        "apikey": API_KEY,
    }

    try:
        resp = requests.get(url, params=params, timeout=20)
        resp.raise_for_status()

        data = resp.json()

        if "Note" in data:
            raise Exception("AlphaVantage rate limit")

        if "Error Message" in data:
            raise Exception(data["Error Message"])

        def to_float(x):
            try:
                return float(x)
            except:
                return None

        return {
            "trailing_pe": to_float(data.get("TrailingPE")),
            "forward_pe": to_float(data.get("ForwardPE")),
            "peg": to_float(data.get("PEGRatio")),
        }

    except Exception as e:
        print(f"[PE] {symbol}", e)
        return None


# 兼容旧代码（很重要）
def get_us_pe(symbol):
    return get_stock_pe(symbol)