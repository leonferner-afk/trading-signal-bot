# Strategy research

267 symbols with data (1 failed), 10 years of daily bars. Control group: 93 stocks that were already large caps in 2015. Primary cost 40 bps per side (Swedish retail: courtage + FX + slippage). Validation from 2023-01-21, out-of-sample (OOS) from 2024-11-22. Setups invalidated at the next open (skipped): 1287.

Portfolio: max 8 positions, max 3 new per day, 1% risk per trade, max 25% of equity per position, no leverage, marked to market daily. 'vs random' = share of 40 random-order portfolios from the same eligible trades that this ranking beat.

## Portfolio — universe: all

SPY buy-and-hold: +15.0%/yr, max DD -34%, Sharpe 0.85 · train+val Sharpe 0.81 · OOS +16.7%/yr, Sharpe 1.0

| rule set | trades/yr | exposure | win% | avgR | CAGR | max DD | Sharpe | train+val Sharpe | OOS CAGR | OOS Sharpe | vs random |
|---|---|---|---|---|---|---|---|---|---|---|---|
| random picks (reference) | 76.0 | 86% | 23 | +0.11 | +3.2% | -68% | 0.26 | 0.36 | -8.9% | -0.12 | — |
| random picks, trend filter | 64.2 | 78% | 23 | +0.26 | +14.7% | -49% | 0.67 | 0.90 | -11.8% | -0.27 | — |
| RS leaders, trend filter | 72.4 | 67% | 23 | +0.36 | +20.1% | -39% | 0.72 | 0.81 | +0.8% | 0.23 | 100% |
| RS leaders near 52w high | 65.7 | 75% | 25 | +0.52 | +23.3% | -37% | 0.84 | 0.88 | +27.6% | 0.81 | 100% |
| signals score>=70, trend | 46.7 | 63% | 21 | +0.23 | +8.0% | -37% | 0.47 | 0.62 | -8.3% | -0.18 | 10% |
| signals score>=70, trend, RS top 20% | 40.9 | 51% | 23 | +0.49 | +16.8% | -39% | 0.81 | 0.90 | +11.3% | 0.54 | 80% |
| signals, trend, RS top 20% | 79.5 | 77% | 21 | +0.53 | +29.4% | -56% | 0.92 | 0.95 | +36.9% | 0.97 | 100% |
| signals, trend, RS top 20%, near 52w high | 77.2 | 78% | 21 | +0.36 | +17.2% | -50% | 0.68 | 0.74 | +17.4% | 0.62 | 85% |

Cost sensitivity (full-period CAGR / Sharpe):

| rule set | 15 bps | 40 bps | 70 bps |
|---|---|---|---|
| RS leaders, trend filter | +21.0% / 0.76 | +20.1% / 0.72 | +14.0% / 0.57 |
| RS leaders near 52w high | +28.6% / 0.98 | +23.3% / 0.84 | +16.6% / 0.66 |
| signals score>=70, trend | +11.7% / 0.63 | +8.0% / 0.47 | +4.2% / 0.30 |
| signals score>=70, trend, RS top 20% | +20.0% / 0.94 | +16.8% / 0.81 | +13.0% / 0.66 |
| signals, trend, RS top 20% | +36.6% / 1.08 | +29.4% / 0.92 | +21.1% / 0.73 |
| signals, trend, RS top 20%, near 52w high | +23.3% / 0.85 | +17.2% / 0.68 | +11.5% / 0.51 |

Exit variant (stop 2.5 x ATR instead of 1.5 x ATR / structural):

| rule set | CAGR | max DD | Sharpe | OOS Sharpe |
|---|---|---|---|---|
| random picks (reference) | +8.3% | -48% | 0.49 | -0.34 |
| random picks, trend filter | +7.5% | -38% | 0.49 | -0.26 |
| RS leaders, trend filter | +14.7% | -29% | 0.72 | 0.38 |
| RS leaders near 52w high | +24.5% | -26% | 1.07 | 0.60 |
| signals score>=70, trend | +8.7% | -32% | 0.58 | -0.23 |
| signals score>=70, trend, RS top 20% | +16.5% | -29% | 0.98 | 0.67 |
| signals, trend, RS top 20% | +11.5% | -43% | 0.60 | 0.54 |
| signals, trend, RS top 20%, near 52w high | +12.1% | -34% | 0.63 | 0.37 |

