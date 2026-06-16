import requests
import re
import json

def get_a_share_pe_full(symbol_code, market="sh"):
    """
    获取 A 股静态 PE、动态 PE(TTM)、PEG
    symbol_code: 纯数字代码，如 '600519'
    market: 'sh' 或 'sz'
    返回 dict
    """
    full_symbol = f"{market}{symbol_code}"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://finance.sina.com.cn",
    }
    session = requests.Session()
    session.trust_env = False   # 绕过本地代理

    # ========== 1. 静态市盈率（腾讯财经） ==========
    pe_static = None
    try:
        url_tencent = f"https://qt.gtimg.cn/q={full_symbol}"
        resp = session.get(url_tencent, headers=headers, timeout=10)
        resp.encoding = "gbk"
        fields_tencent = resp.text.split('"')[1].split("~")
        # 静态市盈率在索引 39
        if len(fields_tencent) > 39:
            pe_static = float(fields_tencent[39]) if fields_tencent[39] else None
    except Exception as e:
        print(f"腾讯静态PE获取失败: {e}")

    # ========== 2. 动态市盈率（新浪行情） ==========
    pe_ttm = None
    try:
        url_sina = f"https://hq.sinajs.cn/list={full_symbol}"
        resp = session.get(url_sina, headers=headers, timeout=10)
        resp.encoding = "gbk"
        text = resp.text
        # 提取数据部分（可能包含类似 var hq_str_sh600519="..." 的前缀）
        data_str = text.split('"')[1] if '"' in text else text.split("=")[1]
        fields_sina = data_str.split(",")
        # 动态市盈率在索引 43（第44个字段）
        if len(fields_sina) > 43:
            pe_ttm = float(fields_sina[43]) if fields_sina[43] else None
    except Exception as e:
        print(f"新浪动态PE获取失败: {e}")

    # ========== 3. 净利润增长率（新浪 fund.js） ==========
    profit_growth = None
    try:
        url_fund = f"https://finance.sina.com.cn/realstock/company/{full_symbol}/fund.js"
        resp = session.get(url_fund, headers=headers, timeout=10)
        text = resp.text
        # 提取 JSON 部分（格式：var fund_data = {...};）
        match = re.search(r"var fund_data = (\{.*?\});", text, re.DOTALL)
        if not match:
            match = re.search(r"(\{.*?\})", text, re.DOTALL)
        if match:
            data = json.loads(match.group(1))
            # 净利润增长率（字符串，如 "15.23" 表示 15.23%）
            growth_str = data.get("net_profit_growth", "0")
            if growth_str and growth_str != "--":
                profit_growth = float(growth_str) / 100.0   # 转换为小数，例如 15.23% -> 0.1523
    except Exception as e:
        print(f"净利润增长率获取失败: {e}")

    # ========== 4. 计算 PEG = 动态PE / (净利润增长率 * 100) ==========
    peg = None
    if pe_ttm and profit_growth and profit_growth > 0:
        peg = pe_ttm / (profit_growth * 100)
    # 如果净利润增长率缺失，也可以用静态PE计算，但这里使用动态PE更贴合

    result = {
        "symbol": full_symbol,
        "trailing_pe": pe_static,
        "forward_pe_ttm": pe_ttm,
        "peg": round(peg, 2) if peg else None,
    }
    print(f"==== {full_symbol} ====")
    print(f"静态市盈率: {result['trailing_pe']}")
    print(f"动态市盈率 (TTM): {result['forward_pe_ttm']}")
    print(f"净利润增长率: {profit_growth*100 if profit_growth else None}%")
    print(f"PEG: {result['peg']}")
    return result

# 测试
if __name__ == "__main__":
    get_a_share_pe_full("600519", "sh")   # 贵州茅台
    print()
    get_a_share_pe_full("000001", "sz")   # 平安银行