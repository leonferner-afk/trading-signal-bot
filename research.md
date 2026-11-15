# Strategy research

278 symbols with data (1 failed), 10 years of daily bars. Control group: 105 stocks that were already large caps in 2015. Primary cost 20 bps per side (USD account: courtage + slippage; 40 bps ≈ trading from a SEK account). Validation from 2023-03-11, out-of-sample (OOS) from 2025-01-10. Setups invalidated at the next open (skipped): 1310.

Portfolio: max 8 positions, max 3 new per day, 1% risk per trade, max 25% of equity per position, no leverage, marked to market daily. 'vs random' = share of 40 random-order portfolios from the same eligible trades that this ranking beat.

## Portfolio — universe: all

SPY buy-and-hold: +14.8%/yr, max DD -34%, Sharpe 0.83 · train+val Sharpe 0.81 · OOS +16.5%/yr, Sharpe 0.98

| rule set | trades/yr | exposure | win% | avgR | CAGR | max DD | Sharpe | train+val Sharpe | OOS CAGR | OOS Sharpe | vs random |
|---|---|---|---|---|---|---|---|---|---|---|---|
| random picks (reference) | 78.6 | 86% | 21 | +0.23 | +9.3% | -53% | 0.45 | 0.54 | -0.9% | 0.12 | — |
| random picks, trend filter | 64.3 | 78% | 21 | +0.27 | +7.4% | -56% | 0.41 | 0.53 | -5.7% | -0.05 | — |
| RS leaders, trend filter | 74.1 | 66% | 23 | +0.39 | +21.2% | -42% | 0.75 | 0.91 | +0.7% | 0.21 | 100% |
| RS leaders near 52w high | 66.2 | 76% | 25 | +0.59 | +31.0% | -42% | 1.02 | 1.17 | +14.9% | 0.55 | 100% |
| signals score>=70, trend | 47.4 | 63% | 20 | +0.25 | +8.2% | -35% | 0.48 | 0.61 | -4.4% | -0.08 | 20% |
| signals score>=70, trend, RS top 20% | 41.9 | 50% | 22 | +0.47 | +17.8% | -33% | 0.84 | 0.94 | +5.0% | 0.33 | 70% |
| signals, trend, RS top 20% | 76.1 | 79% | 22 | +0.68 | +36.7% | -48% | 1.08 | 1.21 | +23.2% | 0.72 | 95% |
| signals, trend, RS top 20%, near 52w high | 72.4 | 79% | 22 | +0.54 | +28.9% | -32% | 1.01 | 1.16 | +22.9% | 0.74 | 100% |

Cost sensitivity (full-period CAGR / Sharpe):

| rule set | 20 bps | 40 bps | 70 bps |
|---|---|---|---|
| RS leaders, trend filter | +21.2% / 0.75 | +17.5% / 0.65 | +12.2% / 0.51 |
| RS leaders near 52w high | +31.0% / 1.02 | +26.6% / 0.91 | +19.8% / 0.74 |
| signals score>=70, trend | +8.2% / 0.48 | +5.3% / 0.35 | +1.4% / 0.17 |
| signals score>=70, trend, RS top 20% | +17.8% / 0.84 | +15.2% / 0.74 | +11.4% / 0.59 |
| signals, trend, RS top 20% | +36.7% / 1.08 | +30.7% / 0.95 | +24.0% / 0.79 |
| signals, trend, RS top 20%, near 52w high | +28.9% / 1.01 | +23.8% / 0.87 | +17.1% / 0.68 |

Exit variant (stop 2.5 x ATR instead of 1.5 x ATR / structural):

| rule set | CAGR | max DD | Sharpe | OOS Sharpe |
|---|---|---|---|---|
| random picks (reference) | +7.6% | -51% | 0.45 | 0.03 |
| random picks, trend filter | +12.8% | -27% | 0.72 | 0.45 |
| RS leaders, trend filter | +19.5% | -27% | 0.91 | -0.07 |
| RS leaders near 52w high | +22.8% | -24% | 1.02 | 0.39 |
| signals score>=70, trend | +10.6% | -28% | 0.68 | -0.09 |
| signals score>=70, trend, RS top 20% | +16.6% | -28% | 0.97 | 0.31 |
| signals, trend, RS top 20% | +18.8% | -36% | 0.89 | 0.62 |
| signals, trend, RS top 20%, near 52w high | +15.8% | -26% | 0.78 | 0.39 |

### Per trade — universe: all (one position per symbol, t over monthly means)

