# Strategy research

278 symbols with data (1 failed), 10 years of daily bars. Control group: 105 stocks that were already large caps in 2015. Primary cost 20 bps per side (USD account: courtage + slippage; 40 bps ≈ trading from a SEK account). Validation from 2023-02-19, out-of-sample (OOS) from 2024-12-21. Setups invalidated at the next open (skipped): 1304.

Portfolio: max 8 positions, max 3 new per day, 1% risk per trade, max 25% of equity per position, no leverage, marked to market daily. 'vs random' = share of 40 random-order portfolios from the same eligible trades that this ranking beat.

## Portfolio — universe: all

SPY buy-and-hold: +15.1%/yr, max DD -34%, Sharpe 0.85 · train+val Sharpe 0.82 · OOS +16.0%/yr, Sharpe 0.97

| rule set | trades/yr | exposure | win% | avgR | CAGR | max DD | Sharpe | train+val Sharpe | OOS CAGR | OOS Sharpe | vs random |
|---|---|---|---|---|---|---|---|---|---|---|---|
| random picks (reference) | 77.5 | 87% | 20 | +0.15 | +6.9% | -62% | 0.37 | 0.60 | -21.5% | -0.61 | — |
| random picks, trend filter | 68.6 | 78% | 22 | +0.36 | +15.6% | -39% | 0.67 | 0.75 | +12.6% | 0.52 | — |
| RS leaders, trend filter | 70.7 | 69% | 22 | +0.40 | +19.5% | -44% | 0.71 | 0.88 | -0.4% | 0.18 | 82% |
| RS leaders near 52w high | 61.0 | 77% | 24 | +0.53 | +29.4% | -44% | 1.01 | 1.07 | +20.9% | 0.71 | 100% |
| signals score>=70, trend | 46.7 | 63% | 22 | +0.32 | +12.0% | -35% | 0.65 | 0.73 | +1.1% | 0.17 | 33% |
| signals score>=70, trend, RS top 20% | 41.5 | 50% | 22 | +0.50 | +19.0% | -33% | 0.89 | 0.97 | +8.8% | 0.49 | 68% |
| signals, trend, RS top 20% | 78.4 | 78% | 22 | +0.71 | +39.2% | -48% | 1.13 | 1.27 | +19.3% | 0.65 | 97% |
| signals, trend, RS top 20%, near 52w high | 75.0 | 79% | 22 | +0.53 | +29.4% | -32% | 1.01 | 1.15 | +20.0% | 0.68 | 100% |

Cost sensitivity (full-period CAGR / Sharpe):

| rule set | 20 bps | 40 bps | 70 bps |
|---|---|---|---|
| RS leaders, trend filter | +19.5% / 0.71 | +16.0% / 0.62 | +11.1% / 0.48 |
| RS leaders near 52w high | +29.4% / 1.01 | +21.7% / 0.81 | +16.0% / 0.65 |
| signals score>=70, trend | +12.0% / 0.65 | +9.1% / 0.52 | +5.1% / 0.34 |
| signals score>=70, trend, RS top 20% | +19.0% / 0.89 | +16.4% / 0.79 | +12.7% / 0.65 |
| signals, trend, RS top 20% | +39.2% / 1.13 | +33.0% / 0.99 | +26.0% / 0.84 |
| signals, trend, RS top 20%, near 52w high | +29.4% / 1.01 | +24.2% / 0.87 | +17.4% / 0.68 |

Exit variant (stop 2.5 x ATR instead of 1.5 x ATR / structural):

| rule set | CAGR | max DD | Sharpe | OOS Sharpe |
|---|---|---|---|---|
| random picks (reference) | +4.2% | -50% | 0.30 | 0.14 |
| random picks, trend filter | +11.3% | -38% | 0.64 | 0.36 |
| RS leaders, trend filter | +19.2% | -36% | 0.92 | 0.44 |
| RS leaders near 52w high | +22.3% | -33% | 1.01 | 0.75 |
| signals score>=70, trend | +12.2% | -29% | 0.76 | -0.04 |
| signals score>=70, trend, RS top 20% | +17.4% | -28% | 1.02 | 0.39 |
| signals, trend, RS top 20% | +17.6% | -36% | 0.84 | 0.44 |
| signals, trend, RS top 20%, near 52w high | +16.6% | -26% | 0.81 | 0.44 |

### Per trade — universe: all (one position per symbol, t over monthly means)

