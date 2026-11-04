import pandas as pd

from app.data.stock_client import StockClient


def _bars(closes):
    idx = pd.DatetimeIndex(closes)
    return pd.DataFrame({"open": 1.0, "high": 1.0, "low": 1.0, "close": 1.0, "volume": 1.0,
                         "open_time": idx, "close_time": idx}, index=idx)


def test_unfinished_daily_bar_is_dropped_unless_partial_is_wanted():
    now = pd.Timestamp.now(tz="UTC")
    frame = _bars([now - pd.Timedelta(days=1), now + pd.Timedelta(hours=3)])   # yesterday, today's open session
    assert len(StockClient()._finished(frame, "1d")) == 1
    assert len(StockClient(include_partial=True)._finished(frame, "1d")) == 2
    assert len(StockClient()._finished(frame, "1h")) == 2                       # intraday bars are left alone
