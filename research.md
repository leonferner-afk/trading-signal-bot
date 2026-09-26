# Strategy research

267 symbols with data (1 failed), 10 years of daily bars. Control group: 93 stocks that were already large caps in 2015. Primary cost 40 bps per side (Swedish retail: courtage + FX + slippage). Validation from 2023-01-21, out-of-sample (OOS) from 2024-11-22. Setups invalidated at the next open (skipped): 1286.

Portfolio: max 8 positions, max 3 new per day, 1% risk per trade, max 25% of equity per position, no leverage, marked to market daily. 'vs random' = share of 40 random-order portfolios from the same eligible trades that this ranking beat.

## Portfolio — universe: all

SPY buy-and-hold: +15.0%/yr, max DD -34%, Sharpe 0.85 · train+val Sharpe 0.81 · OOS +16.7%/yr, Sharpe 1.0

| rule set | trades/yr | exposure | win% | avgR | CAGR | max DD | Sharpe | train+val Sharpe | OOS CAGR | OOS Sharpe | vs random |
|---|---|---|---|---|---|---|---|---|---|---|---|
| random picks (reference) | 79.0 | 87% | 21 | +0.10 | +2.0% | -64% | 0.22 | 0.29 | -12.2% | -0.24 | — |
| random picks, trend filter | 68.3 | 77% | 19 | +0.08 | -0.3% | -55% | 0.12 | 0.36 | -21.1% | -0.72 | — |
| RS leaders, trend filter | 72.4 | 67% | 23 | +0.36 | +20.1% | -39% | 0.72 | 0.81 | +0.8% | 0.23 | 100% |
| RS leaders near 52w high | 65.7 | 75% | 25 | +0.52 | +23.3% | -37% | 0.84 | 0.88 | +27.6% | 0.81 | 100% |
| signals score>=70, trend | 46.7 | 63% | 21 | +0.23 | +8.0% | -37% | 0.47 | 0.62 | -8.3% | -0.18 | 28% |
| signals score>=70, trend, RS top 20% | 40.9 | 51% | 23 | +0.49 | +16.8% | -39% | 0.81 | 0.90 | +11.3% | 0.54 | 82% |
| signals, trend, RS top 20% | 79.0 | 77% | 21 | +0.51 | +29.6% | -56% | 0.93 | 0.96 | +36.9% | 0.97 | 100% |
| signals, trend, RS top 20%, near 52w high | 77.2 | 78% | 21 | +0.36 | +17.2% | -50% | 0.68 | 0.74 | +17.4% | 0.62 | 95% |

Cost sensitivity (full-period CAGR / Sharpe):

| rule set | 15 bps | 40 bps | 70 bps |
|---|---|---|---|
| RS leaders, trend filter | +21.0% / 0.76 | +20.1% / 0.72 | +14.0% / 0.57 |
| RS leaders near 52w high | +28.6% / 0.98 | +23.3% / 0.84 | +16.6% / 0.66 |
| signals score>=70, trend | +11.7% / 0.63 | +8.0% / 0.47 | +4.2% / 0.30 |
| signals score>=70, trend, RS top 20% | +20.0% / 0.94 | +16.8% / 0.81 | +13.0% / 0.66 |
| signals, trend, RS top 20% | +36.7% / 1.09 | +29.6% / 0.93 | +21.3% / 0.73 |
| signals, trend, RS top 20%, near 52w high | +23.3% / 0.85 | +17.2% / 0.68 | +11.5% / 0.51 |

Exit variant (stop 2.5 x ATR instead of 1.5 x ATR / structural):

| rule set | CAGR | max DD | Sharpe | OOS Sharpe |
|---|---|---|---|---|
| random picks (reference) | +10.6% | -43% | 0.58 | -0.17 |
| random picks, trend filter | +16.7% | -39% | 0.87 | 0.47 |
| RS leaders, trend filter | +14.7% | -29% | 0.72 | 0.38 |
| RS leaders near 52w high | +24.5% | -26% | 1.07 | 0.60 |
| signals score>=70, trend | +8.7% | -31% | 0.58 | -0.23 |
| signals score>=70, trend, RS top 20% | +16.5% | -29% | 0.98 | 0.67 |
| signals, trend, RS top 20% | +11.6% | -43% | 0.60 | 0.54 |
| signals, trend, RS top 20%, near 52w high | +12.1% | -34% | 0.63 | 0.37 |

