# Strategy research

278 symbols with data (1 failed), 10 years of daily bars. Control group: 105 stocks that were already large caps in 2015. Primary cost 20 bps per side (USD account: courtage + slippage; 40 bps ≈ trading from a SEK account). Validation from 2023-01-28, out-of-sample (OOS) from 2024-11-29. Setups invalidated at the next open (skipped): 1315.

Portfolio: max 8 positions, max 3 new per day, 1% risk per trade, max 25% of equity per position, no leverage, marked to market daily. 'vs random' = share of 40 random-order portfolios from the same eligible trades that this ranking beat.

## Portfolio — universe: all

SPY buy-and-hold: +15.0%/yr, max DD -34%, Sharpe 0.84 · train+val Sharpe 0.82 · OOS +15.8%/yr, Sharpe 0.95

| rule set | trades/yr | exposure | win% | avgR | CAGR | max DD | Sharpe | train+val Sharpe | OOS CAGR | OOS Sharpe | vs random |
|---|---|---|---|---|---|---|---|---|---|---|---|
| random picks (reference) | 77.6 | 86% | 21 | +0.23 | +8.6% | -62% | 0.42 | 0.62 | -15.3% | -0.35 | — |
| random picks, trend filter | 65.5 | 78% | 22 | +0.39 | +16.2% | -39% | 0.71 | 0.87 | +4.8% | 0.28 | — |
| RS leaders, trend filter | 73.8 | 66% | 23 | +0.38 | +20.7% | -42% | 0.75 | 0.84 | +6.1% | 0.34 | 97% |
| RS leaders near 52w high | 66.0 | 76% | 26 | +0.70 | +35.2% | -34% | 1.14 | 1.22 | +24.1% | 0.74 | 100% |
| signals score>=70, trend | 46.6 | 63% | 21 | +0.29 | +10.1% | -35% | 0.56 | 0.69 | +4.3% | 0.30 | 30% |
| signals score>=70, trend, RS top 20% | 41.4 | 51% | 23 | +0.55 | +20.0% | -33% | 0.93 | 1.07 | +13.1% | 0.64 | 80% |
| signals, trend, RS top 20% | 77.4 | 78% | 22 | +0.74 | +37.8% | -48% | 1.11 | 1.18 | +43.8% | 1.03 | 100% |
| signals, trend, RS top 20%, near 52w high | 75.1 | 79% | 22 | +0.53 | +28.9% | -32% | 1.01 | 1.12 | +31.5% | 0.86 | 97% |

Cost sensitivity (full-period CAGR / Sharpe):

| rule set | 20 bps | 40 bps | 70 bps |
|---|---|---|---|
| RS leaders, trend filter | +20.7% / 0.75 | +17.0% / 0.66 | +11.8% / 0.52 |
| RS leaders near 52w high | +35.2% / 1.14 | +30.6% / 1.03 | +24.0% / 0.87 |
| signals score>=70, trend | +10.1% / 0.56 | +7.2% / 0.44 | +3.3% / 0.26 |
| signals score>=70, trend, RS top 20% | +20.0% / 0.93 | +17.4% / 0.83 | +13.7% / 0.68 |
| signals, trend, RS top 20% | +37.8% / 1.11 | +32.4% / 0.99 | +25.2% / 0.83 |
| signals, trend, RS top 20%, near 52w high | +28.9% / 1.01 | +23.6% / 0.87 | +16.6% / 0.67 |

Exit variant (stop 2.5 x ATR instead of 1.5 x ATR / structural):

| rule set | CAGR | max DD | Sharpe | OOS Sharpe |
|---|---|---|---|---|
| random picks (reference) | +3.4% | -43% | 0.27 | -0.71 |
| random picks, trend filter | +14.2% | -30% | 0.80 | -0.10 |
| RS leaders, trend filter | +20.0% | -28% | 0.95 | 1.02 |
| RS leaders near 52w high | +29.2% | -24% | 1.25 | 0.43 |
| signals score>=70, trend | +11.5% | -29% | 0.72 | 0.01 |
| signals score>=70, trend, RS top 20% | +17.5% | -28% | 1.02 | 0.58 |
| signals, trend, RS top 20% | +17.7% | -36% | 0.85 | 0.50 |
| signals, trend, RS top 20%, near 52w high | +15.4% | -24% | 0.77 | 0.40 |

### Per trade — universe: all (one position per symbol, t over monthly means)

