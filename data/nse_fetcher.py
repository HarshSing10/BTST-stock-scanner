import io
import requests
import pandas as pd
from utils.constants import HEADERS

def fetch_nse_index_symbols(index_url: str) -> list:
    """Downloads and parses the official CSV of index constituents from NSE."""
    response = requests.get(index_url, headers=HEADERS, timeout=15)
    response.raise_for_status()

    df = pd.read_csv(io.StringIO(response.text))
    
    if "Symbol" not in df.columns:
        raise ValueError(f"Expected column 'Symbol' not found in downloaded data from {index_url}")
        
    return df["Symbol"].tolist()