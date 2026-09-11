"""DEV-ONLY smoke server.

Monkeypatches BinanceClient.get_klines with an engineered synthetic
breakout scenario so the full stack (API, DB, dashboard) can be exercised
end-to-end while this sandbox's egress policy blocks real market-data
hosts. This script is never used in production and must never be pointed
at by the real app — it exists purely to prove the wiring works.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from tests.fixtures import make_synthetic_ohlcv
import app.data.binance_client as bc


def fake_get_klines(self, symbol, interval, limit=500):
    seed = abs(hash(symbol)) % 1000
    df = make_synthetic_ohlcv(n=max(limit, 300), start_price=100, trend_per_bar=0.0, volatility=0.3, seed=seed)
    close_col = df.columns.get_loc("close")
    high_col = df.columns.get_loc("high")
    low_col = df.columns.get_loc("low")
    open_col = df.columns.get_loc("open")
    vol_col = df.columns.get_loc("volume")
    for i in range(len(df) - 25, len(df) - 1):
        df.iloc[i, close_col] = 100 + np.sin(i) * 0.3
        df.iloc[i, open_col] = 100 + np.sin(i - 1) * 0.3
        df.iloc[i, high_col] = 100.6
        df.iloc[i, low_col] = 99.4
        df.iloc[i, vol_col] = 1000
    if symbol in ("BTCUSDT", "ETHUSDT"):
        df.iloc[-1, open_col] = 100.5
        df.iloc[-1, close_col] = 106.0
        df.iloc[-1, high_col] = 106.5
        df.iloc[-1, low_col] = 100.3
        df.iloc[-1, vol_col] = 4000
    now = pd.Timestamp.now(tz="UTC")
    shift = now - df["close_time"].iloc[-1]
    df["close_time"] = df["close_time"] + shift
    df["open_time"] = df["open_time"] + shift
    return df.set_index("close_time", drop=False)


bc.BinanceClient.get_klines = fake_get_klines

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="127.0.0.1", port=8020, log_level="warning")