| group | exit | policy | n | win% | avgR | medR | t | excess vs random (t) | ≥+50% | OOS n | OOS avgR |
|---|---|---|---|---|---|---|---|---|---|---|---|
| breakout | fixed | all | 6495 | 17 | +0.291 | -1.11 | 1.27 | -0.309 (-3.66) | 3.2% | 1446 | -0.005 |
| breakout | fixed | SPY>200d & stock>200d | 5157 | 17 | +0.244 | -1.12 | 0.63 | -0.203 (-2.85) | 3.0% | 1159 | +0.028 |
| breakout | fixed | SPY>200d & stock>200d & RS>=0.8 | 2130 | 18 | +0.454 | -1.08 | 1.89 | -0.143 (-1.33) | 5.5% | 506 | +0.558 |
| breakout | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1743 | 18 | +0.487 | -1.08 | 1.86 | -0.037 (-0.30) | 4.4% | 390 | +0.727 |
| breakout | fixed | score>=70 & SPY>200d & stock>200d | 751 | 22 | +0.481 | -1.00 | 2.44 | +0.083 (0.55) | 5.9% | 151 | +0.259 |
| breakout | fixed | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 457 | 23 | +0.603 | -0.98 | 2.90 | +0.147 (0.70) | 7.7% | 100 | +0.427 |
| momentum | fixed | all | 5374 | 22 | +0.268 | -1.04 | 1.89 | -0.283 (-3.79) | 3.6% | 1194 | -0.000 |
| momentum | fixed | SPY>200d & stock>200d | 4747 | 22 | +0.307 | -1.04 | 1.94 | -0.083 (-1.32) | 3.5% | 1081 | +0.026 |
| momentum | fixed | SPY>200d & stock>200d & RS>=0.8 | 1922 | 22 | +0.395 | -1.02 | 2.15 | -0.121 (-1.55) | 6.2% | 443 | +0.253 |
| momentum | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1589 | 23 | +0.401 | -1.03 | 2.09 | -0.060 (-0.70) | 4.6% | 357 | +0.250 |
| momentum | fixed | score>=70 & SPY>200d & stock>200d | 154 | 24 | +0.567 | -0.91 | 2.08 | +0.327 (1.18) | 13.0% | 38 | +0.893 |
| momentum | fixed | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 95 | 25 | +0.748 | -0.88 | 1.92 | +0.275 (0.73) | 15.8% | 26 | +0.976 |
| combined | fixed | all | 8167 | 19 | +0.276 | -1.08 | 1.64 | -0.296 (-4.23) | 3.3% | 1796 | +0.092 |
| combined | fixed | SPY>200d & stock>200d | 6735 | 19 | +0.245 | -1.08 | 1.00 | -0.167 (-2.81) | 3.1% | 1500 | +0.093 |
| combined | fixed | SPY>200d & stock>200d & RS>=0.8 | 2805 | 20 | +0.426 | -1.04 | 2.10 | -0.135 (-1.69) | 5.5% | 655 | +0.594 |
| combined | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 2313 | 21 | +0.427 | -1.05 | 2.07 | -0.050 (-0.58) | 4.3% | 510 | +0.638 |
| combined | fixed | score>=70 & SPY>200d & stock>200d | 825 | 23 | +0.504 | -0.98 | 2.27 | +0.075 (0.55) | 6.6% | 174 | +0.295 |
| combined | fixed | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 501 | 24 | +0.615 | -0.96 | 2.60 | +0.089 (0.46) | 8.6% | 115 | +0.445 |
| baseline_random | fixed | all | 17819 | 24 | +0.343 | -1.02 | 4.82 | — (—) | 4.9% | 4068 | +0.198 |
| baseline_random | fixed | SPY>200d & stock>200d | 11337 | 23 | +0.316 | -1.05 | 3.03 | — (—) | 3.5% | 2592 | +0.151 |
| baseline_random | fixed | SPY>200d & stock>200d & RS>=0.8 | 4594 | 23 | +0.378 | -1.03 | 3.51 | — (—) | 6.2% | 1112 | +0.277 |
| baseline_random | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 3137 | 23 | +0.436 | -1.04 | 3.24 | — (—) | 4.0% | 678 | +0.355 |
| breakout | wide | all | 5219 | 33 | +0.305 | -0.95 | 3.25 | -0.159 (-2.90) | 5.5% | 1145 | +0.235 |
| breakout | wide | SPY>200d & stock>200d | 4201 | 33 | +0.316 | -0.96 | 2.36 | -0.065 (-1.35) | 5.1% | 930 | +0.255 |
| breakout | wide | SPY>200d & stock>200d & RS>=0.8 | 1782 | 35 | +0.451 | -0.93 | 2.98 | -0.095 (-1.56) | 9.2% | 417 | +0.423 |
| breakout | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1486 | 35 | +0.477 | -0.93 | 3.36 | -0.018 (-0.27) | 7.4% | 327 | +0.379 |
| breakout | wide | score>=70 & SPY>200d & stock>200d | 724 | 33 | +0.390 | -0.91 | 2.57 | -0.004 (-0.04) | 9.0% | 144 | +0.149 |
| breakout | wide | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 435 | 34 | +0.491 | -0.90 | 3.05 | +0.035 (0.23) | 11.5% | 94 | +0.285 |
| momentum | wide | all | 4470 | 32 | +0.271 | -0.98 | 2.85 | -0.176 (-3.01) | 4.8% | 964 | +0.122 |
| momentum | wide | SPY>200d & stock>200d | 3968 | 33 | +0.314 | -0.98 | 2.96 | -0.021 (-0.39) | 4.7% | 880 | +0.143 |
| momentum | wide | SPY>200d & stock>200d & RS>=0.8 | 1623 | 33 | +0.371 | -0.96 | 2.65 | -0.109 (-1.62) | 8.0% | 370 | +0.256 |
| momentum | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1369 | 33 | +0.352 | -0.97 | 2.40 | -0.098 (-1.39) | 5.8% | 295 | +0.270 |
| momentum | wide | score>=70 & SPY>200d & stock>200d | 138 | 31 | +0.331 | -0.88 | 1.45 | +0.026 (0.14) | 15.2% | 33 | +0.733 |
| momentum | wide | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 81 | 32 | +0.482 | -0.81 | 1.56 | -0.008 (-0.03) | 19.8% | 22 | +0.964 |
| combined | wide | all | 6214 | 33 | +0.288 | -0.97 | 3.22 | -0.170 (-3.32) | 5.2% | 1353 | +0.193 |
| combined | wide | SPY>200d & stock>200d | 5191 | 33 | +0.312 | -0.98 | 2.55 | -0.059 (-1.35) | 4.8% | 1151 | +0.205 |
| combined | wide | SPY>200d & stock>200d & RS>=0.8 | 2252 | 33 | +0.391 | -0.95 | 2.74 | -0.114 (-2.06) | 8.3% | 527 | +0.364 |
| combined | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1884 | 34 | +0.399 | -0.95 | 2.90 | -0.061 (-1.04) | 6.6% | 408 | +0.345 |
| combined | wide | score>=70 & SPY>200d & stock>200d | 783 | 33 | +0.384 | -0.90 | 2.20 | -0.032 (-0.32) | 9.1% | 162 | +0.227 |
| combined | wide | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 466 | 33 | +0.478 | -0.89 | 2.61 | -0.031 (-0.23) | 12.0% | 105 | +0.384 |
| baseline_random | wide | all | 12420 | 35 | +0.314 | -0.94 | 5.34 | — (—) | 6.3% | 2734 | +0.244 |
| baseline_random | wide | SPY>200d & stock>200d | 8147 | 34 | +0.313 | -0.97 | 3.60 | — (—) | 4.7% | 1860 | +0.172 |
| baseline_random | wide | SPY>200d & stock>200d & RS>=0.8 | 3411 | 34 | +0.373 | -0.96 | 4.15 | — (—) | 8.3% | 798 | +0.311 |
| baseline_random | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 2491 | 35 | +0.426 | -0.97 | 4.13 | — (—) | 5.7% | 520 | +0.419 |