### Per trade — universe: all (one position per symbol, t over monthly means)

| group | exit | policy | n | win% | avgR | medR | t | excess vs random (t) | ≥+50% | OOS n | OOS avgR |
|---|---|---|---|---|---|---|---|---|---|---|---|
| breakout | fixed | all | 6292 | 17 | +0.124 | -1.23 | -0.20 | -0.404 (-4.52) | 3.2% | 1422 | -0.167 |
| breakout | fixed | SPY>200d & stock>200d | 5003 | 17 | +0.065 | -1.24 | -1.04 | -0.301 (-4.08) | 3.0% | 1144 | -0.158 |
| breakout | fixed | SPY>200d & stock>200d & RS>=0.8 | 2073 | 18 | +0.286 | -1.17 | 0.50 | -0.276 (-2.60) | 5.4% | 502 | +0.397 |
| breakout | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1690 | 18 | +0.302 | -1.18 | 0.51 | -0.176 (-1.46) | 4.4% | 385 | +0.537 |
| breakout | fixed | score>=70 & SPY>200d & stock>200d | 743 | 23 | +0.419 | -1.06 | 2.15 | +0.113 (0.75) | 5.8% | 155 | +0.150 |
| breakout | fixed | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 445 | 24 | +0.583 | -1.02 | 2.91 | +0.232 (1.06) | 7.6% | 101 | +0.348 |
| momentum | fixed | all | 5168 | 22 | +0.187 | -1.12 | 0.93 | -0.300 (-3.92) | 3.7% | 1163 | -0.070 |
| momentum | fixed | SPY>200d & stock>200d | 4564 | 22 | +0.223 | -1.13 | 1.07 | -0.085 (-1.33) | 3.5% | 1055 | -0.052 |
| momentum | fixed | SPY>200d & stock>200d & RS>=0.8 | 1849 | 23 | +0.321 | -1.08 | 1.79 | -0.120 (-1.52) | 6.3% | 441 | +0.179 |
| momentum | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1519 | 23 | +0.328 | -1.11 | 1.67 | -0.048 (-0.54) | 4.7% | 349 | +0.159 |
| momentum | fixed | score>=70 & SPY>200d & stock>200d | 153 | 24 | +0.526 | -0.95 | 1.99 | +0.393 (1.37) | 13.1% | 38 | +0.988 |
| momentum | fixed | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 93 | 24 | +0.582 | -0.93 | 1.36 | +0.020 (0.06) | 15.0% | 27 | +1.046 |
| combined | fixed | all | 7886 | 19 | +0.148 | -1.17 | 0.23 | -0.360 (-4.90) | 3.4% | 1757 | -0.002 |
| combined | fixed | SPY>200d & stock>200d | 6501 | 19 | +0.115 | -1.17 | -0.43 | -0.219 (-3.55) | 3.1% | 1475 | -0.015 |
| combined | fixed | SPY>200d & stock>200d & RS>=0.8 | 2720 | 20 | +0.285 | -1.13 | 0.99 | -0.218 (-2.75) | 5.5% | 654 | +0.438 |
| combined | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 2230 | 21 | +0.283 | -1.14 | 1.04 | -0.117 (-1.34) | 4.4% | 505 | +0.440 |
| combined | fixed | score>=70 & SPY>200d & stock>200d | 816 | 23 | +0.446 | -1.04 | 1.96 | +0.104 (0.76) | 6.5% | 176 | +0.239 |
| combined | fixed | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 487 | 24 | +0.569 | -1.01 | 2.56 | +0.161 (0.80) | 8.4% | 115 | +0.428 |
| baseline_random | fixed | all | 17001 | 24 | +0.272 | -1.08 | 4.03 | — (—) | 5.0% | 3905 | +0.131 |
| baseline_random | fixed | SPY>200d & stock>200d | 10850 | 23 | +0.236 | -1.12 | 2.09 | — (—) | 3.6% | 2513 | +0.073 |
| baseline_random | fixed | SPY>200d & stock>200d & RS>=0.8 | 4368 | 23 | +0.317 | -1.09 | 3.02 | — (—) | 6.3% | 1070 | +0.236 |
| baseline_random | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 2964 | 24 | +0.369 | -1.12 | 2.49 | — (—) | 4.2% | 649 | +0.265 |
| breakout | wide | all | 5049 | 33 | +0.253 | -0.99 | 2.56 | -0.174 (-3.10) | 5.6% | 1125 | +0.185 |
| breakout | wide | SPY>200d & stock>200d | 4068 | 33 | +0.260 | -1.01 | 1.73 | -0.075 (-1.54) | 5.1% | 917 | +0.204 |
| breakout | wide | SPY>200d & stock>200d & RS>=0.8 | 1733 | 35 | +0.410 | -0.96 | 2.49 | -0.102 (-1.63) | 9.2% | 413 | +0.405 |
| breakout | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1439 | 35 | +0.431 | -0.97 | 2.73 | -0.026 (-0.41) | 7.5% | 324 | +0.349 |
| breakout | wide | score>=70 & SPY>200d & stock>200d | 716 | 33 | +0.359 | -0.96 | 2.39 | +0.031 (0.29) | 8.9% | 148 | +0.148 |
| breakout | wide | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 423 | 35 | +0.494 | -0.92 | 3.03 | +0.077 (0.49) | 11.6% | 94 | +0.343 |
| momentum | wide | all | 4298 | 32 | +0.220 | -1.02 | 2.04 | -0.203 (-3.48) | 4.9% | 936 | +0.085 |
| momentum | wide | SPY>200d & stock>200d | 3817 | 32 | +0.258 | -1.02 | 2.13 | -0.037 (-0.72) | 4.7% | 855 | +0.104 |
| momentum | wide | SPY>200d & stock>200d & RS>=0.8 | 1555 | 33 | +0.327 | -1.00 | 2.09 | -0.138 (-2.39) | 8.0% | 364 | +0.232 |
| momentum | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1305 | 33 | +0.298 | -1.01 | 1.67 | -0.127 (-2.05) | 5.8% | 287 | +0.218 |
| momentum | wide | score>=70 & SPY>200d & stock>200d | 137 | 31 | +0.299 | -0.91 | 1.31 | +0.050 (0.26) | 15.3% | 32 | +0.732 |
| momentum | wide | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 79 | 30 | +0.363 | -0.86 | 0.98 | -0.178 (-0.73) | 20.2% | 22 | +0.890 |
| combined | wide | all | 5989 | 33 | +0.235 | -1.01 | 2.43 | -0.191 (-3.73) | 5.3% | 1321 | +0.150 |
| combined | wide | SPY>200d & stock>200d | 5007 | 33 | +0.253 | -1.02 | 1.69 | -0.073 (-1.71) | 5.0% | 1129 | +0.163 |
| combined | wide | SPY>200d & stock>200d & RS>=0.8 | 2172 | 33 | +0.340 | -0.99 | 2.07 | -0.141 (-2.78) | 8.4% | 522 | +0.328 |
| combined | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1810 | 34 | +0.337 | -0.99 | 2.17 | -0.076 (-1.43) | 6.7% | 405 | +0.279 |
| combined | wide | score>=70 & SPY>200d & stock>200d | 774 | 33 | +0.353 | -0.95 | 1.99 | -0.002 (-0.02) | 9.0% | 165 | +0.226 |
| combined | wide | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 453 | 34 | +0.470 | -0.91 | 2.59 | +0.011 (0.08) | 12.1% | 105 | +0.428 |
| baseline_random | wide | all | 11864 | 35 | +0.274 | -0.98 | 4.80 | — (—) | 6.4% | 2641 | +0.201 |
| baseline_random | wide | SPY>200d & stock>200d | 7803 | 34 | +0.265 | -1.01 | 2.88 | — (—) | 4.7% | 1798 | +0.123 |
| baseline_random | wide | SPY>200d & stock>200d & RS>=0.8 | 3246 | 34 | +0.338 | -1.00 | 3.69 | — (—) | 8.5% | 772 | +0.284 |
| baseline_random | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 2358 | 35 | +0.388 | -1.01 | 3.35 | — (—) | 6.0% | 500 | +0.346 |

