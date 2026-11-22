# Strategy research

278 symbols with data (1 failed), 10 years of daily bars. Control group: 105 stocks that were already large caps in 2015. Primary cost 20 bps per side (USD account: courtage + slippage; 40 bps ≈ trading from a SEK account). Validation from 2023-03-18, out-of-sample (OOS) from 2025-01-17. Setups invalidated at the next open (skipped): 1309.

Portfolio: max 8 positions, max 3 new per day, 1% risk per trade, max 25% of equity per position, no leverage, marked to market daily. 'vs random' = share of 40 random-order portfolios from the same eligible trades that this ranking beat.

## Portfolio — universe: all

SPY buy-and-hold: +13.4%/yr, max DD -34%, Sharpe 0.77 · train+val Sharpe 0.8 · OOS +9.3%/yr, Sharpe 0.6

| rule set | trades/yr | exposure | win% | avgR | CAGR | max DD | Sharpe | train+val Sharpe | OOS CAGR | OOS Sharpe | vs random |
|---|---|---|---|---|---|---|---|---|---|---|---|
| random picks (reference) | 82.6 | 87% | 21 | +0.24 | +13.6% | -55% | 0.58 | 0.74 | -5.3% | -0.03 | — |
| random picks, trend filter | 70.3 | 77% | 19 | +0.20 | +9.4% | -51% | 0.48 | 0.61 | -4.8% | -0.03 | — |
| RS leaders, trend filter | 73.8 | 66% | 23 | +0.39 | +21.2% | -42% | 0.75 | 0.96 | -9.1% | -0.05 | 100% |
| RS leaders near 52w high | 66.5 | 75% | 24 | +0.58 | +30.1% | -45% | 1.00 | 1.18 | -5.4% | 0.07 | 100% |
| signals score>=70, trend | 47.7 | 62% | 20 | +0.24 | +7.9% | -35% | 0.47 | 0.61 | -6.0% | -0.15 | 17% |
| signals score>=70, trend, RS top 20% | 41.8 | 50% | 21 | +0.45 | +17.1% | -33% | 0.82 | 0.93 | +3.7% | 0.27 | 82% |
| signals, trend, RS top 20% | 77.2 | 78% | 22 | +0.70 | +36.6% | -48% | 1.07 | 1.25 | +17.4% | 0.61 | 100% |
| signals, trend, RS top 20%, near 52w high | 74.4 | 79% | 22 | +0.53 | +28.1% | -34% | 0.98 | 1.16 | +17.2% | 0.62 | 97% |

Cost sensitivity (full-period CAGR / Sharpe):

| rule set | 20 bps | 40 bps | 70 bps |
|---|---|---|---|
| RS leaders, trend filter | +21.2% / 0.75 | +17.6% / 0.65 | +12.3% / 0.52 |
| RS leaders near 52w high | +30.1% / 1.00 | +25.8% / 0.89 | +19.0% / 0.71 |
| signals score>=70, trend | +7.9% / 0.47 | +5.0% / 0.34 | +1.1% / 0.16 |
| signals score>=70, trend, RS top 20% | +17.1% / 0.82 | +14.6% / 0.72 | +10.8% / 0.57 |
| signals, trend, RS top 20% | +36.6% / 1.07 | +30.3% / 0.94 | +23.8% / 0.79 |
| signals, trend, RS top 20%, near 52w high | +28.1% / 0.98 | +23.0% / 0.84 | +16.2% / 0.65 |

Exit variant (stop 2.5 x ATR instead of 1.5 x ATR / structural):

| rule set | CAGR | max DD | Sharpe | OOS Sharpe |
|---|---|---|---|---|
| random picks (reference) | +7.8% | -43% | 0.46 | -0.09 |
| random picks, trend filter | +16.3% | -39% | 0.89 | -0.14 |
| RS leaders, trend filter | +18.8% | -27% | 0.88 | 0.04 |
| RS leaders near 52w high | +22.1% | -27% | 0.99 | -0.08 |
| signals score>=70, trend | +9.9% | -29% | 0.64 | -0.31 |
| signals score>=70, trend, RS top 20% | +15.6% | -28% | 0.93 | 0.17 |
| signals, trend, RS top 20% | +15.4% | -36% | 0.76 | 0.45 |
| signals, trend, RS top 20%, near 52w high | +13.4% | -25% | 0.69 | 0.36 |

### Per trade — universe: all (one position per symbol, t over monthly means)