## Portfolio — universe: largecap_2015

SPY buy-and-hold: +15.0%/yr, max DD -34%, Sharpe 0.84 · train+val Sharpe 0.82 · OOS +15.8%/yr, Sharpe 0.95

| rule set | trades/yr | exposure | win% | avgR | CAGR | max DD | Sharpe | train+val Sharpe | OOS CAGR | OOS Sharpe | vs random |
|---|---|---|---|---|---|---|---|---|---|---|---|
| random picks (reference) | 41.9 | 87% | 23 | +0.10 | +4.2% | -30% | 0.35 | 0.53 | -5.4% | -0.32 | — |
| random picks, trend filter | 38.3 | 74% | 20 | +0.04 | +0.6% | -41% | 0.11 | 0.21 | -3.7% | -0.23 | — |
| RS leaders, trend filter | 42.0 | 76% | 23 | +0.25 | +7.3% | -36% | 0.47 | 0.60 | +3.6% | 0.28 | 75% |
| RS leaders near 52w high | 40.2 | 76% | 22 | +0.22 | +3.8% | -29% | 0.30 | 0.43 | +0.9% | 0.14 | 50% |
| signals score>=70, trend | 15.1 | 37% | 24 | +0.35 | +3.5% | -16% | 0.41 | 0.47 | +4.1% | 0.47 | 40% |
| signals score>=70, trend, RS top 20% | 10.9 | 26% | 23 | +0.39 | +2.8% | -19% | 0.37 | 0.51 | +2.0% | 0.30 | 0% |
| signals, trend, RS top 20% | 42.6 | 78% | 20 | +0.32 | +5.9% | -30% | 0.45 | 0.55 | -0.9% | 0.04 | 72% |
| signals, trend, RS top 20%, near 52w high | 43.0 | 78% | 20 | +0.29 | +6.5% | -33% | 0.49 | 0.63 | -1.5% | 0.00 | 72% |

Cost sensitivity (full-period CAGR / Sharpe):

| rule set | 20 bps | 40 bps | 70 bps |
|---|---|---|---|
| RS leaders, trend filter | +7.3% / 0.47 | +4.4% / 0.32 | +0.1% / 0.11 |
| RS leaders near 52w high | +3.8% / 0.30 | +0.8% / 0.14 | -3.8% / -0.12 |
| signals score>=70, trend | +3.5% / 0.41 | +2.1% / 0.26 | +0.1% / 0.06 |
| signals score>=70, trend, RS top 20% | +2.8% / 0.37 | +1.7% / 0.24 | +0.2% / 0.06 |
| signals, trend, RS top 20% | +5.9% / 0.45 | +2.5% / 0.24 | -2.4% / -0.06 |
| signals, trend, RS top 20%, near 52w high | +6.5% / 0.49 | +3.1% / 0.29 | -1.8% / -0.03 |

Exit variant (stop 2.5 x ATR instead of 1.5 x ATR / structural):

| rule set | CAGR | max DD | Sharpe | OOS Sharpe |
|---|---|---|---|---|
| random picks (reference) | +8.6% | -19% | 0.63 | -0.15 |
| random picks, trend filter | +7.5% | -18% | 0.64 | -0.22 |
| RS leaders, trend filter | +10.9% | -25% | 0.69 | 0.22 |
| RS leaders near 52w high | +11.9% | -22% | 0.74 | -0.12 |
| signals score>=70, trend | +2.1% | -16% | 0.28 | 0.35 |
| signals score>=70, trend, RS top 20% | +2.8% | -17% | 0.39 | 0.37 |
| signals, trend, RS top 20% | +7.6% | -21% | 0.56 | 0.05 |
| signals, trend, RS top 20%, near 52w high | +6.5% | -27% | 0.51 | 0.02 |

### Per trade — universe: largecap_2015 (one position per symbol, t over monthly means)