## Portfolio — universe: largecap_2015

SPY buy-and-hold: +15.0%/yr, max DD -34%, Sharpe 0.85 · train+val Sharpe 0.81 · OOS +16.7%/yr, Sharpe 1.0

| rule set | trades/yr | exposure | win% | avgR | CAGR | max DD | Sharpe | train+val Sharpe | OOS CAGR | OOS Sharpe | vs random |
|---|---|---|---|---|---|---|---|---|---|---|---|
| random picks (reference) | 45.5 | 87% | 26 | +0.21 | +6.3% | -38% | 0.45 | 0.40 | +5.6% | 0.43 | — |
| random picks, trend filter | 36.6 | 77% | 24 | +0.16 | +4.4% | -18% | 0.38 | 0.54 | -6.2% | -0.33 | — |
| RS leaders, trend filter | 42.6 | 76% | 25 | +0.30 | +11.1% | -32% | 0.63 | 0.76 | +3.2% | 0.26 | 100% |
| RS leaders near 52w high | 40.5 | 76% | 24 | +0.15 | +4.8% | -31% | 0.34 | 0.52 | -5.3% | -0.16 | 78% |
| signals score>=70, trend | 15.2 | 37% | 24 | +0.17 | +1.4% | -21% | 0.20 | 0.21 | +3.4% | 0.40 | 20% |
| signals score>=70, trend, RS top 20% | 10.4 | 24% | 21 | +0.09 | +0.8% | -20% | 0.14 | 0.23 | +1.2% | 0.19 | 0% |
| signals, trend, RS top 20% | 43.2 | 76% | 22 | +0.28 | +5.8% | -39% | 0.43 | 0.56 | -0.7% | 0.06 | 95% |
| signals, trend, RS top 20%, near 52w high | 42.6 | 75% | 22 | +0.24 | +4.0% | -39% | 0.33 | 0.44 | -1.2% | 0.02 | 90% |