### Per trade — universe: all (one position per symbol, t over monthly means)

| group | exit | policy | n | win% | avgR | medR | t | excess vs random (t) | ≥+50% | OOS n | OOS avgR |
|---|---|---|---|---|---|---|---|---|---|---|---|
| breakout | fixed | all | 6294 | 17 | +0.119 | -1.23 | -0.24 | -0.408 (-4.60) | 3.2% | 1422 | -0.167 |
| breakout | fixed | SPY>200d & stock>200d | 5004 | 17 | +0.064 | -1.24 | -1.04 | -0.301 (-4.09) | 3.0% | 1144 | -0.158 |
| breakout | fixed | SPY>200d & stock>200d & RS>=0.8 | 2074 | 18 | +0.284 | -1.17 | 0.48 | -0.278 (-2.62) | 5.4% | 502 | +0.397 |
| breakout | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1691 | 18 | +0.300 | -1.18 | 0.49 | -0.178 (-1.47) | 4.4% | 385 | +0.537 |
| breakout | fixed | score>=70 & SPY>200d & stock>200d | 743 | 23 | +0.419 | -1.06 | 2.15 | +0.113 (0.75) | 5.8% | 155 | +0.150 |
| breakout | fixed | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 445 | 24 | +0.583 | -1.02 | 2.91 | +0.232 (1.06) | 7.6% | 101 | +0.348 |
| momentum | fixed | all | 5163 | 22 | +0.187 | -1.12 | 0.92 | -0.300 (-3.92) | 3.7% | 1164 | -0.070 |
| momentum | fixed | SPY>200d & stock>200d | 4558 | 22 | +0.223 | -1.13 | 1.07 | -0.085 (-1.33) | 3.5% | 1055 | -0.052 |
| momentum | fixed | SPY>200d & stock>200d & RS>=0.8 | 1848 | 23 | +0.318 | -1.08 | 1.78 | -0.123 (-1.55) | 6.3% | 441 | +0.179 |
| momentum | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1518 | 23 | +0.324 | -1.11 | 1.65 | -0.051 (-0.57) | 4.7% | 349 | +0.159 |
| momentum | fixed | score>=70 & SPY>200d & stock>200d | 153 | 24 | +0.526 | -0.95 | 1.99 | +0.393 (1.37) | 13.1% | 38 | +0.988 |
| momentum | fixed | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 93 | 24 | +0.582 | -0.93 | 1.36 | +0.020 (0.06) | 15.0% | 27 | +1.046 |
| combined | fixed | all | 7889 | 19 | +0.143 | -1.17 | 0.19 | -0.364 (-4.98) | 3.4% | 1758 | -0.002 |
| combined | fixed | SPY>200d & stock>200d | 6501 | 19 | +0.113 | -1.17 | -0.44 | -0.220 (-3.56) | 3.1% | 1475 | -0.015 |
| combined | fixed | SPY>200d & stock>200d & RS>=0.8 | 2720 | 20 | +0.285 | -1.13 | 0.99 | -0.218 (-2.75) | 5.5% | 654 | +0.438 |
| combined | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 2230 | 21 | +0.283 | -1.14 | 1.04 | -0.117 (-1.34) | 4.4% | 505 | +0.440 |
| combined | fixed | score>=70 & SPY>200d & stock>200d | 816 | 23 | +0.446 | -1.04 | 1.96 | +0.104 (0.76) | 6.5% | 176 | +0.239 |
| combined | fixed | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 487 | 24 | +0.569 | -1.01 | 2.56 | +0.161 (0.80) | 8.4% | 115 | +0.428 |
| baseline_random | fixed | all | 17001 | 24 | +0.272 | -1.08 | 4.03 | — (—) | 5.0% | 3905 | +0.131 |
| baseline_random | fixed | SPY>200d & stock>200d | 10850 | 23 | +0.236 | -1.12 | 2.09 | — (—) | 3.6% | 2513 | +0.073 |
| baseline_random | fixed | SPY>200d & stock>200d & RS>=0.8 | 4368 | 23 | +0.317 | -1.09 | 3.02 | — (—) | 6.3% | 1070 | +0.236 |
| baseline_random | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 2964 | 24 | +0.369 | -1.12 | 2.49 | — (—) | 4.2% | 649 | +0.265 |
| breakout | wide | all | 5051 | 33 | +0.253 | -0.99 | 2.55 | -0.174 (-3.11) | 5.6% | 1125 | +0.185 |
| breakout | wide | SPY>200d & stock>200d | 4071 | 33 | +0.259 | -1.01 | 1.72 | -0.077 (-1.56) | 5.1% | 917 | +0.204 |
| breakout | wide | SPY>200d & stock>200d & RS>=0.8 | 1734 | 35 | +0.409 | -0.96 | 2.48 | -0.105 (-1.68) | 9.2% | 413 | +0.405 |
| breakout | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1440 | 35 | +0.430 | -0.97 | 2.71 | -0.029 (-0.46) | 7.5% | 324 | +0.349 |
| breakout | wide | score>=70 & SPY>200d & stock>200d | 716 | 33 | +0.359 | -0.96 | 2.39 | +0.031 (0.29) | 8.9% | 148 | +0.148 |
| breakout | wide | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 423 | 35 | +0.494 | -0.92 | 3.03 | +0.077 (0.49) | 11.6% | 94 | +0.343 |
| momentum | wide | all | 4297 | 32 | +0.218 | -1.02 | 2.03 | -0.204 (-3.50) | 4.9% | 937 | +0.085 |
| momentum | wide | SPY>200d & stock>200d | 3815 | 32 | +0.256 | -1.02 | 2.11 | -0.038 (-0.74) | 4.7% | 855 | +0.104 |
| momentum | wide | SPY>200d & stock>200d & RS>=0.8 | 1554 | 33 | +0.325 | -1.00 | 2.09 | -0.139 (-2.40) | 8.0% | 364 | +0.232 |
| momentum | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1304 | 33 | +0.295 | -1.01 | 1.66 | -0.128 (-2.06) | 5.8% | 287 | +0.218 |
| momentum | wide | score>=70 & SPY>200d & stock>200d | 137 | 31 | +0.299 | -0.91 | 1.31 | +0.050 (0.26) | 15.3% | 32 | +0.732 |
| momentum | wide | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 79 | 30 | +0.363 | -0.86 | 0.98 | -0.178 (-0.73) | 20.2% | 22 | +0.890 |
| combined | wide | all | 5991 | 33 | +0.235 | -1.01 | 2.43 | -0.191 (-3.73) | 5.3% | 1322 | +0.149 |
| combined | wide | SPY>200d & stock>200d | 5009 | 33 | +0.253 | -1.02 | 1.69 | -0.073 (-1.72) | 5.0% | 1129 | +0.163 |
| combined | wide | SPY>200d & stock>200d & RS>=0.8 | 2173 | 33 | +0.339 | -0.99 | 2.05 | -0.143 (-2.83) | 8.4% | 522 | +0.328 |
| combined | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1811 | 34 | +0.337 | -1.00 | 2.15 | -0.079 (-1.51) | 6.7% | 405 | +0.279 |
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
| random picks (reference) | 43.8 | 87% | 23 | +0.05 | +3.6% | -32% | 0.30 | 0.30 | -3.5% | -0.15 | — |
| random picks, trend filter | 34.6 | 77% | 25 | +0.23 | +3.7% | -21% | 0.34 | 0.41 | -3.8% | -0.18 | — |
| RS leaders, trend filter | 42.6 | 76% | 25 | +0.30 | +11.1% | -32% | 0.63 | 0.76 | +3.2% | 0.26 | 100% |
| RS leaders near 52w high | 40.5 | 76% | 24 | +0.15 | +4.8% | -31% | 0.34 | 0.52 | -5.3% | -0.16 | 78% |
| signals score>=70, trend | 15.2 | 37% | 24 | +0.17 | +1.4% | -21% | 0.20 | 0.21 | +3.4% | 0.40 | 25% |
| signals score>=70, trend, RS top 20% | 10.4 | 24% | 21 | +0.09 | +0.8% | -20% | 0.14 | 0.23 | +1.2% | 0.19 | 0% |
| signals, trend, RS top 20% | 43.2 | 76% | 22 | +0.28 | +5.8% | -39% | 0.43 | 0.56 | -0.7% | 0.06 | 95% |
| signals, trend, RS top 20%, near 52w high | 42.6 | 75% | 22 | +0.24 | +4.0% | -39% | 0.33 | 0.44 | -1.2% | 0.02 | 93% |

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
| random picks (reference) | +6.7% | -25% | 0.50 | -0.00 |
| random picks, trend filter | +2.0% | -23% | 0.23 | -0.37 |
| RS leaders, trend filter | +10.8% | -24% | 0.66 | -0.28 |
| RS leaders near 52w high | +9.6% | -23% | 0.62 | -0.47 |
| signals score>=70, trend | +0.6% | -22% | 0.12 | 0.38 |
| signals score>=70, trend, RS top 20% | +1.3% | -20% | 0.21 | 0.36 |
| signals, trend, RS top 20% | +7.8% | -28% | 0.57 | 0.07 |
| signals, trend, RS top 20%, near 52w high | +4.8% | -32% | 0.39 | 0.06 |