| group | exit | policy | n | win% | avgR | medR | t | excess vs random (t) | ≥+50% | OOS n | OOS avgR |
|---|---|---|---|---|---|---|---|---|---|---|---|
| breakout | fixed | all | 2265 | 17 | +0.077 | -1.17 | -0.52 | -0.411 (-3.39) | 0.2% | 432 | -0.218 |
| breakout | fixed | SPY>200d & stock>200d | 1860 | 16 | -0.000 | -1.18 | -0.63 | -0.233 (-2.25) | 0.1% | 358 | -0.196 |
| breakout | fixed | SPY>200d & stock>200d & RS>=0.8 | 757 | 18 | +0.290 | -1.12 | 1.35 | +0.077 (0.36) | 0.1% | 154 | +0.108 |
| breakout | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 710 | 18 | +0.306 | -1.12 | 1.39 | +0.114 (0.53) | 0.1% | 150 | +0.178 |
| breakout | fixed | score>=70 & SPY>200d & stock>200d | 161 | 22 | +0.209 | -1.02 | 1.00 | -0.031 (-0.11) | 0.0% | 27 | +0.444 |
| breakout | fixed | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 106 | 22 | +0.261 | -1.00 | 1.18 | -0.007 (-0.02) | 0.0% | 16 | +0.412 |
| momentum | fixed | all | 2172 | 22 | +0.173 | -1.10 | 0.98 | -0.254 (-2.71) | 0.1% | 429 | -0.100 |
| momentum | fixed | SPY>200d & stock>200d | 1938 | 22 | +0.210 | -1.10 | 0.81 | -0.073 (-0.85) | 0.1% | 393 | -0.039 |
| momentum | fixed | SPY>200d & stock>200d & RS>=0.8 | 831 | 22 | +0.234 | -1.08 | 0.21 | -0.215 (-1.98) | 0.0% | 167 | +0.036 |
| momentum | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 789 | 22 | +0.217 | -1.08 | 0.03 | -0.206 (-1.87) | 0.0% | 162 | +0.065 |
| momentum | fixed | score>=70 & SPY>200d & stock>200d | 15 | 20 | +0.106 | -1.03 | 0.39 | +0.035 (0.05) | 0.0% | 3 | -1.150 |
| momentum | fixed | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 8 | 25 | +0.909 | -0.90 | 0.74 | +0.039 (0.03) | 0.0% | 2 | -1.090 |
| combined | fixed | all | 3075 | 19 | +0.117 | -1.12 | 0.05 | -0.335 (-3.51) | 0.2% | 583 | -0.173 |
| combined | fixed | SPY>200d & stock>200d | 2627 | 19 | +0.084 | -1.13 | -0.26 | -0.168 (-2.10) | 0.1% | 499 | -0.138 |
| combined | fixed | SPY>200d & stock>200d & RS>=0.8 | 1126 | 20 | +0.216 | -1.08 | 0.27 | -0.167 (-1.54) | 0.0% | 217 | -0.036 |
| combined | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1068 | 20 | +0.201 | -1.09 | 0.25 | -0.140 (-1.33) | 0.0% | 212 | +0.017 |
| combined | fixed | score>=70 & SPY>200d & stock>200d | 172 | 22 | +0.241 | -1.02 | 1.17 | -0.012 (-0.05) | 0.0% | 30 | +0.284 |
| combined | fixed | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 112 | 22 | +0.347 | -0.97 | 1.44 | +0.058 (0.17) | 0.0% | 18 | +0.245 |
| baseline_random | fixed | all | 7378 | 25 | +0.282 | -1.06 | 4.00 | — (—) | 0.7% | 1482 | +0.169 |
| baseline_random | fixed | SPY>200d & stock>200d | 4840 | 23 | +0.220 | -1.09 | 2.13 | — (—) | 0.3% | 961 | +0.111 |
| baseline_random | fixed | SPY>200d & stock>200d & RS>=0.8 | 1934 | 23 | +0.283 | -1.07 | 2.18 | — (—) | 0.4% | 422 | +0.057 |
| baseline_random | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1721 | 23 | +0.275 | -1.07 | 1.92 | — (—) | 0.2% | 363 | +0.098 |
| breakout | wide | all | 1935 | 33 | +0.180 | -1.00 | 1.39 | -0.227 (-3.04) | 0.3% | 359 | +0.105 |
| breakout | wide | SPY>200d & stock>200d | 1592 | 33 | +0.194 | -1.01 | 1.42 | -0.034 (-0.50) | 0.2% | 300 | +0.158 |
| breakout | wide | SPY>200d & stock>200d & RS>=0.8 | 671 | 33 | +0.267 | -0.97 | 1.30 | -0.121 (-1.38) | 0.0% | 134 | +0.059 |
| breakout | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 634 | 33 | +0.266 | -0.97 | 1.34 | -0.080 (-0.91) | 0.0% | 130 | +0.078 |
| breakout | wide | score>=70 & SPY>200d & stock>200d | 161 | 32 | +0.169 | -0.93 | 0.53 | -0.131 (-0.71) | 0.0% | 27 | +0.319 |
| breakout | wide | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 106 | 32 | +0.328 | -0.92 | 1.29 | -0.102 (-0.43) | 0.0% | 16 | +0.469 |
| momentum | wide | all | 1846 | 32 | +0.185 | -1.02 | 1.85 | -0.187 (-2.48) | 0.1% | 355 | +0.019 |
| momentum | wide | SPY>200d & stock>200d | 1648 | 32 | +0.230 | -1.02 | 2.02 | +0.022 (0.33) | 0.1% | 329 | +0.053 |
| momentum | wide | SPY>200d & stock>200d & RS>=0.8 | 715 | 33 | +0.268 | -0.99 | 1.33 | -0.118 (-1.48) | 0.0% | 146 | -0.065 |
| momentum | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 679 | 33 | +0.272 | -0.99 | 1.45 | -0.068 (-0.83) | 0.0% | 143 | -0.046 |
| momentum | wide | score>=70 & SPY>200d & stock>200d | 14 | 29 | +0.005 | -0.99 | 0.33 | +0.046 (0.09) | 0.0% | 3 | -1.085 |
| momentum | wide | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 7 | 43 | +0.817 | -0.91 | 0.92 | -0.009 (-0.01) | 0.0% | 2 | -1.053 |
| combined | wide | all | 2437 | 33 | +0.178 | -1.01 | 1.64 | -0.210 (-3.04) | 0.3% | 455 | +0.068 |
| combined | wide | SPY>200d & stock>200d | 2093 | 33 | +0.196 | -1.02 | 1.69 | -0.015 (-0.25) | 0.1% | 399 | +0.110 |
| combined | wide | SPY>200d & stock>200d & RS>=0.8 | 915 | 34 | +0.283 | -0.98 | 1.62 | -0.081 (-1.17) | 0.0% | 181 | -0.036 |
| combined | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 869 | 33 | +0.283 | -0.99 | 1.62 | -0.037 (-0.58) | 0.0% | 177 | -0.017 |
| combined | wide | score>=70 & SPY>200d & stock>200d | 171 | 32 | +0.176 | -0.93 | 0.73 | -0.108 (-0.61) | 0.0% | 30 | +0.178 |
| combined | wide | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 111 | 32 | +0.368 | -0.91 | 1.47 | -0.077 (-0.33) | 0.0% | 18 | +0.300 |
| baseline_random | wide | all | 5207 | 36 | +0.284 | -0.95 | 4.86 | — (—) | 0.8% | 997 | +0.240 |
| baseline_random | wide | SPY>200d & stock>200d | 3511 | 34 | +0.234 | -1.00 | 2.72 | — (—) | 0.2% | 713 | +0.162 |
| baseline_random | wide | SPY>200d & stock>200d & RS>=0.8 | 1485 | 35 | +0.296 | -0.98 | 2.86 | — (—) | 0.4% | 313 | +0.115 |
| baseline_random | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1335 | 35 | +0.295 | -0.99 | 2.65 | — (—) | 0.3% | 269 | +0.160 |

