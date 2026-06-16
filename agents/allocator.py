def allocate(cycle_info):

    cycle = cycle_info["cycle"]
    risk = cycle_info["risk"]

    # 默认
    allocation = {
        "equity_etf": 0.6,
        "gold": 0.2,
        "cash": 0.2
    }

    # 高利率环境（降低权益）
    if cycle == "high_rate":
        allocation = {
            "equity_etf": 0.5,
            "gold": 0.3,
            "cash": 0.2
        }

    # 降息周期（增加风险资产）
    elif cycle == "easing":
        allocation = {
            "equity_etf": 0.75,
            "gold": 0.15,
            "cash": 0.1
        }

    # 高风险环境
    if risk == "high":
        allocation["equity_etf"] -= 0.1
        allocation["gold"] += 0.1

    return allocation