import logging
import threading
import pandas as pd
from typing import List, Dict
from config import LOOKBACK_DAYS_INIT
from scanner.processor import process_ticker
from scanner.threading_manager import execute_multithreading

class NSEBTSTScanner:
    """An institutional-grade technical scanner for NSE Midcap and Smallcap stocks."""

    def __init__(self, tickers: List[str], lookback_days: int = LOOKBACK_DAYS_INIT):
        self.tickers = [t if t.endswith(".NS") else f"{t}.NS" for t in tickers]
        self.lookback_days = lookback_days
        self.results: List[Dict] = []
        self._lock = threading.Lock()

    def _threaded_process(self, ticker: str) -> None:
        """Internal callback to capture processed ticker results securely."""
        result = process_ticker(ticker)
        if result:
            with self._lock:
                self.results.append(result)

    def run(self) -> pd.DataFrame:
        """Executes multi-threaded data fetching and processing."""
        logging.info(f"Initiating institutional scan across {len(self.tickers)} assets...")
        
        execute_multithreading(self.tickers, self._threaded_process)

        logging.info("Scan sequence complete. Parsing generated output...")
        return pd.DataFrame(self.results)