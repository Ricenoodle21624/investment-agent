import os
import requests
import time

API_KEY = os.environ.get("ALPHA_VANTAGE_KEY", "你的API密钥")  # 替换为你的真实 Key

def get_pe_data(symbol):
    """
    通过 Alpha Vantage OVERVIEW 获取一只股票的市盈率数据。
    symbol 格式：
      - 美股：直接填代码，如 "AAPL"
      - 港股：代码.交易所，如 "0700.HK" 或 "00700.HK"
    返回 dict 包含 TrailingPE, ForwardPE, PEGRatio
    """
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "OVERVIEW",
        "symbol": symbol,
        "apikey": API_KEY,
    }
    try:
        resp = requests.get(url, params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json()

        # 如果触发限流，等待后重试
        if "Note" in data:
            print(f"⚠️ 触发请求频率限制，等待 12 秒后重试 {symbol}...")
            time.sleep(12)
            resp = requests.get(url, params=params, timeout=15)
            data = resp.json()

        if "Error Message" in data:
            raise ValueError(f"API 返回错误: {data['Error Message']}")

        trailing_pe = data.get("TrailingPE", "N/A")
        forward_pe = data.get("ForwardPE", "N/A")
        peg = data.get("PEGRatio", "N/A")

        print(f"==== {symbol} 市盈率 ====")
        print(f"静态市盈率 (Trailing PE): {trailing_pe}")
        print(f"预期市盈率 (Forward PE): {forward_pe}")
        print(f"PEG 比率: {peg}")
        print()
        return {
            "symbol": symbol,
            "trailing_pe": trailing_pe,
            "forward_pe": forward_pe,
            "peg": peg,
        }

    except Exception as e:
        print(f"❌ 获取 {symbol} 失败: {e}")
        return None

if __name__ == "__main__":
    # 测试美股
    #get_pe_data("AAPL")      # 苹果
    #time.sleep(12)           # 免费版每分钟最多 5 次，控制频率
    #get_pe_data("TSLA")      # 特斯拉

    #time.sleep(12)
    # 测试港股（注意港股代码可能有前导零，常见格式：00700.HK 或 0700.HK）
    get_pe_data("00700.HK")   # 腾讯控股 (00700)
    #time.sleep(12)
    get_pe_data("09988.HK")   # 阿里巴巴-SW (09988)