## Momentum rotation — universe: all (from 2018-01-10, 20 bps per side)

| benchmark | CAGR | max DD | Sharpe | train+val Sharpe | OOS CAGR | OOS Sharpe |
|---|---|---|---|---|---|---|
| SPY buy-and-hold | +14.3% | -34% | 0.80 | 0.76 | +15.8% | 0.95 |
| equal-weight universe (no costs) | +26.1% | -42% | 1.01 | 1.01 | +24.4% | 1.00 |

| rule set | trades/yr | exposure | win% | avg trade | avg days | CAGR | max DD | Sharpe | train+val Sharpe | OOS CAGR | OOS Sharpe | vs random | CAGR @40 / @70 bps | without best stock |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| top5, in RS>=0.8, out RS<0.5 | 10 | 92% | 38 | +23.7% | 106 | +26.5% | -75% | 0.69 | 0.61 | +47.6% | 0.89 | 60% | +25.6% / +24.3% | SE: +27.3%, Sharpe 0.70 |
| top5, in RS>=0.8, out RS<0.5, stop -20% | 16 | 92% | 29 | +17.9% | 70 | +31.2% | -66% | 0.75 | 0.76 | +27.1% | 0.69 | 75% | +30.0% / +28.1% | SE: +26.5%, Sharpe 0.69 |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d | 20 | 81% | 38 | +6.2% | 48 | +13.9% | -74% | 0.51 | 0.69 | -23.2% | -0.12 | 20% | +12.1% / +9.6% | MARA: +11.0%, Sharpe 0.46 |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | 26 | 80% | 33 | +3.8% | 38 | +9.8% | -71% | 0.44 | 0.54 | -11.3% | 0.10 | 15% | +7.8% / +5.0% | CELH: +15.6%, Sharpe 0.53 |
| top5, in RS>=0.8, out RS<0.7 | 12 | 93% | 44 | +12.0% | 93 | +20.9% | -76% | 0.62 | 0.57 | +33.2% | 0.76 | 30% | +19.9% / +18.4% | ENPH: +19.8%, Sharpe 0.60 |
| top5, in RS>=0.8, out RS<0.7, stop -20% | 18 | 92% | 35 | +10.6% | 63 | +21.8% | -77% | 0.62 | 0.51 | +56.1% | 0.97 | 55% | +20.2% / +18.0% | VKTX: +15.1%, Sharpe 0.53 |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d | 22 | 80% | 39 | +4.0% | 45 | +9.8% | -77% | 0.44 | 0.53 | -10.6% | 0.19 | 35% | +8.0% / +5.3% | TSLA: +15.6%, Sharpe 0.54 |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | 27 | 80% | 34 | +3.9% | 36 | +10.1% | -68% | 0.44 | 0.49 | -0.5% | 0.31 | 10% | +8.0% / +4.9% | CELH: +5.9%, Sharpe 0.37 |
| top8, in RS>=0.8, out RS<0.5 | 16 | 93% | 44 | +22.6% | 110 | +35.9% | -69% | 0.85 | 0.88 | +34.1% | 0.78 | 85% | +35.1% / +33.8% | SE: +33.3%, Sharpe 0.81 |
| top8, in RS>=0.8, out RS<0.5, stop -20% | 24 | 92% | 34 | +14.4% | 71 | +30.0% | -62% | 0.76 | 0.80 | +24.2% | 0.66 | 80% | +28.2% / +26.3% | SE: +25.3%, Sharpe 0.69 |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d | 30 | 80% | 39 | +9.5% | 52 | +31.2% | -58% | 0.79 | 0.82 | +27.1% | 0.70 | 85% | +29.4% / +26.9% | APP: +24.1%, Sharpe 0.68 |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | 37 | 80% | 34 | +6.9% | 41 | +26.4% | -67% | 0.72 | 0.73 | +26.6% | 0.69 | 90% | +24.2% / +21.4% | NIO: +27.6%, Sharpe 0.74 |
| top8, in RS>=0.8, out RS<0.7 | 19 | 92% | 49 | +18.8% | 94 | +35.8% | -58% | 0.83 | 0.85 | +34.1% | 0.77 | 75% | +38.4% / +33.1% | MARA: +29.1%, Sharpe 0.75 |
| top8, in RS>=0.8, out RS<0.7, stop -20% | 28 | 91% | 32 | +14.6% | 60 | +26.0% | -71% | 0.69 | 0.67 | +30.5% | 0.73 | 60% | +25.1% / +22.9% | MARA: +20.2%, Sharpe 0.61 |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d | 32 | 80% | 41 | +7.8% | 48 | +23.5% | -54% | 0.67 | 0.73 | +10.6% | 0.47 | 55% | +21.7% / +19.0% | MARA: +23.0%, Sharpe 0.67 |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | 40 | 80% | 33 | +9.5% | 38 | +28.1% | -63% | 0.72 | 0.78 | +12.4% | 0.50 | 90% | +26.2% / +22.9% | MARA: +26.4%, Sharpe 0.70 |
| top8, in RS>=0.8, out RS<0.5, 12-1 month momentum | 18 | 91% | 34 | +20.4% | 99 | +27.3% | -63% | 0.73 | 0.69 | +43.1% | 0.87 | 70% | +26.3% / +24.9% | SE: +24.6%, Sharpe 0.69 |
| top8, in RS>=0.8, out RS<0.5, monthly | 11 | 94% | 39 | +49.3% | 150 | +37.3% | -63% | 0.87 | 0.80 | +61.9% | 1.06 | 75% | +36.6% / +35.6% | ENPH: +34.3%, Sharpe 0.83 |
| top8, in RS>=0.8, out RS<0.5, volatility-adjusted | 14 | 93% | 46 | +26.3% | 126 | +37.9% | -47% | 0.98 | 0.96 | +57.5% | 1.07 | 95% | +37.0% / +35.7% | RKLB: +31.6%, Sharpe 0.87 |

