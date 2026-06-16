def format_pe(v):

    if not v:
        return "N/A"

    try:
        return f"{v:.2f}"
    except:
        return str(v)

def safe(v, default="N/A"):
    return default if v is None else v


def build_report(
    data,
    cycle_info,
    allocation,
    analysis,
    market,
    valuation
):

    timestamp = data.get("timestamp", "unknown")

    # ==========================
    # 宏观数据（安全兜底）
    # ==========================
    us10y = safe(data.get("us10y"), "N/A")
    cpi = safe(data.get("cpi"), "N/A")
    fed_rate = safe(data.get("fed_rate"), "N/A")

    # ==========================
    # 市场数据（关键修复）
    # ==========================
    def mget(group, key):
        try:
            return market.get(group, {}).get(key, "N/A")
        except:
            return "N/A"

    nasdaq = mget("us", "nasdaq")
    sp500 = mget("us", "sp500")
    vix = mget("us", "vix")

    gold = mget("global", "gold")
    hstech = mget("global", "hstech")

    shanghai = mget("china", "shanghai")
    chinext = mget("china", "chinext")

    # ==========================
    # 分析兜底
    # ==========================
    if not analysis:
        analysis = "暂无AI分析输出（可能模型限流或解析失败）"

    # ==========================
    # 估值（关键修复：分组输出）
    # ==========================
    def format_valuation_block(title, items):
        text = f"\n{title}\n\n"
        if not items:
            return text + "暂无数据\n"

        for k, v in items.items():
            if isinstance(v, dict):
                text += f"{v.get('name', k)}\n"
                d = v.get("data", {}) or {}
                text += f"PE: {safe(d.get('trailing_pe'))}\n"
                text += f"Forward PE: {safe(d.get('forward_pe'))}\n"
                text += f"PEG: {safe(d.get('peg'))}\n\n"
        return text

    us_val = valuation.get("us", {})
    hk_val = valuation.get("hk", {})
    a_val = valuation.get("a", {})

    report = f"""
投资决策日报

数据时间
{timestamp}

━━━━━━━━━━━━━━━━━━

宏观数据

美国10年国债收益率
{us10y}

美国CPI同比
{cpi}

联邦基金利率
{fed_rate}

━━━━━━━━━━━━━━━━━━

全球市场表现

纳斯达克指数
{nasdaq}

标普500指数
{sp500}

VIX恐慌指数
{vix}

黄金现货（沪金AU0）
{gold}

恒生科技指数
{hstech}

上证指数
{shanghai}

创业板指数
{chinext}

━━━━━━━━━━━━━━━━━━

资产配置建议

权益ETF
{int(allocation.get("equity_etf", 0) * 100)}%

黄金
{int(allocation.get("gold", 0) * 100)}%

现金
{int(allocation.get("cash", 0) * 100)}%

━━━━━━━━━━━━━━━━━━

AI市场分析

{analysis}

━━━━━━━━━━━━━━━━━━

{format_valuation_block("美股估值", us_val)}

━━━━━━━━━━━━━━━━━━

{format_valuation_block("港股估值", hk_val)}

━━━━━━━━━━━━━━━━━━

{format_valuation_block("A股估值", a_val)}

━━━━━━━━━━━━━━━━━━
"""

    return report