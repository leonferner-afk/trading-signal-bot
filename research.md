# Strategy research

278 symbols with data (1 failed), 10 years of daily bars. Control group: 105 stocks that were already large caps in 2015. Primary cost 40 bps per side (Swedish retail: courtage + FX + slippage). Validation from 2023-01-21, out-of-sample (OOS) from 2024-11-22. Setups invalidated at the next open (skipped): 1323.

Portfolio: max 8 positions, max 3 new per day, 1% risk per trade, max 25% of equity per position, no leverage, marked to market daily. 'vs random' = share of 40 random-order portfolios from the same eligible trades that this ranking beat.

## Portfolio — universe: all

SPY buy-and-hold: +15.0%/yr, max DD -34%, Sharpe 0.85 · train+val Sharpe 0.81 · OOS +16.7%/yr, Sharpe 1.0

| rule set | trades/yr | exposure | win% | avgR | CAGR | max DD | Sharpe | train+val Sharpe | OOS CAGR | OOS Sharpe | vs random |
|---|---|---|---|---|---|---|---|---|---|---|---|
| random picks (reference) | 77.8 | 87% | 22 | +0.17 | +2.7% | -59% | 0.24 | 0.49 | -26.6% | -0.81 | — |
| random picks, trend filter | 65.7 | 78% | 22 | +0.31 | +14.3% | -45% | 0.64 | 0.67 | +0.2% | 0.15 | — |
| RS leaders, trend filter | 72.1 | 68% | 22 | +0.34 | +19.1% | -43% | 0.70 | 0.76 | +2.3% | 0.27 | 93% |
| RS leaders near 52w high | 65.5 | 76% | 26 | +0.57 | +24.9% | -35% | 0.88 | 0.93 | +28.5% | 0.83 | 100% |
| signals score>=70, trend | 47.4 | 63% | 21 | +0.21 | +7.5% | -37% | 0.45 | 0.59 | -8.3% | -0.18 | 10% |
| signals score>=70, trend, RS top 20% | 41.6 | 51% | 23 | +0.46 | +16.7% | -36% | 0.80 | 0.92 | +10.7% | 0.52 | 72% |
| signals, trend, RS top 20% | 77.7 | 78% | 22 | +0.62 | +31.4% | -52% | 0.97 | 1.01 | +40.2% | 0.99 | 100% |
| signals, trend, RS top 20%, near 52w high | 73.9 | 79% | 22 | +0.47 | +25.8% | -36% | 0.92 | 1.03 | +22.0% | 0.71 | 97% |

Cost sensitivity (full-period CAGR / Sharpe):

| rule set | 15 bps | 40 bps | 70 bps |
|---|---|---|---|
| RS leaders, trend filter | +19.9% / 0.73 | +19.1% / 0.70 | +13.1% / 0.54 |
| RS leaders near 52w high | +30.5% / 1.02 | +24.9% / 0.88 | +18.6% / 0.71 |
| signals score>=70, trend | +11.2% / 0.61 | +7.5% / 0.45 | +3.6% / 0.27 |
| signals score>=70, trend, RS top 20% | +19.9% / 0.93 | +16.7% / 0.80 | +12.9% / 0.66 |
| signals, trend, RS top 20% | +38.8% / 1.13 | +31.4% / 0.97 | +24.3% / 0.80 |
| signals, trend, RS top 20%, near 52w high | +32.2% / 1.08 | +25.8% / 0.92 | +18.8% / 0.72 |

Exit variant (stop 2.5 x ATR instead of 1.5 x ATR / structural):

| rule set | CAGR | max DD | Sharpe | OOS Sharpe |
|---|---|---|---|---|
| random picks (reference) | +2.0% | -41% | 0.21 | -1.42 |
| random picks, trend filter | +16.7% | -31% | 0.89 | -0.35 |
| RS leaders, trend filter | +21.1% | -29% | 0.95 | 0.81 |
| RS leaders near 52w high | +25.2% | -26% | 1.09 | 0.60 |
| signals score>=70, trend | +9.7% | -31% | 0.63 | -0.23 |
| signals score>=70, trend, RS top 20% | +15.7% | -29% | 0.93 | 0.64 |
| signals, trend, RS top 20% | +16.2% | -40% | 0.79 | 0.54 |
| signals, trend, RS top 20%, near 52w high | +14.2% | -28% | 0.72 | 0.40 |

### Per trade — universe: all (one position per symbol, t over monthly means)

