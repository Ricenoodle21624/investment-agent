from datetime import datetime, timedelta


def get_market_briefing(market_data, valuation_data):
    """
    生成简单市场简报（V1版）
    """

    report = []

    # ======================
    # 美股
    # ======================
    report.append("【美股市场】")

    nasdaq = market_data.get("nasdaq")
    sp500 = market_data.get("sp500")
    vix = market_data.get("vix")

    report.append(f"纳斯达克: {nasdaq}")
    report.append(f"标普500: {sp500}")
    report.append(f"VIX: {vix}")

    if vix and vix > 20:
        report.append("⚠️ 风险提示：VIX偏高，市场波动加剧")

    # ======================
    # 宏观
    # ======================
    report.append("\n【宏观环境】")

    cpi = market_data.get("cpi")
    rate = market_data.get("fed_rate")

    report.append(f"CPI: {cpi}%")
    report.append(f"利率: {rate}%")

    if cpi and cpi > 4:
        report.append("⚠️ 通胀仍偏高，利率维持高位风险")

    # ======================
    # 港股
    # ======================
    report.append("\n【港股】")

    hstech = market_data.get("hstech")
    report.append(f"恒生科技: {hstech}")

    # ======================
    # A股
    # ======================
    report.append("\n【A股】")

    sh = market_data.get("shanghai")
    cyb = market_data.get("chinext")

    report.append(f"上证: {sh}")
    report.append(f"创业板: {cyb}")

    # ======================
    # AI估值提醒（简单版）
    # ======================
    report.append("\n【AI板块】")

    for symbol, item in valuation_data.items():
        pe = item.get("data", {})
        name = item.get("name")

        if pe.get("trailing_pe") and pe.get("trailing_pe") > 50:
            report.append(f"⚠️ {name} 估值偏高")

    return "\n".join(report)