| group | exit | policy | n | win% | avgR | medR | t | excess vs random (t) | ≥+50% | OOS n | OOS avgR |
|---|---|---|---|---|---|---|---|---|---|---|---|
| breakout | fixed | all | 6527 | 17 | +0.270 | -1.11 | 1.06 | -0.333 (-3.93) | 3.2% | 1478 | -0.008 |
| breakout | fixed | SPY>200d & stock>200d | 5172 | 16 | +0.214 | -1.12 | 0.31 | -0.226 (-3.20) | 3.0% | 1191 | -0.007 |
| breakout | fixed | SPY>200d & stock>200d & RS>=0.8 | 2143 | 18 | +0.384 | -1.08 | 1.18 | -0.204 (-1.94) | 5.4% | 514 | +0.427 |
| breakout | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1749 | 18 | +0.419 | -1.08 | 1.14 | -0.110 (-0.91) | 4.3% | 393 | +0.614 |
| breakout | fixed | score>=70 & SPY>200d & stock>200d | 744 | 22 | +0.442 | -1.00 | 2.11 | +0.035 (0.23) | 5.9% | 138 | +0.282 |
| breakout | fixed | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 454 | 23 | +0.560 | -0.98 | 2.51 | +0.074 (0.36) | 7.7% | 91 | +0.424 |
| momentum | fixed | all | 5416 | 22 | +0.257 | -1.04 | 1.69 | -0.303 (-4.01) | 3.6% | 1239 | +0.057 |
| momentum | fixed | SPY>200d & stock>200d | 4783 | 22 | +0.292 | -1.04 | 1.71 | -0.096 (-1.49) | 3.4% | 1121 | +0.081 |
| momentum | fixed | SPY>200d & stock>200d & RS>=0.8 | 1948 | 22 | +0.370 | -1.02 | 2.03 | -0.107 (-1.32) | 6.2% | 467 | +0.234 |
| momentum | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1607 | 23 | +0.378 | -1.03 | 1.98 | -0.038 (-0.43) | 4.5% | 372 | +0.218 |
| momentum | fixed | score>=70 & SPY>200d & stock>200d | 159 | 23 | +0.522 | -0.92 | 1.99 | +0.305 (1.12) | 12.6% | 40 | +0.823 |
| momentum | fixed | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 98 | 24 | +0.694 | -0.90 | 1.80 | +0.264 (0.72) | 15.3% | 27 | +0.911 |
| combined | fixed | all | 8227 | 19 | +0.265 | -1.07 | 1.43 | -0.315 (-4.46) | 3.3% | 1860 | +0.107 |
| combined | fixed | SPY>200d & stock>200d | 6776 | 19 | +0.226 | -1.08 | 0.70 | -0.183 (-3.08) | 3.0% | 1558 | +0.086 |
| combined | fixed | SPY>200d & stock>200d & RS>=0.8 | 2830 | 20 | +0.386 | -1.04 | 1.73 | -0.146 (-1.86) | 5.4% | 680 | +0.468 |
| combined | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 2330 | 21 | +0.392 | -1.05 | 1.70 | -0.062 (-0.74) | 4.2% | 525 | +0.561 |
| combined | fixed | score>=70 & SPY>200d & stock>200d | 823 | 22 | +0.461 | -0.99 | 1.87 | +0.020 (0.15) | 6.6% | 163 | +0.308 |
| combined | fixed | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 501 | 23 | +0.567 | -0.96 | 2.16 | +0.013 (0.07) | 8.6% | 107 | +0.433 |
| baseline_random | fixed | all | 17943 | 25 | +0.348 | -1.01 | 4.80 | — (—) | 4.9% | 4124 | +0.241 |
| baseline_random | fixed | SPY>200d & stock>200d | 11333 | 23 | +0.324 | -1.04 | 2.88 | — (—) | 3.5% | 2601 | +0.177 |
| baseline_random | fixed | SPY>200d & stock>200d & RS>=0.8 | 4628 | 23 | +0.356 | -1.03 | 3.22 | — (—) | 6.1% | 1129 | +0.224 |
| baseline_random | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 3158 | 23 | +0.409 | -1.04 | 2.89 | — (—) | 4.0% | 698 | +0.309 |
| breakout | wide | all | 5254 | 33 | +0.295 | -0.95 | 3.05 | -0.166 (-2.96) | 5.5% | 1182 | +0.263 |
| breakout | wide | SPY>200d & stock>200d | 4218 | 33 | +0.306 | -0.96 | 2.15 | -0.062 (-1.29) | 5.0% | 958 | +0.282 |
| breakout | wide | SPY>200d & stock>200d & RS>=0.8 | 1791 | 34 | +0.424 | -0.93 | 2.53 | -0.089 (-1.47) | 9.0% | 432 | +0.358 |
| breakout | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1489 | 35 | +0.461 | -0.92 | 2.92 | -0.020 (-0.30) | 7.3% | 334 | +0.338 |
| breakout | wide | score>=70 & SPY>200d & stock>200d | 717 | 33 | +0.377 | -0.92 | 2.42 | -0.004 (-0.03) | 9.1% | 132 | +0.180 |
| breakout | wide | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 432 | 34 | +0.471 | -0.90 | 2.79 | +0.034 (0.22) | 11.6% | 87 | +0.244 |
| momentum | wide | all | 4507 | 32 | +0.262 | -0.98 | 2.61 | -0.189 (-3.22) | 4.8% | 1006 | +0.153 |
| momentum | wide | SPY>200d & stock>200d | 3997 | 33 | +0.302 | -0.98 | 2.70 | -0.025 (-0.49) | 4.6% | 915 | +0.180 |
| momentum | wide | SPY>200d & stock>200d & RS>=0.8 | 1643 | 33 | +0.351 | -0.96 | 2.31 | -0.107 (-1.81) | 7.8% | 394 | +0.242 |
| momentum | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1386 | 33 | +0.331 | -0.97 | 2.04 | -0.106 (-1.64) | 5.6% | 315 | +0.254 |
| momentum | wide | score>=70 & SPY>200d & stock>200d | 143 | 29 | +0.290 | -0.88 | 1.27 | -0.002 (-0.01) | 14.7% | 37 | +0.573 |
| momentum | wide | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 84 | 30 | +0.420 | -0.83 | 1.32 | -0.022 (-0.09) | 19.1% | 25 | +0.698 |
| combined | wide | all | 6268 | 33 | +0.279 | -0.97 | 2.97 | -0.181 (-3.51) | 5.1% | 1403 | +0.225 |
| combined | wide | SPY>200d & stock>200d | 5226 | 33 | +0.302 | -0.98 | 2.27 | -0.062 (-1.47) | 4.8% | 1194 | +0.233 |
| combined | wide | SPY>200d & stock>200d & RS>=0.8 | 2268 | 33 | +0.374 | -0.95 | 2.41 | -0.098 (-1.82) | 8.2% | 549 | +0.328 |
| combined | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1897 | 34 | +0.388 | -0.95 | 2.60 | -0.053 (-0.92) | 6.5% | 425 | +0.325 |
| combined | wide | score>=70 & SPY>200d & stock>200d | 780 | 32 | +0.366 | -0.91 | 1.98 | -0.038 (-0.39) | 9.1% | 153 | +0.245 |
| combined | wide | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 465 | 33 | +0.453 | -0.89 | 2.24 | -0.047 (-0.35) | 12.0% | 100 | +0.323 |
| baseline_random | wide | all | 12501 | 35 | +0.317 | -0.94 | 5.22 | — (—) | 6.2% | 2744 | +0.285 |
| baseline_random | wide | SPY>200d & stock>200d | 8151 | 34 | +0.315 | -0.97 | 3.35 | — (—) | 4.7% | 1856 | +0.200 |
| baseline_random | wide | SPY>200d & stock>200d & RS>=0.8 | 3432 | 33 | +0.343 | -0.97 | 3.72 | — (—) | 8.2% | 820 | +0.266 |
| baseline_random | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 2511 | 35 | +0.403 | -0.97 | 3.75 | — (—) | 5.7% | 542 | +0.382 |

## Portfolio — universe: largecap_2015

SPY buy-and-hold: +14.8%/yr, max DD -34%, Sharpe 0.83 · train+val Sharpe 0.81 · OOS +16.5%/yr, Sharpe 0.98

| rule set | trades/yr | exposure | win% | avgR | CAGR | max DD | Sharpe | train+val Sharpe | OOS CAGR | OOS Sharpe | vs random |
|---|---|---|---|---|---|---|---|---|---|---|---|
| random picks (reference) | 43.5 | 88% | 24 | +0.19 | +5.8% | -28% | 0.44 | 0.50 | -0.6% | 0.09 | — |
| random picks, trend filter | 38.2 | 75% | 20 | +0.11 | +2.2% | -24% | 0.23 | 0.27 | -1.7% | -0.03 | — |
| RS leaders, trend filter | 42.7 | 76% | 23 | +0.24 | +7.0% | -36% | 0.45 | 0.56 | +0.8% | 0.17 | 65% |
| RS leaders near 52w high | 40.9 | 76% | 22 | +0.21 | +3.7% | -29% | 0.30 | 0.31 | +3.6% | 0.33 | 38% |
| signals score>=70, trend | 14.8 | 36% | 23 | +0.26 | +2.8% | -16% | 0.33 | 0.34 | +2.4% | 0.28 | 47% |
| signals score>=70, trend, RS top 20% | 10.9 | 25% | 22 | +0.32 | +2.2% | -19% | 0.29 | 0.33 | +1.4% | 0.22 | 3% |
| signals, trend, RS top 20% | 40.8 | 78% | 21 | +0.32 | +6.8% | -30% | 0.48 | 0.52 | +4.5% | 0.38 | 60% |
| signals, trend, RS top 20%, near 52w high | 41.9 | 78% | 21 | +0.32 | +7.4% | -33% | 0.53 | 0.59 | +4.3% | 0.37 | 65% |