| group | exit | policy | n | win% | avgR | medR | t | excess vs random (t) | ≥+50% | OOS n | OOS avgR |
|---|---|---|---|---|---|---|---|---|---|---|---|
| breakout | fixed | all | 6503 | 17 | +0.118 | -1.24 | -0.26 | -0.399 (-4.71) | 3.1% | 1457 | -0.152 |
| breakout | fixed | SPY>200d & stock>200d | 5165 | 17 | +0.065 | -1.25 | -1.01 | -0.289 (-4.08) | 2.9% | 1172 | -0.134 |
| breakout | fixed | SPY>200d & stock>200d & RS>=0.8 | 2135 | 18 | +0.316 | -1.18 | 0.80 | -0.220 (-2.03) | 5.2% | 511 | +0.432 |
| breakout | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1748 | 18 | +0.340 | -1.18 | 0.87 | -0.100 (-0.81) | 4.2% | 394 | +0.584 |
| breakout | fixed | score>=70 & SPY>200d & stock>200d | 753 | 22 | +0.406 | -1.06 | 2.03 | +0.099 (0.66) | 5.7% | 155 | +0.150 |
| breakout | fixed | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 458 | 23 | +0.543 | -1.03 | 2.64 | +0.151 (0.73) | 7.4% | 103 | +0.319 |
| momentum | fixed | all | 5384 | 22 | +0.172 | -1.12 | 0.82 | -0.299 (-4.01) | 3.6% | 1211 | -0.079 |
| momentum | fixed | SPY>200d & stock>200d | 4755 | 22 | +0.207 | -1.13 | 0.92 | -0.095 (-1.52) | 3.4% | 1096 | -0.057 |
| momentum | fixed | SPY>200d & stock>200d & RS>=0.8 | 1925 | 23 | +0.312 | -1.09 | 1.60 | -0.127 (-1.61) | 6.2% | 447 | +0.196 |
| momentum | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1591 | 23 | +0.313 | -1.11 | 1.52 | -0.047 (-0.55) | 4.5% | 359 | +0.168 |
| momentum | fixed | score>=70 & SPY>200d & stock>200d | 154 | 24 | +0.514 | -0.96 | 1.92 | +0.362 (1.31) | 13.0% | 39 | +0.927 |
| momentum | fixed | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 95 | 25 | +0.705 | -0.91 | 1.82 | +0.293 (0.78) | 15.8% | 27 | +1.046 |
| combined | fixed | all | 8180 | 19 | +0.137 | -1.18 | 0.17 | -0.355 (-5.05) | 3.2% | 1815 | -0.017 |
| combined | fixed | SPY>200d & stock>200d | 6746 | 19 | +0.105 | -1.18 | -0.49 | -0.217 (-3.65) | 3.0% | 1521 | -0.023 |
| combined | fixed | SPY>200d & stock>200d & RS>=0.8 | 2812 | 21 | +0.317 | -1.13 | 1.16 | -0.178 (-2.20) | 5.3% | 660 | +0.510 |
| combined | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 2320 | 21 | +0.312 | -1.14 | 1.15 | -0.081 (-0.94) | 4.2% | 515 | +0.521 |
| combined | fixed | score>=70 & SPY>200d & stock>200d | 827 | 23 | +0.432 | -1.04 | 1.84 | +0.092 (0.67) | 6.4% | 177 | +0.230 |
| combined | fixed | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 502 | 24 | +0.558 | -1.01 | 2.33 | +0.094 (0.49) | 8.4% | 117 | +0.401 |
| baseline_random | fixed | all | 17767 | 24 | +0.265 | -1.08 | 4.00 | — (—) | 4.8% | 4053 | +0.126 |
| baseline_random | fixed | SPY>200d & stock>200d | 11326 | 23 | +0.229 | -1.12 | 2.07 | — (—) | 3.4% | 2605 | +0.070 |
| baseline_random | fixed | SPY>200d & stock>200d & RS>=0.8 | 4576 | 23 | +0.313 | -1.09 | 2.93 | — (—) | 6.1% | 1113 | +0.216 |
| baseline_random | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 3139 | 23 | +0.351 | -1.12 | 2.38 | — (—) | 4.0% | 685 | +0.253 |
| breakout | wide | all | 5227 | 33 | +0.252 | -0.99 | 2.54 | -0.166 (-3.04) | 5.4% | 1154 | +0.192 |
| breakout | wide | SPY>200d & stock>200d | 4208 | 33 | +0.261 | -1.01 | 1.67 | -0.065 (-1.34) | 5.0% | 942 | +0.205 |
| breakout | wide | SPY>200d & stock>200d & RS>=0.8 | 1784 | 35 | +0.403 | -0.97 | 2.48 | -0.097 (-1.60) | 8.9% | 420 | +0.385 |
| breakout | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1488 | 35 | +0.426 | -0.97 | 2.81 | -0.017 (-0.26) | 7.2% | 332 | +0.344 |
| breakout | wide | score>=70 & SPY>200d & stock>200d | 726 | 33 | +0.347 | -0.96 | 2.20 | +0.008 (0.07) | 8.8% | 148 | +0.148 |
| breakout | wide | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 436 | 34 | +0.456 | -0.93 | 2.78 | +0.037 (0.24) | 11.2% | 96 | +0.313 |
| momentum | wide | all | 4482 | 32 | +0.214 | -1.03 | 2.07 | -0.193 (-3.38) | 4.7% | 973 | +0.082 |
| momentum | wide | SPY>200d & stock>200d | 3978 | 32 | +0.255 | -1.02 | 2.21 | -0.030 (-0.59) | 4.5% | 889 | +0.100 |
| momentum | wide | SPY>200d & stock>200d & RS>=0.8 | 1627 | 33 | +0.318 | -1.00 | 2.05 | -0.132 (-2.16) | 7.7% | 373 | +0.218 |
| momentum | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1372 | 33 | +0.295 | -1.01 | 1.75 | -0.114 (-1.77) | 5.6% | 298 | +0.210 |
| momentum | wide | score>=70 & SPY>200d & stock>200d | 138 | 31 | +0.288 | -0.92 | 1.22 | +0.028 (0.15) | 15.2% | 33 | +0.673 |
| momentum | wide | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 81 | 32 | +0.440 | -0.83 | 1.38 | -0.017 (-0.07) | 19.8% | 22 | +0.890 |
| combined | wide | all | 6227 | 33 | +0.232 | -1.01 | 2.41 | -0.182 (-3.63) | 5.1% | 1366 | +0.154 |
| combined | wide | SPY>200d & stock>200d | 5201 | 33 | +0.254 | -1.02 | 1.76 | -0.064 (-1.52) | 4.8% | 1166 | +0.164 |
| combined | wide | SPY>200d & stock>200d & RS>=0.8 | 2255 | 33 | +0.342 | -0.99 | 2.18 | -0.120 (-2.20) | 8.1% | 531 | +0.334 |
| combined | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1887 | 34 | +0.346 | -0.99 | 2.29 | -0.064 (-1.11) | 6.4% | 414 | +0.304 |
| combined | wide | score>=70 & SPY>200d & stock>200d | 785 | 33 | +0.341 | -0.95 | 1.82 | -0.020 (-0.20) | 8.9% | 166 | +0.218 |
| combined | wide | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 467 | 33 | +0.443 | -0.92 | 2.32 | -0.031 (-0.22) | 11.8% | 107 | +0.399 |
| baseline_random | wide | all | 12395 | 35 | +0.268 | -0.98 | 4.77 | — (—) | 6.1% | 2737 | +0.201 |
| baseline_random | wide | SPY>200d & stock>200d | 8143 | 34 | +0.260 | -1.02 | 2.86 | — (—) | 4.5% | 1862 | +0.127 |
| baseline_random | wide | SPY>200d & stock>200d & RS>=0.8 | 3402 | 34 | +0.328 | -1.00 | 3.66 | — (—) | 8.1% | 799 | +0.274 |
| baseline_random | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 2491 | 35 | +0.376 | -1.01 | 3.40 | — (—) | 5.7% | 523 | +0.371 |