| group | exit | policy | n | win% | avgR | medR | t | excess vs random (t) | ≥+50% | OOS n | OOS avgR |
|---|---|---|---|---|---|---|---|---|---|---|---|
| breakout | fixed | all | 6492 | 17 | +0.287 | -1.11 | 1.35 | -0.344 (-4.31) | 3.2% | 1438 | +0.002 |
| breakout | fixed | SPY>200d & stock>200d | 5148 | 16 | +0.239 | -1.12 | 0.70 | -0.254 (-3.46) | 3.0% | 1161 | +0.008 |
| breakout | fixed | SPY>200d & stock>200d & RS>=0.8 | 2129 | 18 | +0.412 | -1.08 | 1.59 | -0.184 (-1.79) | 5.5% | 500 | +0.488 |
| breakout | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1738 | 18 | +0.448 | -1.08 | 1.54 | -0.090 (-0.77) | 4.4% | 382 | +0.677 |
| breakout | fixed | score>=70 & SPY>200d & stock>200d | 747 | 22 | +0.468 | -1.00 | 2.45 | +0.023 (0.16) | 5.9% | 139 | +0.331 |
| breakout | fixed | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 454 | 23 | +0.573 | -0.98 | 2.61 | +0.106 (0.52) | 7.7% | 91 | +0.482 |
| momentum | fixed | all | 5381 | 22 | +0.269 | -1.04 | 1.94 | -0.323 (-4.52) | 3.6% | 1199 | +0.054 |
| momentum | fixed | SPY>200d & stock>200d | 4755 | 22 | +0.307 | -1.04 | 2.00 | -0.136 (-2.23) | 3.4% | 1087 | +0.087 |
| momentum | fixed | SPY>200d & stock>200d & RS>=0.8 | 1934 | 23 | +0.387 | -1.02 | 2.24 | -0.115 (-1.43) | 6.2% | 453 | +0.261 |
| momentum | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1596 | 23 | +0.392 | -1.03 | 2.16 | -0.053 (-0.60) | 4.6% | 361 | +0.229 |
| momentum | fixed | score>=70 & SPY>200d & stock>200d | 156 | 24 | +0.556 | -0.91 | 2.07 | +0.309 (1.16) | 12.8% | 37 | +0.993 |
| momentum | fixed | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 97 | 25 | +0.720 | -0.88 | 1.89 | +0.261 (0.69) | 15.5% | 26 | +1.018 |
| combined | fixed | all | 8174 | 19 | +0.277 | -1.07 | 1.70 | -0.332 (-5.08) | 3.3% | 1800 | +0.112 |
| combined | fixed | SPY>200d & stock>200d | 6737 | 19 | +0.245 | -1.08 | 1.06 | -0.217 (-3.63) | 3.1% | 1512 | +0.097 |
| combined | fixed | SPY>200d & stock>200d & RS>=0.8 | 2811 | 20 | +0.403 | -1.04 | 1.97 | -0.154 (-1.95) | 5.4% | 660 | +0.517 |
| combined | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 2315 | 21 | +0.408 | -1.05 | 1.93 | -0.073 (-0.90) | 4.3% | 509 | +0.604 |
| combined | fixed | score>=70 & SPY>200d & stock>200d | 823 | 23 | +0.491 | -0.98 | 2.25 | +0.013 (0.10) | 6.6% | 161 | +0.380 |
| combined | fixed | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 500 | 23 | +0.584 | -0.95 | 2.30 | +0.042 (0.22) | 8.6% | 106 | +0.504 |
| baseline_random | fixed | all | 17443 | 25 | +0.376 | -1.02 | 5.23 | — (—) | 5.1% | 4082 | +0.246 |
| baseline_random | fixed | SPY>200d & stock>200d | 11014 | 24 | +0.358 | -1.04 | 3.54 | — (—) | 3.7% | 2559 | +0.188 |
| baseline_random | fixed | SPY>200d & stock>200d & RS>=0.8 | 4539 | 23 | +0.372 | -1.03 | 3.64 | — (—) | 6.3% | 1107 | +0.231 |
| baseline_random | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 3090 | 24 | +0.425 | -1.04 | 3.22 | — (—) | 4.0% | 687 | +0.283 |
| breakout | wide | all | 5219 | 33 | +0.303 | -0.95 | 3.23 | -0.156 (-3.27) | 5.5% | 1146 | +0.263 |
| breakout | wide | SPY>200d & stock>200d | 4197 | 33 | +0.314 | -0.96 | 2.34 | -0.088 (-1.96) | 5.1% | 933 | +0.283 |
| breakout | wide | SPY>200d & stock>200d & RS>=0.8 | 1784 | 34 | +0.435 | -0.93 | 2.73 | -0.090 (-1.50) | 9.1% | 418 | +0.414 |
| breakout | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1485 | 35 | +0.467 | -0.92 | 3.11 | -0.000 (-0.00) | 7.4% | 325 | +0.368 |
| breakout | wide | score>=70 & SPY>200d & stock>200d | 720 | 33 | +0.387 | -0.91 | 2.75 | +0.002 (0.01) | 9.0% | 133 | +0.181 |
| breakout | wide | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 432 | 33 | +0.472 | -0.90 | 2.83 | +0.054 (0.35) | 11.6% | 87 | +0.247 |
| momentum | wide | all | 4480 | 32 | +0.268 | -0.98 | 2.78 | -0.179 (-3.28) | 4.8% | 974 | +0.151 |
| momentum | wide | SPY>200d & stock>200d | 3976 | 33 | +0.311 | -0.98 | 2.91 | -0.055 (-1.14) | 4.6% | 888 | +0.184 |
| momentum | wide | SPY>200d & stock>200d & RS>=0.8 | 1637 | 33 | +0.360 | -0.96 | 2.48 | -0.125 (-2.08) | 7.9% | 383 | +0.273 |
| momentum | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1379 | 33 | +0.339 | -0.97 | 2.21 | -0.101 (-1.60) | 5.7% | 304 | +0.274 |
| momentum | wide | score>=70 & SPY>200d & stock>200d | 140 | 31 | +0.326 | -0.88 | 1.49 | +0.025 (0.14) | 15.0% | 34 | +0.742 |
| momentum | wide | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 83 | 33 | +0.466 | -0.81 | 1.57 | -0.010 (-0.04) | 19.3% | 24 | +0.868 |
| combined | wide | all | 6225 | 33 | +0.286 | -0.97 | 3.17 | -0.170 (-3.78) | 5.1% | 1359 | +0.224 |
| combined | wide | SPY>200d & stock>200d | 5200 | 33 | +0.308 | -0.98 | 2.49 | -0.084 (-2.14) | 4.8% | 1163 | +0.232 |
| combined | wide | SPY>200d & stock>200d & RS>=0.8 | 2258 | 33 | +0.385 | -0.95 | 2.63 | -0.114 (-2.07) | 8.2% | 533 | +0.368 |
| combined | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1890 | 34 | +0.395 | -0.94 | 2.81 | -0.045 (-0.80) | 6.6% | 414 | +0.346 |
| combined | wide | score>=70 & SPY>200d & stock>200d | 780 | 33 | +0.381 | -0.91 | 2.37 | -0.021 (-0.23) | 9.1% | 151 | +0.268 |
| combined | wide | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 464 | 33 | +0.460 | -0.89 | 2.41 | -0.020 (-0.15) | 12.1% | 99 | +0.350 |
| baseline_random | wide | all | 12262 | 36 | +0.338 | -0.95 | 5.41 | — (—) | 6.3% | 2799 | +0.275 |
| baseline_random | wide | SPY>200d & stock>200d | 8122 | 34 | +0.330 | -0.97 | 3.87 | — (—) | 4.7% | 1858 | +0.203 |
| baseline_random | wide | SPY>200d & stock>200d & RS>=0.8 | 3405 | 34 | +0.365 | -0.97 | 3.99 | — (—) | 8.3% | 811 | +0.275 |
| baseline_random | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 2499 | 34 | +0.395 | -0.97 | 3.55 | — (—) | 5.3% | 542 | +0.305 |

