import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
FRED_API_KEY = os.getenv("FRED_API_KEY")

BASE_URL = (
    "https://api.stlouisfed.org/fred/series/observations"
)


def get_fred_series(series_id):

    try:

        url = (
            f"{BASE_URL}"
            f"?series_id={series_id}"
            f"&api_key={FRED_API_KEY}"
            f"&file_type=json"
        )

        r = requests.get(url, timeout=15)

        r.raise_for_status()

        data = r.json()

        observations = data.get(
            "observations",
            []
        )

        if not observations:
            return None

        value = observations[-1]["value"]

        if value == ".":
            return None

        return float(value)

    except Exception as e:

        print(f"[fred:{series_id}] {e}")

        return None


# 美国10年国债收益率
def get_us10y():
    return get_fred_series("DGS10")


# CPI
def get_cpi():
    return get_fred_series("CPIAUCSL")


# 联邦基金利率
def get_fed_rate():
    return get_fred_series("FEDFUNDS")


# 纳斯达克指数
def get_nasdaq():
    return get_fred_series("NASDAQCOM")


# 标普500
def get_sp500():
    return get_fred_series("SP500")


# VIX
def get_vix():
    return get_fred_series("VIXCLS")


# 黄金（LBMA Gold Price）
def get_gold():
    return get_fred_series(
        "GOLDAMGBD228NLBM"
    )

def get_fred_observations(series_id):

    url = (
        "https://api.stlouisfed.org/fred/series/observations"
        f"?series_id={series_id}"
        f"&api_key={FRED_API_KEY}"
        f"&file_type=json"
    )

    r = requests.get(url, timeout=15)
    data = r.json()

    return data.get("observations", [])

def fetch_fred_series(
    series_id,
    start_date="2010-01-01"
):

    url = (
        "https://api.stlouisfed.org/fred/"
        "series/observations"
    )

    params = {
        "series_id": series_id,
        "api_key": FRED_API_KEY,
        "file_type": "json",
        "observation_start": start_date,
        "sort_order": "asc",
        "limit": 100000
    }

    resp = requests.get(
        url,
        params=params,
        timeout=15
    )

    resp.raise_for_status()

    data = resp.json()

    obs = data.get(
        "observations",
        []
    )

    if not obs:
        raise ValueError(
            f"{series_id} 无数据"
        )

    df = pd.DataFrame(obs)

    df["value"] = pd.to_numeric(
        df["value"],
        errors="coerce"
    )

    df["date"] = pd.to_datetime(
        df["date"]
    )

    df = (
        df
        .set_index("date")["value"]
        .dropna()
        .sort_index()
    )

    return df


def get_cpi_yoy():

    try:

        cpi_index = fetch_fred_series(
            "CPIAUCSL"
        )

        cpi_yoy = (
            cpi_index
            .pct_change(periods=12)
            * 100
        )

        return round(
            float(
                cpi_yoy.dropna().iloc[-1]
            ),
            2
        )

    except Exception as e:

        print("[cpi_yoy]", e)

        return None