## Momentum rotation — universe: largecap_2015 (from 2018-01-10, 20 bps per side)

| benchmark | CAGR | max DD | Sharpe | train+val Sharpe | OOS CAGR | OOS Sharpe |
|---|---|---|---|---|---|---|
| SPY buy-and-hold | +14.3% | -34% | 0.80 | 0.76 | +15.8% | 0.95 |
| equal-weight universe (no costs) | +13.4% | -37% | 0.77 | 0.76 | +12.1% | 0.90 |

| rule set | trades/yr | exposure | win% | avg trade | avg days | CAGR | max DD | Sharpe | train+val Sharpe | OOS CAGR | OOS Sharpe | vs random | CAGR @40 / @70 bps | without best stock |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| top5, in RS>=0.8, out RS<0.5 | 10 | 95% | 48 | +7.4% | 116 | +16.4% | -36% | 0.72 | 0.56 | +37.2% | 1.20 | 95% | +15.5% / +14.3% | DVN: +13.3%, Sharpe 0.63 |
| top5, in RS>=0.8, out RS<0.5, stop -20% | 10 | 94% | 51 | +7.5% | 113 | +16.8% | -36% | 0.73 | 0.58 | +37.0% | 1.19 | 90% | +15.9% / +14.7% | DVN: +13.6%, Sharpe 0.64 |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d | 20 | 81% | 48 | +3.0% | 50 | +12.0% | -24% | 0.62 | 0.60 | +15.4% | 0.67 | 90% | +10.3% / +7.8% | AVGO: +11.9%, Sharpe 0.64 |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | 20 | 81% | 49 | +3.0% | 50 | +12.1% | -24% | 0.62 | 0.60 | +15.5% | 0.67 | 100% | +10.3% / +7.8% | AVGO: +11.9%, Sharpe 0.64 |
| top5, in RS>=0.8, out RS<0.7 | 14 | 94% | 49 | +3.9% | 83 | +13.6% | -36% | 0.62 | 0.57 | +21.3% | 0.77 | 95% | +12.4% / +10.7% | META: +11.6%, Sharpe 0.56 |
| top5, in RS>=0.8, out RS<0.7, stop -20% | 14 | 95% | 49 | +4.5% | 81 | +15.6% | -33% | 0.68 | 0.66 | +20.6% | 0.75 | 100% | +14.4% / +12.7% | META: +15.2%, Sharpe 0.67 |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d | 22 | 81% | 47 | +2.3% | 44 | +10.7% | -29% | 0.57 | 0.64 | +6.5% | 0.37 | 95% | +8.8% / +5.9% | AVGO: +9.5%, Sharpe 0.53 |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | 23 | 81% | 48 | +2.3% | 43 | +10.6% | -29% | 0.57 | 0.64 | +6.3% | 0.36 | 95% | +8.7% / +5.8% | AVGO: +9.6%, Sharpe 0.53 |
| top8, in RS>=0.8, out RS<0.5 | 17 | 94% | 46 | +7.3% | 111 | +16.1% | -29% | 0.77 | 0.65 | +29.4% | 1.19 | 100% | +15.2% / +13.9% | DVN: +14.0%, Sharpe 0.70 |
| top8, in RS>=0.8, out RS<0.5, stop -20% | 17 | 94% | 47 | +6.1% | 105 | +14.9% | -29% | 0.73 | 0.61 | +27.1% | 1.12 | 100% | +14.0% / +12.7% | DVN: +12.5%, Sharpe 0.65 |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d | 30 | 80% | 44 | +2.5% | 52 | +9.2% | -27% | 0.56 | 0.52 | +12.3% | 0.67 | 85% | +7.6% / +5.2% | DVN: +8.5%, Sharpe 0.53 |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | 31 | 80% | 44 | +2.5% | 51 | +9.3% | -27% | 0.56 | 0.53 | +12.2% | 0.67 | 90% | +7.6% / +5.2% | DVN: +8.5%, Sharpe 0.53 |
| top8, in RS>=0.8, out RS<0.7 | 22 | 93% | 49 | +3.9% | 81 | +13.0% | -26% | 0.66 | 0.64 | +15.3% | 0.73 | 100% | +11.8% / +10.1% | META: +10.1%, Sharpe 0.55 |
| top8, in RS>=0.8, out RS<0.7, stop -20% | 23 | 93% | 48 | +4.0% | 78 | +12.7% | -29% | 0.65 | 0.63 | +14.8% | 0.71 | 95% | +11.5% / +9.7% | AVGO: +10.3%, Sharpe 0.56 |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d | 35 | 80% | 47 | +1.9% | 45 | +8.5% | -29% | 0.53 | 0.57 | +5.6% | 0.37 | 95% | +6.7% / +4.0% | AVGO: +7.8%, Sharpe 0.50 |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | 35 | 80% | 47 | +1.9% | 45 | +8.4% | -29% | 0.52 | 0.57 | +5.4% | 0.36 | 90% | +6.6% / +3.9% | AVGO: +7.9%, Sharpe 0.50 |
| top8, in RS>=0.8, out RS<0.5, 12-1 month momentum | 19 | 90% | 32 | +2.6% | 92 | +6.0% | -40% | 0.38 | 0.36 | +7.1% | 0.43 | 15% | +5.1% / +3.8% | GE: +4.4%, Sharpe 0.31 |
| top8, in RS>=0.8, out RS<0.5, monthly | 12 | 93% | 49 | +9.5% | 146 | +13.8% | -26% | 0.67 | 0.59 | +22.4% | 0.95 | 95% | +13.1% / +13.7% | DVN: +13.6%, Sharpe 0.66 |
| top8, in RS>=0.8, out RS<0.5, volatility-adjusted | 16 | 93% | 56 | +6.6% | 114 | +12.1% | -23% | 0.71 | 0.68 | +12.3% | 0.81 | 100% | +11.2% / +10.0% | GE: +9.0%, Sharpe 0.56 |