## Portfolio — universe: largecap_2015

SPY buy-and-hold: +15.1%/yr, max DD -34%, Sharpe 0.85 · train+val Sharpe 0.82 · OOS +16.0%/yr, Sharpe 0.97

| rule set | trades/yr | exposure | win% | avgR | CAGR | max DD | Sharpe | train+val Sharpe | OOS CAGR | OOS Sharpe | vs random |
|---|---|---|---|---|---|---|---|---|---|---|---|
| random picks (reference) | 47.4 | 87% | 25 | +0.37 | +9.4% | -22% | 0.65 | 0.62 | +15.1% | 0.95 | — |
| random picks, trend filter | 36.5 | 76% | 24 | +0.29 | +7.9% | -19% | 0.63 | 0.75 | -0.7% | 0.02 | — |
| RS leaders, trend filter | 40.2 | 77% | 26 | +0.46 | +13.5% | -32% | 0.74 | 0.79 | +9.9% | 0.55 | 97% |
| RS leaders near 52w high | 41.3 | 76% | 25 | +0.46 | +14.9% | -20% | 0.83 | 0.80 | +17.3% | 0.89 | 100% |
| signals score>=70, trend | 15.0 | 36% | 23 | +0.28 | +2.9% | -16% | 0.36 | 0.28 | +5.7% | 0.62 | 28% |
| signals score>=70, trend, RS top 20% | 10.8 | 25% | 22 | +0.34 | +2.4% | -19% | 0.33 | 0.35 | +2.5% | 0.37 | 10% |
| signals, trend, RS top 20% | 41.8 | 78% | 21 | +0.29 | +6.3% | -30% | 0.46 | 0.51 | +3.5% | 0.29 | 68% |
| signals, trend, RS top 20%, near 52w high | 42.5 | 78% | 21 | +0.28 | +6.8% | -33% | 0.50 | 0.58 | +2.9% | 0.26 | 75% |

Cost sensitivity (full-period CAGR / Sharpe):

| rule set | 20 bps | 40 bps | 70 bps |
|---|---|---|---|
| RS leaders, trend filter | +13.5% / 0.74 | +10.3% / 0.60 | +5.8% / 0.39 |
| RS leaders near 52w high | +14.9% / 0.83 | +11.6% / 0.67 | +6.8% / 0.44 |
| signals score>=70, trend | +2.9% / 0.36 | +1.6% / 0.21 | -0.4% / 0.00 |
| signals score>=70, trend, RS top 20% | +2.4% / 0.33 | +1.4% / 0.21 | -0.1% / 0.02 |
| signals, trend, RS top 20% | +6.3% / 0.46 | +2.9% / 0.26 | -1.9% / -0.04 |
| signals, trend, RS top 20%, near 52w high | +6.8% / 0.50 | +3.5% / 0.30 | -1.4% / -0.01 |

Exit variant (stop 2.5 x ATR instead of 1.5 x ATR / structural):

| rule set | CAGR | max DD | Sharpe | OOS Sharpe |
|---|---|---|---|---|
| random picks (reference) | +9.1% | -26% | 0.68 | 0.38 |
| random picks, trend filter | +8.0% | -30% | 0.66 | 0.41 |
| RS leaders, trend filter | +13.6% | -21% | 0.84 | 0.69 |
| RS leaders near 52w high | +9.4% | -20% | 0.63 | 0.30 |
| signals score>=70, trend | +1.7% | -16% | 0.24 | 0.60 |
| signals score>=70, trend, RS top 20% | +2.9% | -17% | 0.41 | 0.45 |
| signals, trend, RS top 20% | +7.2% | -21% | 0.53 | 0.26 |
| signals, trend, RS top 20%, near 52w high | +6.2% | -27% | 0.48 | 0.40 |

### Per trade — universe: largecap_2015 (one position per symbol, t over monthly means)

