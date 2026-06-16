EVENTS = [
    {
        "name": "FOMC会议",
        "date": "2026-06-17",
        "desc": "美联储利率决议，影响全球流动性"
    },
    {
        "name": "美国CPI",
        "date": "2026-06-12",
        "desc": "通胀核心数据"
    },
    {
        "name": "NVIDIA财报",
        "date": "2026-06-25",
        "desc": "AI板块最关键事件"
    }
]
def get_event_analysis():

    from datetime import datetime

    today = datetime.now().date()

    result = []

    for e in EVENTS:

        d = datetime.strptime(e["date"], "%Y-%m-%d").date()
        days = (d - today).days

        if days >= 0:

            result.append(
                f"{e['name']} ({days}天后)\n"
                f"重点：{e['desc']}\n"
            )

    return "\n".join(result)