| group | exit | policy | n | win% | avgR | medR | t | excess vs random (t) | ≥+50% | OOS n | OOS avgR |
|---|---|---|---|---|---|---|---|---|---|---|---|
| breakout | fixed | all | 6516 | 16 | +0.252 | -1.11 | 0.94 | -0.326 (-3.89) | 3.2% | 1473 | -0.034 |
| breakout | fixed | SPY>200d & stock>200d | 5158 | 16 | +0.204 | -1.12 | 0.26 | -0.211 (-3.02) | 3.0% | 1185 | -0.030 |
| breakout | fixed | SPY>200d & stock>200d & RS>=0.8 | 2141 | 17 | +0.373 | -1.08 | 1.09 | -0.196 (-1.87) | 5.4% | 513 | +0.409 |
| breakout | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1748 | 18 | +0.409 | -1.08 | 1.09 | -0.098 (-0.82) | 4.3% | 392 | +0.610 |
| breakout | fixed | score>=70 & SPY>200d & stock>200d | 741 | 22 | +0.437 | -1.00 | 2.04 | +0.043 (0.29) | 5.9% | 139 | +0.265 |
| breakout | fixed | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 453 | 23 | +0.545 | -0.98 | 2.31 | +0.058 (0.28) | 7.7% | 92 | +0.396 |
| momentum | fixed | all | 5410 | 21 | +0.239 | -1.04 | 1.56 | -0.294 (-3.88) | 3.6% | 1231 | +0.012 |
| momentum | fixed | SPY>200d & stock>200d | 4775 | 22 | +0.273 | -1.04 | 1.59 | -0.088 (-1.36) | 3.4% | 1113 | +0.042 |
| momentum | fixed | SPY>200d & stock>200d & RS>=0.8 | 1942 | 22 | +0.356 | -1.03 | 1.96 | -0.093 (-1.14) | 6.2% | 467 | +0.178 |
| momentum | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1601 | 22 | +0.363 | -1.04 | 1.89 | -0.026 (-0.29) | 4.5% | 372 | +0.154 |
| momentum | fixed | score>=70 & SPY>200d & stock>200d | 159 | 23 | +0.474 | -0.92 | 1.79 | +0.272 (0.99) | 11.9% | 41 | +0.778 |
| momentum | fixed | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 98 | 24 | +0.694 | -0.90 | 1.80 | +0.293 (0.81) | 15.3% | 27 | +0.911 |
| combined | fixed | all | 8215 | 19 | +0.245 | -1.08 | 1.28 | -0.310 (-4.46) | 3.3% | 1852 | +0.063 |
| combined | fixed | SPY>200d & stock>200d | 6763 | 19 | +0.211 | -1.08 | 0.59 | -0.174 (-2.96) | 3.1% | 1551 | +0.049 |
| combined | fixed | SPY>200d & stock>200d & RS>=0.8 | 2825 | 20 | +0.369 | -1.05 | 1.60 | -0.141 (-1.78) | 5.4% | 680 | +0.413 |
| combined | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 2326 | 20 | +0.373 | -1.05 | 1.57 | -0.058 (-0.68) | 4.3% | 525 | +0.499 |
| combined | fixed | score>=70 & SPY>200d & stock>200d | 820 | 22 | +0.457 | -0.99 | 1.88 | +0.040 (0.30) | 6.6% | 165 | +0.285 |
| combined | fixed | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 500 | 23 | +0.554 | -0.96 | 2.03 | +0.010 (0.05) | 8.6% | 108 | +0.409 |
| baseline_random | fixed | all | 17956 | 24 | +0.323 | -1.02 | 4.55 | — (—) | 4.9% | 4092 | +0.173 |
| baseline_random | fixed | SPY>200d & stock>200d | 11335 | 22 | +0.301 | -1.05 | 2.65 | — (—) | 3.5% | 2563 | +0.131 |
| baseline_random | fixed | SPY>200d & stock>200d & RS>=0.8 | 4634 | 22 | +0.335 | -1.03 | 2.98 | — (—) | 6.1% | 1121 | +0.170 |
| baseline_random | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 3161 | 23 | +0.387 | -1.05 | 2.66 | — (—) | 4.0% | 697 | +0.261 |
| breakout | wide | all | 5243 | 33 | +0.280 | -0.95 | 2.83 | -0.159 (-2.85) | 5.5% | 1177 | +0.213 |
| breakout | wide | SPY>200d & stock>200d | 4208 | 32 | +0.292 | -0.96 | 1.96 | -0.057 (-1.17) | 5.0% | 952 | +0.234 |
| breakout | wide | SPY>200d & stock>200d & RS>=0.8 | 1789 | 33 | +0.407 | -0.93 | 2.32 | -0.093 (-1.50) | 9.0% | 430 | +0.319 |
| breakout | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1487 | 34 | +0.449 | -0.93 | 2.72 | -0.022 (-0.31) | 7.3% | 332 | +0.313 |
| breakout | wide | score>=70 & SPY>200d & stock>200d | 714 | 32 | +0.369 | -0.91 | 2.11 | -0.016 (-0.15) | 9.1% | 133 | +0.134 |
| breakout | wide | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 431 | 33 | +0.456 | -0.90 | 2.49 | +0.006 (0.04) | 11.6% | 88 | +0.196 |
| momentum | wide | all | 4493 | 32 | +0.248 | -0.98 | 2.44 | -0.180 (-3.06) | 4.7% | 1001 | +0.105 |
| momentum | wide | SPY>200d & stock>200d | 3982 | 32 | +0.289 | -0.98 | 2.54 | -0.017 (-0.33) | 4.6% | 910 | +0.133 |
| momentum | wide | SPY>200d & stock>200d & RS>=0.8 | 1638 | 32 | +0.331 | -0.97 | 2.10 | -0.111 (-1.81) | 7.8% | 392 | +0.171 |
| momentum | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1381 | 32 | +0.312 | -0.97 | 1.86 | -0.107 (-1.61) | 5.7% | 313 | +0.183 |
| momentum | wide | score>=70 & SPY>200d & stock>200d | 143 | 29 | +0.242 | -0.88 | 0.98 | -0.030 (-0.16) | 14.0% | 38 | +0.480 |
| momentum | wide | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 84 | 31 | +0.404 | -0.86 | 1.24 | -0.012 (-0.05) | 19.1% | 25 | +0.644 |
| combined | wide | all | 6255 | 33 | +0.264 | -0.97 | 2.74 | -0.175 (-3.40) | 5.1% | 1397 | +0.173 |
| combined | wide | SPY>200d & stock>200d | 5213 | 32 | +0.285 | -0.98 | 2.05 | -0.058 (-1.36) | 4.8% | 1186 | +0.184 |
| combined | wide | SPY>200d & stock>200d & RS>=0.8 | 2264 | 32 | +0.352 | -0.95 | 2.17 | -0.105 (-1.91) | 8.2% | 546 | +0.268 |
| combined | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1893 | 33 | +0.369 | -0.95 | 2.38 | -0.057 (-0.96) | 6.5% | 422 | +0.269 |
| combined | wide | score>=70 & SPY>200d & stock>200d | 778 | 32 | +0.356 | -0.91 | 1.72 | -0.046 (-0.46) | 9.1% | 155 | +0.189 |
| combined | wide | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 464 | 33 | +0.438 | -0.89 | 2.02 | -0.064 (-0.46) | 12.1% | 101 | +0.274 |
| baseline_random | wide | all | 12492 | 35 | +0.296 | -0.95 | 4.88 | — (—) | 6.2% | 2723 | +0.223 |
| baseline_random | wide | SPY>200d & stock>200d | 8141 | 33 | +0.296 | -0.97 | 3.03 | — (—) | 4.7% | 1834 | +0.144 |
| baseline_random | wide | SPY>200d & stock>200d & RS>=0.8 | 3434 | 32 | +0.326 | -0.97 | 3.46 | — (—) | 8.1% | 817 | +0.206 |
| baseline_random | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 2512 | 34 | +0.388 | -0.97 | 3.49 | — (—) | 5.7% | 543 | +0.321 |

## Portfolio — universe: largecap_2015

SPY buy-and-hold: +13.4%/yr, max DD -34%, Sharpe 0.77 · train+val Sharpe 0.8 · OOS +9.3%/yr, Sharpe 0.6

| rule set | trades/yr | exposure | win% | avgR | CAGR | max DD | Sharpe | train+val Sharpe | OOS CAGR | OOS Sharpe | vs random |
|---|---|---|---|---|---|---|---|---|---|---|---|
| random picks (reference) | 42.0 | 87% | 25 | +0.32 | +8.8% | -29% | 0.61 | 0.46 | +12.8% | 0.82 | — |
| random picks, trend filter | 37.3 | 74% | 21 | +0.12 | +3.4% | -26% | 0.31 | 0.35 | +3.8% | 0.31 | — |
| RS leaders, trend filter | 42.9 | 75% | 22 | +0.19 | +5.5% | -36% | 0.38 | 0.50 | -1.7% | 0.01 | 50% |
| RS leaders near 52w high | 41.3 | 76% | 21 | +0.15 | +2.5% | -29% | 0.23 | 0.27 | +0.8% | 0.12 | 23% |
| signals score>=70, trend | 14.6 | 35% | 22 | +0.22 | +2.4% | -16% | 0.30 | 0.34 | +1.9% | 0.23 | 28% |
| signals score>=70, trend, RS top 20% | 10.8 | 25% | 21 | +0.26 | +1.7% | -19% | 0.25 | 0.31 | +1.4% | 0.22 | 0% |
| signals, trend, RS top 20% | 41.9 | 78% | 21 | +0.30 | +6.0% | -30% | 0.45 | 0.53 | +1.8% | 0.16 | 55% |
| signals, trend, RS top 20%, near 52w high | 43.0 | 78% | 21 | +0.30 | +6.7% | -33% | 0.50 | 0.60 | +1.6% | 0.15 | 75% |