| group | exit | policy | n | win% | avgR | medR | t | excess vs random (t) | ≥+50% | OOS n | OOS avgR |
|---|---|---|---|---|---|---|---|---|---|---|---|
| breakout | fixed | all | 2272 | 17 | +0.085 | -1.16 | -0.45 | -0.528 (-4.64) | 0.2% | 449 | -0.200 |
| breakout | fixed | SPY>200d & stock>200d | 1863 | 16 | +0.012 | -1.17 | -0.53 | -0.314 (-2.85) | 0.1% | 374 | -0.187 |
| breakout | fixed | SPY>200d & stock>200d & RS>=0.8 | 760 | 18 | +0.287 | -1.12 | 1.25 | +0.049 (0.23) | 0.1% | 157 | +0.057 |
| breakout | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 712 | 18 | +0.315 | -1.12 | 1.34 | +0.125 (0.59) | 0.1% | 152 | +0.182 |
| breakout | fixed | score>=70 & SPY>200d & stock>200d | 159 | 22 | +0.199 | -1.02 | 1.03 | -0.055 (-0.20) | 0.0% | 26 | +0.579 |
| breakout | fixed | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 104 | 21 | +0.218 | -1.01 | 1.07 | -0.026 (-0.07) | 0.0% | 14 | +0.550 |
| momentum | fixed | all | 2178 | 22 | +0.181 | -1.09 | 1.17 | -0.353 (-3.83) | 0.1% | 444 | +0.010 |
| momentum | fixed | SPY>200d & stock>200d | 1945 | 22 | +0.218 | -1.10 | 0.98 | -0.118 (-1.39) | 0.1% | 409 | +0.070 |
| momentum | fixed | SPY>200d & stock>200d & RS>=0.8 | 834 | 23 | +0.236 | -1.07 | 0.29 | -0.175 (-1.61) | 0.0% | 175 | +0.114 |
| momentum | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 792 | 22 | +0.223 | -1.08 | 0.14 | -0.131 (-1.15) | 0.0% | 170 | +0.152 |
| momentum | fixed | score>=70 & SPY>200d & stock>200d | 16 | 19 | +0.083 | -0.97 | 0.37 | -0.059 (-0.08) | 0.0% | 4 | -0.926 |
| momentum | fixed | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 9 | 22 | +0.780 | -0.89 | 0.72 | +0.150 (0.15) | 0.0% | 3 | -0.812 |
| combined | fixed | all | 3084 | 20 | +0.130 | -1.12 | 0.27 | -0.438 (-4.65) | 0.2% | 608 | -0.090 |
| combined | fixed | SPY>200d & stock>200d | 2634 | 20 | +0.100 | -1.12 | -0.03 | -0.230 (-2.77) | 0.1% | 524 | -0.051 |
| combined | fixed | SPY>200d & stock>200d & RS>=0.8 | 1130 | 21 | +0.223 | -1.08 | 0.28 | -0.159 (-1.65) | 0.0% | 226 | -0.011 |
| combined | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1071 | 20 | +0.218 | -1.09 | 0.35 | -0.087 (-0.90) | 0.0% | 220 | +0.082 |
| combined | fixed | score>=70 & SPY>200d & stock>200d | 171 | 22 | +0.229 | -1.02 | 1.15 | -0.048 (-0.18) | 0.0% | 30 | +0.378 |
| combined | fixed | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 111 | 22 | +0.303 | -0.98 | 1.32 | +0.038 (0.11) | 0.0% | 17 | +0.310 |
| baseline_random | fixed | all | 7059 | 27 | +0.367 | -1.05 | 4.94 | — (—) | 0.7% | 1437 | +0.385 |
| baseline_random | fixed | SPY>200d & stock>200d | 4628 | 24 | +0.287 | -1.08 | 2.94 | — (—) | 0.3% | 952 | +0.271 |
| baseline_random | fixed | SPY>200d & stock>200d & RS>=0.8 | 1893 | 24 | +0.259 | -1.08 | 2.10 | — (—) | 0.4% | 423 | +0.076 |
| baseline_random | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1715 | 23 | +0.216 | -1.09 | 1.52 | — (—) | 0.2% | 365 | +0.146 |
| breakout | wide | all | 1936 | 33 | +0.189 | -0.99 | 1.55 | -0.229 (-3.28) | 0.3% | 373 | +0.147 |
| breakout | wide | SPY>200d & stock>200d | 1589 | 33 | +0.208 | -1.00 | 1.62 | -0.060 (-0.95) | 0.2% | 312 | +0.206 |
| breakout | wide | SPY>200d & stock>200d & RS>=0.8 | 674 | 33 | +0.268 | -0.97 | 1.26 | -0.088 (-1.08) | 0.0% | 135 | +0.112 |
| breakout | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 636 | 33 | +0.271 | -0.96 | 1.36 | -0.037 (-0.43) | 0.0% | 130 | +0.150 |
| breakout | wide | score>=70 & SPY>200d & stock>200d | 159 | 32 | +0.176 | -0.93 | 0.67 | -0.192 (-1.01) | 0.0% | 26 | +0.476 |
| breakout | wide | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 104 | 32 | +0.306 | -0.93 | 1.20 | -0.095 (-0.42) | 0.0% | 14 | +0.616 |
| momentum | wide | all | 1853 | 32 | +0.191 | -1.02 | 1.92 | -0.192 (-2.66) | 0.1% | 371 | +0.101 |
| momentum | wide | SPY>200d & stock>200d | 1654 | 33 | +0.236 | -1.02 | 2.08 | -0.039 (-0.67) | 0.1% | 344 | +0.141 |
| momentum | wide | SPY>200d & stock>200d & RS>=0.8 | 720 | 34 | +0.257 | -0.99 | 1.28 | -0.119 (-1.76) | 0.0% | 153 | +0.012 |
| momentum | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 684 | 34 | +0.264 | -0.99 | 1.49 | -0.046 (-0.60) | 0.0% | 150 | +0.044 |
| momentum | wide | score>=70 & SPY>200d & stock>200d | 15 | 27 | -0.006 | -0.94 | 0.31 | -0.055 (-0.12) | 0.0% | 4 | -0.852 |
| momentum | wide | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 8 | 38 | +0.696 | -0.53 | 0.89 | +0.085 (0.11) | 0.0% | 3 | -0.753 |
| combined | wide | all | 2447 | 33 | +0.183 | -1.01 | 1.76 | -0.216 (-3.34) | 0.3% | 475 | +0.137 |
| combined | wide | SPY>200d & stock>200d | 2102 | 33 | +0.201 | -1.02 | 1.81 | -0.060 (-1.20) | 0.1% | 419 | +0.180 |
| combined | wide | SPY>200d & stock>200d & RS>=0.8 | 922 | 34 | +0.274 | -0.99 | 1.53 | -0.069 (-1.17) | 0.0% | 186 | +0.038 |
| combined | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 876 | 34 | +0.276 | -0.99 | 1.59 | -0.007 (-0.11) | 0.0% | 182 | +0.069 |
| combined | wide | score>=70 & SPY>200d & stock>200d | 170 | 32 | +0.180 | -0.93 | 0.83 | -0.177 (-0.97) | 0.0% | 30 | +0.299 |
| combined | wide | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 110 | 32 | +0.343 | -0.92 | 1.36 | -0.077 (-0.36) | 0.0% | 17 | +0.374 |
| baseline_random | wide | all | 5068 | 38 | +0.334 | -0.95 | 4.96 | — (—) | 0.8% | 1013 | +0.364 |
| baseline_random | wide | SPY>200d & stock>200d | 3501 | 35 | +0.280 | -0.98 | 3.28 | — (—) | 0.3% | 718 | +0.248 |
| baseline_random | wide | SPY>200d & stock>200d & RS>=0.8 | 1474 | 35 | +0.268 | -1.00 | 2.67 | — (—) | 0.4% | 316 | +0.119 |
| baseline_random | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1345 | 34 | +0.231 | -1.01 | 2.18 | — (—) | 0.3% | 278 | +0.193 |

## Momentum rotation — universe: all (from 2018-02-02, 20 bps per side)

