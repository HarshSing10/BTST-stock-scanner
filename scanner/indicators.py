import numpy as np
import pandas as pd

def calculate_rsi(series: pd.Series, period: int = 14) -> pd.Series:
    """Calculates Relative Strength Index using Wilder's EMA smoothing technique."""
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).copy()
    loss = (-delta.where(delta < 0, 0)).copy()

    avg_gain = gain.rolling(window=period, min_periods=period).mean()
    avg_loss = loss.rolling(window=period, min_periods=period).mean()

    for i in range(period, len(series)):
        avg_gain.iloc[i] = (avg_gain.iloc[i - 1] * (period - 1) + gain.iloc[i]) / period
        avg_loss.iloc[i] = (avg_loss.iloc[i - 1] * (period - 1) + loss.iloc[i]) / period

    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

def calculate_adx(df: pd.DataFrame, period: int = 14) -> tuple[pd.Series, pd.Series, pd.Series]:
    """Calculates Average Directional Index (ADX), +DI, and -DI."""
    high = df["High"]
    low = df["Low"]
    close = df["Close"]

    tr1 = high - low
    tr2 = (high - close.shift(1)).abs()
    tr3 = (low - close.shift(1)).abs()
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)

    up_move = high.diff()
    down_move = low.shift(1) - low

    plus_dm = np.where((up_move > down_move) & (up_move > 0), up_move, 0.0)
    minus_dm = np.where((down_move > up_move) & (down_move > 0), down_move, 0.0)

    atr = tr.rolling(window=period).mean()
    smoothed_plus_dm = pd.Series(plus_dm).rolling(window=period).mean()
    smoothed_minus_dm = pd.Series(minus_dm).rolling(window=period).mean()

    for i in range(period, len(df)):
        atr.iloc[i] = (atr.iloc[i - 1] * (period - 1) + tr.iloc[i]) / period
        smoothed_plus_dm.iloc[i] = (smoothed_plus_dm.iloc[i - 1] * (period - 1) + plus_dm[i]) / period
        smoothed_minus_dm.iloc[i] = (smoothed_minus_dm.iloc[i - 1] * (period - 1) + minus_dm[i]) / period

    plus_di = 100 * (smoothed_plus_dm / atr)
    minus_di = 100 * (smoothed_minus_dm / atr)

    dx = 100 * (plus_di - minus_di).abs() / (plus_di + minus_di)
    adx = dx.rolling(window=period).mean()

    for i in range(period * 2, len(df)):
        adx.iloc[i] = (adx.iloc[i - 1] * (period - 1) + dx.iloc[i]) / period

    return adx, pd.Series(plus_di, index=df.index), pd.Series(minus_di, index=df.index)

def add_smas(df: pd.DataFrame) -> pd.DataFrame:
    """Applies Simple Moving Averages."""
    df["SMA20"] = df["Close"].rolling(window=20).mean()
    df["SMA50"] = df["Close"].rolling(window=50).mean()
    df["SMA200"] = df["Close"].rolling(window=200).mean()
    return df