Cost sensitivity (full-period CAGR / Sharpe):

| rule set | 20 bps | 40 bps | 70 bps |
|---|---|---|---|
| RS leaders, trend filter | +7.0% / 0.45 | +4.0% / 0.31 | -0.3% / 0.08 |
| RS leaders near 52w high | +3.7% / 0.30 | +0.7% / 0.13 | -4.0% / -0.13 |
| signals score>=70, trend | +2.8% / 0.33 | +1.5% / 0.19 | -0.5% / -0.02 |
| signals score>=70, trend, RS top 20% | +2.2% / 0.29 | +1.1% / 0.16 | -0.4% / -0.02 |
| signals, trend, RS top 20% | +6.8% / 0.48 | +3.4% / 0.28 | -1.4% / -0.01 |
| signals, trend, RS top 20%, near 52w high | +7.4% / 0.53 | +4.1% / 0.33 | -0.8% / 0.02 |

Exit variant (stop 2.5 x ATR instead of 1.5 x ATR / structural):

| rule set | CAGR | max DD | Sharpe | OOS Sharpe |
|---|---|---|---|---|
| random picks (reference) | +7.5% | -23% | 0.57 | 0.73 |
| random picks, trend filter | +5.0% | -24% | 0.45 | 1.04 |
| RS leaders, trend filter | +11.1% | -25% | 0.70 | 0.26 |
| RS leaders near 52w high | +13.0% | -22% | 0.81 | 0.21 |
| signals score>=70, trend | +2.1% | -16% | 0.28 | 0.56 |
| signals score>=70, trend, RS top 20% | +2.7% | -17% | 0.38 | 0.48 |
| signals, trend, RS top 20% | +7.7% | -21% | 0.55 | 0.42 |
| signals, trend, RS top 20%, near 52w high | +6.9% | -27% | 0.52 | 0.49 |

### Per trade — universe: largecap_2015 (one position per symbol, t over monthly means)

| group | exit | policy | n | win% | avgR | medR | t | excess vs random (t) | ≥+50% | OOS n | OOS avgR |
|---|---|---|---|---|---|---|---|---|---|---|---|
| breakout | fixed | all | 2286 | 17 | +0.077 | -1.16 | -0.57 | -0.453 (-3.73) | 0.2% | 469 | -0.194 |
| breakout | fixed | SPY>200d & stock>200d | 1876 | 16 | +0.004 | -1.18 | -0.69 | -0.271 (-2.60) | 0.1% | 393 | -0.196 |
| breakout | fixed | SPY>200d & stock>200d & RS>=0.8 | 762 | 18 | +0.287 | -1.12 | 1.22 | +0.053 (0.24) | 0.1% | 163 | +0.023 |
| breakout | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 714 | 18 | +0.315 | -1.12 | 1.30 | +0.095 (0.44) | 0.1% | 158 | +0.142 |
| breakout | fixed | score>=70 & SPY>200d & stock>200d | 159 | 21 | +0.183 | -1.02 | 0.96 | -0.056 (-0.20) | 0.0% | 27 | +0.414 |
| breakout | fixed | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 104 | 21 | +0.222 | -1.01 | 1.08 | -0.030 (-0.09) | 0.0% | 15 | +0.442 |
| momentum | fixed | all | 2197 | 22 | +0.182 | -1.09 | 1.01 | -0.282 (-2.99) | 0.1% | 471 | +0.052 |
| momentum | fixed | SPY>200d & stock>200d | 1962 | 23 | +0.219 | -1.10 | 0.80 | -0.096 (-1.08) | 0.1% | 435 | +0.112 |
| momentum | fixed | SPY>200d & stock>200d & RS>=0.8 | 839 | 23 | +0.222 | -1.07 | 0.11 | -0.228 (-2.05) | 0.0% | 184 | +0.132 |
| momentum | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 796 | 22 | +0.209 | -1.07 | -0.02 | -0.220 (-1.94) | 0.0% | 178 | +0.177 |
| momentum | fixed | score>=70 & SPY>200d & stock>200d | 17 | 18 | -0.036 | -1.06 | 0.18 | -0.172 (-0.25) | 0.0% | 5 | -1.131 |
| momentum | fixed | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 9 | 22 | +0.681 | -0.91 | 0.62 | -0.212 (-0.20) | 0.0% | 3 | -1.108 |
| combined | fixed | all | 3107 | 20 | +0.128 | -1.12 | 0.08 | -0.368 (-3.80) | 0.2% | 639 | -0.064 |
| combined | fixed | SPY>200d & stock>200d | 2654 | 20 | +0.098 | -1.13 | -0.25 | -0.196 (-2.35) | 0.1% | 552 | -0.028 |
| combined | fixed | SPY>200d & stock>200d & RS>=0.8 | 1131 | 21 | +0.221 | -1.08 | 0.25 | -0.168 (-1.50) | 0.0% | 235 | -0.005 |
| combined | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1071 | 20 | +0.218 | -1.09 | 0.33 | -0.134 (-1.23) | 0.0% | 228 | +0.090 |
| combined | fixed | score>=70 & SPY>200d & stock>200d | 172 | 22 | +0.202 | -1.02 | 1.06 | -0.055 (-0.21) | 0.0% | 32 | +0.172 |
| combined | fixed | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 111 | 22 | +0.298 | -1.00 | 1.34 | +0.036 (0.11) | 0.0% | 18 | +0.183 |
| baseline_random | fixed | all | 7336 | 26 | +0.321 | -1.05 | 4.34 | — (—) | 0.7% | 1469 | +0.339 |
| baseline_random | fixed | SPY>200d & stock>200d | 4807 | 23 | +0.261 | -1.08 | 2.39 | — (—) | 0.3% | 994 | +0.225 |
| baseline_random | fixed | SPY>200d & stock>200d & RS>=0.8 | 1939 | 24 | +0.293 | -1.06 | 2.19 | — (—) | 0.4% | 432 | +0.147 |
| baseline_random | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1725 | 23 | +0.289 | -1.07 | 1.99 | — (—) | 0.2% | 372 | +0.224 |
| breakout | wide | all | 1951 | 33 | +0.186 | -0.99 | 1.40 | -0.251 (-3.36) | 0.3% | 392 | +0.167 |
| breakout | wide | SPY>200d & stock>200d | 1603 | 33 | +0.206 | -1.00 | 1.43 | -0.053 (-0.77) | 0.2% | 330 | +0.215 |
| breakout | wide | SPY>200d & stock>200d & RS>=0.8 | 676 | 33 | +0.265 | -0.97 | 1.16 | -0.126 (-1.47) | 0.0% | 140 | +0.129 |
| breakout | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 638 | 33 | +0.271 | -0.96 | 1.29 | -0.078 (-0.90) | 0.0% | 135 | +0.179 |
| breakout | wide | score>=70 & SPY>200d & stock>200d | 159 | 33 | +0.183 | -0.92 | 0.73 | -0.093 (-0.49) | 0.0% | 27 | +0.459 |
| breakout | wide | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 104 | 33 | +0.321 | -0.92 | 1.31 | -0.056 (-0.24) | 0.0% | 15 | +0.599 |
| momentum | wide | all | 1869 | 33 | +0.193 | -1.02 | 1.81 | -0.214 (-2.89) | 0.1% | 392 | +0.143 |
| momentum | wide | SPY>200d & stock>200d | 1668 | 33 | +0.239 | -1.02 | 1.97 | -0.002 (-0.03) | 0.1% | 364 | +0.184 |
| momentum | wide | SPY>200d & stock>200d & RS>=0.8 | 723 | 34 | +0.253 | -0.99 | 1.20 | -0.125 (-1.62) | 0.0% | 161 | +0.044 |
| momentum | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 686 | 34 | +0.261 | -0.99 | 1.42 | -0.070 (-0.86) | 0.0% | 157 | +0.078 |
| momentum | wide | score>=70 & SPY>200d & stock>200d | 16 | 25 | -0.023 | -0.93 | 0.27 | -0.037 (-0.08) | 0.0% | 5 | -0.738 |
| momentum | wide | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 8 | 38 | +0.703 | -0.50 | 0.90 | -0.049 (-0.08) | 0.0% | 3 | -0.735 |
| combined | wide | all | 2465 | 33 | +0.185 | -1.01 | 1.61 | -0.238 (-3.44) | 0.3% | 497 | +0.169 |
| combined | wide | SPY>200d & stock>200d | 2116 | 33 | +0.202 | -1.02 | 1.63 | -0.041 (-0.71) | 0.1% | 438 | +0.208 |
| combined | wide | SPY>200d & stock>200d & RS>=0.8 | 922 | 34 | +0.270 | -0.99 | 1.45 | -0.092 (-1.39) | 0.0% | 192 | +0.072 |
| combined | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 875 | 34 | +0.275 | -0.99 | 1.55 | -0.043 (-0.66) | 0.0% | 187 | +0.112 |
| combined | wide | score>=70 & SPY>200d & stock>200d | 171 | 32 | +0.184 | -0.92 | 0.91 | -0.078 (-0.43) | 0.0% | 32 | +0.272 |
| combined | wide | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 110 | 33 | +0.357 | -0.91 | 1.47 | -0.035 (-0.15) | 0.0% | 18 | +0.377 |
| baseline_random | wide | all | 5208 | 37 | +0.315 | -0.94 | 5.13 | — (—) | 0.8% | 987 | +0.381 |
| baseline_random | wide | SPY>200d & stock>200d | 3506 | 35 | +0.268 | -0.99 | 2.93 | — (—) | 0.2% | 723 | +0.274 |
| baseline_random | wide | SPY>200d & stock>200d & RS>=0.8 | 1487 | 35 | +0.300 | -0.98 | 2.73 | — (—) | 0.4% | 320 | +0.195 |
| baseline_random | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1336 | 35 | +0.302 | -0.99 | 2.56 | — (—) | 0.3% | 278 | +0.251 |