| benchmark | CAGR | max DD | Sharpe | train+val Sharpe | OOS CAGR | OOS Sharpe |
|---|---|---|---|---|---|---|
| SPY buy-and-hold | +14.2% | -34% | 0.79 | 0.75 | +16.0% | 0.97 |
| equal-weight universe (no costs) | +25.8% | -42% | 1.00 | 1.00 | +24.5% | 1.01 |

| rule set | trades/yr | exposure | win% | avg trade | avg days | CAGR | max DD | Sharpe | train+val Sharpe | OOS CAGR | OOS Sharpe | vs random | CAGR @40 / @70 bps | without best stock |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| top5, in RS>=0.8, out RS<0.5 | 11 | 92% | 40 | +24.8% | 107 | +24.9% | -75% | 0.67 | 0.60 | +48.4% | 0.90 | 40% | +24.0% / +22.6% | SE: +25.1%, Sharpe 0.67 |
| top5, in RS>=0.8, out RS<0.5, stop -20% | 15 | 91% | 32 | +18.2% | 74 | +24.7% | -75% | 0.66 | 0.68 | +19.6% | 0.60 | 40% | +23.4% / +21.5% | SE: +25.9%, Sharpe 0.69 |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d | 21 | 81% | 38 | +6.3% | 48 | +11.9% | -74% | 0.48 | 0.66 | -22.3% | -0.10 | 10% | +10.1% / +7.6% | MARA: +9.4%, Sharpe 0.43 |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | 25 | 80% | 35 | +4.4% | 39 | +9.6% | -71% | 0.43 | 0.53 | -8.9% | 0.14 | 20% | +7.6% / +4.8% | CELH: +15.4%, Sharpe 0.53 |
| top5, in RS>=0.8, out RS<0.7 | 12 | 93% | 46 | +13.1% | 93 | +18.3% | -76% | 0.58 | 0.52 | +32.4% | 0.75 | 35% | +17.2% / +15.7% | ENPH: +18.8%, Sharpe 0.59 |
| top5, in RS>=0.8, out RS<0.7, stop -20% | 17 | 92% | 37 | +12.0% | 66 | +23.0% | -77% | 0.64 | 0.52 | +59.0% | 1.00 | 35% | +21.5% / +19.3% | VKTX: +17.6%, Sharpe 0.57 |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d | 22 | 80% | 40 | +4.2% | 45 | +9.6% | -77% | 0.44 | 0.52 | -7.7% | 0.23 | 20% | +7.8% / +5.0% | TSLA: +15.4%, Sharpe 0.53 |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | 27 | 80% | 36 | +4.5% | 37 | +10.5% | -68% | 0.45 | 0.49 | +0.5% | 0.33 | 25% | +8.4% / +5.3% | CELH: +6.3%, Sharpe 0.38 |
| top8, in RS>=0.8, out RS<0.5 | 16 | 92% | 40 | +22.9% | 108 | +33.6% | -69% | 0.82 | 0.87 | +29.0% | 0.72 | 95% | +32.7% / +31.4% | SE: +31.6%, Sharpe 0.78 |
| top8, in RS>=0.8, out RS<0.5, stop -20% | 23 | 92% | 35 | +16.1% | 74 | +30.1% | -62% | 0.76 | 0.84 | +18.5% | 0.59 | 55% | +28.7% / +26.8% | SE: +25.1%, Sharpe 0.68 |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d | 30 | 80% | 39 | +9.5% | 53 | +29.0% | -58% | 0.76 | 0.82 | +20.5% | 0.61 | 95% | +27.3% / +24.7% | APP: +22.1%, Sharpe 0.65 |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | 36 | 80% | 35 | +7.5% | 43 | +26.2% | -67% | 0.72 | 0.76 | +22.2% | 0.63 | 75% | +24.3% / +21.5% | NIO: +27.4%, Sharpe 0.74 |
| top8, in RS>=0.8, out RS<0.7 | 19 | 92% | 48 | +18.5% | 93 | +34.5% | -58% | 0.81 | 0.83 | +35.5% | 0.79 | 90% | +37.0% / +31.6% | MARA: +26.4%, Sharpe 0.71 |
| top8, in RS>=0.8, out RS<0.7, stop -20% | 27 | 91% | 35 | +16.8% | 64 | +29.1% | -71% | 0.73 | 0.72 | +34.5% | 0.77 | 65% | +27.7% / +25.5% | MARA: +20.7%, Sharpe 0.62 |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d | 33 | 80% | 41 | +7.8% | 49 | +21.7% | -54% | 0.64 | 0.70 | +10.6% | 0.47 | 35% | +19.9% / +17.1% | MARA: +20.8%, Sharpe 0.63 |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | 40 | 80% | 34 | +10.2% | 39 | +28.8% | -63% | 0.73 | 0.80 | +12.8% | 0.50 | 80% | +26.5% / +23.1% | MARA: +25.7%, Sharpe 0.69 |
| top8, in RS>=0.8, out RS<0.5, 12-1 month momentum | 18 | 91% | 33 | +20.1% | 99 | +23.9% | -63% | 0.68 | 0.68 | +30.8% | 0.73 | 50% | +22.9% / +21.4% | SE: +20.0%, Sharpe 0.61 |
| top8, in RS>=0.8, out RS<0.5, monthly | 11 | 94% | 42 | +51.1% | 153 | +34.8% | -64% | 0.83 | 0.79 | +52.6% | 0.97 | 70% | +34.1% / +33.1% | ENPH: +34.4%, Sharpe 0.84 |
| top8, in RS>=0.8, out RS<0.5, volatility-adjusted | 15 | 93% | 47 | +27.0% | 125 | +36.3% | -46% | 0.95 | 0.98 | +46.8% | 0.95 | 100% | +35.3% / +34.0% | RKLB: +30.1%, Sharpe 0.84 |
| top8, in RS>=0.8, out RS<0.5, max 2/sector | 17 | 91% | 41 | +31.4% | 109 | +39.3% | -65% | 0.85 | 0.87 | +34.0% | 0.78 | 90% | +38.3% / +36.8% | GME: +36.8%, Sharpe 0.87 |
| top8, in RS>=0.8, out RS<0.5, max 3/sector | 16 | 94% | 46 | +28.8% | 113 | +39.5% | -58% | 0.89 | 0.94 | +36.9% | 0.80 | 90% | +37.5% / +36.2% | SE: +33.6%, Sharpe 0.81 |

