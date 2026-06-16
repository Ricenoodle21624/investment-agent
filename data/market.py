from data.fred import get_fred_series
from data.fred import get_cpi_yoy

from data.ak_market import (
    get_gold,
    get_hstech,
    get_shanghai,
    get_chinext
)


def get_market_data():

    return {

        # ===== 宏观 =====

        "us10y":
            get_fred_series("DGS10"),

        "fed_rate":
            get_fred_series("FEDFUNDS"),

        "cpi":
            get_cpi_yoy(),

        # ===== 美股 =====

        "nasdaq":
            get_fred_series("NASDAQCOM"),

        "sp500":
            get_fred_series("SP500"),

        "vix":
            get_fred_series("VIXCLS"),

        # ===== 黄金 =====

        "gold":
            get_gold(),

        # ===== 港股 =====

        "hstech":
            get_hstech(),

        # ===== A股 =====

        "shanghai":
            get_shanghai(),

        "chinext":
            get_chinext()
    }