## Rotation: pre-registered selection (2015 large caps, train+validation only)

Gates: train+val Sharpe > SPY's, ranking beats >= 90% of random selections, CAGR without the single best stock >= SPY's, max drawdown at most 10 points worse than SPY's.

**Chosen: none — no rule set passed every gate**

| rule set | passes | train+val Sharpe | failed gates |
|---|---|---|---|
| top5, in RS>=0.8, out RS<0.5 | ❌ | 0.56 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top5, in RS>=0.8, out RS<0.5, stop -20% | ❌ | 0.58 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d | ❌ | 0.60 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | ❌ | 0.60 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top5, in RS>=0.8, out RS<0.7 | ❌ | 0.57 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top5, in RS>=0.8, out RS<0.7, stop -20% | ❌ | 0.66 | train_val_sharpe_beats_spy |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d | ❌ | 0.64 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | ❌ | 0.64 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5 | ❌ | 0.65 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5, stop -20% | ❌ | 0.61 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d | ❌ | 0.52 | train_val_sharpe_beats_spy, ranking_beats_random, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | ❌ | 0.53 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.7 | ❌ | 0.64 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.7, stop -20% | ❌ | 0.63 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d | ❌ | 0.57 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | ❌ | 0.57 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5, 12-1 month momentum | ❌ | 0.36 | train_val_sharpe_beats_spy, ranking_beats_random, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5, monthly | ❌ | 0.59 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5, volatility-adjusted | ❌ | 0.68 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |

Calendar-year returns (2015 large caps, 20 bps per side):

| | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|---|---|---|---|
| SPY | -7% | +31% | +18% | +29% | -18% | +26% | +25% | +18% | +14% |
| equal-weight group | -8% | +29% | +14% | +31% | -4% | +16% | +16% | +17% | +11% |
| top5, in RS>=0.8, out RS<0.5 | -6% | +8% | +13% | +21% | +0% | +11% | +37% | +15% | +56% |
| top5, in RS>=0.8, out RS<0.5, stop -20% | -7% | +8% | +14% | +22% | -0% | +14% | +36% | +14% | +56% |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d | +0% | +3% | +16% | +21% | -1% | +21% | +19% | +9% | +20% |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | +0% | +3% | +16% | +22% | -1% | +21% | +19% | +9% | +20% |
| top5, in RS>=0.8, out RS<0.7 | -3% | +8% | +7% | +21% | -4% | +19% | +30% | -2% | +54% |
| top5, in RS>=0.8, out RS<0.7, stop -20% | -3% | +7% | +9% | +22% | +10% | +21% | +30% | -2% | +53% |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d | +3% | -3% | +8% | +21% | -2% | +22% | +29% | -5% | +25% |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | +3% | -3% | +8% | +21% | -2% | +22% | +29% | -5% | +25% |
| top8, in RS>=0.8, out RS<0.5 | -10% | +8% | +17% | +28% | +0% | +23% | +27% | +22% | +32% |
| top8, in RS>=0.8, out RS<0.5, stop -20% | -10% | +8% | +11% | +33% | +1% | +20% | +22% | +23% | +28% |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d | -0% | -5% | +11% | +30% | -2% | +14% | +13% | +14% | +10% |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | -0% | -4% | +11% | +30% | -2% | +14% | +13% | +14% | +9% |
| top8, in RS>=0.8, out RS<0.7 | -8% | +9% | +17% | +18% | +2% | +20% | +25% | +6% | +29% |
| top8, in RS>=0.8, out RS<0.7, stop -20% | -8% | +6% | +13% | +18% | +6% | +21% | +25% | +5% | +29% |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d | +0% | +2% | +12% | +18% | -4% | +9% | +24% | +2% | +14% |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | +0% | +2% | +12% | +18% | -4% | +9% | +24% | +1% | +14% |
| top8, in RS>=0.8, out RS<0.5, 12-1 month momentum | -15% | +10% | +2% | +24% | -12% | +2% | +41% | -1% | +12% |
| top8, in RS>=0.8, out RS<0.5, monthly | -3% | +12% | +16% | +19% | -5% | +26% | +23% | +5% | +34% |
| top8, in RS>=0.8, out RS<0.5, volatility-adjusted | -6% | +16% | +3% | +22% | -8% | +18% | +38% | +20% | +9% |

## Rockets (from 2016-10-24, 20 bps per side, 10 slots x 10%, max 3 new per day)

Rocket day: close >= +jump vs previous close, volume >= 3x the 20-day average, close in the top quarter of the day's range, price >= $5, 20-day dollar volume >= $5M. Buy next open; sell next open after a close more than `trail` below the highest close, or after 40 sessions. 'Random' = same stocks, same liquidity filter, same exit, random dates.

SPY: +15.6%/yr, max DD -34%, Sharpe 0.89 · train+val +15.4%/yr, Sharpe 0.88

