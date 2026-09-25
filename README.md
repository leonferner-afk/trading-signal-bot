# bot-state

Written by the bot, not by hand. Every daily run commits here:

- `reports/latest.md` — today's report (buys, sells, open positions, results)
- `reports/YYYY-MM-DD.md` — one report per trading day
- `tradingbot.db` — the journal: every signal, its real fill and outcome
- `evidence.json`, `research.md` — the latest weekly strategy research

The code lives on `main`.