## Portfolio — universe: largecap_2015

SPY buy-and-hold: +15.0%/yr, max DD -34%, Sharpe 0.85 · train+val Sharpe 0.81 · OOS +16.7%/yr, Sharpe 1.0

| rule set | trades/yr | exposure | win% | avgR | CAGR | max DD | Sharpe | train+val Sharpe | OOS CAGR | OOS Sharpe | vs random |
|---|---|---|---|---|---|---|---|---|---|---|---|
| random picks (reference) | 41.1 | 88% | 26 | +0.24 | +8.8% | -24% | 0.64 | 0.73 | -0.9% | 0.01 | — |
| random picks, trend filter | 36.5 | 76% | 24 | +0.10 | +0.9% | -36% | 0.15 | 0.26 | -9.2% | -0.61 | — |
| RS leaders, trend filter | 41.7 | 76% | 23 | +0.14 | +4.7% | -38% | 0.33 | 0.46 | -4.5% | -0.12 | 82% |
| RS leaders near 52w high | 40.2 | 76% | 22 | +0.10 | +1.0% | -34% | 0.14 | 0.26 | -8.0% | -0.36 | 47% |
| signals score>=70, trend | 15.2 | 37% | 24 | +0.22 | +2.1% | -18% | 0.27 | 0.32 | +2.8% | 0.33 | 42% |
| signals score>=70, trend, RS top 20% | 10.9 | 26% | 22 | +0.21 | +1.6% | -20% | 0.24 | 0.36 | +1.2% | 0.19 | 0% |
| signals, trend, RS top 20% | 41.1 | 78% | 22 | +0.16 | +3.7% | -34% | 0.31 | 0.39 | -0.6% | 0.05 | 80% |
| signals, trend, RS top 20%, near 52w high | 42.2 | 78% | 21 | +0.16 | +4.2% | -37% | 0.35 | 0.48 | -1.5% | -0.01 | 90% |

Cost sensitivity (full-period CAGR / Sharpe):

| rule set | 15 bps | 40 bps | 70 bps |
|---|---|---|---|
| RS leaders, trend filter | +8.3% / 0.52 | +4.7% / 0.33 | +0.4% / 0.12 |
| RS leaders near 52w high | +4.7% / 0.35 | +1.0% / 0.14 | -3.7% / -0.12 |
| signals score>=70, trend | +3.8% / 0.44 | +2.1% / 0.27 | +0.1% / 0.06 |
| signals score>=70, trend, RS top 20% | +3.0% / 0.40 | +1.6% / 0.24 | +0.1% / 0.06 |
| signals, trend, RS top 20% | +7.9% / 0.56 | +3.7% / 0.31 | -1.1% / 0.01 |
| signals, trend, RS top 20%, near 52w high | +8.4% / 0.60 | +4.2% / 0.35 | -0.7% / 0.04 |