| variant | trades | win% | avg trade | median | ≥+50% | worst | random avg | excess vs random t (train+val) | 2015 large caps excess | CAGR | max DD | Sharpe | train+val CAGR / Sharpe | OOS CAGR | random-entry portfolio CAGR | without top 3 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| EPS surprise>0%, reaction>=5% | 1886 | 54 | +4.7% | +2.0% | 4.4% | -51% | +4.4% | -0.26% (-0.41) | -0.22% (n=556) | +7.4% | -40% | 0.45 | +12.0% / 0.65 | -4.4% | +19.9% | +7.4% |
| EPS surprise>0%, reaction>=10% | 910 | 53 | +6.4% | +2.0% | 6.4% | -51% | +4.4% | +0.84% (0.85) | +1.84% (n=125) | +23.6% | -43% | 0.98 | +24.6% / 1.04 | +18.6% | +19.9% | +22.9% |
| EPS surprise>10%, reaction>=5% | 1257 | 54 | +5.2% | +2.4% | 5.0% | -51% | +4.4% | +0.66% (0.81) | -0.67% (n=266) | +14.2% | -45% | 0.68 | +23.5% / 1.02 | -17.8% | +19.9% | +14.6% |
| EPS surprise>10%, reaction>=10% | 703 | 53 | +6.8% | +2.5% | 6.4% | -51% | +4.4% | +1.72% (1.42) | +2.45% (n=68) | +19.0% | -48% | 0.81 | +26.6% / 1.05 | -12.9% | +19.9% | +15.7% |
| jump>=8%, trail 15% | 996 | 45 | +3.9% | -2.7% | 5.2% | -52% | +2.3% | -0.15% (-0.15) | -1.74% (n=115) | +15.6% | -48% | 0.63 | +22.0% / 0.79 | -17.6% | +26.9% | +9.8% |
| jump>=8%, trail 25% | 993 | 51 | +5.3% | +0.6% | 6.8% | -61% | +3.0% | +0.39% (0.34) | -1.70% (n=115) | +14.8% | -68% | 0.59 | +22.0% / 0.78 | -14.0% | +20.8% | +10.9% |
| jump>=15%, trail 15% | 538 | 43 | +4.7% | -4.6% | 6.7% | -52% | +2.3% | -0.22% (-0.15) | -4.51% (n=23) | +17.7% | -38% | 0.70 | +21.0% / 0.78 | -2.7% | +26.9% | +11.4% |
| jump>=15%, trail 25% | 535 | 47 | +6.7% | -2.4% | 9.2% | -61% | +3.0% | +1.18% (0.65) | -4.75% (n=23) | +14.5% | -60% | 0.57 | +19.2% / 0.69 | -12.8% | +20.8% | +6.2% |

Pre-registered gates: excess vs random entries t >= 2 (train+val); portfolio beats SPY on train+val CAGR and Sharpe; positive excess among 2015 large caps; CAGR without the 3 best stocks >= SPY's; max drawdown >= -50%.

**Chosen: none — no rocket variant passed every gate**

| variant | passes | failed gates |
|---|---|---|
| EPS surprise>0%, reaction>=5% | ❌ | beats_random_entries_same_stocks, beats_spy_train_val, holds_in_2015_largecaps, without_top3_beats_spy |
| EPS surprise>0%, reaction>=10% | ❌ | beats_random_entries_same_stocks |
| EPS surprise>10%, reaction>=5% | ❌ | beats_random_entries_same_stocks, holds_in_2015_largecaps, without_top3_beats_spy |
| EPS surprise>10%, reaction>=10% | ❌ | beats_random_entries_same_stocks |
| jump>=8%, trail 15% | ❌ | beats_random_entries_same_stocks, beats_spy_train_val, holds_in_2015_largecaps, without_top3_beats_spy |
| jump>=8%, trail 25% | ❌ | beats_random_entries_same_stocks, beats_spy_train_val, holds_in_2015_largecaps, without_top3_beats_spy, drawdown_tolerable |
| jump>=15%, trail 15% | ❌ | beats_random_entries_same_stocks, beats_spy_train_val, holds_in_2015_largecaps, without_top3_beats_spy |
| jump>=15%, trail 25% | ❌ | beats_random_entries_same_stocks, beats_spy_train_val, holds_in_2015_largecaps, without_top3_beats_spy, drawdown_tolerable |

## Mean R by year (all universe, fixed exit)

| group | policy | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| combined | all | +0.80 | -0.43 | +0.34 | +1.07 | +0.03 | -0.44 | +0.53 | +0.42 | +0.23 | -0.03 |
| combined | SPY>200d & stock>200d | +0.84 | -0.42 | +0.08 | +0.94 | -0.03 | -0.79 | +0.38 | +0.42 | +0.19 | +0.01 |
| combined | SPY>200d & stock>200d & RS>=0.8 | +0.84 | -0.27 | +0.47 | +1.45 | -0.41 | -0.36 | +0.35 | +0.60 | +0.83 | +0.33 |
| combined | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | +0.91 | -0.13 | +0.59 | +1.35 | -0.52 | -0.07 | +0.30 | +0.46 | +0.81 | +0.54 |
| combined | score>=70 & SPY>200d & stock>200d | +0.99 | +0.65 | +0.42 | +1.14 | -0.54 | -0.96 | +0.43 | +0.69 | +0.52 | +0.12 |
| combined | score>=70 & SPY>200d & stock>200d & RS>=0.8 | +0.65 | +1.33 | +0.61 | +1.08 | -0.53 | -1.15 | +0.41 | +1.00 | +0.70 | +0.19 |
| baseline_random | all | +0.95 | +0.06 | +0.55 | +0.98 | +0.15 | -0.28 | +0.61 | +0.42 | +0.30 | +0.17 |
| baseline_random | SPY>200d & stock>200d | +0.99 | -0.24 | +0.52 | +0.85 | +0.17 | -0.78 | +0.26 | +0.42 | +0.21 | +0.15 |
| baseline_random | SPY>200d & stock>200d & RS>=0.8 | +0.97 | +0.11 | +0.66 | +1.15 | -0.24 | -0.74 | +0.47 | +0.51 | +0.39 | +0.19 |
| baseline_random | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | +0.94 | +0.28 | +0.75 | +0.96 | -0.29 | -0.63 | +0.55 | +0.60 | +0.64 | +0.10 |