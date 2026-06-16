from datetime import datetime
from data.fred import (
    get_fred_series,
    get_cpi_yoy
)

def get_macro_data():

    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

        # FRED真实数据
        "us10y": get_fred_series("DGS10"),     # 10年美债
        "cpi": get_cpi_yoy(),
        "fed_rate": get_fred_series("FEDFUNDS") # 利率
    }