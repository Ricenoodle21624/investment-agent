import requests
import os
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")


def get_stock_pe(symbol):

    url = "https://www.alphavantage.co/query"

    params = {
        "function": "OVERVIEW",
        "symbol": symbol,
        "apikey": API_KEY,
    }

    try:

        resp = requests.get(
            url,
            params=params,
            timeout=15
        )

        resp.raise_for_status()

        data = resp.json()

        if "Note" in data:
            print(f"[PE] {symbol} rate limit")
            return None

        if "Error Message" in data:
            print(f"[PE] {symbol} error")
            return None

        return {
            "trailing_pe": try_float(
                data.get("TrailingPE")
            ),
            "forward_pe": try_float(
                data.get("ForwardPE")
            ),
            "peg": try_float(
                data.get("PEGRatio")
            )
        }

    except Exception as e:

        print(f"[PE] {symbol}", e)

        return None


def try_float(v):

    try:
        return float(v)
    except:
        return None