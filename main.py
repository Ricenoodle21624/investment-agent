from data_layer.market_snapshot import get_market_snapshot
from data_layer.event_generator import generate_events
from ai_layer.prompt_builder import build_prompt
from ai_layer.market_ai import run_ai
from data.valuation_service import get_valuation_data
from report.builder import build_report
from mailer.sender import send_email
from datetime import datetime

def main():
    today = datetime.now().strftime(
        "%Y-%m-%d"
    )

    subject = (
        f"Investment Agent Daily Report | "
        f"{today}"
    )
    snapshot = get_market_snapshot()
    from pprint import pprint

    print("\n===== SNAPSHOT =====")
    pprint(snapshot)

    valuation = get_valuation_data()

    print("\n===== VALUATION =====")
    pprint(valuation)

    events = generate_events("2026-06-14")

    prompt = build_prompt({
        "date": "2026-06-14",
        "market": snapshot,
        "events": events,
        "focus_themes": ["AI", "rates", "liquidity"]
    })

    analysis = run_ai(prompt)


    report = build_report(
        data={
            "timestamp": "today",

            "cpi":
                snapshot["us"]["cpi"],

            "us10y":
                snapshot["us"]["us10y"],

            "fed_rate":
                snapshot["us"]["fed_rate"]
        },
        cycle_info={"cycle": "AI liquidity regime", "risk": "dynamic"},
        allocation={"equity_etf": 0.7, "gold": 0.2, "cash": 0.1},
        analysis=analysis,
        market=snapshot,
        valuation=valuation
    )

    print(report)
    print("\n========== REPORT END ==========\n")

    print("\n========== EMAIL START ==========\n")

    try:

        send_email(
        subject=subject,
        content=report
    )

        print(
            "[EMAIL] SUCCESS"
        )

    except Exception as e:

        print(
            "[EMAIL] FAIL:",
            e
        )

    print("\n========== ALL DONE ==========\n")

if __name__ == "__main__":
    main()