## Momentum rotation — universe: largecap_2015 (from 2018-02-02, 20 bps per side)

| benchmark | CAGR | max DD | Sharpe | train+val Sharpe | OOS CAGR | OOS Sharpe |
|---|---|---|---|---|---|---|
| SPY buy-and-hold | +14.2% | -34% | 0.79 | 0.75 | +16.0% | 0.97 |
| equal-weight universe (no costs) | +14.0% | -37% | 0.80 | 0.71 | +18.3% | 1.31 |

| rule set | trades/yr | exposure | win% | avg trade | avg days | CAGR | max DD | Sharpe | train+val Sharpe | OOS CAGR | OOS Sharpe | vs random | CAGR @40 / @70 bps | without best stock |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| top5, in RS>=0.8, out RS<0.5 | 10 | 95% | 51 | +9.7% | 116 | +16.5% | -36% | 0.72 | 0.66 | +25.4% | 0.90 | 95% | +15.6% / +14.3% | DVN: +12.9%, Sharpe 0.61 |
| top5, in RS>=0.8, out RS<0.5, stop -20% | 10 | 94% | 53 | +9.6% | 112 | +16.7% | -36% | 0.73 | 0.68 | +25.2% | 0.89 | 95% | +15.8% / +14.5% | DVN: +13.3%, Sharpe 0.63 |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d | 20 | 81% | 48 | +3.4% | 50 | +11.6% | -26% | 0.60 | 0.67 | +7.6% | 0.41 | 100% | +9.9% / +7.3% | AVGO: +11.6%, Sharpe 0.62 |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | 20 | 81% | 49 | +3.4% | 50 | +11.7% | -26% | 0.61 | 0.67 | +7.7% | 0.41 | 95% | +10.0% / +7.4% | AVGO: +11.6%, Sharpe 0.62 |
| top5, in RS>=0.8, out RS<0.7 | 14 | 94% | 49 | +5.4% | 85 | +12.7% | -36% | 0.58 | 0.58 | +15.7% | 0.61 | 95% | +11.5% / +9.8% | INTC: +10.7%, Sharpe 0.55 |
| top5, in RS>=0.8, out RS<0.7, stop -20% | 14 | 95% | 49 | +5.9% | 83 | +14.7% | -33% | 0.65 | 0.67 | +15.1% | 0.60 | 100% | +13.5% / +11.8% | INTC: +13.1%, Sharpe 0.63 |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d | 22 | 81% | 47 | +2.8% | 44 | +10.4% | -29% | 0.56 | 0.66 | +4.2% | 0.29 | 100% | +8.5% / +5.6% | AVGO: +9.2%, Sharpe 0.52 |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | 23 | 81% | 48 | +2.7% | 44 | +10.3% | -29% | 0.55 | 0.66 | +4.0% | 0.28 | 100% | +8.4% / +5.5% | AVGO: +9.3%, Sharpe 0.52 |
| top8, in RS>=0.8, out RS<0.5 | 17 | 94% | 47 | +8.9% | 112 | +16.2% | -29% | 0.77 | 0.72 | +22.4% | 0.96 | 100% | +15.2% / +13.9% | DVN: +14.1%, Sharpe 0.70 |
| top8, in RS>=0.8, out RS<0.5, stop -20% | 17 | 93% | 47 | +7.7% | 107 | +15.0% | -29% | 0.73 | 0.68 | +20.8% | 0.91 | 100% | +14.1% / +12.8% | DVN: +12.7%, Sharpe 0.65 |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d | 31 | 80% | 46 | +2.9% | 52 | +9.2% | -28% | 0.56 | 0.58 | +7.8% | 0.47 | 75% | +7.6% / +5.2% | DVN: +8.6%, Sharpe 0.54 |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | 31 | 80% | 45 | +2.9% | 51 | +9.3% | -28% | 0.56 | 0.59 | +7.7% | 0.47 | 75% | +7.6% / +5.2% | DVN: +8.7%, Sharpe 0.54 |
| top8, in RS>=0.8, out RS<0.7 | 22 | 93% | 50 | +5.0% | 82 | +13.3% | -26% | 0.67 | 0.67 | +14.3% | 0.70 | 95% | +12.1% / +10.3% | META: +10.3%, Sharpe 0.55 |
| top8, in RS>=0.8, out RS<0.7, stop -20% | 23 | 93% | 48 | +5.0% | 80 | +13.0% | -29% | 0.66 | 0.66 | +13.7% | 0.67 | 100% | +11.7% / +9.9% | AVGO: +10.6%, Sharpe 0.56 |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d | 35 | 80% | 48 | +2.2% | 45 | +9.0% | -29% | 0.55 | 0.60 | +6.0% | 0.39 | 95% | +7.2% / +4.5% | AVGO: +8.4%, Sharpe 0.53 |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | 35 | 80% | 48 | +2.2% | 45 | +9.0% | -29% | 0.55 | 0.60 | +5.9% | 0.38 | 95% | +7.1% / +4.4% | AVGO: +8.4%, Sharpe 0.53 |
| top8, in RS>=0.8, out RS<0.5, 12-1 month momentum | 19 | 90% | 34 | +3.5% | 94 | +5.7% | -40% | 0.37 | 0.41 | +1.2% | 0.16 | 10% | +4.8% / +3.4% | GE: +4.1%, Sharpe 0.30 |
| top8, in RS>=0.8, out RS<0.5, monthly | 12 | 93% | 50 | +9.8% | 146 | +13.6% | -27% | 0.67 | 0.64 | +16.7% | 0.76 | 100% | +14.5% / +13.5% | DVN: +13.5%, Sharpe 0.66 |
| top8, in RS>=0.8, out RS<0.5, volatility-adjusted | 16 | 93% | 57 | +7.2% | 116 | +13.2% | -23% | 0.76 | 0.73 | +14.5% | 0.93 | 100% | +12.4% / +11.2% | GE: +10.3%, Sharpe 0.62 |
| top8, in RS>=0.8, out RS<0.5, max 2/sector | 17 | 93% | 46 | +7.2% | 108 | +12.7% | -30% | 0.65 | 0.60 | +18.9% | 0.82 | 95% | +11.8% / +10.4% | DVN: +10.7%, Sharpe 0.58 |
| top8, in RS>=0.8, out RS<0.5, max 3/sector | 17 | 94% | 46 | +8.0% | 108 | +14.8% | -28% | 0.72 | 0.68 | +20.7% | 0.88 | 95% | +13.9% / +12.6% | DVN: +12.9%, Sharpe 0.66 |

