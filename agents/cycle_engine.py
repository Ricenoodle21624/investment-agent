def judge_cycle(data):

    us10y = data["us10y"]
    cpi = data["cpi"]
    rate = data["fed_rate"]

    # 默认状态
    cycle = "unknown"
    risk = "medium"

    # 🔥 简单但非常有效的宏观规则
    if rate > 4.5 and us10y > 4.0:
        cycle = "high_rate"

    if cpi > 3 and rate > 5:
        risk = "high"

    if rate < 3.5:
        cycle = "easing"

    return {
        "cycle": cycle,
        "risk": risk
    }