import requests
import json
import pandas as pd
import re
import requests
from dotenv import load_dotenv



def test_gold_sina_au0():
    """测试新浪财经沪金连续合约日线（抗干扰版）"""
    url = "https://stock2.finance.sina.com.cn/futures/api/jsonp.php/var%20_AU0=/InnerFuturesNewService.getDailyKLine"
    params = {
        "symbol": "AU0",
        "_": int(pd.Timestamp.now().timestamp() * 1000)
    }
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        session = requests.Session()
        session.trust_env = False  # 禁用代理
        resp = session.get(url, params=params, headers=headers, timeout=15)
        resp.raise_for_status()
        text = resp.text

        # 移除开头的注释及所有非 JSONP 内容
        # 正则：匹配从 "var _AU0=" 开始的部分
        match = re.search(r'var _AU0=\(?(.*?)\)?;?\s*$', text, re.DOTALL)
        if not match:
            raise ValueError(f"无法匹配 JSONP 数据，原始内容: {text[:300]}")

        json_str = match.group(1).strip()
        if json_str == "null" or not json_str:
            print("⚠️ 返回 null 或空")
            return False

        # 新浪实际返回的是数组，但可能被外层括号包裹
        data = json.loads(json_str)
        if isinstance(data, dict):
            data = [data]  # 个别情况

        df = pd.DataFrame(data)
        if "d" not in df.columns or "c" not in df.columns:
            print("❌ 缺失字段，现有列:", list(df.columns))
            return False

        df = df[["d", "c"]].rename(columns={"d": "date", "c": "close"})
        df["date"] = pd.to_datetime(df["date"])
        df["close"] = df["close"].astype(float)
        df = df.set_index("date").sort_index()

        print(f"✅ 成功！{len(df)} 条数据")
        print(f"范围: {df.index[0].date()} 至 {df.index[-1].date()}")
        print(f"最新价: {df.iloc[-1]['close']:.2f} 元/克")
        print(df.tail())
        return True

    except Exception as e:
        print(f"❌ 失败: {e}")
        return False

if __name__ == "__main__":
    load_dotenv()
    test_gold_sina_au0()