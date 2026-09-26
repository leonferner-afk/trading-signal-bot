"""Probe: does free Yahoo data give historical earnings dates with EPS
estimate / reported EPS / surprise far enough back to test earnings-based
strategies? Prints coverage per symbol; never guesses."""
from __future__ import annotations

import time

import yfinance as yf

SYMBOLS = ["AAPL", "NVDA", "PLTR", "CROX", "ELF", "DECK", "SMCI", "UPST", "JPM", "KO", "CELH", "APP"]

for symbol in SYMBOLS:
    try:
        df = yf.Ticker(symbol).get_earnings_dates(limit=100)
        if df is None or df.empty:
            print(f"{symbol}: no data")
            continue
        reported = df.dropna(subset=[c for c in df.columns if "Reported" in c])
        cols = list(df.columns)
        print(f"{symbol}: {len(df)} rows, {len(reported)} with reported EPS, "
              f"{reported.index.min().date() if len(reported) else '-'} .. {reported.index.max().date() if len(reported) else '-'}, cols={cols}")
    except Exception as exc:  # report, never guess
        print(f"{symbol}: ERROR {type(exc).__name__}: {exc}")
    time.sleep(1)