Cost sensitivity (full-period CAGR / Sharpe):

| rule set | 20 bps | 40 bps | 70 bps |
|---|---|---|---|
| RS leaders, trend filter | +5.5% / 0.38 | +2.5% / 0.23 | -1.8% / 0.01 |
| RS leaders near 52w high | +2.5% / 0.23 | -0.5% / 0.07 | -5.2% / -0.20 |
| signals score>=70, trend | +2.4% / 0.30 | +1.1% / 0.16 | -0.9% / -0.04 |
| signals score>=70, trend, RS top 20% | +1.7% / 0.25 | +0.7% / 0.13 | -0.8% / -0.05 |
| signals, trend, RS top 20% | +6.0% / 0.45 | +2.7% / 0.25 | -2.1% / -0.05 |
| signals, trend, RS top 20%, near 52w high | +6.7% / 0.50 | +3.4% / 0.29 | -1.5% / -0.01 |

Exit variant (stop 2.5 x ATR instead of 1.5 x ATR / structural):

| rule set | CAGR | max DD | Sharpe | OOS Sharpe |
|---|---|---|---|---|
| random picks (reference) | +5.5% | -26% | 0.44 | -0.00 |
| random picks, trend filter | +3.9% | -16% | 0.37 | -0.38 |
| RS leaders, trend filter | +10.2% | -25% | 0.65 | 0.06 |
| RS leaders near 52w high | +11.8% | -22% | 0.74 | 0.09 |
| signals score>=70, trend | +1.6% | -16% | 0.22 | 0.37 |
| signals score>=70, trend, RS top 20% | +2.1% | -17% | 0.32 | 0.38 |
| signals, trend, RS top 20% | +7.5% | -21% | 0.55 | 0.14 |
| signals, trend, RS top 20%, near 52w high | +6.8% | -27% | 0.52 | 0.24 |

### Per trade — universe: largecap_2015 (one position per symbol, t over monthly means)

| group | exit | policy | n | win% | avgR | medR | t | excess vs random (t) | ≥+50% | OOS n | OOS avgR |
|---|---|---|---|---|---|---|---|---|---|---|---|
| breakout | fixed | all | 2279 | 17 | +0.055 | -1.17 | -0.54 | -0.424 (-3.44) | 0.2% | 466 | -0.229 |
| breakout | fixed | SPY>200d & stock>200d | 1867 | 16 | -0.010 | -1.18 | -0.54 | -0.227 (-2.05) | 0.1% | 389 | -0.232 |
| breakout | fixed | SPY>200d & stock>200d & RS>=0.8 | 761 | 18 | +0.258 | -1.12 | 1.20 | +0.075 (0.34) | 0.1% | 158 | +0.046 |
| breakout | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 713 | 18 | +0.283 | -1.12 | 1.29 | +0.114 (0.52) | 0.1% | 153 | +0.170 |
| breakout | fixed | score>=70 & SPY>200d & stock>200d | 156 | 21 | +0.158 | -1.02 | 0.83 | -0.049 (-0.17) | 0.0% | 27 | +0.414 |
| breakout | fixed | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 103 | 20 | +0.158 | -1.01 | 0.79 | -0.123 (-0.36) | 0.0% | 15 | +0.442 |
| momentum | fixed | all | 2198 | 22 | +0.157 | -1.09 | 0.86 | -0.269 (-2.83) | 0.1% | 465 | +0.002 |
| momentum | fixed | SPY>200d & stock>200d | 1962 | 22 | +0.192 | -1.10 | 0.67 | -0.081 (-0.92) | 0.1% | 429 | +0.063 |
| momentum | fixed | SPY>200d & stock>200d & RS>=0.8 | 839 | 22 | +0.200 | -1.08 | 0.07 | -0.209 (-1.88) | 0.0% | 180 | +0.058 |
| momentum | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 796 | 22 | +0.186 | -1.08 | -0.09 | -0.207 (-1.82) | 0.0% | 174 | +0.102 |
| momentum | fixed | score>=70 & SPY>200d & stock>200d | 18 | 17 | -0.091 | -1.05 | 0.18 | -0.075 (-0.11) | 0.0% | 6 | -1.113 |
| momentum | fixed | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 9 | 22 | +0.681 | -0.91 | 0.62 | -0.132 (-0.12) | 0.0% | 3 | -1.108 |
| combined | fixed | all | 3102 | 19 | +0.105 | -1.12 | -0.01 | -0.350 (-3.64) | 0.2% | 636 | -0.124 |
| combined | fixed | SPY>200d & stock>200d | 2650 | 19 | +0.074 | -1.13 | -0.28 | -0.172 (-2.07) | 0.1% | 549 | -0.091 |
| combined | fixed | SPY>200d & stock>200d & RS>=0.8 | 1134 | 20 | +0.186 | -1.08 | 0.09 | -0.169 (-1.52) | 0.0% | 231 | -0.062 |
| combined | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1074 | 20 | +0.180 | -1.09 | 0.15 | -0.139 (-1.29) | 0.0% | 224 | +0.033 |
| combined | fixed | score>=70 & SPY>200d & stock>200d | 170 | 21 | +0.171 | -1.02 | 0.93 | -0.036 (-0.14) | 0.0% | 33 | +0.136 |
| combined | fixed | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 110 | 21 | +0.239 | -1.00 | 1.07 | -0.054 (-0.16) | 0.0% | 18 | +0.183 |
| baseline_random | fixed | all | 7324 | 25 | +0.292 | -1.05 | 4.05 | — (—) | 0.7% | 1447 | +0.259 |
| baseline_random | fixed | SPY>200d & stock>200d | 4809 | 23 | +0.227 | -1.08 | 2.08 | — (—) | 0.3% | 984 | +0.139 |
| baseline_random | fixed | SPY>200d & stock>200d & RS>=0.8 | 1936 | 23 | +0.262 | -1.07 | 1.97 | — (—) | 0.4% | 427 | +0.074 |
| baseline_random | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1725 | 23 | +0.259 | -1.07 | 1.80 | — (—) | 0.2% | 367 | +0.130 |
| breakout | wide | all | 1944 | 33 | +0.169 | -1.00 | 1.25 | -0.234 (-3.11) | 0.3% | 388 | +0.108 |
| breakout | wide | SPY>200d & stock>200d | 1596 | 33 | +0.189 | -1.00 | 1.31 | -0.029 (-0.41) | 0.2% | 325 | +0.156 |
| breakout | wide | SPY>200d & stock>200d & RS>=0.8 | 674 | 32 | +0.242 | -0.97 | 1.05 | -0.120 (-1.41) | 0.0% | 135 | +0.124 |
| breakout | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 636 | 33 | +0.248 | -0.96 | 1.17 | -0.077 (-0.90) | 0.0% | 130 | +0.185 |
| breakout | wide | score>=70 & SPY>200d & stock>200d | 156 | 31 | +0.166 | -0.92 | 0.69 | -0.054 (-0.28) | 0.0% | 27 | +0.411 |
| breakout | wide | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 103 | 31 | +0.280 | -0.92 | 1.03 | -0.108 (-0.46) | 0.0% | 15 | +0.566 |
| momentum | wide | all | 1865 | 32 | +0.176 | -1.02 | 1.66 | -0.199 (-2.68) | 0.1% | 388 | +0.082 |
| momentum | wide | SPY>200d & stock>200d | 1663 | 32 | +0.222 | -1.02 | 1.84 | +0.018 (0.28) | 0.1% | 360 | +0.125 |
| momentum | wide | SPY>200d & stock>200d & RS>=0.8 | 723 | 33 | +0.233 | -0.99 | 1.06 | -0.117 (-1.50) | 0.0% | 159 | -0.028 |
| momentum | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 686 | 33 | +0.241 | -0.99 | 1.26 | -0.068 (-0.82) | 0.0% | 155 | +0.010 |
| momentum | wide | score>=70 & SPY>200d & stock>200d | 17 | 24 | -0.122 | -0.91 | 0.11 | -0.010 (-0.02) | 0.0% | 6 | -0.900 |
| momentum | wide | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 8 | 38 | +0.610 | -0.87 | 0.77 | -0.087 (-0.14) | 0.0% | 3 | -0.982 |
| combined | wide | all | 2458 | 32 | +0.165 | -1.01 | 1.42 | -0.225 (-3.26) | 0.3% | 492 | +0.110 |
| combined | wide | SPY>200d & stock>200d | 2109 | 32 | +0.181 | -1.02 | 1.43 | -0.025 (-0.43) | 0.1% | 433 | +0.148 |
| combined | wide | SPY>200d & stock>200d & RS>=0.8 | 922 | 33 | +0.237 | -0.99 | 1.18 | -0.099 (-1.49) | 0.0% | 188 | +0.018 |
| combined | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 875 | 33 | +0.242 | -0.99 | 1.29 | -0.053 (-0.83) | 0.0% | 183 | +0.067 |
| combined | wide | score>=70 & SPY>200d & stock>200d | 169 | 31 | +0.157 | -0.91 | 0.83 | -0.034 (-0.19) | 0.0% | 33 | +0.172 |
| combined | wide | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 109 | 31 | +0.312 | -0.92 | 1.18 | -0.089 (-0.39) | 0.0% | 18 | +0.308 |
| baseline_random | wide | all | 5194 | 36 | +0.290 | -0.95 | 4.78 | — (—) | 0.8% | 976 | +0.309 |
| baseline_random | wide | SPY>200d & stock>200d | 3496 | 34 | +0.239 | -1.00 | 2.48 | — (—) | 0.2% | 715 | +0.185 |
| baseline_random | wide | SPY>200d & stock>200d & RS>=0.8 | 1482 | 34 | +0.278 | -0.98 | 2.49 | — (—) | 0.4% | 319 | +0.119 |
| baseline_random | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1334 | 34 | +0.282 | -0.99 | 2.36 | — (—) | 0.3% | 277 | +0.179 |