Cost sensitivity (full-period CAGR / Sharpe):

| rule set | 15 bps | 40 bps | 70 bps |
|---|---|---|---|
| RS leaders, trend filter | +15.2% / 0.82 | +11.1% / 0.63 | +6.4% / 0.41 |
| RS leaders near 52w high | +8.5% / 0.53 | +4.8% / 0.34 | -0.8% / 0.06 |
| signals score>=70, trend | +3.1% / 0.37 | +1.4% / 0.20 | -0.6% / -0.01 |
| signals score>=70, trend, RS top 20% | +2.0% / 0.29 | +0.8% / 0.14 | -0.6% / -0.04 |
| signals, trend, RS top 20% | +10.1% / 0.68 | +5.8% / 0.43 | +1.1% / 0.15 |
| signals, trend, RS top 20%, near 52w high | +8.3% / 0.59 | +4.0% / 0.33 | -1.0% / 0.02 |

Exit variant (stop 2.5 x ATR instead of 1.5 x ATR / structural):

| rule set | CAGR | max DD | Sharpe | OOS Sharpe |
|---|---|---|---|---|
| random picks (reference) | +11.8% | -23% | 0.85 | 0.25 |
| random picks, trend filter | +3.5% | -23% | 0.35 | -1.19 |
| RS leaders, trend filter | +10.8% | -24% | 0.66 | -0.28 |
| RS leaders near 52w high | +9.6% | -23% | 0.62 | -0.47 |
| signals score>=70, trend | +0.6% | -22% | 0.12 | 0.38 |
| signals score>=70, trend, RS top 20% | +1.3% | -20% | 0.21 | 0.36 |
| signals, trend, RS top 20% | +7.8% | -28% | 0.57 | 0.07 |
| signals, trend, RS top 20%, near 52w high | +4.9% | -32% | 0.40 | 0.06 |

### Per trade — universe: largecap_2015 (one position per symbol, t over monthly means)