Exit variant (stop 2.5 x ATR instead of 1.5 x ATR / structural):

| rule set | CAGR | max DD | Sharpe | OOS Sharpe |
|---|---|---|---|---|
| random picks (reference) | +6.1% | -23% | 0.47 | -0.36 |
| random picks, trend filter | +4.3% | -21% | 0.40 | -0.39 |
| RS leaders, trend filter | +8.3% | -27% | 0.55 | 0.26 |
| RS leaders near 52w high | +9.5% | -23% | 0.62 | -0.03 |
| signals score>=70, trend | +1.1% | -18% | 0.17 | 0.30 |
| signals score>=70, trend, RS top 20% | +2.0% | -18% | 0.30 | 0.36 |
| signals, trend, RS top 20% | +5.3% | -24% | 0.42 | 0.45 |
| signals, trend, RS top 20%, near 52w high | +4.2% | -34% | 0.35 | 0.39 |

### Per trade — universe: largecap_2015 (one position per symbol, t over monthly means)

| group | exit | policy | n | win% | avgR | medR | t | excess vs random (t) | ≥+50% | OOS n | OOS avgR |
|---|---|---|---|---|---|---|---|---|---|---|---|
| breakout | fixed | all | 2272 | 17 | -0.168 | -1.36 | -2.18 | -0.531 (-4.37) | 0.2% | 436 | -0.421 |
| breakout | fixed | SPY>200d & stock>200d | 1866 | 16 | -0.253 | -1.37 | -2.33 | -0.350 (-3.36) | 0.1% | 362 | -0.407 |
| breakout | fixed | SPY>200d & stock>200d & RS>=0.8 | 761 | 19 | +0.062 | -1.31 | 0.37 | -0.044 (-0.20) | 0.1% | 156 | -0.083 |
| breakout | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 714 | 18 | +0.068 | -1.31 | 0.40 | -0.013 (-0.06) | 0.1% | 152 | -0.041 |
| breakout | fixed | score>=70 & SPY>200d & stock>200d | 162 | 22 | +0.079 | -1.13 | 0.53 | -0.044 (-0.16) | 0.0% | 27 | +0.354 |
| breakout | fixed | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 107 | 22 | +0.127 | -1.13 | 0.79 | -0.048 (-0.14) | 0.0% | 16 | +0.323 |
| momentum | fixed | all | 2174 | 22 | +0.045 | -1.22 | -0.28 | -0.263 (-2.83) | 0.1% | 432 | -0.193 |
| momentum | fixed | SPY>200d & stock>200d | 1939 | 22 | +0.079 | -1.23 | -0.41 | -0.078 (-0.92) | 0.1% | 396 | -0.134 |
| momentum | fixed | SPY>200d & stock>200d & RS>=0.8 | 832 | 22 | +0.114 | -1.19 | -0.75 | -0.228 (-2.09) | 0.0% | 170 | -0.066 |
| momentum | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 790 | 22 | +0.093 | -1.20 | -0.93 | -0.222 (-1.99) | 0.0% | 165 | -0.048 |
| momentum | fixed | score>=70 & SPY>200d & stock>200d | 15 | 20 | -0.013 | -1.15 | 0.25 | +0.042 (0.05) | 0.0% | 3 | -1.241 |
| momentum | fixed | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 8 | 25 | +0.802 | -0.97 | 0.66 | +0.042 (0.04) | 0.0% | 2 | -1.172 |
| combined | fixed | all | 3080 | 19 | -0.069 | -1.27 | -1.47 | -0.398 (-4.17) | 0.2% | 589 | -0.311 |
| combined | fixed | SPY>200d & stock>200d | 2630 | 19 | -0.101 | -1.28 | -1.79 | -0.222 (-2.78) | 0.1% | 505 | -0.276 |
| combined | fixed | SPY>200d & stock>200d & RS>=0.8 | 1128 | 20 | +0.060 | -1.22 | -0.91 | -0.220 (-2.01) | 0.0% | 221 | -0.174 |
| combined | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1070 | 20 | +0.040 | -1.23 | -0.97 | -0.199 (-1.89) | 0.0% | 216 | -0.141 |
| combined | fixed | score>=70 & SPY>200d & stock>200d | 173 | 22 | +0.111 | -1.13 | 0.68 | -0.025 (-0.10) | 0.0% | 30 | +0.194 |
| combined | fixed | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 113 | 22 | +0.213 | -1.09 | 1.05 | +0.018 (0.05) | 0.0% | 18 | +0.157 |
| baseline_random | fixed | all | 7345 | 25 | +0.176 | -1.17 | 2.74 | — (—) | 0.6% | 1464 | +0.081 |
| baseline_random | fixed | SPY>200d & stock>200d | 4833 | 23 | +0.107 | -1.21 | 0.83 | — (—) | 0.3% | 960 | +0.018 |
| baseline_random | fixed | SPY>200d & stock>200d & RS>=0.8 | 1925 | 24 | +0.187 | -1.18 | 1.28 | — (—) | 0.4% | 420 | -0.038 |
| baseline_random | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1715 | 23 | +0.177 | -1.19 | 1.03 | — (—) | 0.2% | 365 | -0.003 |
| breakout | wide | all | 1939 | 33 | +0.110 | -1.07 | 0.60 | -0.227 (-3.03) | 0.3% | 363 | +0.062 |
| breakout | wide | SPY>200d & stock>200d | 1595 | 33 | +0.121 | -1.08 | 0.66 | -0.029 (-0.42) | 0.2% | 304 | +0.112 |
| breakout | wide | SPY>200d & stock>200d & RS>=0.8 | 672 | 33 | +0.203 | -1.05 | 0.72 | -0.132 (-1.55) | 0.0% | 137 | +0.015 |
| breakout | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 635 | 33 | +0.200 | -1.05 | 0.75 | -0.092 (-1.08) | 0.0% | 133 | +0.024 |
| breakout | wide | score>=70 & SPY>200d & stock>200d | 162 | 31 | +0.094 | -0.99 | 0.25 | -0.111 (-0.59) | 0.0% | 27 | +0.296 |
| breakout | wide | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 107 | 32 | +0.250 | -0.99 | 0.99 | -0.126 (-0.52) | 0.0% | 16 | +0.463 |
| momentum | wide | all | 1849 | 32 | +0.113 | -1.09 | 0.95 | -0.196 (-2.66) | 0.1% | 356 | -0.015 |
| momentum | wide | SPY>200d & stock>200d | 1650 | 33 | +0.157 | -1.09 | 1.20 | +0.019 (0.29) | 0.1% | 330 | +0.020 |
| momentum | wide | SPY>200d & stock>200d & RS>=0.8 | 717 | 33 | +0.195 | -1.06 | 0.58 | -0.138 (-1.85) | 0.0% | 149 | -0.080 |
| momentum | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 681 | 33 | +0.197 | -1.06 | 0.70 | -0.091 (-1.17) | 0.0% | 146 | -0.069 |
| momentum | wide | score>=70 & SPY>200d & stock>200d | 14 | 29 | -0.067 | -1.03 | 0.21 | +0.053 (0.10) | 0.0% | 3 | -1.139 |
| momentum | wide | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 7 | 43 | +0.753 | -0.96 | 0.86 | -0.006 (-0.01) | 0.0% | 2 | -1.102 |
| combined | wide | all | 2441 | 33 | +0.105 | -1.08 | 0.78 | -0.215 (-3.13) | 0.3% | 460 | +0.035 |
| combined | wide | SPY>200d & stock>200d | 2095 | 33 | +0.122 | -1.09 | 0.86 | -0.013 (-0.23) | 0.1% | 404 | +0.078 |
| combined | wide | SPY>200d & stock>200d & RS>=0.8 | 917 | 34 | +0.212 | -1.06 | 0.89 | -0.098 (-1.50) | 0.0% | 185 | -0.056 |
| combined | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 871 | 33 | +0.210 | -1.06 | 0.89 | -0.057 (-0.92) | 0.0% | 181 | -0.044 |
| combined | wide | score>=70 & SPY>200d & stock>200d | 172 | 31 | +0.101 | -0.99 | 0.44 | -0.088 (-0.49) | 0.0% | 30 | +0.152 |
| combined | wide | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 112 | 32 | +0.290 | -0.98 | 1.16 | -0.100 (-0.43) | 0.0% | 18 | +0.289 |
| baseline_random | wide | all | 5193 | 36 | +0.222 | -1.01 | 3.94 | — (—) | 0.7% | 993 | +0.189 |
| baseline_random | wide | SPY>200d & stock>200d | 3510 | 34 | +0.167 | -1.07 | 1.71 | — (—) | 0.2% | 709 | +0.120 |
| baseline_random | wide | SPY>200d & stock>200d & RS>=0.8 | 1482 | 35 | +0.247 | -1.04 | 2.24 | — (—) | 0.4% | 311 | +0.071 |
| baseline_random | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1334 | 35 | +0.246 | -1.05 | 2.01 | — (—) | 0.2% | 269 | +0.113 |