### Per trade — universe: largecap_2015 (one position per symbol, t over monthly means)

| group | exit | policy | n | win% | avgR | medR | t | excess vs random (t) | ≥+50% | OOS n | OOS avgR |
|---|---|---|---|---|---|---|---|---|---|---|---|
| breakout | fixed | all | 2041 | 17 | -0.178 | -1.35 | -2.01 | -0.549 (-4.36) | 0.2% | 399 | -0.517 |
| breakout | fixed | SPY>200d & stock>200d | 1690 | 16 | -0.249 | -1.37 | -2.25 | -0.384 (-3.48) | 0.1% | 333 | -0.540 |
| breakout | fixed | SPY>200d & stock>200d & RS>=0.8 | 668 | 19 | +0.078 | -1.31 | -0.28 | -0.160 (-0.95) | 0.1% | 142 | -0.118 |
| breakout | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 627 | 19 | +0.093 | -1.31 | -0.30 | -0.184 (-1.06) | 0.2% | 138 | -0.073 |
| breakout | fixed | score>=70 & SPY>200d & stock>200d | 153 | 22 | +0.087 | -1.13 | 0.45 | -0.045 (-0.17) | 0.0% | 27 | +0.354 |
| breakout | fixed | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 99 | 22 | +0.136 | -1.12 | 0.48 | -0.105 (-0.33) | 0.0% | 16 | +0.323 |
| momentum | fixed | all | 1944 | 23 | +0.084 | -1.21 | -0.02 | -0.267 (-2.78) | 0.1% | 385 | -0.175 |
| momentum | fixed | SPY>200d & stock>200d | 1736 | 23 | +0.119 | -1.22 | -0.00 | -0.059 (-0.62) | 0.1% | 355 | -0.120 |
| momentum | fixed | SPY>200d & stock>200d & RS>=0.8 | 727 | 23 | +0.157 | -1.18 | 0.05 | -0.107 (-0.91) | 0.0% | 152 | -0.062 |
| momentum | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 690 | 23 | +0.166 | -1.19 | 0.21 | -0.098 (-0.81) | 0.0% | 147 | -0.043 |
| momentum | fixed | score>=70 & SPY>200d & stock>200d | 14 | 21 | +0.084 | -1.09 | 0.39 | +0.092 (0.11) | 0.0% | 2 | -1.172 |
| momentum | fixed | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 6 | 17 | +0.170 | -1.00 | 0.14 | -0.300 (-0.30) | 0.0% | 2 | -1.172 |
| combined | fixed | all | 2766 | 20 | -0.060 | -1.27 | -1.40 | -0.426 (-4.41) | 0.2% | 532 | -0.299 |
| combined | fixed | SPY>200d & stock>200d | 2372 | 20 | -0.089 | -1.27 | -1.74 | -0.253 (-2.91) | 0.1% | 460 | -0.281 |
| combined | fixed | SPY>200d & stock>200d & RS>=0.8 | 983 | 20 | +0.066 | -1.22 | -0.67 | -0.166 (-1.50) | 0.0% | 198 | -0.135 |
| combined | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 928 | 20 | +0.076 | -1.23 | -0.57 | -0.164 (-1.46) | 0.0% | 193 | -0.097 |
| combined | fixed | score>=70 & SPY>200d & stock>200d | 163 | 23 | +0.130 | -1.12 | 0.71 | +0.016 (0.06) | 0.0% | 29 | +0.249 |
| combined | fixed | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 103 | 22 | +0.180 | -1.09 | 0.63 | -0.056 (-0.18) | 0.0% | 18 | +0.157 |
| baseline_random | fixed | all | 6516 | 25 | +0.195 | -1.16 | 3.03 | — (—) | 0.7% | 1295 | +0.105 |
| baseline_random | fixed | SPY>200d & stock>200d | 4338 | 23 | +0.125 | -1.20 | 1.01 | — (—) | 0.3% | 866 | +0.037 |
| baseline_random | fixed | SPY>200d & stock>200d & RS>=0.8 | 1694 | 23 | +0.150 | -1.17 | 0.88 | — (—) | 0.5% | 373 | -0.110 |
| baseline_random | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1496 | 23 | +0.158 | -1.18 | 0.83 | — (—) | 0.2% | 324 | -0.061 |
| breakout | wide | all | 1749 | 33 | +0.111 | -1.07 | 0.65 | -0.252 (-3.34) | 0.3% | 332 | +0.028 |
| breakout | wide | SPY>200d & stock>200d | 1445 | 33 | +0.124 | -1.08 | 0.79 | -0.042 (-0.58) | 0.2% | 278 | +0.096 |
| breakout | wide | SPY>200d & stock>200d & RS>=0.8 | 592 | 35 | +0.242 | -1.04 | 1.29 | -0.081 (-0.80) | 0.2% | 126 | +0.033 |
| breakout | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 559 | 34 | +0.235 | -1.04 | 0.95 | -0.102 (-1.18) | 0.0% | 122 | +0.043 |
| breakout | wide | score>=70 & SPY>200d & stock>200d | 153 | 31 | +0.080 | -0.99 | 0.16 | -0.105 (-0.59) | 0.0% | 27 | +0.296 |
| breakout | wide | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 99 | 31 | +0.198 | -0.99 | 0.73 | -0.192 (-0.88) | 0.0% | 16 | +0.463 |
| momentum | wide | all | 1654 | 32 | +0.123 | -1.09 | 0.88 | -0.229 (-2.95) | 0.1% | 320 | -0.014 |
| momentum | wide | SPY>200d & stock>200d | 1480 | 33 | +0.158 | -1.09 | 1.15 | +0.005 (0.07) | 0.1% | 296 | +0.028 |
| momentum | wide | SPY>200d & stock>200d & RS>=0.8 | 629 | 33 | +0.186 | -1.06 | 1.15 | -0.089 (-0.99) | 0.0% | 131 | -0.062 |
| momentum | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 599 | 33 | +0.190 | -1.06 | 1.03 | -0.075 (-0.93) | 0.0% | 128 | -0.050 |
| momentum | wide | score>=70 & SPY>200d & stock>200d | 13 | 31 | +0.022 | -0.98 | 0.39 | +0.128 (0.23) | 0.0% | 2 | -1.102 |
| momentum | wide | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 5 | 40 | +0.487 | -0.98 | 0.49 | +0.052 (0.06) | 0.0% | 2 | -1.102 |
| combined | wide | all | 2189 | 33 | +0.107 | -1.08 | 0.75 | -0.244 (-3.43) | 0.3% | 415 | +0.005 |
| combined | wide | SPY>200d & stock>200d | 1890 | 33 | +0.121 | -1.09 | 0.89 | -0.031 (-0.49) | 0.2% | 367 | +0.060 |
| combined | wide | SPY>200d & stock>200d & RS>=0.8 | 806 | 34 | +0.216 | -1.05 | 1.44 | -0.050 (-0.61) | 0.0% | 165 | -0.057 |
| combined | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 764 | 34 | +0.220 | -1.06 | 1.35 | -0.025 (-0.35) | 0.0% | 161 | -0.044 |
| combined | wide | score>=70 & SPY>200d & stock>200d | 162 | 31 | +0.097 | -0.98 | 0.49 | -0.053 (-0.30) | 0.0% | 29 | +0.200 |
| combined | wide | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 102 | 31 | +0.221 | -0.99 | 0.84 | -0.170 (-0.79) | 0.0% | 18 | +0.289 |
| baseline_random | wide | all | 4607 | 37 | +0.242 | -1.00 | 4.23 | — (—) | 0.8% | 883 | +0.202 |
| baseline_random | wide | SPY>200d & stock>200d | 3156 | 34 | +0.180 | -1.06 | 1.87 | — (—) | 0.2% | 644 | +0.119 |
| baseline_random | wide | SPY>200d & stock>200d & RS>=0.8 | 1288 | 36 | +0.260 | -1.03 | 2.22 | — (—) | 0.5% | 274 | +0.040 |
| baseline_random | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1155 | 36 | +0.267 | -1.04 | 2.01 | — (—) | 0.3% | 239 | +0.064 |