## Momentum rotation — universe: all (from 2018-03-02, 20 bps per side)

| benchmark | CAGR | max DD | Sharpe | train+val Sharpe | OOS CAGR | OOS Sharpe |
|---|---|---|---|---|---|---|
| SPY buy-and-hold | +13.1% | -34% | 0.74 | 0.77 | +9.3% | 0.60 |
| equal-weight universe (no costs) | +23.7% | -42% | 0.93 | 1.01 | +13.8% | 0.63 |

| rule set | trades/yr | exposure | win% | avg trade | avg days | CAGR | max DD | Sharpe | train+val Sharpe | OOS CAGR | OOS Sharpe | vs random | CAGR @40 / @70 bps | without best stock |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| top5, in RS>=0.8, out RS<0.5 | 10 | 93% | 37 | +17.9% | 110 | +13.6% | -79% | 0.51 | 0.42 | +35.9% | 0.78 | 25% | +12.8% / +11.6% | SE: +18.7%, Sharpe 0.58 |
| top5, in RS>=0.8, out RS<0.5, stop -20% | 15 | 91% | 31 | +17.0% | 74 | +21.2% | -75% | 0.61 | 0.68 | +3.7% | 0.40 | 55% | +22.1% / +20.3% | SE: +21.7%, Sharpe 0.63 |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d | 21 | 81% | 37 | +5.2% | 48 | +6.8% | -74% | 0.39 | 0.58 | -26.9% | -0.21 | 5% | +5.1% / +2.6% | MARA: +3.3%, Sharpe 0.31 |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | 26 | 80% | 34 | +3.9% | 39 | +7.4% | -71% | 0.39 | 0.54 | -18.3% | -0.04 | 10% | +5.5% / +2.6% | CELH: +13.1%, Sharpe 0.49 |
| top5, in RS>=0.8, out RS<0.7 | 12 | 93% | 44 | +12.2% | 93 | +12.9% | -76% | 0.50 | 0.48 | +19.0% | 0.60 | 0% | +11.8% / +10.3% | ENPH: +15.5%, Sharpe 0.54 |
| top5, in RS>=0.8, out RS<0.7, stop -20% | 18 | 92% | 36 | +10.7% | 65 | +17.2% | -77% | 0.56 | 0.48 | +40.1% | 0.83 | 60% | +15.8% / +13.7% | VKTX: +12.2%, Sharpe 0.49 |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d | 23 | 80% | 38 | +3.2% | 44 | +4.0% | -77% | 0.34 | 0.45 | -13.6% | 0.08 | 5% | +2.2% / -0.4% | TSLA: +9.5%, Sharpe 0.44 |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | 28 | 80% | 35 | +3.8% | 37 | +7.4% | -68% | 0.39 | 0.49 | -8.5% | 0.16 | 15% | +5.3% / +2.3% | CELH: +3.3%, Sharpe 0.32 |
| top8, in RS>=0.8, out RS<0.5 | 17 | 92% | 41 | +21.9% | 108 | +25.4% | -70% | 0.70 | 0.78 | +10.0% | 0.47 | 75% | +24.5% / +23.1% | SE: +22.9%, Sharpe 0.65 |
| top8, in RS>=0.8, out RS<0.5, stop -20% | 25 | 92% | 32 | +15.4% | 69 | +23.1% | -68% | 0.65 | 0.76 | +3.6% | 0.40 | 75% | +21.7% / +20.5% | MARA: +28.9%, Sharpe 0.71 |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d | 31 | 80% | 38 | +8.5% | 52 | +23.3% | -58% | 0.67 | 0.77 | +5.8% | 0.40 | 75% | +21.6% / +19.1% | APP: +16.7%, Sharpe 0.56 |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | 38 | 80% | 35 | +6.9% | 43 | +22.2% | -67% | 0.65 | 0.74 | +8.0% | 0.43 | 75% | +20.4% / +17.6% | NIO: +23.5%, Sharpe 0.67 |
| top8, in RS>=0.8, out RS<0.7 | 19 | 92% | 47 | +18.6% | 94 | +29.3% | -58% | 0.74 | 0.80 | +19.0% | 0.59 | 70% | +28.1% / +26.5% | MARA: +21.3%, Sharpe 0.63 |
| top8, in RS>=0.8, out RS<0.7, stop -20% | 28 | 91% | 33 | +15.7% | 64 | +24.1% | -71% | 0.66 | 0.67 | +23.9% | 0.65 | 65% | +22.8% / +20.7% | MARA: +17.8%, Sharpe 0.57 |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d | 34 | 80% | 40 | +7.1% | 48 | +16.6% | -54% | 0.56 | 0.66 | -1.0% | 0.27 | 50% | +14.8% / +12.2% | MARA: +14.2%, Sharpe 0.52 |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | 41 | 80% | 33 | +9.4% | 39 | +24.2% | -63% | 0.66 | 0.75 | +4.8% | 0.37 | 90% | +22.0% / +18.7% | MARA: +21.3%, Sharpe 0.62 |
| top8, in RS>=0.8, out RS<0.5, 12-1 month momentum | 19 | 92% | 31 | +18.7% | 96 | +19.6% | -63% | 0.61 | 0.65 | +13.8% | 0.53 | 55% | +18.6% / +17.1% | SE: +15.8%, Sharpe 0.54 |
| top8, in RS>=0.8, out RS<0.5, monthly | 12 | 95% | 42 | +49.0% | 150 | +32.7% | -62% | 0.79 | 0.81 | +35.9% | 0.78 | 75% | +32.0% / +30.9% | ENPH: +31.1%, Sharpe 0.78 |
| top8, in RS>=0.8, out RS<0.5, volatility-adjusted | 15 | 93% | 48 | +26.0% | 126 | +31.6% | -47% | 0.87 | 0.95 | +30.2% | 0.74 | 100% | +30.8% / +29.4% | RKLB: +26.1%, Sharpe 0.77 |
| top8, in RS>=0.8, out RS<0.5, max 2/sector | 16 | 93% | 41 | +26.2% | 109 | +36.0% | -56% | 0.85 | 0.96 | +17.5% | 0.57 | 95% | +35.1% / +33.9% | SE: +33.2%, Sharpe 0.78 |
| top8, in RS>=0.8, out RS<0.5, max 3/sector | 16 | 94% | 42 | +25.4% | 110 | +29.3% | -58% | 0.75 | 0.84 | +15.9% | 0.56 | 75% | +28.4% / +27.1% | SE: +25.0%, Sharpe 0.68 |
| top8, in RS>=0.8, out RS<0.5, sell below 50d | 62 | 87% | 36 | +9.8% | 28 | +42.0% | -60% | 0.92 | 1.09 | +0.8% | 0.29 | 100% | +38.1% / +32.5% | MARA: +31.5%, Sharpe 0.79 |
| top8, in RS>=0.8, out RS<0.5, sell below 50d after +30% over 200d | 58 | 88% | 38 | +10.3% | 30 | +28.2% | -59% | 0.75 | 0.89 | +0.9% | 0.30 | 80% | +24.7% / +19.7% | MARA: +29.5%, Sharpe 0.77 |