## Momentum rotation — universe: all (from 2018-01-03, 40 bps per side)

| benchmark | CAGR | max DD | Sharpe | train+val Sharpe | OOS CAGR | OOS Sharpe |
|---|---|---|---|---|---|---|
| SPY buy-and-hold | +14.5% | -34% | 0.81 | 0.76 | +16.7% | 1.00 |
| equal-weight universe (no costs) | +26.5% | -42% | 1.02 | 1.00 | +26.5% | 1.07 |

| rule set | trades/yr | exposure | win% | avg trade | avg days | CAGR | max DD | Sharpe | train+val Sharpe | OOS CAGR | OOS Sharpe | vs random | CAGR @15 / @70 bps | without best stock |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| top5, in RS>=0.8, out RS<0.5 | 10 | 93% | 37 | +15.4% | 107 | +18.2% | -80% | 0.57 | 0.47 | +45.4% | 0.87 | 20% | +19.2% / +17.0% | SE: +24.5%, Sharpe 0.66 |
| top5, in RS>=0.8, out RS<0.5, stop -20% | 16 | 92% | 29 | +16.8% | 68 | +27.3% | -67% | 0.70 | 0.70 | +25.4% | 0.67 | 65% | +28.8% / +25.5% | SE: +22.7%, Sharpe 0.64 |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d | 20 | 81% | 37 | +5.6% | 48 | +11.0% | -76% | 0.46 | 0.65 | -25.6% | -0.17 | 10% | +13.1% / +8.5% | MARA: +8.8%, Sharpe 0.42 |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | 26 | 80% | 32 | +3.0% | 37 | +6.1% | -73% | 0.37 | 0.46 | -11.8% | 0.09 | 5% | +8.6% / +3.2% | CELH: +11.7%, Sharpe 0.47 |
| top5, in RS>=0.8, out RS<0.7 | 12 | 93% | 44 | +11.3% | 93 | +17.5% | -76% | 0.57 | 0.51 | +31.3% | 0.74 | 20% | +18.7% / +16.0% | ENPH: +17.8%, Sharpe 0.57 |
| top5, in RS>=0.8, out RS<0.7, stop -20% | 18 | 92% | 33 | +8.5% | 60 | +17.2% | -78% | 0.56 | 0.42 | +57.0% | 0.98 | 20% | +19.1% / +14.8% | VKTX: +12.3%, Sharpe 0.49 |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d | 22 | 80% | 39 | +3.5% | 45 | +7.8% | -79% | 0.41 | 0.49 | -11.3% | 0.17 | 15% | +10.1% / +5.1% | TSLA: +13.5%, Sharpe 0.50 |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | 28 | 80% | 33 | +2.8% | 35 | +5.7% | -70% | 0.36 | 0.37 | +0.6% | 0.33 | 10% | +8.3% / +2.6% | CELH: +1.6%, Sharpe 0.29 |
| top8, in RS>=0.8, out RS<0.5 | 16 | 92% | 41 | +21.2% | 108 | +32.7% | -71% | 0.81 | 0.82 | +32.0% | 0.75 | 60% | +33.9% / +31.0% | SE: +30.3%, Sharpe 0.76 |
| top8, in RS>=0.8, out RS<0.5, stop -20% | 24 | 91% | 34 | +13.4% | 71 | +27.5% | -63% | 0.72 | 0.76 | +21.3% | 0.63 | 80% | +29.1% / +25.6% | SE: +22.1%, Sharpe 0.64 |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d | 30 | 80% | 38 | +8.9% | 52 | +29.0% | -58% | 0.76 | 0.78 | +26.3% | 0.69 | 85% | +31.2% / +26.5% | APP: +22.0%, Sharpe 0.65 |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | 37 | 80% | 34 | +6.5% | 42 | +25.3% | -68% | 0.70 | 0.70 | +27.9% | 0.71 | 85% | +27.7% / +22.5% | NIO: +26.5%, Sharpe 0.72 |
| top8, in RS>=0.8, out RS<0.7 | 19 | 92% | 48 | +18.5% | 95 | +35.6% | -58% | 0.82 | 0.84 | +34.7% | 0.78 | 85% | +37.0% / +34.0% | MARA: +29.9%, Sharpe 0.75 |
| top8, in RS>=0.8, out RS<0.7, stop -20% | 28 | 91% | 33 | +15.2% | 62 | +26.2% | -72% | 0.69 | 0.67 | +31.2% | 0.74 | 70% | +28.0% / +24.0% | MARA: +20.7%, Sharpe 0.62 |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d | 32 | 80% | 39 | +7.3% | 48 | +22.1% | -55% | 0.65 | 0.70 | +11.3% | 0.48 | 55% | +24.4% / +19.3% | MARA: +20.6%, Sharpe 0.63 |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | 40 | 80% | 33 | +9.2% | 38 | +26.7% | -66% | 0.70 | 0.75 | +12.6% | 0.50 | 75% | +29.6% / +23.4% | MARA: +26.5%, Sharpe 0.70 |

