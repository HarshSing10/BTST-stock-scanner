import threading
from typing import List, Callable

def execute_multithreading(tickers: List[str], target_func: Callable[[str], None]) -> None:
    """Manages thread pool for concurrent data processing."""
    threads = []
    
    for ticker in tickers:
        t = threading.Thread(target=target_func, args=(ticker,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()