# Sagoton — Trading Signal Platform

A signal-only quant platform that scans a market, scores candidate setups
on a transparent 0-100 scale, and tells you the entry/stop/target and the
*why* behind each one. **It never places an order.** It analyzes, ranks,
and notifies — a human decides.

Optimizing for "so few bad trades as possible," not "a signal every day."
When nothing clears the quality bar, the correct output is
`NO HIGH-CONVICTION SETUPS TODAY`, and the system says exactly that.

## Why crypto / Binance

The brief asks for one market first, chosen for stable real-time and
historical data, volume, candles, low latency, and reasonable cost. Binance's
public spot REST API (`/api/v3/klines`, `/ticker/24hr`, `/depth`) needs no
API key for market data, is free, and crypto trades 24/7 (no market-hours
edge cases). That made it the most realistic "start with one market" choice
without needing a provisioning step for a paid data vendor. The architecture
(`app/data/binance_client.py`) is isolated behind a small interface so a
second market/provider can be added later without touching the strategy,
scoring, or backtest layers.

## A known limitation of the environment this was built in

**This specific development sandbox blocks outbound access to every market
data host** (Binance, Yahoo Finance, CoinGecko, Alpha Vantage, Finnhub,
and others all return `403` at the network layer — verified before writing
any code). That means real live/historical prices could not be pulled
*while building this*, no matter which provider was chosen.

Rather than fabricate scan results, backtests, or win rates to look
finished, the code was built to be genuinely correct and was verified two
ways:
1. **Unit tests** (`backend/tests/`) against clearly-labeled *synthetic*
   fixtures (`tests/fixtures.py`) — they check the math (indicator
   formulas, scoring arithmetic, stop/target fills, cost application,
   walk-forward bucketing), never a claim about real market performance.
2. **A dev-only smoke server** (`backend/scripts/dev_smoke_server.py`)
   that monkeypatches the Binance client to prove the full pipeline
   (scan → score → journal → API → dashboard) wires together correctly.
   It is not part of the app and must never be used as a data source.

Run this anywhere with normal internet access (your machine, a VPS, a
container platform) and `app/data/binance_client.py` talks to the real
Binance API — nothing else needs to change.

## Architecture

```
MARKET SCAN → CANDIDATES → MULTI-FACTOR ANALYSIS → RISK/REWARD
            → QUALITY FILTER → RANKING → SIGNAL or NO TRADE
```

```
backend/app/
  data/            Binance REST client (real, no key needed) + optional
                    CryptoPanic news client (explicit "no data" if unset)
  features/        indicators.py (EMA/SMA/VWAP/RSI/MACD/ATR/ADX/Bollinger),
                    volume.py (relative volume, volume trend),
                    structure.py (swing points, S/R, breakout, trend structure)
  regime/          classifier.py — TRENDING_UP/DOWN, RANGE, HIGH/LOW
                    volatility, RISK_ON/OFF (from BTC as anchor), and a
                    documented per-strategy regime-fit table
  strategies/      breakout.py, momentum.py, reversal.py — each with its
                    own, independently-justified logic and its own raw
                    momentum/volume/structure component scores
  scoring/         score.py — combines strategy + regime + catalyst +
                    risk/reward into one transparent 0-100 breakdown
  risk/            risk_reward.py — ATR/structure-derived entry/stop/target,
                    flags (not hides) unrealistic targets
  scanner/         scanner.py — orchestrates the whole pipeline per symbol,
                    one signal per symbol per scan (no duplicate alerts)
  backtest/        engine.py (causal, cost-aware, event-driven simulator),
                    metrics.py (win rate/expectancy/profit factor/Sharpe/
                    drawdown), walk_forward.py (train/validation/OOS split
                    + rolling walk-forward consistency check)
  paper_trading/   simulator.py — checks OPEN journal signals against real,
                    finer-grained forward price data, logs the actual
                    outcome, fires "SÄLJ NU" the moment one resolves
  notify/          notifier.py (KÖP NU / SÄLJ NU formatting + delivery),
                    telegram_client.py (real Telegram Bot API client),
                    trading_hours.py (optional quiet-hours gate on entries)
  pipeline.py      Shared "what to do with a fresh scan result" logic
                    (dedupe → journal → notify) used by both the manual
                    scan endpoint and the scheduler
  scheduler.py     Background asyncio loops: entry scan every
                    SCAN_LOOP_MINUTES, exit monitor every
                    MONITOR_LOOP_MINUTES — opt-in via ENABLE_SCHEDULER
  journal/         repository.py — SQLite-backed trade journal (section 17
                    fields) + performance aggregation + open-signal dedupe
  db.py            SQLAlchemy models (signals, backtest_runs)
  main.py          FastAPI app wiring it all together + serving the
                    dashboard
frontend/          Static dark dashboard (index.html/app.js/styles.css) —
                    Scanner / Journal / Performance / Backtest tabs
```