## Momentum rotation — universe: largecap_2015 (from 2018-03-02, 20 bps per side)

| benchmark | CAGR | max DD | Sharpe | train+val Sharpe | OOS CAGR | OOS Sharpe |
|---|---|---|---|---|---|---|
| SPY buy-and-hold | +13.1% | -34% | 0.74 | 0.77 | +9.3% | 0.60 |
| equal-weight universe (no costs) | +13.9% | -37% | 0.80 | 0.76 | +14.1% | 1.02 |

| rule set | trades/yr | exposure | win% | avg trade | avg days | CAGR | max DD | Sharpe | train+val Sharpe | OOS CAGR | OOS Sharpe | vs random | CAGR @40 / @70 bps | without best stock |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| top5, in RS>=0.8, out RS<0.5 | 10 | 95% | 49 | +9.1% | 115 | +15.1% | -36% | 0.67 | 0.61 | +23.8% | 0.85 | 95% | +14.2% / +12.9% | DVN: +11.7%, Sharpe 0.57 |
| top5, in RS>=0.8, out RS<0.5, stop -20% | 11 | 94% | 51 | +8.9% | 110 | +15.4% | -36% | 0.69 | 0.63 | +23.6% | 0.85 | 100% | +14.5% / +13.2% | DVN: +12.2%, Sharpe 0.59 |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d | 21 | 81% | 47 | +3.0% | 50 | +10.3% | -26% | 0.55 | 0.61 | +6.1% | 0.36 | 90% | +8.5% / +5.9% | AVGO: +10.3%, Sharpe 0.57 |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | 21 | 81% | 48 | +3.0% | 49 | +10.4% | -26% | 0.55 | 0.62 | +6.2% | 0.36 | 80% | +8.6% / +6.0% | AVGO: +10.3%, Sharpe 0.57 |
| top5, in RS>=0.8, out RS<0.7 | 14 | 94% | 48 | +4.9% | 84 | +10.9% | -36% | 0.52 | 0.56 | +7.7% | 0.39 | 90% | +9.7% / +8.0% | INTC: +9.1%, Sharpe 0.48 |
| top5, in RS>=0.8, out RS<0.7, stop -20% | 14 | 95% | 48 | +5.4% | 82 | +13.0% | -33% | 0.59 | 0.65 | +7.5% | 0.39 | 95% | +11.8% / +10.0% | INTC: +11.4%, Sharpe 0.57 |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d | 23 | 81% | 46 | +2.3% | 44 | +8.5% | -29% | 0.48 | 0.64 | -3.2% | 0.02 | 95% | +6.6% / +3.8% | AVGO: +7.4%, Sharpe 0.44 |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | 24 | 81% | 46 | +2.3% | 43 | +8.5% | -29% | 0.48 | 0.64 | -3.3% | 0.01 | 100% | +6.5% / +3.6% | AVGO: +7.4%, Sharpe 0.44 |
| top8, in RS>=0.8, out RS<0.5 | 17 | 94% | 47 | +8.0% | 109 | +14.3% | -29% | 0.70 | 0.66 | +18.2% | 0.81 | 100% | +13.4% / +12.1% | DVN: +12.2%, Sharpe 0.63 |
| top8, in RS>=0.8, out RS<0.5, stop -20% | 18 | 93% | 47 | +6.8% | 104 | +13.1% | -29% | 0.66 | 0.62 | +16.4% | 0.75 | 95% | +12.2% / +10.9% | DVN: +10.8%, Sharpe 0.58 |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d | 32 | 80% | 44 | +2.5% | 52 | +7.8% | -28% | 0.49 | 0.53 | +4.3% | 0.31 | 80% | +6.1% / +3.7% | DVN: +7.3%, Sharpe 0.47 |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | 32 | 80% | 44 | +2.5% | 51 | +7.8% | -28% | 0.49 | 0.54 | +4.2% | 0.31 | 75% | +6.2% / +3.8% | DVN: +7.4%, Sharpe 0.48 |
| top8, in RS>=0.8, out RS<0.7 | 22 | 93% | 49 | +4.6% | 82 | +11.8% | -26% | 0.61 | 0.65 | +8.6% | 0.47 | 100% | +10.6% / +8.8% | META: +8.9%, Sharpe 0.50 |
| top8, in RS>=0.8, out RS<0.7, stop -20% | 23 | 93% | 48 | +4.6% | 80 | +11.4% | -29% | 0.60 | 0.64 | +8.0% | 0.45 | 100% | +10.2% / +8.4% | AVGO: +9.1%, Sharpe 0.51 |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d | 36 | 80% | 48 | +2.0% | 45 | +7.7% | -29% | 0.49 | 0.58 | +1.5% | 0.17 | 100% | +5.9% / +3.1% | AVGO: +7.1%, Sharpe 0.46 |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | 36 | 80% | 48 | +2.0% | 45 | +7.7% | -29% | 0.49 | 0.57 | +1.3% | 0.17 | 95% | +5.8% / +3.1% | AVGO: +7.1%, Sharpe 0.46 |
| top8, in RS>=0.8, out RS<0.5, 12-1 month momentum | 19 | 90% | 33 | +3.2% | 93 | +4.4% | -40% | 0.31 | 0.40 | -3.5% | -0.06 | 10% | +3.5% / +2.1% | GE: +2.8%, Sharpe 0.24 |
| top8, in RS>=0.8, out RS<0.5, monthly | 13 | 93% | 51 | +10.6% | 146 | +12.8% | -26% | 0.63 | 0.69 | +7.5% | 0.41 | 95% | +13.6% / +12.6% | DVN: +12.6%, Sharpe 0.62 |
| top8, in RS>=0.8, out RS<0.5, volatility-adjusted | 16 | 93% | 56 | +6.6% | 114 | +11.9% | -23% | 0.70 | 0.69 | +11.2% | 0.74 | 95% | +11.1% / +9.9% | GE: +9.3%, Sharpe 0.57 |
| top8, in RS>=0.8, out RS<0.5, max 2/sector | 18 | 93% | 44 | +6.5% | 105 | +10.9% | -30% | 0.57 | 0.55 | +14.0% | 0.65 | 90% | +9.9% / +8.6% | DVN: +9.2%, Sharpe 0.51 |
| top8, in RS>=0.8, out RS<0.5, max 3/sector | 18 | 94% | 45 | +7.2% | 106 | +12.9% | -28% | 0.65 | 0.62 | +16.1% | 0.73 | 100% | +12.0% / +10.7% | DVN: +11.0%, Sharpe 0.59 |
| top8, in RS>=0.8, out RS<0.5, sell below 50d | 63 | 87% | 36 | +0.8% | 28 | +5.5% | -25% | 0.38 | 0.54 | -5.9% | -0.22 | 30% | +2.4% / -2.1% | DVN: +4.1%, Sharpe 0.31 |
| top8, in RS>=0.8, out RS<0.5, sell below 50d after +30% over 200d | 34 | 90% | 45 | +2.5% | 54 | +8.7% | -24% | 0.53 | 0.64 | -0.4% | 0.07 | 100% | +7.0% / +4.4% | AVGO: +8.3%, Sharpe 0.51 |

