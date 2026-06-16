import akshare as ak
import pandas as pd
import os
from fredapi import Fred
from dotenv import load_dotenv
import requests
load_dotenv()

def test_hstech_ak_sina():
    """使用 akshare 的新浪源获取恒生科技指数"""
    try:
        # 关键：强制 akshare 底层请求不走代理（避免个别环境问题）
        import os
        os.environ["HTTP_PROXY"] = ""
        os.environ["HTTPS_PROXY"] = ""

        print("通过 akshare (新浪源) 获取恒生科技指数...")
        df = ak.stock_hk_index_daily_sina(symbol="HSTECH")
        df = df[["date", "close"]]
        df["date"] = pd.to_datetime(df["date"])
        df = df.set_index("date").sort_index()

        print(f"✅ 成功！{len(df)} 条数据")
        print(f"范围: {df.index[0].date()} ~ {df.index[-1].date()}")
        print(f"最新收盘: {df.iloc[-1]['close']:.2f}")
        print(df.tail())
        return True
    except Exception as e:
        print(f"❌ akshare 新浪接口失败: {e}")
        return False


def test_cpi_yoy_direct():
    """直接用 requests 获取 CPIAUCSL_PC1（CPI 同比）"""
    api_key = os.getenv("FRED_API_KEY")
    series_id = "CPIAUCSL_PC1"

    url = "https://api.stlouisfed.org/fred/series/observations"
    
    params = {
        "series_id": series_id,
        "api_key": api_key,
        "file_type": "json",
        "observation_start": "2020-01-01",
        "sort_order": "desc",          # 最新数据在前
        "limit": 10,
    }

    try:
        resp = requests.get(url, params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json()

        if "observations" not in data:
            print("❌ 返回数据异常:", data)
            return False

        obs = data["observations"]
        if not obs:
            print("❌ 没有观测数据")
            return False

        # 转换为 Series
        df = pd.DataFrame(obs)
        df["value"] = pd.to_numeric(df["value"], errors="coerce")
        df["date"] = pd.to_datetime(df["date"])
        df = df.set_index("date")["value"].dropna().sort_index()

        print("✅ CPI 同比数据（最近 6 个值）：")
        print(df.tail(6))
        print(f"\n最新日期: {df.index[-1].strftime('%Y-%m-%d')}")
        print(f"最新 CPI 同比: {df.iloc[-1]:.1f}%")
        return True

    except Exception as e:
        print(f"❌ 失败: {e}")
        return False

def get_cpi_yoy(start_date="2010-01-01"):
    """计算 CPI 同比变化率（单位：%）"""
    # 获取原始 CPI 指数（至少需 13 个月历史）
    cpi_index = get_fred_series("CPIAUCSL", start=start_date)
    cpi_index = cpi_index.sort_index()
    # 同比 = (本月值 / 去年同月值 - 1) * 100
    cpi_yoy = cpi_index.pct_change(periods=12) * 100
    cpi_yoy = cpi_yoy.dropna()
    return cpi_yoy
    
if __name__ == "__main__":
    #test_cpi_yoy_direct()
    #test_cpi_yoy()
    yoy = get_cpi_yoy()
    print(f"最新 CPI 同比: {yoy.iloc[-1]:.1f}%")   # 应输出 4.2%
    print(yoy.tail(6))
