import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("FRED_API_KEY")

def fetch_fred_series(series_id, start_date="2010-01-01"):
    """
    通用 FRED 系列获取函数（与你自己封装的 get_fred_series 逻辑一致）
    返回 pandas.Series，索引为日期，值为数值
    """
    url = "https://api.stlouisfed.org/fred/series/observations"
    params = {
        "series_id": series_id,
        "api_key": API_KEY,
        "file_type": "json",
        "observation_start": start_date,
        "sort_order": "asc",
        "limit": 100000,  # 足够大
    }
    resp = requests.get(url, params=params, timeout=15)
    resp.raise_for_status()
    data = resp.json()
    obs = data.get("observations", [])
    if not obs:
        raise ValueError("未获取到任何观测值")
    
    df = pd.DataFrame(obs)
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    df["date"] = pd.to_datetime(df["date"])
    df = df.set_index("date")["value"].dropna().sort_index()
    return df

def get_cpi_yoy():
    """获取 CPI 同比变化率（单位：%）"""
    # 获取原始 CPI 指数（月度）
    cpi_index = fetch_fred_series("CPIAUCSL", start_date="2010-01-01")
    # 计算 12 个月同比： (当前值 / 去年同期值 - 1) * 100
    cpi_yoy = cpi_index.pct_change(periods=12) * 100
    return cpi_yoy.dropna()

def test_cpi_yoy():
    """完整测试：打印 CPI 同比最新值及近期趋势"""
    print("="*60)
    print("CPI 同比变化率测试 (基于 FRED CPIAUCSL)")
    print("="*60)

    try:
        yoy = get_cpi_yoy()
        if yoy.empty:
            print("❌ 计算后的同比数据为空")
            return False

        latest_date = yoy.index[-1]
        latest_val = yoy.iloc[-1]
        print(f"\n✅ 数据获取成功")
        print(f"最新数据日期: {latest_date.strftime('%Y-%m-%d')}")
        print(f"最新 CPI 同比: {latest_val:.1f}%")
        print("\n最近 6 个月同比数据：")
        print(yoy.tail(6).to_string(float_format=lambda x: f"{x:.1f}%"))
        return True

    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        return False

if __name__ == "__main__":
    test_cpi_yoy()