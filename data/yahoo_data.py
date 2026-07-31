import datetime
import yfinance as yf
import pandas as pd

def download_yahoo_data(ticker: str, lookback_days: int) -> pd.DataFrame:
    """Downloads historical market data using yfinance."""
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=lookback_days) 
    
    df = yf.download(ticker, start=start_date, end=end_date, progress=False)
    return df