| group | exit | policy | n | win% | avgR | medR | t | excess vs random (t) | ≥+50% | OOS n | OOS avgR |
|---|---|---|---|---|---|---|---|---|---|---|---|
| breakout | fixed | all | 2040 | 17 | -0.177 | -1.35 | -2.01 | -0.548 (-4.36) | 0.2% | 399 | -0.517 |
| breakout | fixed | SPY>200d & stock>200d | 1689 | 16 | -0.248 | -1.37 | -2.25 | -0.383 (-3.47) | 0.1% | 333 | -0.540 |
| breakout | fixed | SPY>200d & stock>200d & RS>=0.8 | 668 | 19 | +0.078 | -1.31 | -0.28 | -0.160 (-0.95) | 0.1% | 142 | -0.118 |
| breakout | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 627 | 19 | +0.093 | -1.31 | -0.30 | -0.184 (-1.06) | 0.2% | 138 | -0.073 |
| breakout | fixed | score>=70 & SPY>200d & stock>200d | 153 | 22 | +0.087 | -1.13 | 0.45 | -0.045 (-0.17) | 0.0% | 27 | +0.354 |
| breakout | fixed | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 99 | 22 | +0.136 | -1.12 | 0.48 | -0.105 (-0.33) | 0.0% | 16 | +0.323 |
| momentum | fixed | all | 1949 | 23 | +0.085 | -1.21 | -0.03 | -0.268 (-2.78) | 0.1% | 384 | -0.174 |
| momentum | fixed | SPY>200d & stock>200d | 1742 | 23 | +0.120 | -1.22 | -0.02 | -0.061 (-0.63) | 0.1% | 355 | -0.121 |
| momentum | fixed | SPY>200d & stock>200d & RS>=0.8 | 728 | 23 | +0.165 | -1.18 | 0.11 | -0.097 (-0.84) | 0.0% | 152 | -0.065 |
| momentum | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 691 | 23 | +0.175 | -1.19 | 0.28 | -0.087 (-0.73) | 0.0% | 147 | -0.043 |
| momentum | fixed | score>=70 & SPY>200d & stock>200d | 14 | 21 | +0.084 | -1.09 | 0.39 | +0.092 (0.11) | 0.0% | 2 | -1.172 |
| momentum | fixed | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 6 | 17 | +0.170 | -1.00 | 0.14 | -0.300 (-0.30) | 0.0% | 2 | -1.172 |
| combined | fixed | all | 2764 | 20 | -0.057 | -1.27 | -1.39 | -0.425 (-4.42) | 0.2% | 531 | -0.299 |
| combined | fixed | SPY>200d & stock>200d | 2371 | 20 | -0.085 | -1.27 | -1.73 | -0.251 (-2.91) | 0.1% | 460 | -0.282 |
| combined | fixed | SPY>200d & stock>200d & RS>=0.8 | 983 | 20 | +0.066 | -1.22 | -0.68 | -0.167 (-1.51) | 0.0% | 198 | -0.137 |
| combined | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 928 | 20 | +0.076 | -1.23 | -0.57 | -0.164 (-1.46) | 0.0% | 193 | -0.097 |
| combined | fixed | score>=70 & SPY>200d & stock>200d | 163 | 23 | +0.130 | -1.12 | 0.71 | +0.016 (0.06) | 0.0% | 29 | +0.249 |
| combined | fixed | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 103 | 22 | +0.180 | -1.09 | 0.63 | -0.056 (-0.18) | 0.0% | 18 | +0.157 |
| baseline_random | fixed | all | 6516 | 25 | +0.195 | -1.16 | 3.03 | — (—) | 0.7% | 1295 | +0.105 |
| baseline_random | fixed | SPY>200d & stock>200d | 4338 | 23 | +0.125 | -1.20 | 1.01 | — (—) | 0.3% | 866 | +0.037 |
| baseline_random | fixed | SPY>200d & stock>200d & RS>=0.8 | 1694 | 23 | +0.150 | -1.17 | 0.88 | — (—) | 0.5% | 373 | -0.110 |
| baseline_random | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1496 | 23 | +0.158 | -1.18 | 0.83 | — (—) | 0.2% | 324 | -0.061 |
| breakout | wide | all | 1747 | 33 | +0.112 | -1.07 | 0.66 | -0.251 (-3.33) | 0.3% | 332 | +0.028 |
| breakout | wide | SPY>200d & stock>200d | 1443 | 33 | +0.126 | -1.08 | 0.81 | -0.041 (-0.56) | 0.2% | 278 | +0.096 |
| breakout | wide | SPY>200d & stock>200d & RS>=0.8 | 591 | 35 | +0.245 | -1.04 | 1.32 | -0.075 (-0.74) | 0.2% | 126 | +0.033 |
| breakout | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 558 | 34 | +0.237 | -1.04 | 1.00 | -0.095 (-1.08) | 0.0% | 122 | +0.043 |
| breakout | wide | score>=70 & SPY>200d & stock>200d | 153 | 31 | +0.080 | -0.99 | 0.16 | -0.105 (-0.59) | 0.0% | 27 | +0.296 |
| breakout | wide | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 99 | 31 | +0.198 | -0.99 | 0.73 | -0.192 (-0.88) | 0.0% | 16 | +0.463 |
| momentum | wide | all | 1655 | 33 | +0.128 | -1.09 | 0.91 | -0.227 (-2.92) | 0.1% | 319 | -0.013 |
| momentum | wide | SPY>200d & stock>200d | 1482 | 33 | +0.163 | -1.09 | 1.17 | +0.007 (0.10) | 0.1% | 296 | +0.026 |
| momentum | wide | SPY>200d & stock>200d & RS>=0.8 | 630 | 33 | +0.191 | -1.06 | 1.18 | -0.086 (-0.96) | 0.0% | 131 | -0.065 |
| momentum | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 600 | 33 | +0.196 | -1.06 | 1.06 | -0.071 (-0.88) | 0.0% | 128 | -0.050 |
| momentum | wide | score>=70 & SPY>200d & stock>200d | 13 | 31 | +0.022 | -0.98 | 0.39 | +0.128 (0.23) | 0.0% | 2 | -1.102 |
| momentum | wide | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 5 | 40 | +0.487 | -0.98 | 0.49 | +0.052 (0.06) | 0.0% | 2 | -1.102 |
| combined | wide | all | 2187 | 33 | +0.107 | -1.08 | 0.75 | -0.245 (-3.43) | 0.3% | 414 | +0.006 |
| combined | wide | SPY>200d & stock>200d | 1889 | 33 | +0.121 | -1.09 | 0.88 | -0.032 (-0.51) | 0.2% | 367 | +0.059 |
| combined | wide | SPY>200d & stock>200d & RS>=0.8 | 805 | 34 | +0.218 | -1.05 | 1.46 | -0.048 (-0.58) | 0.0% | 165 | -0.059 |
| combined | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 763 | 34 | +0.222 | -1.06 | 1.38 | -0.020 (-0.28) | 0.0% | 161 | -0.044 |
| combined | wide | score>=70 & SPY>200d & stock>200d | 162 | 31 | +0.097 | -0.98 | 0.49 | -0.053 (-0.30) | 0.0% | 29 | +0.200 |
| combined | wide | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 102 | 31 | +0.221 | -0.99 | 0.84 | -0.170 (-0.79) | 0.0% | 18 | +0.289 |
| baseline_random | wide | all | 4607 | 37 | +0.242 | -1.00 | 4.23 | — (—) | 0.8% | 883 | +0.202 |
| baseline_random | wide | SPY>200d & stock>200d | 3156 | 34 | +0.180 | -1.06 | 1.87 | — (—) | 0.2% | 644 | +0.119 |
| baseline_random | wide | SPY>200d & stock>200d & RS>=0.8 | 1288 | 36 | +0.260 | -1.03 | 2.22 | — (—) | 0.5% | 274 | +0.040 |
| baseline_random | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1155 | 36 | +0.267 | -1.04 | 2.01 | — (—) | 0.3% | 239 | +0.064 |