## Mean R by year (all universe, fixed exit)

| group | policy | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| combined | all | +0.64 | -0.61 | +0.17 | +0.90 | -0.12 | -0.55 | +0.40 | +0.28 | +0.13 | -0.11 |
| combined | SPY>200d & stock>200d | +0.68 | -0.58 | -0.12 | +0.79 | -0.17 | -0.95 | +0.24 | +0.32 | +0.09 | -0.08 |
| combined | SPY>200d & stock>200d & RS>=0.8 | +0.66 | -0.34 | +0.17 | +1.37 | -0.56 | -0.55 | +0.18 | +0.55 | +0.70 | +0.14 |
| combined | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | +0.70 | -0.21 | +0.24 | +1.23 | -0.62 | -0.26 | +0.13 | +0.42 | +0.65 | +0.32 |
| combined | score>=70 & SPY>200d & stock>200d | +0.99 | +0.55 | +0.39 | +1.05 | -0.60 | -1.04 | +0.36 | +0.65 | +0.48 | +0.06 |
| combined | score>=70 & SPY>200d & stock>200d & RS>=0.8 | +0.84 | +1.54 | +0.65 | +0.99 | -0.58 | -1.22 | +0.26 | +0.92 | +0.67 | +0.16 |
| baseline_random | all | +0.91 | -0.02 | +0.45 | +0.93 | +0.05 | -0.35 | +0.54 | +0.35 | +0.24 | +0.12 |
| baseline_random | SPY>200d & stock>200d | +0.91 | -0.34 | +0.39 | +0.79 | +0.07 | -0.90 | +0.19 | +0.35 | +0.14 | +0.10 |
| baseline_random | SPY>200d & stock>200d & RS>=0.8 | +1.10 | +0.05 | +0.51 | +1.13 | -0.34 | -0.85 | +0.41 | +0.47 | +0.38 | +0.12 |
| baseline_random | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | +0.96 | +0.23 | +0.58 | +0.97 | -0.38 | -0.75 | +0.44 | +0.60 | +0.57 | +0.02 |