## Momentum rotation — universe: all (from 2018-02-23, 20 bps per side)

| benchmark | CAGR | max DD | Sharpe | train+val Sharpe | OOS CAGR | OOS Sharpe |
|---|---|---|---|---|---|---|
| SPY buy-and-hold | +14.0% | -34% | 0.79 | 0.76 | +16.5% | 0.98 |
| equal-weight universe (no costs) | +25.4% | -42% | 0.99 | 1.00 | +24.1% | 0.99 |

| rule set | trades/yr | exposure | win% | avg trade | avg days | CAGR | max DD | Sharpe | train+val Sharpe | OOS CAGR | OOS Sharpe | vs random | CAGR @40 / @70 bps | without best stock |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| top5, in RS>=0.8, out RS<0.5 | 10 | 93% | 37 | +18.3% | 110 | +14.8% | -79% | 0.53 | 0.41 | +43.7% | 0.85 | 10% | +14.0% / +12.8% | SE: +21.1%, Sharpe 0.62 |
| top5, in RS>=0.8, out RS<0.5, stop -20% | 15 | 91% | 31 | +17.5% | 73 | +21.0% | -77% | 0.61 | 0.64 | +13.3% | 0.53 | 40% | +19.7% / +17.8% | SE: +24.4%, Sharpe 0.66 |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d | 21 | 81% | 37 | +5.7% | 48 | +8.4% | -74% | 0.42 | 0.59 | -23.6% | -0.13 | 5% | +6.8% / +4.3% | MARA: +4.9%, Sharpe 0.34 |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | 26 | 80% | 34 | +4.0% | 39 | +8.5% | -71% | 0.41 | 0.54 | -14.5% | 0.04 | 10% | +6.6% / +3.7% | CELH: +14.2%, Sharpe 0.51 |
| top5, in RS>=0.8, out RS<0.7 | 12 | 93% | 44 | +12.6% | 93 | +15.6% | -76% | 0.54 | 0.49 | +31.3% | 0.74 | 30% | +14.5% / +13.0% | ENPH: +15.5%, Sharpe 0.54 |
| top5, in RS>=0.8, out RS<0.7, stop -20% | 18 | 92% | 35 | +10.6% | 64 | +19.7% | -77% | 0.60 | 0.49 | +51.7% | 0.94 | 15% | +18.3% / +16.1% | VKTX: +12.4%, Sharpe 0.49 |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d | 22 | 80% | 38 | +3.5% | 45 | +5.6% | -77% | 0.37 | 0.46 | -10.0% | 0.16 | 5% | +3.8% / +1.2% | TSLA: +11.2%, Sharpe 0.47 |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | 27 | 80% | 34 | +3.8% | 37 | +8.4% | -68% | 0.41 | 0.49 | -4.4% | 0.24 | 30% | +6.4% / +3.3% | CELH: +4.3%, Sharpe 0.34 |
| top8, in RS>=0.8, out RS<0.5 | 17 | 92% | 41 | +22.0% | 107 | +28.5% | -70% | 0.74 | 0.80 | +22.4% | 0.64 | 55% | +27.5% / +26.1% | SE: +26.3%, Sharpe 0.70 |
| top8, in RS>=0.8, out RS<0.5, stop -20% | 24 | 92% | 34 | +14.8% | 73 | +25.5% | -62% | 0.69 | 0.76 | +14.8% | 0.55 | 70% | +24.2% / +22.2% | SE: +20.3%, Sharpe 0.61 |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d | 30 | 80% | 38 | +9.2% | 53 | +25.0% | -58% | 0.70 | 0.77 | +15.1% | 0.54 | 90% | +23.3% / +20.8% | APP: +18.3%, Sharpe 0.59 |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | 37 | 80% | 35 | +7.2% | 43 | +22.2% | -67% | 0.65 | 0.71 | +15.7% | 0.54 | 55% | +20.4% / +17.6% | NIO: +23.5%, Sharpe 0.67 |
| top8, in RS>=0.8, out RS<0.7 | 19 | 92% | 47 | +18.7% | 94 | +31.9% | -57% | 0.77 | 0.79 | +31.6% | 0.75 | 60% | +30.8% / +29.1% | MARA: +23.7%, Sharpe 0.67 |
| top8, in RS>=0.8, out RS<0.7, stop -20% | 28 | 91% | 33 | +16.0% | 64 | +25.1% | -71% | 0.67 | 0.66 | +32.8% | 0.76 | 65% | +23.7% / +21.5% | MARA: +18.9%, Sharpe 0.59 |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d | 33 | 80% | 40 | +7.6% | 49 | +18.1% | -54% | 0.58 | 0.65 | +7.0% | 0.41 | 35% | +16.3% / +13.7% | MARA: +15.9%, Sharpe 0.55 |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | 41 | 80% | 33 | +9.7% | 39 | +24.4% | -63% | 0.67 | 0.73 | +10.0% | 0.46 | 75% | +22.1% / +18.8% | MARA: +21.7%, Sharpe 0.63 |
| top8, in RS>=0.8, out RS<0.5, 12-1 month momentum | 19 | 92% | 32 | +19.0% | 97 | +20.9% | -63% | 0.63 | 0.65 | +22.2% | 0.63 | 40% | +19.9% / +18.5% | SE: +16.8%, Sharpe 0.56 |
| top8, in RS>=0.8, out RS<0.5, monthly | 12 | 94% | 42 | +48.8% | 152 | +32.9% | -64% | 0.80 | 0.79 | +44.6% | 0.89 | 70% | +32.2% / +31.2% | ENPH: +32.4%, Sharpe 0.80 |
| top8, in RS>=0.8, out RS<0.5, volatility-adjusted | 15 | 93% | 49 | +26.1% | 125 | +31.1% | -47% | 0.86 | 0.92 | +34.5% | 0.80 | 100% | +30.2% / +28.9% | RKLB: +25.8%, Sharpe 0.76 |
| top8, in RS>=0.8, out RS<0.5, max 2/sector | 16 | 93% | 41 | +26.3% | 109 | +39.0% | -56% | 0.90 | 0.97 | +29.1% | 0.72 | 100% | +38.0% / +36.9% | SE: +36.0%, Sharpe 0.82 |
| top8, in RS>=0.8, out RS<0.5, max 3/sector | 16 | 94% | 42 | +25.4% | 109 | +32.1% | -58% | 0.79 | 0.85 | +25.9% | 0.68 | 80% | +31.2% / +29.8% | SE: +27.7%, Sharpe 0.72 |
| top8, in RS>=0.8, out RS<0.5, sell below 50d | 61 | 87% | 36 | +9.9% | 28 | +44.7% | -60% | 0.95 | 1.14 | +3.3% | 0.34 | 95% | +40.7% / +35.0% | MARA: +34.0%, Sharpe 0.83 |
| top8, in RS>=0.8, out RS<0.5, sell below 50d after +30% over 200d | 58 | 88% | 38 | +10.4% | 30 | +30.6% | -59% | 0.79 | 0.94 | +4.3% | 0.36 | 70% | +27.0% / +21.9% | MARA: +31.9%, Sharpe 0.81 |