## Momentum rotation — universe: all (from 2018-01-03, 40 bps per side)

| benchmark | CAGR | max DD | Sharpe | train+val Sharpe | OOS CAGR | OOS Sharpe |
|---|---|---|---|---|---|---|
| SPY buy-and-hold | +14.5% | -34% | 0.81 | 0.76 | +16.7% | 1.00 |
| equal-weight universe (no costs) | +27.2% | -43% | 1.03 | 1.01 | +27.2% | 1.07 |

| rule set | trades/yr | exposure | win% | avg trade | avg days | CAGR | max DD | Sharpe | train+val Sharpe | OOS CAGR | OOS Sharpe | vs random | CAGR @15 / @70 bps |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| top5, in RS>=0.8, out RS<0.5 | 10 | 92% | 40 | +20.4% | 108 | +24.1% | -79% | 0.66 | 0.61 | +37.4% | 0.80 | 40% | +25.2% / +22.8% |
| top5, in RS>=0.8, out RS<0.5, stop -20% | 16 | 92% | 28 | +15.2% | 68 | +21.2% | -75% | 0.61 | 0.58 | +27.1% | 0.69 | 55% | +22.7% / +19.4% |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d | 21 | 81% | 37 | +4.3% | 48 | +7.5% | -78% | 0.40 | 0.58 | -25.6% | -0.18 | 15% | +9.6% / +5.1% |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | 26 | 80% | 32 | +2.6% | 37 | +4.7% | -76% | 0.35 | 0.42 | -11.8% | 0.09 | 10% | +7.2% / +1.9% |
| top5, in RS>=0.8, out RS<0.7 | 12 | 93% | 44 | +12.1% | 93 | +18.2% | -76% | 0.58 | 0.52 | +31.8% | 0.74 | 30% | +19.5% / +16.7% |
| top5, in RS>=0.8, out RS<0.7, stop -20% | 18 | 92% | 33 | +8.7% | 60 | +17.6% | -78% | 0.57 | 0.42 | +57.8% | 0.99 | 40% | +19.5% / +15.2% |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d | 22 | 80% | 39 | +3.6% | 45 | +8.5% | -79% | 0.42 | 0.51 | -10.9% | 0.18 | 10% | +10.8% / +5.8% |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | 28 | 80% | 32 | +2.6% | 35 | +4.2% | -74% | 0.34 | 0.34 | +1.1% | 0.34 | 10% | +6.8% / +1.1% |
| top8, in RS>=0.8, out RS<0.5 | 16 | 93% | 43 | +20.0% | 108 | +31.0% | -67% | 0.78 | 0.80 | +28.3% | 0.71 | 60% | +32.2% / +29.6% |
| top8, in RS>=0.8, out RS<0.5, stop -20% | 25 | 92% | 32 | +10.9% | 69 | +20.6% | -69% | 0.62 | 0.70 | +6.0% | 0.42 | 20% | +22.2% / +18.8% |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d | 30 | 80% | 38 | +8.6% | 52 | +28.0% | -58% | 0.74 | 0.77 | +23.4% | 0.65 | 85% | +30.1% / +25.5% |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | 37 | 80% | 34 | +6.8% | 42 | +27.0% | -66% | 0.73 | 0.73 | +29.4% | 0.73 | 75% | +29.4% / +24.2% |
| top8, in RS>=0.8, out RS<0.7 | 19 | 92% | 48 | +23.6% | 95 | +37.8% | -59% | 0.85 | 0.87 | +38.2% | 0.82 | 90% | +39.6% / +36.1% |
| top8, in RS>=0.8, out RS<0.7, stop -20% | 28 | 92% | 32 | +15.6% | 62 | +30.1% | -72% | 0.74 | 0.72 | +36.6% | 0.79 | 70% | +31.9% / +28.0% |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d | 32 | 80% | 40 | +8.8% | 48 | +25.5% | -55% | 0.70 | 0.77 | +11.0% | 0.48 | 65% | +27.9% / +22.7% |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | 40 | 80% | 33 | +9.8% | 37 | +28.4% | -66% | 0.72 | 0.78 | +13.6% | 0.52 | 70% | +31.6% / +25.0% |

