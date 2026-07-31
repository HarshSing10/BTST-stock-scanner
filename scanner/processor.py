import logging
import pandas as pd
from typing import Optional, Dict
from config import LOOKBACK_DAYS_FETCH
from utils.helpers import flatten_multiindex
from data.yahoo_data import download_yahoo_data
from scanner.indicators import add_smas
from scanner.filters import evaluate_filters

def process_ticker(ticker: str) -> Optional[Dict]:
    """Downloads data, prepares dataframes, computes indicators, and filters."""
    try:
        df = download_yahoo_data(ticker, LOOKBACK_DAYS_FETCH)
        if df.empty or len(df) < 200:
            return None

        df = flatten_multiindex(df)
        df = add_smas(df)
        df["Daily_Range"] = df["High"] - df["Low"]

        # Resample for Weekly and Monthly Candles
        df_weekly = df.resample('W').agg({'Open': 'first', 'Close': 'last'})
        df_monthly = df.resample('ME').agg({'Open': 'first', 'Close': 'last'})

        latest = df.iloc[-1]
        prev_row = df.iloc[-2]
        
        current_range = float(latest["Daily_Range"])
        
        passed_filters = evaluate_filters(
            df=df, 
            df_weekly=df_weekly, 
            df_monthly=df_monthly, 
            latest=latest, 
            prev_row=prev_row, 
            current_range=current_range
        )

        if passed_filters:
            return {
                "Ticker": ticker.replace(".NS", ""),
                "Close": round(float(latest["Close"]), 2),
                "SMA20": round(float(latest["SMA20"]), 2),
                "SMA50": round(float(latest["SMA50"]), 2),
                "SMA200": round(float(latest["SMA200"]), 2),
                "Daily_Range": round(current_range, 2),
                "Prev_Vol": int(float(prev_row["Volume"]))
            }
            
        return None

    except Exception as e:
        logging.error(f"Error executing processing loop for {ticker}: {e}")
        return None