## Momentum rotation — universe: largecap_2015 (from 2018-02-23, 20 bps per side)

| benchmark | CAGR | max DD | Sharpe | train+val Sharpe | OOS CAGR | OOS Sharpe |
|---|---|---|---|---|---|---|
| SPY buy-and-hold | +14.0% | -34% | 0.79 | 0.76 | +16.5% | 0.98 |
| equal-weight universe (no costs) | +14.5% | -37% | 0.83 | 0.73 | +20.7% | 1.43 |

| rule set | trades/yr | exposure | win% | avg trade | avg days | CAGR | max DD | Sharpe | train+val Sharpe | OOS CAGR | OOS Sharpe | vs random | CAGR @40 / @70 bps | without best stock |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| top5, in RS>=0.8, out RS<0.5 | 10 | 95% | 48 | +8.7% | 115 | +14.7% | -36% | 0.66 | 0.57 | +29.2% | 1.00 | 95% | +13.8% / +12.5% | DVN: +12.3%, Sharpe 0.59 |
| top5, in RS>=0.8, out RS<0.5, stop -20% | 10 | 94% | 52 | +8.7% | 112 | +15.2% | -36% | 0.68 | 0.60 | +28.9% | 0.99 | 100% | +14.3% / +13.0% | DVN: +12.8%, Sharpe 0.61 |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d | 20 | 81% | 48 | +3.1% | 50 | +10.8% | -26% | 0.57 | 0.62 | +10.4% | 0.50 | 85% | +9.1% / +6.5% | AVGO: +11.0%, Sharpe 0.60 |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | 20 | 81% | 48 | +3.1% | 50 | +10.8% | -26% | 0.57 | 0.62 | +10.4% | 0.51 | 75% | +9.1% / +6.6% | AVGO: +11.0%, Sharpe 0.60 |
| top5, in RS>=0.8, out RS<0.7 | 14 | 94% | 47 | +4.8% | 84 | +11.4% | -36% | 0.54 | 0.54 | +15.3% | 0.61 | 100% | +10.3% / +8.6% | INTC: +9.8%, Sharpe 0.51 |
| top5, in RS>=0.8, out RS<0.7, stop -20% | 14 | 95% | 47 | +5.3% | 82 | +13.5% | -33% | 0.61 | 0.63 | +14.9% | 0.60 | 100% | +12.3% / +10.5% | INTC: +12.2%, Sharpe 0.59 |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d | 23 | 81% | 46 | +2.4% | 44 | +9.1% | -30% | 0.50 | 0.61 | +3.6% | 0.27 | 100% | +7.1% / +4.3% | AVGO: +7.9%, Sharpe 0.46 |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | 23 | 81% | 46 | +2.4% | 44 | +9.0% | -30% | 0.50 | 0.60 | +3.4% | 0.26 | 100% | +7.0% / +4.2% | AVGO: +7.9%, Sharpe 0.46 |
| top8, in RS>=0.8, out RS<0.5 | 17 | 94% | 46 | +7.9% | 110 | +14.6% | -29% | 0.71 | 0.65 | +23.3% | 0.98 | 100% | +13.7% / +12.3% | DVN: +12.5%, Sharpe 0.65 |
| top8, in RS>=0.8, out RS<0.5, stop -20% | 18 | 94% | 46 | +6.7% | 105 | +13.3% | -29% | 0.67 | 0.60 | +22.0% | 0.95 | 100% | +12.4% / +11.1% | DVN: +11.1%, Sharpe 0.59 |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d | 31 | 80% | 45 | +2.5% | 52 | +8.2% | -27% | 0.51 | 0.52 | +9.6% | 0.55 | 80% | +6.6% / +4.2% | DVN: +7.7%, Sharpe 0.49 |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | 31 | 80% | 44 | +2.5% | 51 | +8.2% | -27% | 0.51 | 0.52 | +9.5% | 0.55 | 85% | +6.6% / +4.2% | DVN: +7.7%, Sharpe 0.49 |
| top8, in RS>=0.8, out RS<0.7 | 23 | 93% | 48 | +4.4% | 82 | +12.1% | -26% | 0.63 | 0.61 | +15.9% | 0.75 | 100% | +10.9% / +9.2% | META: +9.2%, Sharpe 0.51 |
| top8, in RS>=0.8, out RS<0.7, stop -20% | 23 | 93% | 47 | +4.4% | 80 | +11.8% | -29% | 0.62 | 0.60 | +15.3% | 0.73 | 100% | +10.6% / +8.8% | AVGO: +9.5%, Sharpe 0.52 |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d | 35 | 80% | 47 | +1.9% | 45 | +8.0% | -29% | 0.50 | 0.53 | +7.6% | 0.46 | 90% | +6.1% / +3.4% | AVGO: +7.3%, Sharpe 0.48 |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | 36 | 80% | 47 | +1.9% | 45 | +7.9% | -29% | 0.50 | 0.53 | +7.4% | 0.45 | 95% | +6.0% / +3.3% | AVGO: +7.4%, Sharpe 0.48 |
| top8, in RS>=0.8, out RS<0.5, 12-1 month momentum | 19 | 90% | 33 | +3.1% | 93 | +4.9% | -40% | 0.33 | 0.39 | +1.5% | 0.18 | 10% | +4.0% / +2.7% | GE: +3.4%, Sharpe 0.26 |
| top8, in RS>=0.8, out RS<0.5, monthly | 13 | 94% | 50 | +9.8% | 144 | +12.5% | -27% | 0.62 | 0.64 | +13.2% | 0.62 | 100% | +13.3% / +12.3% | DVN: +12.3%, Sharpe 0.61 |
| top8, in RS>=0.8, out RS<0.5, volatility-adjusted | 16 | 93% | 55 | +6.6% | 114 | +12.6% | -23% | 0.73 | 0.68 | +16.6% | 1.03 | 100% | +11.8% / +10.5% | GE: +9.8%, Sharpe 0.60 |
| top8, in RS>=0.8, out RS<0.5, max 2/sector | 18 | 93% | 44 | +6.3% | 106 | +11.3% | -30% | 0.59 | 0.52 | +21.0% | 0.89 | 95% | +10.4% / +9.0% | DVN: +9.5%, Sharpe 0.53 |
| top8, in RS>=0.8, out RS<0.5, max 3/sector | 18 | 94% | 44 | +7.0% | 107 | +13.2% | -28% | 0.66 | 0.60 | +22.4% | 0.94 | 90% | +12.3% / +10.9% | DVN: +11.4%, Sharpe 0.60 |
| top8, in RS>=0.8, out RS<0.5, sell below 50d | 63 | 87% | 36 | +0.8% | 28 | +5.8% | -25% | 0.40 | 0.53 | -1.9% | -0.00 | 45% | +2.7% / -1.8% | DVN: +4.4%, Sharpe 0.33 |
| top8, in RS>=0.8, out RS<0.5, sell below 50d after +30% over 200d | 33 | 90% | 44 | +2.4% | 54 | +9.0% | -26% | 0.55 | 0.60 | +5.9% | 0.41 | 75% | +7.2% / +4.6% | AVGO: +8.5%, Sharpe 0.53 |