## Momentum rotation — universe: largecap_2015 (from 2018-01-03, 40 bps per side)

| benchmark | CAGR | max DD | Sharpe | train+val Sharpe | OOS CAGR | OOS Sharpe |
|---|---|---|---|---|---|---|
| SPY buy-and-hold | +14.5% | -34% | 0.81 | 0.76 | +16.7% | 1.00 |
| equal-weight universe (no costs) | +13.8% | -37% | 0.79 | 0.75 | +13.7% | 1.01 |

| rule set | trades/yr | exposure | win% | avg trade | avg days | CAGR | max DD | Sharpe | train+val Sharpe | OOS CAGR | OOS Sharpe | vs random | CAGR @15 / @70 bps | without best stock |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| top5, in RS>=0.8, out RS<0.5 | 10 | 95% | 43 | +6.5% | 111 | +14.6% | -37% | 0.66 | 0.49 | +36.4% | 1.18 | 95% | +15.7% / +13.3% | GE: +14.0%, Sharpe 0.63 |
| top5, in RS>=0.8, out RS<0.5, stop -20% | 11 | 94% | 48 | +6.6% | 108 | +15.1% | -37% | 0.68 | 0.52 | +36.2% | 1.17 | 95% | +16.2% / +13.8% | GE: +15.5%, Sharpe 0.68 |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d | 20 | 81% | 44 | +2.4% | 49 | +9.4% | -30% | 0.51 | 0.48 | +13.6% | 0.61 | 75% | +11.6% / +6.9% | AVGO: +9.5%, Sharpe 0.53 |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | 20 | 81% | 44 | +2.4% | 49 | +9.4% | -30% | 0.51 | 0.48 | +13.7% | 0.62 | 85% | +11.6% / +6.9% | AVGO: +9.5%, Sharpe 0.53 |
| top5, in RS>=0.8, out RS<0.7 | 14 | 94% | 45 | +3.3% | 82 | +11.9% | -36% | 0.56 | 0.50 | +20.4% | 0.74 | 90% | +13.4% / +10.2% | META: +9.7%, Sharpe 0.49 |
| top5, in RS>=0.8, out RS<0.7, stop -20% | 14 | 95% | 45 | +3.9% | 80 | +13.9% | -34% | 0.62 | 0.59 | +19.7% | 0.73 | 100% | +15.4% / +12.1% | META: +13.2%, Sharpe 0.60 |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d | 23 | 81% | 43 | +1.8% | 44 | +8.2% | -32% | 0.46 | 0.52 | +4.8% | 0.31 | 100% | +10.6% / +5.4% | AVGO: +7.0%, Sharpe 0.42 |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | 23 | 81% | 43 | +1.8% | 43 | +8.1% | -32% | 0.46 | 0.52 | +4.6% | 0.30 | 100% | +10.6% / +5.3% | AVGO: +7.1%, Sharpe 0.42 |
| top8, in RS>=0.8, out RS<0.5 | 17 | 94% | 45 | +7.1% | 109 | +16.1% | -29% | 0.76 | 0.63 | +29.8% | 1.20 | 100% | +17.2% / +14.7% | DVN: +13.9%, Sharpe 0.70 |
| top8, in RS>=0.8, out RS<0.5, stop -20% | 18 | 93% | 45 | +5.9% | 104 | +14.9% | -30% | 0.72 | 0.60 | +27.2% | 1.13 | 100% | +16.0% / +13.5% | DVN: +12.5%, Sharpe 0.65 |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d | 31 | 80% | 42 | +2.3% | 52 | +8.3% | -30% | 0.51 | 0.46 | +11.6% | 0.65 | 90% | +10.3% / +5.9% | DVN: +7.3%, Sharpe 0.47 |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | 31 | 80% | 42 | +2.2% | 51 | +8.3% | -30% | 0.51 | 0.47 | +11.5% | 0.64 | 95% | +10.3% / +5.8% | DVN: +7.3%, Sharpe 0.47 |
| top8, in RS>=0.8, out RS<0.7 | 23 | 93% | 46 | +3.6% | 80 | +12.1% | -27% | 0.63 | 0.60 | +14.9% | 0.72 | 100% | +13.6% / +10.3% | META: +9.2%, Sharpe 0.51 |
| top8, in RS>=0.8, out RS<0.7, stop -20% | 23 | 93% | 45 | +3.6% | 78 | +11.8% | -31% | 0.61 | 0.58 | +14.3% | 0.70 | 100% | +13.3% / +9.9% | AVGO: +9.4%, Sharpe 0.52 |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d | 35 | 80% | 45 | +1.5% | 45 | +6.8% | -32% | 0.44 | 0.48 | +4.5% | 0.32 | 85% | +9.2% / +4.1% | AVGO: +6.2%, Sharpe 0.42 |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | 36 | 80% | 45 | +1.5% | 44 | +6.8% | -32% | 0.44 | 0.48 | +4.4% | 0.31 | 90% | +9.1% / +4.1% | AVGO: +6.2%, Sharpe 0.42 |

