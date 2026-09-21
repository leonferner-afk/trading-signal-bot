# Trading Signal Bot

A signal-only stock-opportunity caller that scans a watchlist, scores
candidate setups on a transparent 0-100 scale, and tells you the
entry/stop/target and the *why* behind each one. **It never places an
order.** It analyzes, ranks, and notifies — a human decides.

**This is a swing/position-trade caller, not a day-trading bot.** It runs
on daily bars and hunts for a handful of large, weeks-to-months moves —
including, occasionally, the rare setup that could double — rather than
many small intraday trades. Optimizing for "so few bad calls as possible,"
not "a signal every day": when nothing clears the quality bar, the correct
output is `NO HIGH-CONVICTION SETUPS TODAY`, and the system says exactly
that.

**Be clear-eyed about what "could go up 100% in a month" means**: those
are, by definition, the most volatile, least certain setups in the
watchlist. This system finds and scores them honestly (see "Aggressive
move" below) — it does not, and cannot, promise that outcome. A big
target on the dashboard is a *possibility being measured*, not a
prediction.

## Why US stocks / Yahoo Finance

Chosen for two reasons: (1) US equities have the deepest bench of liquid,
high-beta growth/momentum names — the category most likely to produce the
large, month-scale moves this system hunts for — and (2) `yfinance`
(wrapping Yahoo Finance's public chart data) is the only genuinely
zero-cost option that covers thousands of US tickers. Alpha Vantage's free
tier allows 25 requests/day (unusable for scanning a watchlist); Finnhub's
free tier no longer includes stock candles. `yfinance` is unofficial —
there's no published SLA — so the client (`app/data/stock_client.py`)
leans harder on retries and an explicit `DataUnavailable` escape hatch
than an official API would need. It also impersonates a real browser's
TLS handshake (`curl_cffi`), since Yahoo has been tightening anti-bot
defenses that otherwise return empty responses to plain HTTP clients on
shared cloud-host IPs. For daily bars specifically, if Yahoo still fails
after retries the client falls back to Stooq's free CSV export — a
different, key-free provider, so a Yahoo-side block or outage doesn't
take the whole app down with it.

**Honest tradeoff of the $0 data budget**: this scans a *watchlist*
(`app/config.py` / the Settings tab), not the whole market. A real
full-market screener (scanning thousands of tickers for breakout
patterns) needs either a paid bulk-data/screener API or non-trivial
scraping — neither fits a zero-budget build. The default watchlist is a
starting set of liquid, historically volatile growth/momentum names
(edit it any time in Settings) — not a "best picks" endorsement, and not
exhaustive. See the Roadmap for the upgrade path if that budget changes.

## A known limitation of the environment this was built in

**This specific development sandbox blocks outbound access to every market
data host** (Yahoo Finance, Binance, CoinGecko, Alpha Vantage, Finnhub,
and others all return `403` at the network layer — verified before
writing any code). That means real live/historical prices could not be
pulled *while building this*, no matter which provider was chosen.

Rather than fabricate scan results, backtests, or win rates to look
finished, the code was built to be genuinely correct and was verified two
ways:
1. **Unit tests** (`backend/tests/`) against clearly-labeled *synthetic*
   fixtures (`tests/fixtures.py`) — they check the math (indicator
   formulas, scoring arithmetic, stop/target fills, cost application,
   walk-forward bucketing), never a claim about real market performance.
2. **A dev-only smoke server** (`backend/scripts/dev_smoke_server.py`)
   that monkeypatches the stock client to prove the full pipeline
   (scan → score → journal → API → dashboard) wires together correctly.
   It is not part of the app and must never be used as a data source.

Run this anywhere with normal internet access (GitHub Codespaces, your own
machine, a VPS) and `app/data/stock_client.py` talks to the real Yahoo
Finance API — nothing else needs to change.

## Architecture

```
MARKET SCAN → CANDIDATES → MULTI-FACTOR ANALYSIS → RISK/REWARD
            → QUALITY FILTER → RANKING → SIGNAL or NO TRADE
```

```
backend/app/
  data/            stock_client.py (Yahoo Finance via yfinance, real,
                    no key needed) + earnings_calendar.py (next scheduled
                    earnings date, additive-only warning) +
                    news_client.py (provider-agnostic catalyst scoring
                    types — no source wired up yet, see below)
  features/        indicators.py (EMA/SMA/VWAP/RSI/MACD/ATR/ADX/Bollinger),
                    volume.py (relative volume, volume trend),
                    structure.py (swing points, S/R, breakout, trend structure)
  regime/          classifier.py — TRENDING_UP/DOWN, RANGE, HIGH/LOW
                    volatility, RISK_ON/OFF (from SPY as anchor), and a
                    documented per-strategy regime-fit table
  strategies/      breakout.py, momentum.py, reversal.py — each with its
                    own, independently-justified logic and its own raw
                    momentum/volume/structure component scores
  scoring/         score.py — combines strategy + regime + catalyst +
                    risk/reward into one transparent 0-100 breakdown
  risk/            risk_reward.py (ATR/structure-derived entry/stop/
                    target, flags — not hides — extreme targets) +
                    position_sizing.py (fixed-fractional position size
                    from portfolio size / risk %)
  scanner/         scanner.py — orchestrates the whole pipeline per symbol,
                    one signal per symbol per scan (no duplicate alerts)
  backtest/        engine.py (causal, cost-aware, event-driven simulator),
                    metrics.py (win rate/expectancy/profit factor/Sharpe/
                    drawdown), walk_forward.py (train/validation/OOS split
                    + rolling walk-forward consistency check)
  paper_trading/   simulator.py — checks OPEN journal signals against real
                    forward price data, logs the actual outcome, fires
                    "SÄLJ NU" the moment one resolves
  notify/          notifier.py (KÖP NU / SÄLJ NU formatting + delivery),
                    telegram_client.py (real Telegram Bot API client),
                    trading_hours.py (optional quiet-hours gate on entries)
  runtime_settings.py  DB-backed overrides layered on top of .env defaults
                    (Telegram creds, watchlist, thresholds, scheduler
                    cadence, quiet hours, position sizing) — read by every
                    consumer above instead of the raw env settings, so the
                    dashboard Settings tab can change any of it live
  pipeline.py      Shared "what to do with a fresh scan result" logic
                    (dedupe → journal → notify) used by both the manual
                    scan endpoint and the scheduler
  scheduler.py     Background asyncio loops: entry scan + exit monitor.
                    Always running; each cycle re-reads runtime_settings
                    to decide whether to actually do anything, so
                    enabling/disabling or re-timing from the Settings tab
                    takes effect within ~60s, no restart needed
  journal/         repository.py — SQLite-backed trade journal (section 17
                    fields) + performance aggregation + open-signal dedupe
                    + chronological equity curve
  db.py            SQLAlchemy models (signals, backtest_runs, app_settings)
  main.py          FastAPI app wiring it all together + serving the
                    dashboard
frontend/          Static dark dashboard (index.html/app.js/styles.css) —
                    Scanner / Journal / Performance / Backtest / Settings
```

## Notifications: "KÖP NU" → "SÄLJ NU"

This is a **long-only, buy-and-hold-to-target workflow**: buy on a real
signal, sell into target/stop, repeat. Only `LONG` signals push a Telegram
alert — a `SHORT` candidate still shows up in the dashboard/journal (for
stats and completeness) but is never framed as "köp nu"/"sälj nu", since
there's nothing to sell on a position you were never long (this assumes
ordinary cash/spot buying — margin/short-selling is a different, riskier
mechanic this system doesn't target).

1. **Entry scan** (every `SCAN_LOOP_MINUTES`, default 60 — a daily bar
   doesn't change until the next trading day closes, so hourly is already
   more than enough): the same pipeline as the manual *Run Scan* button. A
   qualifying LONG signal that isn't already an open position sends
   **"🟢 KÖP NU"** — entry/stop/target/R:R/suggested position size/why,
   plus (once you've run a backtest for that symbol+strategy) the real
   historical average holding time and which hours similar setups have
   triggered at. It is then journaled as `OPEN`.
2. **Exit monitor** (every `MONITOR_LOOP_MINUTES`, default 60, checked
   against daily candles by default): the moment an open position's
   target or stop is hit — or it expires after 90 days untouched (this
   system's horizon is weeks-to-months, so that's real runway, not a
   token limit) — **"🔴 SÄLJ NU"** fires with the real outcome, MFE/MAE,
   and holding time.
3. **No duplicate alerts**: while a symbol+strategy+direction already has
   an `OPEN` journal entry, the scanner will not re-alert on the same
   setup every cycle — it's already being watched for its exit.
4. **Optional "quiet hours" gate** (`TRADING_HOURS_ENABLED=true`): only
   suppresses new *entry* alerts outside your configured window/timezone/
   days — the underlying signal is still journaled either way. Exit
   alerts are **never** gated.

Delivery is via **Telegram** — set `TELEGRAM_BOT_TOKEN` / `TELEGRAM_CHAT_ID`
either in `.env` or, easier, paste them into the **Settings tab** (takes
effect immediately) — plus console logging and an optional generic
webhook. Yahoo Finance and Telegram's API host are both blocked by this
sandbox's network policy (verified the same way), so delivery itself
couldn't be tested live here — `notify_entry`/`notify_exit` are covered by
unit tests with the HTTP call stubbed out (`tests/test_notifier.py`), and
the dev smoke server proves the full scan → dedupe → journal → notify →
exit loop wires together correctly end to end.

Every "KÖP NU" also includes a **suggested position size** (fixed-
fractional risk model: portfolio size × risk-per-trade % ÷ stop distance,
capped at 100% of portfolio) — configurable in Settings, advisory only,
never executes anything.

### Settings tab — change config live, no redeploy

Telegram credentials, watchlist, score thresholds, scheduler on/off and
cadence, quiet hours, and position sizing are all editable from the
dashboard's **Settings** tab. Under the hood this writes to a single-row
`app_settings` DB table (`app/runtime_settings.py`) that overrides the
`.env` default for just that field — `.env` remains the fallback for
anything you haven't explicitly changed in the UI. The scheduler polls its
own enabled-state every ~60s, so flipping it on/off in Settings takes
effect without restarting the process.

### Design choices that matter

- **No single indicator creates a signal.** Each strategy requires
  multiple independent, real confirmations (e.g. breakout needs the level
  break *and* ≥1.5x relative volume *and* MACD/ADX agreement).
- **Score is arithmetic, not vibes.** `momentum(0-25) + volume(0-20) +
  structure(0-20) + regime_fit(0-15) + catalyst(0-10) + risk_reward(0-10)
  = total`. The dashboard shows every component.
- **Missing news ≠ good news.** No stock news/catalyst provider is wired
  up yet (see "What's intentionally minimal" below) — catalyst always
  scores 0/10 with an explicit reason, never assumed positive.
- **Earnings-date risk is surfaced, never asserted absent.** If a
  qualifying LONG signal's ~1-month holding window would span a scheduled
  earnings report (`app/data/earnings_calendar.py`), a warning is added —
  real gap risk a swing position can't out-ATR. A missing warning means
  "no near-term date found or the lookup failed," never "confirmed clear
  of earnings" — it's additive-only by design.
- **"Aggressive move" targets are flagged, never hidden or capped away.**
  Targets scale with the stock's *own* ATR (up to 10x its daily range —
  deliberately wide, since this system is meant to size a real "could
  double" target when a stock's own volatility supports it). A target
  implying more than an 80% move gets an explicit warning rather than
  being silently trusted or silently suppressed — that threshold is set
  high on purpose so it only fires for the most extreme, penny-stock-grade
  cases, not ordinary big-mover targets.
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
cp .env.example .env   # edit if you want a different watchlist/webhook/etc.
uvicorn app.main:app --reload --port 8000
```

Open `http://localhost:8000`. The dashboard talks to the API on the same
origin; static files are served by FastAPI directly (no separate build
step). This needs real network access to Yahoo Finance to do anything
useful — GitHub Codespaces or your own machine, not this dev sandbox.

### Deploying it 24/7 (Railway)

Codespaces is a dev session — it pauses itself and isn't meant to run
unattended. For the scheduler/Telegram alerts to run around the clock you
need a real always-on host. This repo is pre-configured
(`backend/railway.json`) for [Railway](https://railway.app), which has a
usable free tier and needs no server administration:

1. Go to **railway.app** → sign in with GitHub.
2. **New Project** → **Deploy from GitHub repo** → pick
   `leonferner-afk/trading-signal-bot`.
3. Once created, open the service → **Settings** → set **Root Directory**
   to `backend` (the app code lives there, not the repo root).
4. Still in Settings → **Networking** → **Generate Domain** — this gives
   you the public URL for the dashboard.
5. Optional but recommended — **Variables** tab: add `TELEGRAM_BOT_TOKEN`,
   `TELEGRAM_CHAT_ID`, `ENABLE_SCHEDULER=true`. (You can skip this and set
   the same things later from the dashboard's own Settings tab instead —
   either works, env vars just mean it's configured from the very first
   boot.)
6. Railway redeploys automatically; open the generated URL once the
   deploy finishes.

**Persistence caveat**: without a Railway Volume, the container's
filesystem (including the SQLite journal/settings DB) is wiped on every
redeploy. Fine for just trying it out; if you want your journal and
Settings-tab changes to survive redeploys, add a Volume (service →
**Volumes** → mount at e.g. `/data`) and set the env var
`DB_PATH=/data/tradingbot.db`.

### Running the test suite

```bash
cd backend && source .venv/bin/activate
pytest tests/ -v
```

All tests run against synthetic, clearly-labeled fixtures and verify
calculation correctness — they are not a claim about live trading
performance (see "A known limitation" above).

### Using it day to day

- **Scanner tab** → *Run Scan*: pulls fresh daily candles for the
  watchlist, runs all three strategies per symbol, keeps the best-scoring
  one if it clears the WATCH threshold (70/100), and shows ranked signal
  cards or the `NO HIGH-CONVICTION SETUPS TODAY` banner. Every skipped
  symbol and every evaluated-but-rejected candidate is listed in the
  diagnostics panel — nothing is silently dropped.
- **Journal tab** → every signal that ever cleared the filter, with its
  full feature/score breakdown, persisted to SQLite.
- **Performance tab** → aggregated win rate / expectancy / profit factor /
  drawdown from *closed* signals only, plus a chronological **equity
  curve** (cumulative per-trade % return over time, hover a point for the
  trade behind it) so you can see whether the edge is holding, not just
  trust an aggregate number. Honest empty state until paper trading or
  backtests have produced closed outcomes.
- **Backtest tab** → pick a symbol/strategy/interval, run a real historical
  backtest with fees+slippage, see the train/validation/out-of-sample
  split and a walk-forward consistency check, with an explicit
  reliable/unreliable verdict and the reason for it. **Do this before
  trusting any signal with real money** — it's the only way to know
  whether a strategy has actually shown edge on real data.
- **Settings tab** → Telegram, watchlist, thresholds, scheduler, quiet
  hours, position sizing — all live, no restart.
- **Update Paper Trades** button → checks every OPEN journal signal
  against real subsequent price action and closes it with the actual
  outcome (target/stop/expired) plus MFE/MAE/holding time (fires "SÄLJ NU"
  for anything that resolved).
- With the scheduler enabled (Settings tab or `ENABLE_SCHEDULER=true`),
  both of the above happen automatically in the background on the cadence
  you set — you don't need the dashboard open at all, just Telegram
  configured.

## What's intentionally minimal

Per the principle of preferring "a smaller working quant engine over an
enormous system with fake functionality":

- A curated watchlist, not a full-market screener (see the $0-budget
  tradeoff above).
- Three strategies (breakout, momentum, reversal), not a dozen.
- Eight indicators, each with a stated reason to exist — not twenty for
  the sake of looking sophisticated.
- **No stock news/catalyst source is wired up yet.** `app/data/news_client.py`
  keeps the scoring logic (`catalyst_score`) and types provider-agnostic;
  wiring up a real source (e.g. Finnhub's free-tier company-news endpoint)
  is a matter of adding one fetch function and calling it from the
  scanner — not a rewrite. Until then catalyst honestly scores 0/10.
- Walk-forward analysis here evaluates whether these *fixed, rule-based*
  strategies' edge holds across sequential time windows — there is no
  parameter-fitting step to "train," since none of the strategies fit
  parameters to data.

## Roadmap — what's next

1. **Run real backtests** (blocked in this dev sandbox — needs Codespaces
   or a machine with normal network access) across the watchlist and all
   three strategies. This is the priority: everything else is secondary
   until we know which strategy/symbol combos actually have out-of-sample
   edge after costs. Expect some to come back `NOT_PROFITABLE_AFTER_COSTS`
   — that's the system working, not failing.
2. **Paper-trade the survivors** for a few weeks-to-months (matching this
   system's own holding horizon) before trusting a signal with real
   money — the only way to get an honest "similar setups hit target X% of
   the time" number for a live-running instance, not just backtested
   history.
3. Retire or re-tune anything that doesn't hold up out-of-sample, rather
   than adding more strategies on top of unproven ones.
4. **A real stock news/catalyst source** (Finnhub's free-tier company-news
   endpoint — 2-minute signup, no cost) is the next-cheapest upgrade:
   catalyst currently always scores 0/10, and news/earnings surprises are
   often the actual trigger behind the large moves this system hunts for.
   `app/data/news_client.py`'s scoring logic is already provider-agnostic,
   so this is a matter of adding one fetch function, not a rewrite.
5. If budget changes: a paid screener API (Polygon.io, Twelve Data) to
   scan the full market instead of a curated watchlist — meaningfully
   widens the net for rare, large-move setups beyond the current ~50-name
   list.

## Absolute rules this system follows

No guaranteed profit claims, no fabricated predictions/confidence/
backtests/market data, no automatic trading, no forced daily trades. Every
number on the dashboard is either pulled from real market data or computed
directly from it — an empty state is always preferred over an invented
one. A "could double" target is a measured possibility grounded in that
stock's own volatility, never a promise.
