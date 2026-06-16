from data.market import get_market_data


def get_market_snapshot():
    """
    统一市场快照层
    - 不做分析
    - 只做结构化汇总
    """

    market = get_market_data()

    snapshot = {
        "us": {
        "nasdaq": market.get("nasdaq"),
        "sp500": market.get("sp500"),
        "vix": market.get("vix"),
        "us10y": market.get("us10y"),
        "fed_rate": market.get("fed_rate"),
        "cpi": market.get("cpi"),
        },
        "china": {
            "shanghai": market.get("shanghai"),
            "chinext": market.get("chinext"),
        },

        "global": {
            "gold": market.get("gold"),
            "hstech": market.get("hstech"),
        }
    }

    return snapshot