## Momentum rotation — universe: largecap_2015 (from 2018-01-03, 40 bps per side)

| benchmark | CAGR | max DD | Sharpe | train+val Sharpe | OOS CAGR | OOS Sharpe |
|---|---|---|---|---|---|---|
| SPY buy-and-hold | +14.5% | -34% | 0.81 | 0.76 | +16.7% | 1.00 |
| equal-weight universe (no costs) | +14.7% | -37% | 0.83 | 0.78 | +15.0% | 1.07 |

| rule set | trades/yr | exposure | win% | avg trade | avg days | CAGR | max DD | Sharpe | train+val Sharpe | OOS CAGR | OOS Sharpe | vs random | CAGR @15 / @70 bps |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| top5, in RS>=0.8, out RS<0.5 | 10 | 94% | 46 | +12.3% | 113 | +22.2% | -35% | 0.85 | 0.86 | +24.2% | 0.85 | 100% | +23.3% / +20.9% |
| top5, in RS>=0.8, out RS<0.5, stop -20% | 11 | 94% | 45 | +11.2% | 107 | +20.6% | -35% | 0.80 | 0.80 | +24.1% | 0.85 | 95% | +21.8% / +19.3% |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d | 20 | 81% | 44 | +3.5% | 49 | +13.7% | -29% | 0.65 | 0.74 | +6.8% | 0.38 | 75% | +15.9% / +11.1% |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | 20 | 81% | 44 | +3.5% | 49 | +13.7% | -28% | 0.65 | 0.74 | +6.8% | 0.38 | 80% | +16.0% / +11.1% |
| top5, in RS>=0.8, out RS<0.7 | 14 | 94% | 46 | +5.7% | 81 | +17.1% | -32% | 0.72 | 0.75 | +15.7% | 0.63 | 100% | +18.7% / +15.4% |
| top5, in RS>=0.8, out RS<0.7, stop -20% | 14 | 93% | 46 | +5.5% | 79 | +16.5% | -32% | 0.70 | 0.74 | +14.4% | 0.60 | 100% | +18.1% / +14.7% |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d | 23 | 80% | 46 | +2.8% | 43 | +12.3% | -30% | 0.61 | 0.69 | +7.3% | 0.39 | 100% | +14.8% / +9.3% |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | 23 | 80% | 46 | +2.7% | 43 | +12.0% | -30% | 0.60 | 0.68 | +6.6% | 0.37 | 100% | +14.6% / +9.0% |
| top8, in RS>=0.8, out RS<0.5 | 16 | 92% | 46 | +10.1% | 110 | +18.5% | -29% | 0.82 | 0.81 | +20.6% | 0.89 | 100% | +19.6% / +17.2% |
| top8, in RS>=0.8, out RS<0.5, stop -20% | 17 | 92% | 45 | +9.7% | 106 | +18.4% | -31% | 0.82 | 0.79 | +21.8% | 0.94 | 95% | +19.4% / +17.0% |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d | 29 | 80% | 45 | +4.2% | 54 | +13.7% | -26% | 0.72 | 0.78 | +8.4% | 0.51 | 100% | +15.7% / +11.3% |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | 29 | 80% | 44 | +4.1% | 53 | +13.7% | -26% | 0.73 | 0.78 | +8.6% | 0.52 | 100% | +15.8% / +11.3% |
| top8, in RS>=0.8, out RS<0.7 | 24 | 93% | 45 | +4.2% | 77 | +12.9% | -32% | 0.63 | 0.66 | +9.7% | 0.51 | 100% | +14.5% / +11.0% |
| top8, in RS>=0.8, out RS<0.7, stop -20% | 24 | 93% | 45 | +4.2% | 75 | +12.6% | -31% | 0.62 | 0.67 | +7.5% | 0.42 | 100% | +14.2% / +10.7% |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d | 35 | 80% | 44 | +2.0% | 44 | +8.9% | -32% | 0.52 | 0.62 | +1.7% | 0.18 | 100% | +11.3% / +6.2% |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | 36 | 80% | 44 | +1.9% | 44 | +8.6% | -32% | 0.51 | 0.62 | +0.2% | 0.12 | 100% | +10.9% / +5.8% |