## Notifications: "KÖP NU" → "SÄLJ NU"

This is a **long-only, spot accumulation workflow**: buy on a real signal,
sell into target/stop, repeat. Only `LONG` signals push a Telegram alert —
a `SHORT` candidate still shows up in the dashboard/journal (for stats and
completeness) but is never framed as "köp nu"/"sälj nu", since there's
nothing to sell on a position you were never long.

1. **Entry scan** (every `SCAN_LOOP_MINUTES`, default 30): the same
   pipeline as the manual *Run Scan* button. A qualifying LONG signal that
   isn't already an open position sends **"🟢 KÖP NU"** — entry/stop/
   target/R:R/why, plus (once you've run a backtest for that symbol+
   strategy) the real historical average holding time and the hours (UTC)
   that setup has most often triggered at, so you know roughly when to
   expect the follow-up. It is then journaled as `OPEN`.
2. **Exit monitor** (every `MONITOR_LOOP_MINUTES`, default 5, checked
   against `MONITOR_KLINE_INTERVAL`-granularity candles — finer than the
   entry strategy's own timeframe so a stop/target hit is caught
   promptly): the moment an open position's target or stop is hit (or it
   expires after 48h untouched), **"🔴 SÄLJ NU"** fires with the real
   outcome, MFE/MAE, and holding time.
3. **No duplicate alerts**: while a symbol+strategy+direction already has
   an `OPEN` journal entry, the scanner will not re-alert on the same
   setup every cycle — it's already being watched for its exit.
4. **Optional "quiet hours" gate** (`TRADING_HOURS_ENABLED=true`): only
   suppresses new *entry* alerts outside your configured window/timezone/
   days — the underlying signal is still journaled either way. Exit
   alerts are **never** gated; once you're in a position you want to know
   it closed regardless of the hour. Off by default since crypto trades
   24/7. Note: all three current strategies are intraday-to-swing
   (≤48h max holding) — there's no long-horizon strategy yet where the
   gate would be a non-issue by design rather than by choice.

Delivery is via **Telegram** (set `TELEGRAM_BOT_TOKEN` / `TELEGRAM_CHAT_ID`
— see `.env.example` for the 2-minute setup) plus console logging and an
optional generic webhook. Telegram's API host is also blocked by this
sandbox's network policy (verified the same way as the market-data hosts),
so delivery itself couldn't be tested live here — `notify_entry`/
`notify_exit` are covered by unit tests with the HTTP call stubbed out
(`tests/test_notifier.py`), and the dev smoke server proves the full
scan → dedupe → journal → notify → exit loop wires together correctly
end to end.

### Design choices that matter

- **No single indicator creates a signal.** Each strategy requires
  multiple independent, real confirmations (e.g. breakout needs the level
  break *and* ≥1.5x relative volume *and* MACD/ADX agreement).