## Rotation: pre-registered selection (2015 large caps, train+validation only)

Gates: train+val Sharpe > SPY's, ranking beats >= 90% of random selections, CAGR without the single best stock >= SPY's, max drawdown at most 10 points worse than SPY's.

**Chosen: none — no rule set passed every gate**

| rule set | passes | train+val Sharpe | failed gates |
|---|---|---|---|
| top5, in RS>=0.8, out RS<0.5 | ❌ | 0.57 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top5, in RS>=0.8, out RS<0.5, stop -20% | ❌ | 0.60 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d | ❌ | 0.62 | train_val_sharpe_beats_spy, ranking_beats_random, without_best_stock_beats_spy |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | ❌ | 0.62 | train_val_sharpe_beats_spy, ranking_beats_random, without_best_stock_beats_spy |
| top5, in RS>=0.8, out RS<0.7 | ❌ | 0.54 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top5, in RS>=0.8, out RS<0.7, stop -20% | ❌ | 0.63 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d | ❌ | 0.61 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | ❌ | 0.60 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5 | ❌ | 0.65 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5, stop -20% | ❌ | 0.60 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d | ❌ | 0.52 | train_val_sharpe_beats_spy, ranking_beats_random, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | ❌ | 0.52 | train_val_sharpe_beats_spy, ranking_beats_random, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.7 | ❌ | 0.61 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.7, stop -20% | ❌ | 0.60 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d | ❌ | 0.53 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | ❌ | 0.53 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5, 12-1 month momentum | ❌ | 0.39 | train_val_sharpe_beats_spy, ranking_beats_random, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5, monthly | ❌ | 0.64 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5, volatility-adjusted | ❌ | 0.68 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5, max 2/sector | ❌ | 0.52 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5, max 3/sector | ❌ | 0.60 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5, sell below 50d | ❌ | 0.53 | train_val_sharpe_beats_spy, ranking_beats_random, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5, sell below 50d after +30% over 200d | ❌ | 0.60 | train_val_sharpe_beats_spy, ranking_beats_random, without_best_stock_beats_spy |

Calendar-year returns (2015 large caps, 20 bps per side):

| | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|---|---|---|---|
| SPY | -7% | +31% | +18% | +29% | -18% | +26% | +25% | +18% | +12% |
| equal-weight group | -7% | +29% | +14% | +31% | -4% | +16% | +16% | +17% | +20% |
| top5, in RS>=0.8, out RS<0.5 | -4% | +7% | +13% | +21% | +0% | +11% | +37% | +15% | +36% |
| top5, in RS>=0.8, out RS<0.5, stop -20% | -4% | +8% | +14% | +22% | -0% | +14% | +36% | +14% | +36% |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d | +2% | +3% | +16% | +21% | -1% | +21% | +19% | +9% | +7% |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | +2% | +3% | +16% | +22% | -1% | +21% | +19% | +9% | +7% |
| top5, in RS>=0.8, out RS<0.7 | -6% | +8% | +7% | +21% | -4% | +19% | +30% | -2% | +33% |
| top5, in RS>=0.8, out RS<0.7, stop -20% | -6% | +7% | +9% | +22% | +10% | +21% | +30% | -2% | +33% |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d | -0% | -3% | +8% | +21% | -2% | +22% | +29% | -5% | +13% |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | -0% | -3% | +8% | +21% | -2% | +22% | +29% | -5% | +13% |
| top8, in RS>=0.8, out RS<0.5 | -12% | +8% | +17% | +28% | +0% | +23% | +27% | +22% | +20% |
| top8, in RS>=0.8, out RS<0.5, stop -20% | -12% | +8% | +11% | +33% | +1% | +20% | +22% | +23% | +17% |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d | -2% | -5% | +11% | +30% | -2% | +14% | +13% | +14% | +3% |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | -2% | -4% | +11% | +30% | -2% | +14% | +13% | +14% | +2% |
| top8, in RS>=0.8, out RS<0.7 | -9% | +9% | +17% | +18% | +2% | +20% | +25% | +6% | +23% |
| top8, in RS>=0.8, out RS<0.7, stop -20% | -9% | +6% | +13% | +18% | +6% | +21% | +25% | +5% | +23% |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d | -2% | +2% | +12% | +18% | -4% | +9% | +24% | +2% | +12% |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | -2% | +2% | +12% | +18% | -4% | +9% | +24% | +1% | +12% |
| top8, in RS>=0.8, out RS<0.5, 12-1 month momentum | -15% | +10% | +2% | +24% | -12% | +2% | +41% | -1% | +2% |
| top8, in RS>=0.8, out RS<0.5, monthly | -0% | +12% | +16% | +19% | -5% | +26% | +23% | +5% | +17% |
| top8, in RS>=0.8, out RS<0.5, volatility-adjusted | -2% | +16% | +3% | +22% | -8% | +18% | +38% | +20% | +10% |
| top8, in RS>=0.8, out RS<0.5, max 2/sector | -10% | +8% | +4% | +29% | -0% | +19% | +17% | +10% | +27% |
| top8, in RS>=0.8, out RS<0.5, max 3/sector | -11% | +8% | +10% | +29% | -1% | +24% | +22% | +18% | +22% |
| top8, in RS>=0.8, out RS<0.5, sell below 50d | -7% | +3% | +28% | +21% | +6% | +7% | +4% | +2% | -7% |
| top8, in RS>=0.8, out RS<0.5, sell below 50d after +30% over 200d | -10% | +10% | +26% | +13% | +6% | +22% | +7% | +6% | +2% |

## Rockets (from 2016-12-06, 20 bps per side, 10 slots x 10%, max 3 new per day)

Rocket day: close >= +jump vs previous close, volume >= 3x the 20-day average, close in the top quarter of the day's range, price >= $5, 20-day dollar volume >= $5M. Buy next open; sell next open after a close more than `trail` below the highest close, or after 40 sessions. 'Random' = same stocks, same liquidity filter, same exit, random dates.

SPY: +15.0%/yr, max DD -34%, Sharpe 0.86 · train+val +14.8%/yr, Sharpe 0.85

| variant | trades | win% | avg trade | median | ≥+50% | worst | random avg | excess vs random t (train+val) | 2015 large caps excess | CAGR | max DD | Sharpe | train+val CAGR / Sharpe | OOS CAGR | random-entry portfolio CAGR | without top 3 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| EPS surprise>0%, reaction>=5% | 1916 | 53 | +4.5% | +1.9% | 4.3% | -51% | +4.2% | -0.33% (-0.50) | -0.04% (n=564) | +7.3% | -40% | 0.44 | +9.9% / 0.56 | -3.7% | +13.1% | +7.3% |
| EPS surprise>0%, reaction>=10% | 933 | 53 | +6.0% | +1.5% | 6.2% | -51% | +4.2% | +0.82% (0.81) | +1.54% (n=130) | +22.9% | -43% | 0.96 | +23.9% / 1.00 | +13.6% | +13.1% | +21.9% |
| EPS surprise>10%, reaction>=5% | 1273 | 53 | +4.9% | +2.0% | 5.0% | -51% | +4.2% | +0.62% (0.75) | -0.40% (n=270) | +13.6% | -45% | 0.66 | +22.0% / 0.97 | -16.1% | +13.1% | +15.3% |
| EPS surprise>10%, reaction>=10% | 719 | 52 | +6.3% | +1.5% | 6.3% | -51% | +4.2% | +1.73% (1.41) | +1.90% (n=72) | +17.5% | -48% | 0.76 | +25.4% / 1.01 | -14.3% | +13.1% | +14.3% |
| EPS surprise>20%, reaction>=10%, volume>=2x, RS>=0.8 | 245 | 55 | +8.3% | +2.7% | 6.9% | -36% | +4.2% | +3.52% (1.63) | +3.91% (n=14) | +17.5% | -27% | 0.90 | +23.6% / 1.19 | -9.7% | +13.1% | +11.5% |
| EPS surprise>20%, reaction>=15%, volume>=2x, RS>=0.8 | 175 | 55 | +8.3% | +2.6% | 8.0% | -36% | +4.2% | +1.81% (0.76) | —% (n=4) | +14.4% | -24% | 0.86 | +18.7% / 1.14 | -6.2% | +13.1% | +9.2% |
| EPS surprise>20%, reaction>=10%, volume>=2x, RS>=0.8, trail 10% | 246 | 43 | +3.8% | -3.3% | 3.7% | -21% | +4.2% | -1.84% (-1.11) | +1.76% (n=14) | +8.9% | -16% | 0.77 | +11.9% / 0.99 | -3.5% | +13.1% | +5.1% |
| EPS surprise>20%, reaction>=10%, volume>=2x, RS>=0.8, trail 15% | 245 | 51 | +7.2% | +0.1% | 4.9% | -29% | +4.2% | +2.98% (1.54) | +2.93% (n=14) | +16.8% | -19% | 1.03 | +21.3% / 1.27 | -0.5% | +13.1% | +12.2% |
| EPS surprise>20%, reaction>=10%, volume>=2x, RS>=0.8, take-profit +30% | 245 | 58 | +6.0% | +5.0% | 0.4% | -36% | +4.2% | +2.62% (1.46) | +4.33% (n=14) | +12.1% | -25% | 0.77 | +18.4% / 1.14 | -11.3% | +13.1% | +9.9% |
| EPS surprise>20%, reaction>=10%, volume>=2x, RS>=0.8, take-profit +50% | 245 | 55 | +6.4% | +2.7% | 10.2% | -36% | +4.2% | +2.29% (1.18) | +5.69% (n=14) | +12.9% | -26% | 0.76 | +18.2% / 1.04 | -10.3% | +13.1% | +9.5% |
| EPS surprise>20%, reaction>=10%, volume>=2x, RS>=0.8, trail 15%, take-profit +30% | 245 | 51 | +5.4% | +0.1% | 0.4% | -29% | +4.2% | +2.04% (1.20) | +3.25% (n=14) | +12.4% | -17% | 0.94 | +17.0% / 1.24 | -4.6% | +13.1% | +9.8% |
| jump>=8%, trail 15% | 999 | 45 | +4.0% | -2.6% | 5.3% | -52% | +2.2% | -0.19% (-0.19) | -1.30% (n=114) | +15.2% | -48% | 0.62 | +23.4% / 0.83 | -12.9% | +20.4% | +9.5% |
| jump>=8%, trail 25% | 997 | 51 | +5.4% | +0.7% | 6.8% | -61% | +2.9% | +0.35% (0.30) | -1.22% (n=114) | +15.0% | -68% | 0.59 | +21.4% / 0.76 | -8.6% | +3.8% | +11.0% |
| jump>=15%, trail 15% | 544 | 43 | +4.7% | -4.5% | 6.8% | -52% | +2.2% | -0.69% (-0.48) | -4.26% (n=24) | +18.1% | -38% | 0.70 | +21.7% / 0.79 | +5.6% | +20.4% | +11.8% |
| jump>=15%, trail 25% | 544 | 47 | +6.6% | -2.2% | 9.2% | -61% | +2.9% | +0.67% (0.37) | -4.50% (n=24) | +14.5% | -60% | 0.57 | +20.4% / 0.71 | -6.4% | +3.8% | +6.1% |

