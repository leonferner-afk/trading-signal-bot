"""SYNTHETIC test fixtures only.

Every series generated here is a made-up price path used exclusively to
verify that the calculation code is mathematically correct (e.g. "does our
ATR implementation match a hand-computed value", "does the backtest engine
correctly detect a stop-loss hit given a price path built to hit it").

None of this data is real market data, and nothing derived from it (win
rates, scores, etc.) may ever be reported to a user as an actual result —
that would violate the project's own no-hallucination rule. It exists only
under `tests/`.
"""
from __future__ import annotations

import numpy as np
import pandas as pd


def make_synthetic_ohlcv(
    n: int = 300,
    start_price: float = 100.0,
    trend_per_bar: float = 0.0,
    volatility: float = 0.5,
    seed: int = 42,
    freq: str = "1h",
) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    closes = [start_price]
    for _ in range(n - 1):
        step = trend_per_bar + rng.normal(0, volatility)
        closes.append(max(0.01, closes[-1] + step))
    closes = np.array(closes)

    opens = np.roll(closes, 1)
    opens[0] = start_price
    highs = np.maximum(opens, closes) + rng.uniform(0, volatility, n)
    lows = np.minimum(opens, closes) - rng.uniform(0, volatility, n)
    lows = np.clip(lows, 0.01, None)
    volumes = rng.uniform(1000, 2000, n)

    close_time = pd.date_range("2024-01-01", periods=n, freq=freq, tz="UTC")
    open_time = close_time - pd.Timedelta(freq)

    df = pd.DataFrame(
        {
            "open_time": open_time,
            "open": opens,
            "high": highs,
            "low": lows,
            "close": closes,
            "volume": volumes,
            "close_time": close_time,
            "quote_asset_volume": volumes * closes,
            "num_trades": rng.integers(100, 500, n),
            "taker_buy_base_volume": volumes * 0.5,
            "taker_buy_quote_volume": volumes * closes * 0.5,
        }
    )
    return df.set_index("close_time", drop=False)