## Rotation: pre-registered selection (2015 large caps, train+validation only)

Gates: train+val Sharpe > SPY's, ranking beats >= 90% of random selections, CAGR without the single best stock >= SPY's, max drawdown at most 10 points worse than SPY's.

**Chosen: none — no rule set passed every gate**

| rule set | passes | train+val Sharpe | failed gates |
|---|---|---|---|
| top5, in RS>=0.8, out RS<0.5 | ❌ | 0.66 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top5, in RS>=0.8, out RS<0.5, stop -20% | ❌ | 0.68 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d | ❌ | 0.67 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | ❌ | 0.67 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top5, in RS>=0.8, out RS<0.7 | ❌ | 0.58 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top5, in RS>=0.8, out RS<0.7, stop -20% | ❌ | 0.67 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d | ❌ | 0.66 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | ❌ | 0.66 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5 | ❌ | 0.72 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5, stop -20% | ❌ | 0.68 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d | ❌ | 0.58 | train_val_sharpe_beats_spy, ranking_beats_random, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | ❌ | 0.59 | train_val_sharpe_beats_spy, ranking_beats_random, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.7 | ❌ | 0.67 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.7, stop -20% | ❌ | 0.66 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d | ❌ | 0.60 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | ❌ | 0.60 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5, 12-1 month momentum | ❌ | 0.41 | train_val_sharpe_beats_spy, ranking_beats_random, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5, monthly | ❌ | 0.64 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5, volatility-adjusted | ❌ | 0.73 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5, max 2/sector | ❌ | 0.60 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5, max 3/sector | ❌ | 0.68 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |

Calendar-year returns (2015 large caps, 20 bps per side):

| | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|---|---|---|---|
| SPY | -8% | +31% | +18% | +29% | -18% | +26% | +25% | +18% | +13% |
| equal-weight group | -8% | +29% | +14% | +31% | -4% | +16% | +16% | +17% | +17% |
| top5, in RS>=0.8, out RS<0.5 | +4% | +14% | +12% | +22% | +0% | +11% | +37% | +15% | +34% |
| top5, in RS>=0.8, out RS<0.5, stop -20% | +4% | +14% | +12% | +22% | -0% | +14% | +36% | +14% | +34% |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d | +9% | +3% | +16% | +21% | -1% | +21% | +19% | +9% | +7% |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | +9% | +3% | +16% | +22% | -1% | +21% | +19% | +9% | +7% |
| top5, in RS>=0.8, out RS<0.7 | +4% | +8% | +7% | +21% | -4% | +19% | +30% | -2% | +33% |
| top5, in RS>=0.8, out RS<0.7, stop -20% | +4% | +7% | +9% | +22% | +10% | +21% | +30% | -2% | +32% |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d | +11% | -3% | +8% | +21% | -2% | +22% | +29% | -5% | +13% |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | +11% | -3% | +8% | +21% | -2% | +22% | +29% | -5% | +13% |
| top8, in RS>=0.8, out RS<0.5 | +0% | +7% | +17% | +28% | +0% | +23% | +27% | +22% | +19% |
| top8, in RS>=0.8, out RS<0.5, stop -20% | +0% | +8% | +11% | +33% | +1% | +20% | +22% | +23% | +16% |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d | +8% | -5% | +11% | +30% | -2% | +14% | +13% | +14% | +1% |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | +8% | -4% | +11% | +30% | -2% | +14% | +13% | +14% | +1% |
| top8, in RS>=0.8, out RS<0.7 | +0% | +9% | +17% | +18% | +2% | +20% | +25% | +6% | +21% |
| top8, in RS>=0.8, out RS<0.7, stop -20% | +0% | +6% | +13% | +18% | +6% | +21% | +25% | +5% | +21% |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d | +9% | +2% | +12% | +18% | -4% | +9% | +24% | +2% | +10% |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | +9% | +2% | +12% | +18% | -4% | +9% | +24% | +1% | +10% |
| top8, in RS>=0.8, out RS<0.5, 12-1 month momentum | -11% | +10% | +2% | +24% | -12% | +2% | +41% | -1% | +4% |
| top8, in RS>=0.8, out RS<0.5, monthly | -0% | +12% | +16% | +19% | -5% | +26% | +23% | +5% | +28% |
| top8, in RS>=0.8, out RS<0.5, volatility-adjusted | +4% | +17% | +3% | +22% | -8% | +18% | +38% | +20% | +8% |
| top8, in RS>=0.8, out RS<0.5, max 2/sector | +1% | +7% | +4% | +29% | -0% | +19% | +17% | +10% | +26% |
| top8, in RS>=0.8, out RS<0.5, max 3/sector | +2% | +7% | +10% | +29% | -1% | +24% | +22% | +18% | +22% |

## Rockets (from 2016-11-15, 20 bps per side, 10 slots x 10%, max 3 new per day)

Rocket day: close >= +jump vs previous close, volume >= 3x the 20-day average, close in the top quarter of the day's range, price >= $5, 20-day dollar volume >= $5M. Buy next open; sell next open after a close more than `trail` below the highest close, or after 40 sessions. 'Random' = same stocks, same liquidity filter, same exit, random dates.

SPY: +15.3%/yr, max DD -34%, Sharpe 0.88 · train+val +15.1%/yr, Sharpe 0.86