Pre-registered gates: excess vs random entries t >= 2 (train+val); portfolio beats SPY on train+val CAGR and Sharpe; positive excess among 2015 large caps; CAGR without the 3 best stocks >= SPY's; max drawdown >= -50%.

**Chosen: none — no rocket variant passed every gate**

| variant | passes | failed gates |
|---|---|---|
| EPS surprise>0%, reaction>=5% | ❌ | beats_random_entries_same_stocks, beats_spy_train_val, holds_in_2015_largecaps, without_top3_beats_spy |
| EPS surprise>0%, reaction>=10% | ❌ | beats_random_entries_same_stocks |
| EPS surprise>10%, reaction>=5% | ❌ | beats_random_entries_same_stocks, holds_in_2015_largecaps |
| EPS surprise>10%, reaction>=10% | ❌ | beats_random_entries_same_stocks, without_top3_beats_spy |
| EPS surprise>20%, reaction>=10%, volume>=2x, RS>=0.8 | ❌ | beats_random_entries_same_stocks, without_top3_beats_spy |
| EPS surprise>20%, reaction>=15%, volume>=2x, RS>=0.8 | ❌ | beats_random_entries_same_stocks, holds_in_2015_largecaps, without_top3_beats_spy |
| EPS surprise>20%, reaction>=10%, volume>=2x, RS>=0.8, trail 10% | ❌ | beats_random_entries_same_stocks, beats_spy_train_val, without_top3_beats_spy |
| EPS surprise>20%, reaction>=10%, volume>=2x, RS>=0.8, trail 15% | ❌ | beats_random_entries_same_stocks, without_top3_beats_spy |
| EPS surprise>20%, reaction>=10%, volume>=2x, RS>=0.8, take-profit +30% | ❌ | beats_random_entries_same_stocks, without_top3_beats_spy |
| EPS surprise>20%, reaction>=10%, volume>=2x, RS>=0.8, take-profit +50% | ❌ | beats_random_entries_same_stocks, without_top3_beats_spy |
| EPS surprise>20%, reaction>=10%, volume>=2x, RS>=0.8, trail 15%, take-profit +30% | ❌ | beats_random_entries_same_stocks, without_top3_beats_spy |
| jump>=8%, trail 15% | ❌ | beats_random_entries_same_stocks, beats_spy_train_val, holds_in_2015_largecaps, without_top3_beats_spy |
| jump>=8%, trail 25% | ❌ | beats_random_entries_same_stocks, beats_spy_train_val, holds_in_2015_largecaps, without_top3_beats_spy, drawdown_tolerable |
| jump>=15%, trail 15% | ❌ | beats_random_entries_same_stocks, beats_spy_train_val, holds_in_2015_largecaps, without_top3_beats_spy |
| jump>=15%, trail 25% | ❌ | beats_random_entries_same_stocks, beats_spy_train_val, holds_in_2015_largecaps, without_top3_beats_spy, drawdown_tolerable |

## Mean R by year (all universe, fixed exit)

| group | policy | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| combined | all | +0.84 | -0.44 | +0.30 | +1.11 | +0.03 | -0.44 | +0.53 | +0.42 | +0.23 | -0.06 |
| combined | SPY>200d & stock>200d | +0.93 | -0.43 | +0.03 | +0.94 | -0.03 | -0.79 | +0.38 | +0.42 | +0.19 | -0.05 |
| combined | SPY>200d & stock>200d & RS>=0.8 | +1.04 | -0.26 | +0.35 | +1.46 | -0.41 | -0.36 | +0.35 | +0.60 | +0.83 | +0.05 |
| combined | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | +1.10 | -0.12 | +0.45 | +1.36 | -0.52 | -0.07 | +0.30 | +0.46 | +0.81 | +0.27 |
| combined | score>=70 & SPY>200d & stock>200d | +0.62 | +0.65 | +0.42 | +1.14 | -0.54 | -0.96 | +0.43 | +0.69 | +0.52 | -0.07 |
| combined | score>=70 & SPY>200d & stock>200d & RS>=0.8 | +0.21 | +1.33 | +0.61 | +1.08 | -0.53 | -1.15 | +0.41 | +1.00 | +0.70 | -0.07 |
| baseline_random | all | +1.45 | +0.04 | +0.55 | +0.98 | +0.15 | -0.28 | +0.61 | +0.42 | +0.30 | +0.17 |
| baseline_random | SPY>200d & stock>200d | +1.56 | -0.26 | +0.52 | +0.86 | +0.16 | -0.78 | +0.27 | +0.42 | +0.21 | +0.12 |
| baseline_random | SPY>200d & stock>200d & RS>=0.8 | +1.15 | +0.12 | +0.65 | +1.17 | -0.25 | -0.74 | +0.47 | +0.51 | +0.41 | -0.01 |
| baseline_random | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | +1.05 | +0.28 | +0.73 | +0.94 | -0.29 | -0.63 | +0.55 | +0.60 | +0.65 | -0.06 |