## Rotation: pre-registered selection (2015 large caps, train+validation only)

Gates: train+val Sharpe > SPY's, ranking beats >= 90% of random selections, CAGR without the single best stock >= SPY's, max drawdown at most 10 points worse than SPY's.

**Chosen: none — no rule set passed every gate**

| rule set | passes | train+val Sharpe | failed gates |
|---|---|---|---|
| top5, in RS>=0.8, out RS<0.5 | ❌ | 0.49 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top5, in RS>=0.8, out RS<0.5, stop -20% | ❌ | 0.52 | train_val_sharpe_beats_spy |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d | ❌ | 0.48 | train_val_sharpe_beats_spy, ranking_beats_random, without_best_stock_beats_spy |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | ❌ | 0.48 | train_val_sharpe_beats_spy, ranking_beats_random, without_best_stock_beats_spy |
| top5, in RS>=0.8, out RS<0.7 | ❌ | 0.50 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top5, in RS>=0.8, out RS<0.7, stop -20% | ❌ | 0.59 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d | ❌ | 0.52 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | ❌ | 0.52 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5 | ❌ | 0.63 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5, stop -20% | ❌ | 0.60 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d | ❌ | 0.46 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | ❌ | 0.47 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.7 | ❌ | 0.60 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.7, stop -20% | ❌ | 0.58 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d | ❌ | 0.48 | train_val_sharpe_beats_spy, ranking_beats_random, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | ❌ | 0.48 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |

