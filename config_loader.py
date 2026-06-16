import yaml


def load_watchlist():

    with open(
        "config/watchlist.yaml",
        "r",
        encoding="utf-8"
    ) as f:

        return yaml.safe_load(f)