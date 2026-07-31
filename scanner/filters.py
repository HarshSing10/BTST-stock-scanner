import pandas as pd
from config import VOLUME_THRESHOLD

def evaluate_filters(
    df: pd.DataFrame, 
    df_weekly: pd.DataFrame, 
    df_monthly: pd.DataFrame, 
    latest: pd.Series, 
    prev_row: pd.Series, 
    current_range: float
) -> bool:
    """Comprehensive Filter Engine Logic. Evaluates all quantitative conditions."""
    
    close_price = float(latest["Close"])
    open_price = float(latest["Open"])
    prev_close = float(prev_row["Close"])
    prev_volume = float(prev_row["Volume"])

    sma20 = float(latest["SMA20"])
    sma50 = float(latest["SMA50"])
    sma200 = float(latest["SMA200"])
    
    # 1. Range Expansion: Today's range > max range of the past 7 days
    past_7_ranges_max = df["Daily_Range"].iloc[-8:-1].max()
    range_expansion = current_range > past_7_ranges_max

    # 2. Daily price action
    daily_green = close_price > open_price
    higher_close = close_price > prev_close

    # 3. Weekly & Monthly price action
    weekly_green = float(df_weekly['Close'].iloc[-1]) > float(df_weekly['Open'].iloc[-1])
    monthly_green = float(df_monthly['Close'].iloc[-1]) > float(df_monthly['Open'].iloc[-1])

    # 4. Volume Gate
    volume_check = prev_volume > VOLUME_THRESHOLD

    # 5. Trend Alignment
    trend_aligned = (sma20 > sma50) and (sma50 > sma200)

    # Execution Gate Check
    return (
        range_expansion
        and daily_green
        and higher_close
        and weekly_green
        and monthly_green
        and volume_check
        and trend_aligned
    )