Calendar-year returns (2015 large caps, 40 bps per side):

| | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|---|---|---|---|
| SPY | -6% | +31% | +18% | +29% | -18% | +26% | +25% | +18% | +14% |
| equal-weight group | -7% | +29% | +14% | +31% | -4% | +16% | +16% | +17% | +13% |
| top5, in RS>=0.8, out RS<0.5 | -12% | +6% | +12% | +20% | -0% | +10% | +36% | +14% | +54% |
| top5, in RS>=0.8, out RS<0.5, stop -20% | -12% | +7% | +13% | +21% | -1% | +13% | +35% | +13% | +54% |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d | -7% | +1% | +14% | +20% | -3% | +19% | +18% | +7% | +17% |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | -8% | +1% | +14% | +21% | -3% | +19% | +18% | +7% | +17% |
| top5, in RS>=0.8, out RS<0.7 | -8% | +6% | +5% | +20% | -4% | +18% | +29% | -3% | +52% |
| top5, in RS>=0.8, out RS<0.7, stop -20% | -8% | +5% | +8% | +21% | +9% | +20% | +28% | -3% | +52% |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d | -3% | -5% | +7% | +20% | -4% | +19% | +28% | -6% | +23% |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | -3% | -5% | +7% | +20% | -4% | +19% | +28% | -7% | +23% |
| top8, in RS>=0.8, out RS<0.5 | -6% | +7% | +16% | +27% | -0% | +23% | +26% | +22% | +32% |
| top8, in RS>=0.8, out RS<0.5, stop -20% | -6% | +7% | +10% | +32% | +0% | +19% | +21% | +22% | +29% |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d | +2% | -6% | +10% | +29% | -4% | +12% | +12% | +13% | +10% |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | +2% | -6% | +10% | +29% | -4% | +12% | +12% | +13% | +9% |
| top8, in RS>=0.8, out RS<0.7 | -7% | +7% | +16% | +16% | +2% | +19% | +24% | +5% | +29% |
| top8, in RS>=0.8, out RS<0.7, stop -20% | -7% | +4% | +12% | +16% | +5% | +20% | +24% | +4% | +28% |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d | -0% | -0% | +10% | +16% | -6% | +7% | +22% | -0% | +13% |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | -0% | -1% | +10% | +16% | -6% | +7% | +22% | -0% | +13% |

## Mean R by year (all universe, fixed exit)

| group | policy | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| combined | all | +0.54 | -0.61 | +0.16 | +0.95 | -0.12 | -0.57 | +0.40 | +0.29 | +0.11 | -0.12 |
| combined | SPY>200d & stock>200d | +0.60 | -0.58 | -0.10 | +0.81 | -0.17 | -0.96 | +0.25 | +0.30 | +0.07 | -0.07 |
| combined | SPY>200d & stock>200d & RS>=0.8 | +0.68 | -0.40 | +0.33 | +1.36 | -0.52 | -0.51 | +0.25 | +0.50 | +0.75 | +0.22 |
| combined | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | +0.74 | -0.26 | +0.43 | +1.26 | -0.63 | -0.22 | +0.18 | +0.36 | +0.71 | +0.42 |
| combined | score>=70 & SPY>200d & stock>200d | +0.90 | +0.55 | +0.33 | +1.08 | -0.61 | -1.04 | +0.36 | +0.62 | +0.46 | +0.06 |
| combined | score>=70 & SPY>200d & stock>200d & RS>=0.8 | +0.73 | +1.25 | +0.52 | +1.02 | -0.59 | -1.22 | +0.34 | +0.93 | +0.64 | +0.13 |
| baseline_random | all | +0.87 | -0.04 | +0.44 | +0.90 | +0.07 | -0.34 | +0.52 | +0.34 | +0.23 | +0.13 |
| baseline_random | SPY>200d & stock>200d | +0.89 | -0.34 | +0.39 | +0.75 | +0.08 | -0.86 | +0.17 | +0.33 | +0.13 | +0.10 |
| baseline_random | SPY>200d & stock>200d & RS>=0.8 | +1.07 | +0.03 | +0.51 | +1.11 | -0.32 | -0.83 | +0.40 | +0.45 | +0.33 | +0.12 |
| baseline_random | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | +0.96 | +0.19 | +0.57 | +0.94 | -0.39 | -0.73 | +0.44 | +0.53 | +0.57 | +0.01 |