# Architecture Overview

This project utilizes a **clean, modular architecture** emphasizing the Separation of Concerns (SoC).

- **Data Layer (`data/`)**: Isolated environment for handling data retrieval APIs (YFinance, NSE).
- **Processing Layer (`scanner/`)**: Handles specific quantitative transformations.
  - `indicators.py`: Pure functions computing mathematical indicators.
  - `filters.py`: Isolated logic gates.
  - `processor.py`: Combines data and functions to output formatted dicts.
- **Orchestration Layer (`main.py`, `scanner.py`, `threading_manager.py`)**: Responsible for dispatching workloads concurrently across CPU threads.