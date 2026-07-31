import logging
from data.nse_fetcher import fetch_nse_index_symbols
from utils.constants import MIDCAP_URL, SMALLCAP_URL

def generate_dynamic_watchlist() -> list:
    """Combines the latest constituents of NIFTY Midcap 150 and NIFTY Smallcap 250."""
    logging.info("Downloading latest NIFTY Midcap 150 constituents from NSE...")
    midcap_symbols = fetch_nse_index_symbols(MIDCAP_URL)
    
    logging.info("Downloading latest NIFTY Smallcap 250 constituents from NSE...")
    smallcap_symbols = fetch_nse_index_symbols(SMALLCAP_URL)
    
    combined_symbols = list(set(midcap_symbols + smallcap_symbols))
    return combined_symbols