## Rotation: pre-registered selection (2015 large caps, train+validation only)

Gates: train+val Sharpe > SPY's, ranking beats >= 90% of random selections, CAGR without the single best stock >= SPY's, max drawdown at most 10 points worse than SPY's.

**Chosen: none — no rule set passed every gate**

| rule set | passes | train+val Sharpe | failed gates |
|---|---|---|---|
| top5, in RS>=0.8, out RS<0.5 | ❌ | 0.61 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top5, in RS>=0.8, out RS<0.5, stop -20% | ❌ | 0.63 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d | ❌ | 0.61 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | ❌ | 0.62 | train_val_sharpe_beats_spy, ranking_beats_random, without_best_stock_beats_spy |
| top5, in RS>=0.8, out RS<0.7 | ❌ | 0.56 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top5, in RS>=0.8, out RS<0.7, stop -20% | ❌ | 0.65 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d | ❌ | 0.64 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | ❌ | 0.64 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5 | ❌ | 0.66 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5, stop -20% | ❌ | 0.62 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d | ❌ | 0.53 | train_val_sharpe_beats_spy, ranking_beats_random, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | ❌ | 0.54 | train_val_sharpe_beats_spy, ranking_beats_random, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.7 | ❌ | 0.65 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.7, stop -20% | ❌ | 0.64 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d | ❌ | 0.58 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | ❌ | 0.57 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5, 12-1 month momentum | ❌ | 0.40 | train_val_sharpe_beats_spy, ranking_beats_random, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5, monthly | ❌ | 0.69 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5, volatility-adjusted | ❌ | 0.69 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5, max 2/sector | ❌ | 0.55 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5, max 3/sector | ❌ | 0.62 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5, sell below 50d | ❌ | 0.54 | train_val_sharpe_beats_spy, ranking_beats_random, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5, sell below 50d after +30% over 200d | ❌ | 0.64 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |

Calendar-year returns (2015 large caps, 20 bps per side):

| | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|---|---|---|---|
| SPY | -5% | +31% | +18% | +29% | -18% | +26% | +25% | +18% | +2% |
| equal-weight group | -5% | +29% | +14% | +31% | -4% | +16% | +16% | +17% | +12% |
| top5, in RS>=0.8, out RS<0.5 | -3% | +14% | +12% | +21% | +0% | +11% | +37% | +15% | +30% |
| top5, in RS>=0.8, out RS<0.5, stop -20% | -2% | +14% | +12% | +22% | -0% | +14% | +36% | +14% | +30% |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d | +2% | +3% | +16% | +21% | -1% | +21% | +19% | +9% | +3% |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | +2% | +3% | +16% | +22% | -1% | +21% | +19% | +9% | +3% |
| top5, in RS>=0.8, out RS<0.7 | -4% | +8% | +7% | +21% | -4% | +19% | +30% | -2% | +25% |
| top5, in RS>=0.8, out RS<0.7, stop -20% | -4% | +7% | +9% | +22% | +10% | +21% | +30% | -2% | +26% |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d | +2% | -3% | +8% | +21% | -2% | +22% | +29% | -5% | +6% |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | +2% | -3% | +8% | +21% | -2% | +22% | +29% | -5% | +6% |
| top8, in RS>=0.8, out RS<0.5 | -8% | +8% | +17% | +28% | +0% | +23% | +27% | +22% | +14% |
| top8, in RS>=0.8, out RS<0.5, stop -20% | -8% | +8% | +11% | +33% | +1% | +20% | +22% | +23% | +10% |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d | +0% | -5% | +11% | +30% | -2% | +14% | +13% | +14% | -3% |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | +0% | -4% | +11% | +30% | -2% | +14% | +13% | +14% | -3% |
| top8, in RS>=0.8, out RS<0.7 | -6% | +9% | +17% | +18% | +2% | +20% | +25% | +6% | +15% |
| top8, in RS>=0.8, out RS<0.7, stop -20% | -6% | +6% | +13% | +18% | +6% | +21% | +25% | +5% | +15% |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d | +2% | +2% | +12% | +18% | -4% | +9% | +24% | +2% | +6% |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | +2% | +2% | +12% | +18% | -4% | +9% | +24% | +1% | +6% |
| top8, in RS>=0.8, out RS<0.5, 12-1 month momentum | -14% | +10% | +2% | +24% | -12% | +2% | +41% | -1% | -3% |
| top8, in RS>=0.8, out RS<0.5, monthly | +8% | +12% | +16% | +19% | -5% | +26% | +23% | +5% | +11% |
| top8, in RS>=0.8, out RS<0.5, volatility-adjusted | -2% | +16% | +3% | +22% | -8% | +18% | +38% | +20% | +4% |
| top8, in RS>=0.8, out RS<0.5, max 2/sector | -7% | +7% | +4% | +29% | -0% | +19% | +17% | +10% | +19% |
| top8, in RS>=0.8, out RS<0.5, max 3/sector | -8% | +8% | +10% | +29% | -1% | +24% | +22% | +18% | +16% |
| top8, in RS>=0.8, out RS<0.5, sell below 50d | -5% | +3% | +28% | +21% | +6% | +7% | +4% | +2% | -11% |
| top8, in RS>=0.8, out RS<0.5, sell below 50d after +30% over 200d | -4% | +10% | +26% | +13% | +6% | +22% | +7% | +6% | -5% |

## Rockets (from 2016-12-13, 20 bps per side, 10 slots x 10%, max 3 new per day)

Rocket day: close >= +jump vs previous close, volume >= 3x the 20-day average, close in the top quarter of the day's range, price >= $5, 20-day dollar volume >= $5M. Buy next open; sell next open after a close more than `trail` below the highest close, or after 40 sessions. 'Random' = same stocks, same liquidity filter, same exit, random dates.

SPY: +13.6%/yr, max DD -34%, Sharpe 0.80 · train+val +14.5%/yr, Sharpe 0.83

| variant | trades | win% | avg trade | median | ≥+50% | worst | random avg | excess vs random t (train+val) | 2015 large caps excess | CAGR | max DD | Sharpe | train+val CAGR / Sharpe | OOS CAGR | random-entry portfolio CAGR | without top 3 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| EPS surprise>0%, reaction>=5% | 1926 | 53 | +4.4% | +1.8% | 4.3% | -51% | +4.1% | -0.26% (-0.38) | -0.07% (n=565) | +5.4% | -40% | 0.35 | +10.6% / 0.58 | -14.1% | +11.5% | +5.4% |
| EPS surprise>0%, reaction>=10% | 940 | 52 | +5.8% | +1.5% | 6.2% | -51% | +4.1% | +1.01% (0.97) | +1.43% (n=131) | +21.4% | -43% | 0.90 | +24.1% / 1.01 | +5.3% | +11.5% | +20.5% |
| EPS surprise>10%, reaction>=5% | 1280 | 53 | +4.8% | +1.9% | 4.9% | -51% | +4.1% | +0.63% (0.73) | -0.47% (n=271) | +12.3% | -45% | 0.60 | +22.3% / 0.97 | -22.2% | +11.5% | +12.8% |
| EPS surprise>10%, reaction>=10% | 725 | 52 | +6.0% | +1.3% | 6.2% | -51% | +4.1% | +1.92% (1.55) | +1.72% (n=73) | +16.2% | -48% | 0.71 | +25.9% / 1.02 | -20.6% | +11.5% | +13.0% |
| EPS surprise>20%, reaction>=10%, volume>=2x, RS>=0.8 | 244 | 55 | +8.4% | +2.8% | 7.0% | -36% | +4.1% | +3.63% (1.66) | +3.91% (n=14) | +17.6% | -27% | 0.90 | +23.9% / 1.20 | -9.7% | +11.5% | +11.5% |
| EPS surprise>20%, reaction>=15%, volume>=2x, RS>=0.8 | 174 | 56 | +8.3% | +2.7% | 8.1% | -36% | +4.1% | +1.91% (0.79) | —% (n=4) | +14.4% | -24% | 0.86 | +19.0% / 1.15 | -6.2% | +11.5% | +9.2% |
| EPS surprise>20%, reaction>=10%, volume>=2x, RS>=0.8, trail 10% | 246 | 43 | +3.8% | -3.3% | 3.7% | -21% | +4.1% | -1.63% (-0.98) | +1.76% (n=14) | +8.9% | -16% | 0.77 | +12.1% / 1.00 | -4.1% | +11.5% | +5.1% |
| EPS surprise>20%, reaction>=10%, volume>=2x, RS>=0.8, trail 15% | 245 | 51 | +7.1% | +0.1% | 4.9% | -29% | +4.1% | +3.09% (1.58) | +2.93% (n=14) | +16.8% | -19% | 1.03 | +21.3% / 1.27 | -0.8% | +11.5% | +12.2% |
| EPS surprise>20%, reaction>=10%, volume>=2x, RS>=0.8, take-profit +30% | 244 | 59 | +6.0% | +5.1% | 0.4% | -36% | +4.1% | +2.72% (1.50) | +4.33% (n=14) | +12.1% | -25% | 0.77 | +18.6% / 1.16 | -11.3% | +11.5% | +9.9% |
| EPS surprise>20%, reaction>=10%, volume>=2x, RS>=0.8, take-profit +50% | 244 | 55 | +6.4% | +2.8% | 10.2% | -36% | +4.1% | +2.38% (1.22) | +5.69% (n=14) | +12.9% | -26% | 0.76 | +18.4% / 1.05 | -10.3% | +11.5% | +9.5% |
| EPS surprise>20%, reaction>=10%, volume>=2x, RS>=0.8, trail 15%, take-profit +30% | 245 | 51 | +5.4% | +0.1% | 0.4% | -29% | +4.1% | +2.14% (1.24) | +3.25% (n=14) | +12.4% | -17% | 0.94 | +17.1% / 1.25 | -4.9% | +11.5% | +9.8% |
| EPS surprise>0%, reaction>=10%, max 5 days | 958 | 50 | +0.1% | -0.1% | 0.1% | -29% | +4.1% | -4.27% (-3.97) | -2.16% (n=133) | -1.0% | -31% | -0.02 | +3.1% / 0.33 | -17.0% | +11.5% | -2.1% |
| EPS surprise>0%, reaction>=10%, max 10 days | 952 | 54 | +0.8% | +1.2% | 0.6% | -51% | +4.1% | -3.32% (-3.11) | -1.28% (n=133) | +8.6% | -26% | 0.59 | +10.6% / 0.73 | +0.2% | +11.5% | +5.2% |
| EPS surprise>0%, reaction>=10%, max 20 days | 943 | 54 | +1.8% | +1.3% | 0.9% | -51% | +4.1% | -2.50% (-2.85) | -0.23% (n=131) | +8.4% | -25% | 0.53 | +11.9% / 0.70 | -5.8% | +11.5% | +6.9% |
| jump>=8%, trail 15% | 999 | 45 | +4.0% | -2.6% | 5.3% | -52% | +2.2% | -0.35% (-0.33) | -1.30% (n=114) | +14.8% | -48% | 0.60 | +22.8% / 0.81 | -14.2% | +17.6% | +9.1% |
| jump>=8%, trail 25% | 995 | 51 | +5.4% | +0.7% | 6.8% | -61% | +2.8% | +0.24% (0.21) | -1.22% (n=114) | +14.9% | -68% | 0.59 | +20.9% / 0.75 | -8.6% | +11.6% | +10.9% |
| jump>=15%, trail 15% | 545 | 43 | +4.6% | -4.6% | 6.8% | -52% | +2.2% | -0.77% (-0.53) | -4.26% (n=24) | +17.8% | -38% | 0.70 | +21.5% / 0.79 | +4.1% | +17.6% | +11.5% |
| jump>=15%, trail 25% | 543 | 47 | +6.6% | -1.9% | 9.2% | -61% | +2.8% | +0.63% (0.35) | -4.50% (n=24) | +14.5% | -60% | 0.57 | +20.1% / 0.70 | -6.4% | +11.6% | +6.2% |