| variant | trades | win% | avg trade | median | ≥+50% | worst | random avg | excess vs random t (train+val) | 2015 large caps excess | CAGR | max DD | Sharpe | train+val CAGR / Sharpe | OOS CAGR | random-entry portfolio CAGR | without top 3 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| EPS surprise>0%, reaction>=5% | 1901 | 54 | +4.6% | +1.9% | 4.3% | -51% | +4.3% | -0.43% (-0.67) | -0.36% (n=562) | +7.9% | -41% | 0.47 | +10.2% / 0.56 | -2.2% | +19.6% | +7.9% |
| EPS surprise>0%, reaction>=10% | 922 | 54 | +6.2% | +2.0% | 6.2% | -51% | +4.3% | +0.67% (0.66) | +1.43% (n=129) | +23.5% | -42% | 0.98 | +24.6% / 1.03 | +15.1% | +19.6% | +23.0% |
| EPS surprise>10%, reaction>=5% | 1267 | 53 | +5.0% | +2.0% | 5.1% | -51% | +4.3% | +0.53% (0.65) | -0.77% (n=268) | +13.5% | -44% | 0.66 | +20.1% / 0.90 | -14.3% | +19.6% | +11.7% |
| EPS surprise>10%, reaction>=10% | 714 | 53 | +6.6% | +2.2% | 6.6% | -51% | +4.3% | +1.58% (1.30) | +1.67% (n=71) | +17.1% | -45% | 0.75 | +26.2% / 1.04 | -17.7% | +19.6% | +15.1% |
| EPS surprise>20%, reaction>=10%, volume>=2x, RS>=0.8 | 236 | 57 | +8.8% | +3.6% | 7.2% | -34% | +4.3% | +3.26% (1.51) | +3.80% (n=14) | +17.8% | -27% | 0.92 | +24.8% / 1.25 | -9.0% | +19.6% | +11.8% |
| EPS surprise>20%, reaction>=15%, volume>=2x, RS>=0.8 | 168 | 58 | +9.1% | +4.0% | 8.3% | -33% | +4.3% | +1.41% (0.59) | —% (n=4) | +14.8% | -21% | 0.90 | +18.4% / 1.14 | -1.1% | +19.6% | +10.2% |
| jump>=8%, trail 15% | 1001 | 46 | +4.0% | -2.6% | 5.3% | -52% | +2.2% | -0.09% (-0.08) | -1.56% (n=115) | +15.4% | -48% | 0.62 | +23.2% / 0.82 | -14.3% | +13.9% | +9.7% |
| jump>=8%, trail 25% | 999 | 51 | +5.5% | +0.7% | 6.8% | -61% | +2.9% | +0.47% (0.40) | -1.47% (n=115) | +15.1% | -68% | 0.60 | +21.4% / 0.76 | -5.9% | +16.1% | +11.1% |
| jump>=15%, trail 15% | 543 | 43 | +4.7% | -4.5% | 6.8% | -52% | +2.2% | -0.44% (-0.31) | -4.25% (n=24) | +18.3% | -38% | 0.71 | +21.7% / 0.79 | +4.4% | +13.9% | +12.0% |
| jump>=15%, trail 25% | 542 | 47 | +6.7% | -1.9% | 9.2% | -61% | +2.9% | +0.98% (0.53) | -4.48% (n=24) | +14.7% | -60% | 0.57 | +21.3% / 0.73 | -7.0% | +16.1% | +6.4% |

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
| jump>=8%, trail 15% | ❌ | beats_random_entries_same_stocks, beats_spy_train_val, holds_in_2015_largecaps, without_top3_beats_spy |
| jump>=8%, trail 25% | ❌ | beats_random_entries_same_stocks, beats_spy_train_val, holds_in_2015_largecaps, without_top3_beats_spy, drawdown_tolerable |
| jump>=15%, trail 15% | ❌ | beats_random_entries_same_stocks, beats_spy_train_val, holds_in_2015_largecaps, without_top3_beats_spy |
| jump>=15%, trail 25% | ❌ | beats_random_entries_same_stocks, beats_spy_train_val, holds_in_2015_largecaps, without_top3_beats_spy, drawdown_tolerable |

## Mean R by year (all universe, fixed exit)

| group | policy | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| combined | all | +1.10 | -0.45 | +0.30 | +1.07 | +0.02 | -0.44 | +0.53 | +0.42 | +0.23 | -0.03 |
| combined | SPY>200d & stock>200d | +1.18 | -0.43 | +0.03 | +0.94 | -0.04 | -0.79 | +0.38 | +0.42 | +0.19 | -0.01 |
| combined | SPY>200d & stock>200d & RS>=0.8 | +1.06 | -0.26 | +0.35 | +1.46 | -0.42 | -0.36 | +0.35 | +0.60 | +0.83 | +0.16 |
| combined | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | +1.13 | -0.12 | +0.45 | +1.36 | -0.52 | -0.07 | +0.30 | +0.46 | +0.81 | +0.39 |
| combined | score>=70 & SPY>200d & stock>200d | +0.81 | +0.65 | +0.42 | +1.14 | -0.54 | -0.96 | +0.43 | +0.69 | +0.52 | +0.14 |
| combined | score>=70 & SPY>200d & stock>200d & RS>=0.8 | +0.17 | +1.33 | +0.61 | +1.08 | -0.53 | -1.15 | +0.41 | +1.00 | +0.70 | +0.16 |
| baseline_random | all | +1.69 | +0.15 | +0.63 | +0.88 | +0.21 | -0.24 | +0.56 | +0.44 | +0.37 | +0.15 |
| baseline_random | SPY>200d & stock>200d | +1.69 | -0.21 | +0.52 | +1.14 | +0.16 | -0.68 | +0.32 | +0.36 | +0.26 | +0.13 |
| baseline_random | SPY>200d & stock>200d & RS>=0.8 | +1.62 | +0.01 | +0.60 | +1.39 | -0.19 | -0.38 | +0.46 | +0.40 | +0.44 | +0.03 |
| baseline_random | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | +1.43 | +0.22 | +0.63 | +1.16 | -0.15 | -0.34 | +0.56 | +0.41 | +0.55 | +0.04 |