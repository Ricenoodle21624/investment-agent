import requests
import json
import os

API_KEY = os.environ.get("ALPHA_VANTAGE_KEY", "你的API密钥") 


def get_stock_pe(symbol):
    """获取 PE 数据（调试版）"""
    url = "https://www.alphavantage.co/query"

    params = {
        "function": "OVERVIEW",
        "symbol": symbol,
        "apikey": API_KEY,
    }

    try:
        print(f"\n========== REQUEST ==========")
        print(f"symbol: {symbol}")

        resp = requests.get(url, params=params, timeout=15)
        resp.raise_for_status()

        data = resp.json()

        print("\n========== RESPONSE KEYS ==========")
        print(list(data.keys()))

        # 限流 / 错误检查
        if "Note" in data:
            print("❌ API限流:", data["Note"])
            return None

        if "Error Message" in data:
            print("❌ API错误:", data["Error Message"])
            return None

        trailing_pe = data.get("TrailingPE")
        forward_pe = data.get("ForwardPE")
        peg = data.get("PEGRatio")

        print("\n========== PE DATA ==========")
        print("Trailing PE:", trailing_pe)
        print("Forward PE:", forward_pe)
        print("PEG:", peg)

        return {
            "trailing_pe": trailing_pe,
            "forward_pe": forward_pe,
            "peg": peg
        }

    except Exception as e:
        print("❌ 请求失败:", e)
        return None


if __name__ == "__main__":

    # ====== 测试不同港股写法 ======

    symbols = [
        "00700.HK",   # 你当前用的（可能失败）
        "0700.HK",    # 推荐写法
        "TCEHY"       # ADR（最稳定）
    ]

    for s in symbols:
        print("\n" + "=" * 60)
        result = get_stock_pe(s)

        print("\nRESULT:", result)