Pre-registered gates: excess vs random entries t >= 2 (train+val); portfolio beats SPY on train+val CAGR and Sharpe; positive excess among 2015 large caps; CAGR without the 3 best stocks >= SPY's; max drawdown >= -50%.

**Chosen: none — no rocket variant passed every gate**

| variant | passes | failed gates |
|---|---|---|
| EPS surprise>0%, reaction>=5% | ❌ | beats_random_entries_same_stocks, beats_spy_train_val, holds_in_2015_largecaps, without_top3_beats_spy |
| EPS surprise>0%, reaction>=10% | ❌ | beats_random_entries_same_stocks |
| EPS surprise>10%, reaction>=5% | ❌ | beats_random_entries_same_stocks, holds_in_2015_largecaps, without_top3_beats_spy |
| EPS surprise>10%, reaction>=10% | ❌ | beats_random_entries_same_stocks, without_top3_beats_spy |
| EPS surprise>20%, reaction>=10%, volume>=2x, RS>=0.8 | ❌ | beats_random_entries_same_stocks, without_top3_beats_spy |
| EPS surprise>20%, reaction>=15%, volume>=2x, RS>=0.8 | ❌ | beats_random_entries_same_stocks, holds_in_2015_largecaps, without_top3_beats_spy |
| EPS surprise>20%, reaction>=10%, volume>=2x, RS>=0.8, trail 10% | ❌ | beats_random_entries_same_stocks, beats_spy_train_val, without_top3_beats_spy |
| EPS surprise>20%, reaction>=10%, volume>=2x, RS>=0.8, trail 15% | ❌ | beats_random_entries_same_stocks, without_top3_beats_spy |
| EPS surprise>20%, reaction>=10%, volume>=2x, RS>=0.8, take-profit +30% | ❌ | beats_random_entries_same_stocks, without_top3_beats_spy |
| EPS surprise>20%, reaction>=10%, volume>=2x, RS>=0.8, take-profit +50% | ❌ | beats_random_entries_same_stocks, without_top3_beats_spy |
| EPS surprise>20%, reaction>=10%, volume>=2x, RS>=0.8, trail 15%, take-profit +30% | ❌ | beats_random_entries_same_stocks, without_top3_beats_spy |
| EPS surprise>0%, reaction>=10%, max 5 days | ❌ | beats_random_entries_same_stocks, beats_spy_train_val, holds_in_2015_largecaps, without_top3_beats_spy |
| EPS surprise>0%, reaction>=10%, max 10 days | ❌ | beats_random_entries_same_stocks, beats_spy_train_val, holds_in_2015_largecaps, without_top3_beats_spy |
| EPS surprise>0%, reaction>=10%, max 20 days | ❌ | beats_random_entries_same_stocks, beats_spy_train_val, holds_in_2015_largecaps, without_top3_beats_spy |
| jump>=8%, trail 15% | ❌ | beats_random_entries_same_stocks, beats_spy_train_val, holds_in_2015_largecaps, without_top3_beats_spy |
| jump>=8%, trail 25% | ❌ | beats_random_entries_same_stocks, beats_spy_train_val, holds_in_2015_largecaps, without_top3_beats_spy, drawdown_tolerable |
| jump>=15%, trail 15% | ❌ | beats_random_entries_same_stocks, beats_spy_train_val, holds_in_2015_largecaps, without_top3_beats_spy |
| jump>=15%, trail 25% | ❌ | beats_random_entries_same_stocks, beats_spy_train_val, holds_in_2015_largecaps, without_top3_beats_spy, drawdown_tolerable |

## Mean R by year (all universe, fixed exit)

| group | policy | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| combined | all | +0.77 | -0.45 | +0.30 | +1.07 | +0.03 | -0.44 | +0.53 | +0.42 | +0.23 | -0.15 |
| combined | SPY>200d & stock>200d | +0.87 | -0.44 | +0.03 | +0.94 | -0.03 | -0.79 | +0.38 | +0.42 | +0.19 | -0.14 |
| combined | SPY>200d & stock>200d & RS>=0.8 | +0.91 | -0.23 | +0.35 | +1.46 | -0.42 | -0.36 | +0.35 | +0.60 | +0.83 | -0.05 |
| combined | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | +0.94 | -0.08 | +0.45 | +1.36 | -0.52 | -0.07 | +0.30 | +0.46 | +0.81 | +0.16 |
| combined | score>=70 & SPY>200d & stock>200d | +0.61 | +0.65 | +0.42 | +1.15 | -0.54 | -0.96 | +0.43 | +0.69 | +0.52 | -0.12 |
| combined | score>=70 & SPY>200d & stock>200d & RS>=0.8 | +0.02 | +1.33 | +0.61 | +1.08 | -0.53 | -1.15 | +0.41 | +1.00 | +0.70 | -0.12 |
| baseline_random | all | +1.33 | +0.04 | +0.55 | +0.98 | +0.15 | -0.28 | +0.61 | +0.42 | +0.30 | -0.00 |
| baseline_random | SPY>200d & stock>200d | +1.46 | -0.27 | +0.52 | +0.86 | +0.16 | -0.78 | +0.27 | +0.42 | +0.21 | -0.03 |
| baseline_random | SPY>200d & stock>200d & RS>=0.8 | +1.14 | +0.07 | +0.65 | +1.17 | -0.25 | -0.74 | +0.47 | +0.51 | +0.41 | -0.15 |
| baseline_random | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | +1.04 | +0.22 | +0.73 | +0.94 | -0.29 | -0.63 | +0.55 | +0.60 | +0.65 | -0.18 |