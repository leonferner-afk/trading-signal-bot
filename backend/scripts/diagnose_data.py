"""Probe every market-data source from wherever this runs (e.g. a GitHub
Actions runner) and print a plain pass/fail table. Diagnostic only — it
never feeds the scanner."""
from __future__ import annotations

import datetime as dt
import io
import os
import time
import traceback

import httpx
import pandas as pd

SAMPLE = ["NVDA", "AAPL", "TSLA", "SPY", "PLTR", "AMD", "COIN", "MSTR", "SMCI", "HOOD"]


def _row(name: str, ok: bool, detail: str) -> None:
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}", flush=True)


def probe_yfinance_single() -> None:
    import yfinance as yf

    t0 = time.monotonic()
    try:
        df = yf.Ticker("NVDA").history(period="5y", interval="1d", auto_adjust=True)
        ok = df is not None and not df.empty
        detail = f"{len(df)} rows, last={df.index[-1].date() if ok else None}" if ok else "empty"
        _row("yfinance Ticker.history NVDA 5y", ok, f"{detail} ({time.monotonic() - t0:.1f}s)")
    except Exception as exc:
        _row("yfinance Ticker.history NVDA 5y", False, f"{type(exc).__name__}: {exc}")


def probe_yfinance_batch() -> None:
    import yfinance as yf

    t0 = time.monotonic()
    try:
        df = yf.download(SAMPLE, period="2y", interval="1d", group_by="ticker", auto_adjust=True, threads=True, progress=False)
        got = [s for s in SAMPLE if s in df.columns.get_level_values(0) and not df[s]["Close"].dropna().empty]
        _row("yfinance download batch x10 2y", len(got) == len(SAMPLE), f"{len(got)}/{len(SAMPLE)} symbols with data ({time.monotonic() - t0:.1f}s)")
    except Exception as exc:
        _row("yfinance download batch x10 2y", False, f"{type(exc).__name__}: {exc}")


def probe_stooq() -> None:
    end = dt.date.today()
    params = {"s": "nvda.us", "d1": (end - dt.timedelta(days=800)).strftime("%Y%m%d"), "d2": end.strftime("%Y%m%d"), "i": "d"}
    try:
        r = httpx.get("https://stooq.com/q/d/l/", params=params, timeout=20, follow_redirects=True,
                      headers={"User-Agent": "Mozilla/5.0"})
        text = r.text.strip()
        ok = r.status_code == 200 and text.startswith("Date")
        rows = len(pd.read_csv(io.StringIO(text))) if ok else 0
        _row("stooq CSV NVDA", ok, f"HTTP {r.status_code}, {rows} rows, head={text[:80]!r}")
    except Exception as exc:
        _row("stooq CSV NVDA", False, f"{type(exc).__name__}: {exc}")


def probe_twelvedata() -> None:
    key = os.environ.get("TWELVE_DATA_API_KEY", "")
    if not key:
        _row("twelvedata NVDA", False, "skipped — TWELVE_DATA_API_KEY secret not set")
        return
    try:
        r = httpx.get("https://api.twelvedata.com/time_series",
                      params={"symbol": "NVDA", "interval": "1day", "outputsize": 500, "apikey": key}, timeout=20)
        payload = r.json()
        values = payload.get("values") or []
        _row("twelvedata NVDA", bool(values), f"HTTP {r.status_code}, {len(values)} rows, status={payload.get('status')}, msg={payload.get('message', '')[:120]}")
    except Exception as exc:
        _row("twelvedata NVDA", False, f"{type(exc).__name__}: {exc}")


def probe_app_client() -> None:
    try:
        from app.data.stock_client import StockClient

        with StockClient() as c:
            df = c.get_klines("NVDA", "1d", limit=1000)
        _row("app StockClient.get_klines NVDA 1d", not df.empty, f"{len(df)} rows, last={df['close_time'].iloc[-1]}")
    except Exception:
        _row("app StockClient.get_klines NVDA 1d", False, traceback.format_exc(limit=2).replace("\n", " | "))


if __name__ == "__main__":
    import yfinance

    print(f"python-side yfinance {yfinance.__version__}, now={dt.datetime.now(dt.timezone.utc).isoformat()}")
    probe_yfinance_single()
    probe_yfinance_batch()
    probe_stooq()
    probe_twelvedata()
    probe_app_client()