## Mean R by year (all universe, fixed exit)

| group | policy | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| combined | all | +0.66 | -0.61 | +0.17 | +0.93 | -0.12 | -0.55 | +0.40 | +0.28 | +0.13 | -0.11 |
| combined | SPY>200d & stock>200d | +0.71 | -0.58 | -0.12 | +0.79 | -0.18 | -0.95 | +0.25 | +0.32 | +0.09 | -0.08 |
| combined | SPY>200d & stock>200d & RS>=0.8 | +0.66 | -0.34 | +0.17 | +1.37 | -0.57 | -0.55 | +0.18 | +0.55 | +0.70 | +0.14 |
| combined | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | +0.70 | -0.21 | +0.24 | +1.23 | -0.62 | -0.26 | +0.13 | +0.42 | +0.65 | +0.32 |
| combined | score>=70 & SPY>200d & stock>200d | +0.99 | +0.55 | +0.39 | +1.05 | -0.60 | -1.04 | +0.36 | +0.65 | +0.48 | +0.06 |
| combined | score>=70 & SPY>200d & stock>200d & RS>=0.8 | +0.84 | +1.54 | +0.65 | +0.99 | -0.58 | -1.22 | +0.26 | +0.92 | +0.67 | +0.16 |
| baseline_random | all | +0.91 | -0.02 | +0.45 | +0.93 | +0.05 | -0.35 | +0.54 | +0.35 | +0.24 | +0.12 |
| baseline_random | SPY>200d & stock>200d | +0.91 | -0.34 | +0.39 | +0.79 | +0.07 | -0.90 | +0.19 | +0.35 | +0.14 | +0.10 |
| baseline_random | SPY>200d & stock>200d & RS>=0.8 | +1.10 | +0.05 | +0.51 | +1.13 | -0.34 | -0.85 | +0.41 | +0.47 | +0.38 | +0.12 |
| baseline_random | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | +0.96 | +0.23 | +0.58 | +0.97 | -0.38 | -0.75 | +0.44 | +0.60 | +0.57 | +0.02 |