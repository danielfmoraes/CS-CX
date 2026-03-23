# utils/market_api.py
from pytrends.request import TrendReq
import pandas as pd
import time

def get_market_trends():
    pytrends = TrendReq()
    keywords = ["seguro fiança", "aluguel imobiliária", "garantia aluguel"]
    
    try:
        pytrends.build_payload(keywords, timeframe='today 3-m')
        data = pytrends.interest_over_time()
        if not data.empty:
            return data.reset_index()
        else:
            raise ValueError("No data from Google Trends")
    except:
        # Fallback mock
        return pd.DataFrame({
            "date": ["2026-01", "2026-02", "2026-03", "2026-04", "2026-05"],
            "seguro fiança": [100, 120, 140, 130, 150],
            "garantia aluguel": [80, 90, 110, 105, 120]
        })