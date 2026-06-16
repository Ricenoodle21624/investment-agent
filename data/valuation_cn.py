import requests
import json
import re


def get_cn_stock_pe(symbol, market):
    """
    symbol:
        A股: 600519 / 000001
        港股: 00700.HK
    market:
        sh / sz / hk
    """

    session = requests.Session()
    session.trust_env = False

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    pe_static = None
    pe_ttm = None
    growth = None

    # =========================
    # 1. 处理 symbol 格式
    # =========================

    if market == "hk":
        code = symbol.replace(".HK", "")
        full_symbol = f"hk{int(code)}"   # ✔ 去掉前导0
    else:
        full_symbol = f"{market}{symbol}"

    # ====================
    # 腾讯 PE（静态）
    # ====================

    try:
        url = f"https://qt.gtimg.cn/q={full_symbol}"
        r = session.get(url, headers=headers, timeout=10)
        r.encoding = "gbk"

        fields = r.text.split('"')[1].split("~")

        if len(fields) > 39:
            pe_static = float(fields[39]) if fields[39] else None

    except Exception as e:
        print("[CN PE]", full_symbol, e)

    # ====================
    # 新浪 TTM PE
    # ====================

    try:
        url = f"https://hq.sinajs.cn/list={full_symbol}"
        r = session.get(url, headers=headers, timeout=10)
        r.encoding = "gbk"

        if '"' in r.text:
            data_str = r.text.split('"')[1]
            fields = data_str.split(",")

            if len(fields) > 43:
                pe_ttm = float(fields[43]) if fields[43] else None

    except Exception as e:
        print("[CN TTM]", full_symbol, e)

    # ====================
    # PEG（增长率）
    # ====================

    try:
        url = f"https://finance.sina.com.cn/realstock/company/{full_symbol}/fund.js"
        r = session.get(url, headers=headers, timeout=10)

        match = re.search(r"(\{.*?\})", r.text, re.DOTALL)

        if match:
            data = json.loads(match.group(1))

            growth_str = data.get("net_profit_growth")

            if growth_str and growth_str != "--":
                growth = float(growth_str)   # ✔ 百分比

    except Exception:
        pass

    # ====================
    # PEG 计算（修复）
    # ====================

    peg = None

    if pe_ttm and growth and growth > 0:
        peg = round(pe_ttm / (growth / 100), 2)

    return {
        "trailing_pe": pe_static,
        "forward_pe": pe_ttm,
        "peg": peg
    }