- **Score is arithmetic, not vibes.** `momentum(0-25) + volume(0-20) +
  structure(0-20) + regime_fit(0-15) + catalyst(0-10) + risk_reward(0-10)
  = total`. The dashboard shows every component.
- **Missing news ≠ good news.** With no `CRYPTOPANIC_API_KEY` configured,
  catalyst scores 0/10 with an explicit reason — never assumed positive.
- **Backtests are causal.** The engine only ever gives a strategy
  `df.iloc[:i+1]` at bar *i*; fills happen at the *next* bar's open; every
  fill pays fee + slippage; an ambiguous bar (stop and target both in
  range) assumes the stop hit first.
- **Reliability is graded, not asserted.** A strategy that's profitable
  in-sample but not out-of-sample, or has too few OOS trades, is labeled
  `NOT_PROFITABLE_AFTER_COSTS` / `INSUFFICIENT_DATA` / unreliable — visibly,
  on the dashboard.
- **Paper trading uses real forward data**, not a simulated fill — a
  symbol whose fresh data can't be fetched stays `OPEN` and is reported as
  unavailable, never guessed at.

## Running it

```bash
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # edit if you want news/webhook/different watchlist
uvicorn app.main:app --reload --port 8000
```

Open `http://localhost:8000`. The dashboard talks to the API on the same
origin; static files are served by FastAPI directly (no separate build
step).

### Running the test suite

```bash
cd backend && source .venv/bin/activate
pytest tests/ -v
```

All tests run against synthetic, clearly-labeled fixtures and verify
calculation correctness — they are not a claim about live trading
performance (see "A known limitation" above).

### Using it day to day

- **Scanner tab** → *Run Scan*: pulls fresh candles for the watchlist,
  runs all three strategies per symbol, keeps the best-scoring one if it
  clears the WATCH threshold (70/100), and shows ranked signal cards or
  the `NO HIGH-CONVICTION SETUPS TODAY` banner. Every skipped symbol and
  every evaluated-but-rejected candidate is listed in the diagnostics
  panel — nothing is silently dropped.
- **Journal tab** → every signal that ever cleared the filter, with its
  full feature/score breakdown, persisted to SQLite.
- **Performance tab** → aggregated win rate / expectancy / profit factor /
  drawdown from *closed* signals only; shows an honest empty state until
  paper trading or backtests have produced closed outcomes.
- **Backtest tab** → pick a symbol/strategy/interval, run a real historical
  backtest with fees+slippage, see the train/validation/out-of-sample
  split and a walk-forward consistency check, with an explicit
  reliable/unreliable verdict and the reason for it.
- **Update Paper Trades** button → checks every OPEN journal signal
  against real subsequent price action and closes it with the actual
  outcome (target/stop/expired) plus MFE/MAE/holding time (fires "SÄLJ NU"
  for anything that resolved).
- With `ENABLE_SCHEDULER=true`, both of the above happen automatically in
  the background on the cadence you set — you don't need the dashboard
  open at all, just Telegram configured.

## What's intentionally minimal

Per the brief's own instruction to prefer "a smaller working quant engine
over an enormous system with fake functionality":

- One market (crypto/Binance), not five.
- Three strategies (breakout, momentum, reversal), not a dozen.
- Eight indicators, each with a stated reason to exist — not twenty for
  the sake of looking sophisticated.
- News/catalyst scoring is real but simple (CryptoPanic, optional); it is
  explicitly a small (10/100) part of the score so its absence can never
  look like a strong negative or be mistaken for a positive.
- Walk-forward analysis here evaluates whether these *fixed, rule-based*
  strategies' edge holds across sequential time windows — there is no
  parameter-fitting step to "train," since none of the strategies fit
  parameters to data.

## Absolute rules this system follows

No guaranteed profit claims, no fabricated predictions/confidence/
backtests/market data, no automatic trading, no forced daily trades. Every
number on the dashboard is either pulled from real market data or computed
directly from it — an empty state is always preferred over an invented one.
