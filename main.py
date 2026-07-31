import sys
import logging
from utils.logger import setup_logger
from data.watchlist import generate_dynamic_watchlist
from scanner.scanner import NSEBTSTScanner

def main():
    setup_logger()
    
    # 1. Dynamically Load Watchlist
    try:
        live_watchlist = generate_dynamic_watchlist()
        logging.info(f"Successfully compiled {len(live_watchlist)} index constituents.")
    except Exception as e:
        logging.error(f"Failed to update watchlist from NSE: {e}")
        logging.error("Exiting scanner safely to prevent processing with missing data.")
        sys.exit(1)

    # 2. Execute Scanner
    scanner = NSEBTSTScanner(tickers=live_watchlist)
    qualified_assets_df = scanner.run()

    # 3. Present Results
    print("\n" + "=" * 80)
    print("                      INSTITUTIONAL BTST TRADING RADAR          ")
    print("=" * 80)
    if not qualified_assets_df.empty:
        print(
            qualified_assets_df.sort_values(
                by="Daily_Range", ascending=False
            ).to_string(index=False)
        )
    else:
        print("No assets currently fulfill the comprehensive quantitative filters.")
    print("=" * 80 + "\n")

if __name__ == "__main__":
    main()