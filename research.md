# Strategy research

278 symbols with data (1 failed), 10 years of daily bars. Control group: 105 stocks that were already large caps in 2015. Primary cost 20 bps per side (USD account: courtage + slippage; 40 bps ≈ trading from a SEK account). Validation from 2023-01-31, out-of-sample (OOS) from 2024-12-02. Setups invalidated at the next open (skipped): 1751.

Portfolio: max 8 positions, max 3 new per day, 1% risk per trade, max 25% of equity per position, no leverage, marked to market daily. 'vs random' = share of 40 random-order portfolios from the same eligible trades that this ranking beat.

## Portfolio — universe: all

SPY buy-and-hold: +15.2%/yr, max DD -34%, Sharpe 0.85 · train+val Sharpe 0.82 · OOS +16.4%/yr, Sharpe 0.98

| rule set | trades/yr | exposure | win% | avgR | CAGR | max DD | Sharpe | train+val Sharpe | OOS CAGR | OOS Sharpe | vs random |
|---|---|---|---|---|---|---|---|---|---|---|---|
| random picks (reference) | 79.0 | 86% | 24 | +0.46 | +25.9% | -75% | 0.90 | 0.83 | +16.3% | 0.62 | — |
| random picks, trend filter | 68.9 | 79% | 23 | +0.39 | +15.5% | -64% | 0.68 | 0.76 | -1.2% | 0.13 | — |
| RS leaders, trend filter | 75.1 | 68% | 23 | +0.42 | +24.6% | -39% | 0.85 | 1.00 | -18.3% | -0.30 | 90% |
| RS leaders near 52w high | 65.0 | 75% | 24 | +0.57 | +32.8% | -33% | 1.08 | 1.07 | +36.6% | 1.07 | 100% |
| signals score>=70, trend | 45.9 | 63% | 22 | +0.33 | +12.1% | -35% | 0.65 | 0.81 | +5.0% | 0.34 | 28% |
| signals score>=70, trend, RS top 20% | 41.1 | 51% | 23 | +0.54 | +19.8% | -33% | 0.92 | 1.08 | +13.8% | 0.68 | 70% |
| signals, trend, RS top 20% | 77.1 | 78% | 22 | +0.76 | +38.3% | -48% | 1.11 | 1.19 | +37.1% | 1.00 | 100% |
| signals, trend, RS top 20%, near 52w high | 74.1 | 79% | 22 | +0.57 | +32.9% | -32% | 1.10 | 1.25 | +33.5% | 0.99 | 100% |

Cost sensitivity (full-period CAGR / Sharpe):

| rule set | 20 bps | 40 bps | 70 bps |
|---|---|---|---|
| RS leaders, trend filter | +24.6% / 0.85 | +20.7% / 0.75 | +15.1% / 0.60 |
| RS leaders near 52w high | +32.8% / 1.08 | +27.1% / 0.93 | +20.6% / 0.76 |
| signals score>=70, trend | +12.1% / 0.65 | +9.2% / 0.52 | +5.4% / 0.35 |
| signals score>=70, trend, RS top 20% | +19.8% / 0.92 | +17.2% / 0.82 | +13.5% / 0.68 |
| signals, trend, RS top 20% | +38.3% / 1.11 | +32.8% / 0.99 | +25.6% / 0.83 |
| signals, trend, RS top 20%, near 52w high | +32.9% / 1.10 | +27.4% / 0.96 | +20.3% / 0.77 |

Exit variant (stop 2.5 x ATR instead of 1.5 x ATR / structural):

| rule set | CAGR | max DD | Sharpe | OOS Sharpe |
|---|---|---|---|---|
| random picks (reference) | +11.5% | -37% | 0.61 | 0.00 |
| random picks, trend filter | +12.6% | -44% | 0.70 | 0.64 |
| RS leaders, trend filter | +16.8% | -33% | 0.83 | 0.28 |
| RS leaders near 52w high | +26.0% | -27% | 1.15 | 0.84 |
| signals score>=70, trend | +12.7% | -28% | 0.79 | 0.05 |
| signals score>=70, trend, RS top 20% | +17.6% | -28% | 1.03 | 0.62 |
| signals, trend, RS top 20% | +22.0% | -36% | 1.00 | 0.61 |
| signals, trend, RS top 20%, near 52w high | +16.5% | -24% | 0.82 | 0.49 |

### Per trade — universe: all (one position per symbol, t over monthly means)

| group | exit | policy | n | win% | avgR | medR | t | excess vs random (t) | ≥+50% | OOS n | OOS avgR |
|---|---|---|---|---|---|---|---|---|---|---|---|
| breakout | fixed | all | 6480 | 17 | +0.300 | -1.11 | 1.30 | -0.316 (-4.02) | 3.2% | 1448 | +0.009 |
| breakout | fixed | SPY>200d & stock>200d | 5141 | 17 | +0.254 | -1.12 | 0.67 | -0.221 (-3.34) | 3.0% | 1160 | +0.043 |
| breakout | fixed | SPY>200d & stock>200d & RS>=0.8 | 2122 | 18 | +0.453 | -1.07 | 1.78 | -0.108 (-1.09) | 5.5% | 506 | +0.591 |
| breakout | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1735 | 18 | +0.485 | -1.08 | 1.79 | -0.014 (-0.11) | 4.4% | 390 | +0.765 |
| breakout | fixed | score>=70 & SPY>200d & stock>200d | 748 | 23 | +0.480 | -1.00 | 2.35 | +0.038 (0.26) | 5.9% | 152 | +0.265 |
| breakout | fixed | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 456 | 23 | +0.596 | -0.98 | 2.79 | +0.149 (0.72) | 7.7% | 101 | +0.434 |
| momentum | fixed | all | 5373 | 22 | +0.271 | -1.04 | 2.01 | -0.286 (-3.89) | 3.6% | 1197 | +0.009 |
| momentum | fixed | SPY>200d & stock>200d | 4744 | 22 | +0.310 | -1.04 | 2.07 | -0.100 (-1.77) | 3.5% | 1083 | +0.035 |
| momentum | fixed | SPY>200d & stock>200d & RS>=0.8 | 1919 | 23 | +0.402 | -1.02 | 2.17 | -0.072 (-0.90) | 6.2% | 442 | +0.259 |
| momentum | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1587 | 23 | +0.408 | -1.03 | 2.11 | -0.029 (-0.30) | 4.6% | 354 | +0.224 |
| momentum | fixed | score>=70 & SPY>200d & stock>200d | 154 | 24 | +0.567 | -0.91 | 2.08 | +0.342 (1.25) | 13.0% | 38 | +0.894 |
| momentum | fixed | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 95 | 25 | +0.748 | -0.88 | 1.92 | +0.332 (0.88) | 15.8% | 26 | +0.976 |
| combined | fixed | all | 8154 | 19 | +0.283 | -1.08 | 1.72 | -0.299 (-4.55) | 3.3% | 1799 | +0.102 |
| combined | fixed | SPY>200d & stock>200d | 6721 | 19 | +0.252 | -1.08 | 1.10 | -0.179 (-3.41) | 3.1% | 1502 | +0.103 |
| combined | fixed | SPY>200d & stock>200d & RS>=0.8 | 2797 | 21 | +0.427 | -1.04 | 2.04 | -0.094 (-1.25) | 5.5% | 655 | +0.608 |
| combined | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 2306 | 21 | +0.428 | -1.05 | 2.01 | -0.026 (-0.30) | 4.3% | 508 | +0.629 |
| combined | fixed | score>=70 & SPY>200d & stock>200d | 822 | 23 | +0.504 | -0.98 | 2.17 | +0.031 (0.24) | 6.6% | 175 | +0.300 |
| combined | fixed | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 500 | 24 | +0.609 | -0.96 | 2.48 | +0.114 (0.60) | 8.6% | 116 | +0.451 |
| baseline_random | fixed | all | 17534 | 25 | +0.353 | -1.02 | 5.08 | — (—) | 5.2% | 4225 | +0.165 |
| baseline_random | fixed | SPY>200d & stock>200d | 11206 | 23 | +0.340 | -1.04 | 3.18 | — (—) | 3.7% | 2619 | +0.128 |
| baseline_random | fixed | SPY>200d & stock>200d & RS>=0.8 | 4634 | 23 | +0.346 | -1.03 | 3.07 | — (—) | 6.4% | 1137 | +0.227 |
| baseline_random | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 3182 | 23 | +0.393 | -1.04 | 2.73 | — (—) | 4.0% | 685 | +0.305 |
| breakout | wide | all | 5209 | 34 | +0.308 | -0.95 | 3.39 | -0.133 (-2.65) | 5.5% | 1147 | +0.247 |
| breakout | wide | SPY>200d & stock>200d | 4190 | 33 | +0.319 | -0.96 | 2.50 | -0.075 (-1.87) | 5.1% | 931 | +0.269 |
| breakout | wide | SPY>200d & stock>200d & RS>=0.8 | 1775 | 35 | +0.455 | -0.93 | 3.13 | +0.009 (0.13) | 9.2% | 418 | +0.436 |
| breakout | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1479 | 35 | +0.480 | -0.93 | 3.50 | +0.102 (1.48) | 7.4% | 328 | +0.387 |
| breakout | wide | score>=70 & SPY>200d & stock>200d | 721 | 33 | +0.394 | -0.91 | 2.80 | +0.021 (0.20) | 9.0% | 145 | +0.159 |
| breakout | wide | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 434 | 34 | +0.489 | -0.89 | 3.16 | +0.109 (0.71) | 11.5% | 95 | +0.294 |
| momentum | wide | all | 4471 | 32 | +0.274 | -0.98 | 2.96 | -0.154 (-2.84) | 4.8% | 967 | +0.135 |
| momentum | wide | SPY>200d & stock>200d | 3967 | 33 | +0.317 | -0.98 | 3.08 | -0.041 (-0.86) | 4.7% | 882 | +0.156 |
| momentum | wide | SPY>200d & stock>200d & RS>=0.8 | 1622 | 33 | +0.372 | -0.96 | 2.57 | -0.075 (-1.27) | 8.0% | 370 | +0.271 |
| momentum | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1369 | 33 | +0.352 | -0.97 | 2.31 | -0.049 (-0.80) | 5.8% | 295 | +0.271 |
| momentum | wide | score>=70 & SPY>200d & stock>200d | 138 | 32 | +0.338 | -0.88 | 1.52 | +0.047 (0.26) | 15.2% | 33 | +0.765 |
| momentum | wide | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 81 | 33 | +0.495 | -0.81 | 1.63 | +0.057 (0.22) | 19.8% | 22 | +1.011 |
| combined | wide | all | 6204 | 33 | +0.292 | -0.97 | 3.35 | -0.145 (-3.12) | 5.2% | 1354 | +0.207 |
| combined | wide | SPY>200d & stock>200d | 5181 | 33 | +0.315 | -0.98 | 2.68 | -0.068 (-1.87) | 4.8% | 1153 | +0.218 |
| combined | wide | SPY>200d & stock>200d & RS>=0.8 | 2244 | 34 | +0.398 | -0.95 | 2.89 | -0.043 (-0.75) | 8.3% | 528 | +0.378 |
| combined | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1877 | 34 | +0.406 | -0.95 | 3.05 | +0.028 (0.52) | 6.6% | 409 | +0.346 |
| combined | wide | score>=70 & SPY>200d & stock>200d | 780 | 33 | +0.388 | -0.90 | 2.44 | -0.004 (-0.04) | 9.1% | 163 | +0.239 |
| combined | wide | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 465 | 34 | +0.478 | -0.89 | 2.73 | +0.056 (0.41) | 12.0% | 106 | +0.396 |
| baseline_random | wide | all | 12403 | 36 | +0.315 | -0.94 | 5.48 | — (—) | 6.2% | 2827 | +0.194 |
| baseline_random | wide | SPY>200d & stock>200d | 8153 | 34 | +0.320 | -0.97 | 3.75 | — (—) | 4.8% | 1838 | +0.196 |
| baseline_random | wide | SPY>200d & stock>200d & RS>=0.8 | 3435 | 33 | +0.333 | -0.98 | 3.46 | — (—) | 8.3% | 809 | +0.297 |
| baseline_random | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 2549 | 33 | +0.342 | -0.99 | 3.02 | — (—) | 5.2% | 527 | +0.334 |

## Portfolio — universe: largecap_2015

SPY buy-and-hold: +15.2%/yr, max DD -34%, Sharpe 0.85 · train+val Sharpe 0.82 · OOS +16.4%/yr, Sharpe 0.98

| rule set | trades/yr | exposure | win% | avgR | CAGR | max DD | Sharpe | train+val Sharpe | OOS CAGR | OOS Sharpe | vs random |
|---|---|---|---|---|---|---|---|---|---|---|---|
| random picks (reference) | 44.9 | 87% | 23 | +0.17 | +6.5% | -36% | 0.47 | 0.33 | +12.0% | 0.80 | — |
| random picks, trend filter | 38.3 | 76% | 23 | +0.26 | +5.3% | -24% | 0.45 | 0.49 | +5.3% | 0.43 | — |
| RS leaders, trend filter | 42.1 | 76% | 24 | +0.29 | +12.0% | -28% | 0.69 | 0.80 | +8.1% | 0.48 | 95% |
| RS leaders near 52w high | 38.4 | 76% | 24 | +0.31 | +8.5% | -22% | 0.54 | 0.62 | +5.5% | 0.38 | 78% |
| signals score>=70, trend | 14.6 | 36% | 23 | +0.28 | +2.8% | -16% | 0.35 | 0.40 | +4.1% | 0.47 | 12% |
| signals score>=70, trend, RS top 20% | 10.7 | 25% | 22 | +0.35 | +2.4% | -19% | 0.34 | 0.46 | +2.0% | 0.30 | 5% |
| signals, trend, RS top 20% | 41.0 | 78% | 20 | +0.25 | +5.5% | -30% | 0.42 | 0.51 | +0.3% | 0.11 | 70% |
| signals, trend, RS top 20%, near 52w high | 42.0 | 78% | 20 | +0.25 | +6.2% | -33% | 0.47 | 0.58 | +0.3% | 0.10 | 82% |

Cost sensitivity (full-period CAGR / Sharpe):

| rule set | 20 bps | 40 bps | 70 bps |
|---|---|---|---|
| RS leaders, trend filter | +12.0% / 0.69 | +8.8% / 0.54 | +4.4% / 0.32 |
| RS leaders near 52w high | +8.5% / 0.54 | +5.5% / 0.39 | +1.1% / 0.16 |
| signals score>=70, trend | +2.8% / 0.35 | +1.5% / 0.21 | -0.4% / 0.00 |
| signals score>=70, trend, RS top 20% | +2.4% / 0.34 | +1.4% / 0.21 | -0.1% / 0.03 |
| signals, trend, RS top 20% | +5.5% / 0.42 | +2.2% / 0.22 | -2.5% / -0.07 |
| signals, trend, RS top 20%, near 52w high | +6.2% / 0.47 | +2.9% / 0.26 | -1.9% / -0.04 |

Exit variant (stop 2.5 x ATR instead of 1.5 x ATR / structural):

| rule set | CAGR | max DD | Sharpe | OOS Sharpe |
|---|---|---|---|---|
| random picks (reference) | +10.1% | -23% | 0.74 | 0.86 |
| random picks, trend filter | +7.9% | -33% | 0.67 | 0.67 |
| RS leaders, trend filter | +12.3% | -20% | 0.76 | 0.73 |
| RS leaders near 52w high | +9.1% | -21% | 0.61 | 0.27 |
| signals score>=70, trend | +1.5% | -16% | 0.21 | 0.34 |
| signals score>=70, trend, RS top 20% | +2.9% | -17% | 0.41 | 0.35 |
| signals, trend, RS top 20% | +6.8% | -21% | 0.52 | 0.15 |
| signals, trend, RS top 20%, near 52w high | +5.8% | -27% | 0.46 | 0.15 |

### Per trade — universe: largecap_2015 (one position per symbol, t over monthly means)

| group | exit | policy | n | win% | avgR | medR | t | excess vs random (t) | ≥+50% | OOS n | OOS avgR |
|---|---|---|---|---|---|---|---|---|---|---|---|
| breakout | fixed | all | 2259 | 17 | +0.084 | -1.17 | -0.58 | -0.410 (-3.32) | 0.2% | 433 | -0.217 |
| breakout | fixed | SPY>200d & stock>200d | 1853 | 16 | +0.007 | -1.18 | -0.69 | -0.325 (-2.94) | 0.1% | 358 | -0.195 |
| breakout | fixed | SPY>200d & stock>200d & RS>=0.8 | 754 | 19 | +0.309 | -1.12 | 1.35 | +0.090 (0.43) | 0.1% | 154 | +0.129 |
| breakout | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 707 | 18 | +0.328 | -1.12 | 1.42 | +0.136 (0.66) | 0.1% | 150 | +0.212 |
| breakout | fixed | score>=70 & SPY>200d & stock>200d | 157 | 22 | +0.196 | -1.02 | 0.94 | -0.104 (-0.37) | 0.0% | 27 | +0.444 |
| breakout | fixed | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 104 | 21 | +0.218 | -1.01 | 1.07 | -0.012 (-0.03) | 0.0% | 16 | +0.412 |
| momentum | fixed | all | 2170 | 22 | +0.173 | -1.10 | 1.06 | -0.247 (-2.57) | 0.1% | 429 | -0.088 |
| momentum | fixed | SPY>200d & stock>200d | 1935 | 22 | +0.210 | -1.10 | 0.89 | -0.165 (-1.97) | 0.1% | 393 | -0.027 |
| momentum | fixed | SPY>200d & stock>200d & RS>=0.8 | 827 | 22 | +0.234 | -1.08 | 0.19 | -0.224 (-2.02) | 0.0% | 167 | +0.053 |
| momentum | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 785 | 22 | +0.219 | -1.08 | 0.04 | -0.209 (-1.78) | 0.0% | 162 | +0.087 |
| momentum | fixed | score>=70 & SPY>200d & stock>200d | 15 | 20 | +0.106 | -1.03 | 0.39 | +0.144 (0.19) | 0.0% | 3 | -1.150 |
| momentum | fixed | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 8 | 25 | +0.909 | -0.90 | 0.74 | +0.378 (0.32) | 0.0% | 2 | -1.090 |
| combined | fixed | all | 3067 | 19 | +0.121 | -1.12 | 0.01 | -0.331 (-3.36) | 0.2% | 583 | -0.167 |
| combined | fixed | SPY>200d & stock>200d | 2619 | 19 | +0.087 | -1.13 | -0.31 | -0.258 (-3.20) | 0.1% | 499 | -0.133 |
| combined | fixed | SPY>200d & stock>200d & RS>=0.8 | 1120 | 20 | +0.223 | -1.08 | 0.25 | -0.177 (-1.81) | 0.0% | 217 | -0.029 |
| combined | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1062 | 20 | +0.210 | -1.09 | 0.26 | -0.144 (-1.51) | 0.0% | 212 | +0.033 |
| combined | fixed | score>=70 & SPY>200d & stock>200d | 168 | 22 | +0.229 | -1.02 | 1.10 | -0.079 (-0.29) | 0.0% | 30 | +0.284 |
| combined | fixed | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 110 | 22 | +0.308 | -0.99 | 1.33 | +0.077 (0.22) | 0.0% | 18 | +0.245 |
| baseline_random | fixed | all | 7140 | 26 | +0.305 | -1.06 | 3.98 | — (—) | 0.7% | 1507 | +0.153 |
| baseline_random | fixed | SPY>200d & stock>200d | 4715 | 24 | +0.259 | -1.08 | 2.86 | — (—) | 0.2% | 943 | +0.120 |
| baseline_random | fixed | SPY>200d & stock>200d & RS>=0.8 | 1935 | 23 | +0.252 | -1.08 | 2.16 | — (—) | 0.4% | 420 | +0.025 |
| baseline_random | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1753 | 22 | +0.236 | -1.09 | 1.96 | — (—) | 0.3% | 362 | +0.113 |
| breakout | wide | all | 1930 | 33 | +0.183 | -1.00 | 1.46 | -0.187 (-2.64) | 0.3% | 360 | +0.111 |
| breakout | wide | SPY>200d & stock>200d | 1586 | 33 | +0.198 | -1.01 | 1.45 | -0.100 (-1.60) | 0.2% | 300 | +0.166 |
| breakout | wide | SPY>200d & stock>200d & RS>=0.8 | 669 | 33 | +0.271 | -0.97 | 1.20 | -0.112 (-1.35) | 0.0% | 134 | +0.065 |
| breakout | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 632 | 33 | +0.272 | -0.97 | 1.27 | -0.077 (-0.86) | 0.0% | 130 | +0.088 |
| breakout | wide | score>=70 & SPY>200d & stock>200d | 157 | 32 | +0.169 | -0.93 | 0.61 | -0.216 (-1.18) | 0.0% | 27 | +0.314 |
| breakout | wide | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 104 | 32 | +0.306 | -0.93 | 1.20 | -0.073 (-0.32) | 0.0% | 16 | +0.448 |
| momentum | wide | all | 1846 | 32 | +0.186 | -1.02 | 1.95 | -0.153 (-2.08) | 0.1% | 355 | +0.029 |
| momentum | wide | SPY>200d & stock>200d | 1647 | 33 | +0.231 | -1.02 | 2.12 | -0.047 (-0.75) | 0.1% | 329 | +0.064 |
| momentum | wide | SPY>200d & stock>200d & RS>=0.8 | 714 | 34 | +0.266 | -0.99 | 1.41 | -0.115 (-1.94) | 0.0% | 146 | -0.048 |
| momentum | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 678 | 34 | +0.272 | -0.99 | 1.54 | -0.071 (-1.07) | 0.0% | 143 | -0.026 |
| momentum | wide | score>=70 & SPY>200d & stock>200d | 14 | 29 | +0.005 | -0.99 | 0.33 | -0.053 (-0.10) | 0.0% | 3 | -1.085 |
| momentum | wide | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 7 | 43 | +0.817 | -0.91 | 0.92 | +0.426 (0.50) | 0.0% | 2 | -1.053 |
| combined | wide | all | 2433 | 33 | +0.178 | -1.01 | 1.65 | -0.176 (-2.70) | 0.3% | 455 | +0.077 |
| combined | wide | SPY>200d & stock>200d | 2089 | 33 | +0.196 | -1.02 | 1.69 | -0.084 (-1.60) | 0.1% | 399 | +0.120 |
| combined | wide | SPY>200d & stock>200d & RS>=0.8 | 913 | 34 | +0.282 | -0.99 | 1.72 | -0.071 (-1.25) | 0.0% | 181 | -0.023 |
| combined | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 867 | 34 | +0.283 | -0.99 | 1.74 | -0.034 (-0.55) | 0.0% | 177 | -0.001 |
| combined | wide | score>=70 & SPY>200d & stock>200d | 167 | 32 | +0.176 | -0.93 | 0.82 | -0.192 (-1.08) | 0.0% | 30 | +0.174 |
| combined | wide | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 109 | 32 | +0.348 | -0.92 | 1.37 | -0.043 (-0.19) | 0.0% | 18 | +0.281 |
| baseline_random | wide | all | 5159 | 37 | +0.280 | -0.95 | 4.63 | — (—) | 0.9% | 1025 | +0.165 |
| baseline_random | wide | SPY>200d & stock>200d | 3525 | 34 | +0.249 | -1.00 | 3.28 | — (—) | 0.3% | 684 | +0.192 |
| baseline_random | wide | SPY>200d & stock>200d & RS>=0.8 | 1482 | 35 | +0.273 | -0.99 | 2.79 | — (—) | 0.5% | 298 | +0.095 |
| baseline_random | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1349 | 34 | +0.254 | -1.00 | 2.61 | — (—) | 0.2% | 262 | +0.147 |

## Momentum rotation — universe: all (from 2018-01-12, 20 bps per side)

| benchmark | CAGR | max DD | Sharpe | train+val Sharpe | OOS CAGR | OOS Sharpe |
|---|---|---|---|---|---|---|
| SPY buy-and-hold | +14.3% | -34% | 0.80 | 0.76 | +16.4% | 0.98 |
| equal-weight universe (no costs) | +26.2% | -42% | 1.01 | 1.01 | +25.6% | 1.04 |

| rule set | trades/yr | exposure | win% | avg trade | avg days | CAGR | max DD | Sharpe | train+val Sharpe | OOS CAGR | OOS Sharpe | vs random | CAGR @40 / @70 bps | without best stock |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| top5, in RS>=0.8, out RS<0.5 | 10 | 92% | 39 | +21.4% | 107 | +25.6% | -81% | 0.68 | 0.61 | +52.6% | 0.93 | 35% | +24.8% / +23.5% | SE: +28.1%, Sharpe 0.71 |
| top5, in RS>=0.8, out RS<0.5, stop -20% | 15 | 92% | 33 | +15.4% | 71 | +25.3% | -70% | 0.68 | 0.68 | +29.5% | 0.72 | 80% | +24.1% / +22.3% | RKLB: +20.9%, Sharpe 0.62 |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d | 20 | 81% | 38 | +6.5% | 48 | +15.0% | -74% | 0.53 | 0.72 | -19.8% | -0.05 | 30% | +13.3% / +10.7% | MARA: +12.5%, Sharpe 0.48 |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | 25 | 80% | 34 | +3.3% | 39 | +8.1% | -71% | 0.41 | 0.50 | -8.3% | 0.15 | 5% | +6.2% / +3.4% | CELH: +13.8%, Sharpe 0.51 |
| top5, in RS>=0.8, out RS<0.7 | 12 | 93% | 45 | +12.5% | 93 | +20.7% | -76% | 0.61 | 0.56 | +37.5% | 0.80 | 20% | +19.6% / +18.1% | ENPH: +20.6%, Sharpe 0.61 |
| top5, in RS>=0.8, out RS<0.7, stop -20% | 17 | 93% | 36 | +11.0% | 65 | +23.0% | -77% | 0.64 | 0.53 | +62.8% | 1.03 | 60% | +21.5% / +19.3% | ENPH: +22.1%, Sharpe 0.63 |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d | 22 | 80% | 40 | +4.3% | 45 | +11.5% | -77% | 0.47 | 0.57 | -6.5% | 0.25 | 15% | +9.6% / +6.9% | TSLA: +17.3%, Sharpe 0.56 |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | 27 | 80% | 35 | +3.5% | 36 | +8.6% | -68% | 0.42 | 0.46 | +3.7% | 0.38 | 5% | +6.6% / +3.6% | CELH: +4.5%, Sharpe 0.34 |
| top8, in RS>=0.8, out RS<0.5 | 16 | 92% | 42 | +22.3% | 109 | +36.4% | -69% | 0.86 | 0.90 | +36.1% | 0.80 | 80% | +35.5% / +34.2% | SE: +33.3%, Sharpe 0.81 |
| top8, in RS>=0.8, out RS<0.5, stop -20% | 24 | 93% | 33 | +10.6% | 70 | +25.1% | -71% | 0.69 | 0.71 | +26.3% | 0.68 | 30% | +23.9% / +22.0% | SE: +24.8%, Sharpe 0.68 |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d | 30 | 80% | 40 | +9.4% | 52 | +31.8% | -58% | 0.80 | 0.84 | +29.0% | 0.72 | 85% | +30.1% / +27.5% | APP: +24.8%, Sharpe 0.70 |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | 36 | 80% | 35 | +6.5% | 42 | +25.6% | -67% | 0.71 | 0.73 | +28.9% | 0.72 | 60% | +23.7% / +21.0% | NIO: +26.9%, Sharpe 0.73 |
| top8, in RS>=0.8, out RS<0.7 | 19 | 92% | 48 | +18.5% | 94 | +35.8% | -58% | 0.83 | 0.85 | +39.0% | 0.82 | 90% | +34.6% / +33.0% | MARA: +29.8%, Sharpe 0.76 |
| top8, in RS>=0.8, out RS<0.7, stop -20% | 28 | 91% | 33 | +14.8% | 62 | +25.9% | -71% | 0.69 | 0.67 | +35.6% | 0.79 | 35% | +24.5% / +22.3% | MARA: +19.2%, Sharpe 0.59 |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d | 32 | 80% | 41 | +7.8% | 48 | +23.9% | -54% | 0.68 | 0.75 | +14.2% | 0.52 | 55% | +22.1% / +19.3% | MARA: +22.7%, Sharpe 0.67 |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | 40 | 80% | 34 | +9.2% | 38 | +27.4% | -63% | 0.71 | 0.77 | +15.8% | 0.55 | 80% | +25.1% / +21.8% | MARA: +24.5%, Sharpe 0.67 |
| top8, in RS>=0.8, out RS<0.5, 12-1 month momentum | 18 | 91% | 33 | +20.3% | 99 | +27.0% | -63% | 0.73 | 0.69 | +44.0% | 0.88 | 60% | +26.0% / +24.6% | SE: +24.3%, Sharpe 0.68 |
| top8, in RS>=0.8, out RS<0.5, monthly | 11 | 94% | 39 | +49.3% | 150 | +37.6% | -63% | 0.87 | 0.81 | +66.0% | 1.10 | 75% | +37.0% / +35.9% | ENPH: +34.6%, Sharpe 0.84 |
| top8, in RS>=0.8, out RS<0.5, volatility-adjusted | 14 | 93% | 46 | +26.3% | 126 | +38.0% | -47% | 0.98 | 0.97 | +60.4% | 1.10 | 100% | +37.1% / +35.8% | RKLB: +31.8%, Sharpe 0.87 |

## Momentum rotation — universe: largecap_2015 (from 2018-01-12, 20 bps per side)

| benchmark | CAGR | max DD | Sharpe | train+val Sharpe | OOS CAGR | OOS Sharpe |
|---|---|---|---|---|---|---|
| SPY buy-and-hold | +14.3% | -34% | 0.80 | 0.76 | +16.4% | 0.98 |
| equal-weight universe (no costs) | +13.3% | -37% | 0.77 | 0.75 | +12.7% | 0.94 |

| rule set | trades/yr | exposure | win% | avg trade | avg days | CAGR | max DD | Sharpe | train+val Sharpe | OOS CAGR | OOS Sharpe | vs random | CAGR @40 / @70 bps | without best stock |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| top5, in RS>=0.8, out RS<0.5 | 10 | 95% | 47 | +7.3% | 115 | +16.1% | -36% | 0.71 | 0.56 | +36.4% | 1.18 | 100% | +15.3% / +14.0% | DVN: +13.1%, Sharpe 0.62 |
| top5, in RS>=0.8, out RS<0.5, stop -20% | 10 | 94% | 51 | +7.5% | 111 | +16.6% | -36% | 0.73 | 0.58 | +36.1% | 1.17 | 95% | +15.7% / +14.4% | DVN: +13.6%, Sharpe 0.64 |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d | 20 | 81% | 47 | +3.0% | 50 | +11.8% | -25% | 0.61 | 0.60 | +14.9% | 0.66 | 80% | +10.1% / +7.5% | AVGO: +11.7%, Sharpe 0.63 |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | 20 | 81% | 48 | +3.0% | 49 | +11.9% | -25% | 0.62 | 0.61 | +15.0% | 0.66 | 100% | +10.2% / +7.6% | AVGO: +11.7%, Sharpe 0.63 |
| top5, in RS>=0.8, out RS<0.7 | 14 | 94% | 49 | +3.8% | 83 | +13.3% | -36% | 0.61 | 0.56 | +21.6% | 0.77 | 100% | +12.2% / +10.4% | META: +11.4%, Sharpe 0.55 |
| top5, in RS>=0.8, out RS<0.7, stop -20% | 14 | 95% | 49 | +4.4% | 80 | +15.4% | -33% | 0.67 | 0.65 | +20.9% | 0.76 | 100% | +14.2% / +12.4% | META: +15.0%, Sharpe 0.66 |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d | 22 | 81% | 47 | +2.3% | 44 | +10.5% | -29% | 0.56 | 0.64 | +7.0% | 0.38 | 95% | +8.5% / +5.7% | AVGO: +9.3%, Sharpe 0.52 |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | 23 | 81% | 48 | +2.3% | 43 | +10.4% | -29% | 0.56 | 0.63 | +6.8% | 0.38 | 100% | +8.4% / +5.6% | AVGO: +9.3%, Sharpe 0.52 |
| top8, in RS>=0.8, out RS<0.5 | 17 | 94% | 46 | +7.2% | 110 | +15.8% | -29% | 0.76 | 0.64 | +29.0% | 1.18 | 100% | +14.9% / +13.6% | DVN: +13.6%, Sharpe 0.69 |
| top8, in RS>=0.8, out RS<0.5, stop -20% | 17 | 94% | 47 | +6.0% | 105 | +14.6% | -29% | 0.71 | 0.60 | +26.7% | 1.11 | 95% | +13.7% / +12.4% | DVN: +12.2%, Sharpe 0.64 |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d | 30 | 80% | 44 | +2.5% | 52 | +8.9% | -27% | 0.55 | 0.51 | +12.2% | 0.67 | 90% | +7.3% / +5.0% | DVN: +8.2%, Sharpe 0.52 |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | 31 | 80% | 44 | +2.5% | 51 | +9.0% | -27% | 0.55 | 0.52 | +12.0% | 0.67 | 80% | +7.3% / +5.0% | DVN: +8.2%, Sharpe 0.52 |
| top8, in RS>=0.8, out RS<0.7 | 22 | 93% | 49 | +3.9% | 80 | +12.7% | -26% | 0.65 | 0.63 | +15.6% | 0.74 | 100% | +11.6% / +9.8% | META: +9.8%, Sharpe 0.54 |
| top8, in RS>=0.8, out RS<0.7, stop -20% | 23 | 93% | 48 | +3.9% | 78 | +12.4% | -29% | 0.64 | 0.62 | +15.0% | 0.72 | 100% | +11.2% / +9.4% | AVGO: +10.0%, Sharpe 0.54 |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d | 35 | 80% | 47 | +1.8% | 45 | +8.3% | -29% | 0.52 | 0.56 | +6.0% | 0.39 | 100% | +6.4% / +3.8% | AVGO: +7.6%, Sharpe 0.49 |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | 35 | 80% | 47 | +1.8% | 45 | +8.2% | -29% | 0.51 | 0.56 | +5.9% | 0.38 | 90% | +6.4% / +3.7% | AVGO: +7.7%, Sharpe 0.49 |
| top8, in RS>=0.8, out RS<0.5, 12-1 month momentum | 19 | 90% | 32 | +2.5% | 92 | +5.8% | -40% | 0.37 | 0.36 | +6.6% | 0.41 | 15% | +4.9% / +3.6% | GE: +4.2%, Sharpe 0.30 |
| top8, in RS>=0.8, out RS<0.5, monthly | 12 | 93% | 49 | +9.5% | 146 | +13.7% | -26% | 0.67 | 0.59 | +21.8% | 0.93 | 95% | +13.0% / +13.6% | DVN: +13.5%, Sharpe 0.65 |
| top8, in RS>=0.8, out RS<0.5, volatility-adjusted | 16 | 93% | 54 | +6.2% | 114 | +11.6% | -23% | 0.68 | 0.66 | +12.9% | 0.84 | 100% | +10.7% / +9.5% | GE: +8.6%, Sharpe 0.54 |

## Rotation: pre-registered selection (2015 large caps, train+validation only)

Gates: train+val Sharpe > SPY's, ranking beats >= 90% of random selections, CAGR without the single best stock >= SPY's, max drawdown at most 10 points worse than SPY's.

**Chosen: none — no rule set passed every gate**

| rule set | passes | train+val Sharpe | failed gates |
|---|---|---|---|
| top5, in RS>=0.8, out RS<0.5 | ❌ | 0.56 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top5, in RS>=0.8, out RS<0.5, stop -20% | ❌ | 0.58 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d | ❌ | 0.60 | train_val_sharpe_beats_spy, ranking_beats_random, without_best_stock_beats_spy |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | ❌ | 0.61 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top5, in RS>=0.8, out RS<0.7 | ❌ | 0.56 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top5, in RS>=0.8, out RS<0.7, stop -20% | ❌ | 0.65 | train_val_sharpe_beats_spy |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d | ❌ | 0.64 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | ❌ | 0.63 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5 | ❌ | 0.64 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5, stop -20% | ❌ | 0.60 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d | ❌ | 0.51 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | ❌ | 0.52 | train_val_sharpe_beats_spy, ranking_beats_random, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.7 | ❌ | 0.63 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.7, stop -20% | ❌ | 0.62 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d | ❌ | 0.56 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | ❌ | 0.56 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5, 12-1 month momentum | ❌ | 0.36 | train_val_sharpe_beats_spy, ranking_beats_random, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5, monthly | ❌ | 0.59 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5, volatility-adjusted | ❌ | 0.66 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |

Calendar-year returns (2015 large caps, 20 bps per side):

| | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|---|---|---|---|
| SPY | -8% | +31% | +18% | +29% | -18% | +26% | +25% | +18% | +15% |
| equal-weight group | -9% | +29% | +14% | +31% | -4% | +16% | +16% | +17% | +12% |
| top5, in RS>=0.8, out RS<0.5 | -7% | +8% | +13% | +21% | +0% | +11% | +37% | +15% | +54% |
| top5, in RS>=0.8, out RS<0.5, stop -20% | -7% | +8% | +14% | +22% | -0% | +14% | +36% | +14% | +54% |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d | -0% | +3% | +16% | +21% | -1% | +21% | +19% | +9% | +19% |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | -0% | +3% | +16% | +22% | -1% | +21% | +19% | +9% | +19% |
| top5, in RS>=0.8, out RS<0.7 | -5% | +8% | +7% | +21% | -4% | +19% | +30% | -2% | +53% |
| top5, in RS>=0.8, out RS<0.7, stop -20% | -5% | +7% | +9% | +22% | +10% | +21% | +30% | -2% | +52% |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d | +1% | -3% | +8% | +21% | -2% | +22% | +29% | -5% | +25% |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | +1% | -3% | +8% | +21% | -2% | +22% | +29% | -5% | +25% |
| top8, in RS>=0.8, out RS<0.5 | -11% | +8% | +17% | +28% | +0% | +23% | +27% | +22% | +30% |
| top8, in RS>=0.8, out RS<0.5, stop -20% | -11% | +8% | +11% | +33% | +1% | +20% | +22% | +23% | +27% |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d | -2% | -5% | +11% | +30% | -2% | +14% | +13% | +14% | +9% |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | -2% | -4% | +11% | +30% | -2% | +14% | +13% | +14% | +8% |
| top8, in RS>=0.8, out RS<0.7 | -9% | +9% | +17% | +18% | +2% | +20% | +25% | +6% | +29% |
| top8, in RS>=0.8, out RS<0.7, stop -20% | -9% | +6% | +13% | +18% | +6% | +21% | +25% | +5% | +29% |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d | -2% | +2% | +12% | +18% | -4% | +9% | +24% | +2% | +15% |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | -2% | +2% | +12% | +18% | -4% | +9% | +24% | +1% | +15% |
| top8, in RS>=0.8, out RS<0.5, 12-1 month momentum | -16% | +10% | +2% | +24% | -12% | +2% | +41% | -1% | +12% |
| top8, in RS>=0.8, out RS<0.5, monthly | -3% | +12% | +16% | +19% | -5% | +26% | +23% | +5% | +33% |
| top8, in RS>=0.8, out RS<0.5, volatility-adjusted | -10% | +17% | +3% | +22% | -8% | +18% | +38% | +20% | +9% |

## Rockets (from 2016-10-26, 20 bps per side, 10 slots x 10%, max 3 new per day)

Rocket day: close >= +jump vs previous close, volume >= 3x the 20-day average, close in the top quarter of the day's range, price >= $5, 20-day dollar volume >= $5M. Buy next open; sell next open after a close more than `trail` below the highest close, or after 40 sessions. 'Random' = same stocks, same liquidity filter, same exit, random dates.

SPY: +15.8%/yr, max DD -34%, Sharpe 0.90 · train+val +15.6%/yr, Sharpe 0.89

| variant | trades | win% | avg trade | median | ≥+50% | worst | random avg | excess vs random t (train+val) | 2015 large caps excess | CAGR | max DD | Sharpe | train+val CAGR / Sharpe | OOS CAGR | random-entry portfolio CAGR | without top 3 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| EPS surprise>0%, reaction>=5% | 1885 | 54 | +4.7% | +2.0% | 4.3% | -51% | +4.4% | -0.15% (-0.25) | -0.24% (n=550) | +7.7% | -41% | 0.45 | +12.6% / 0.65 | -8.6% | +28.8% | +7.7% |
| EPS surprise>0%, reaction>=10% | 915 | 54 | +6.4% | +2.1% | 6.2% | -51% | +4.4% | +0.95% (0.95) | +1.88% (n=125) | +23.4% | -42% | 0.98 | +25.2% / 1.06 | +19.5% | +28.8% | +22.9% |
| EPS surprise>10%, reaction>=5% | 1263 | 54 | +5.1% | +2.1% | 5.1% | -51% | +4.4% | +0.73% (0.89) | -0.67% (n=264) | +12.8% | -44% | 0.62 | +21.2% / 0.93 | -20.8% | +28.8% | +10.7% |
| EPS surprise>10%, reaction>=10% | 709 | 54 | +6.8% | +2.6% | 6.6% | -51% | +4.4% | +1.82% (1.53) | +2.46% (n=68) | +18.8% | -44% | 0.80 | +27.0% / 1.06 | -14.3% | +28.8% | +16.8% |
| EPS surprise>20%, reaction>=10%, volume>=2x, RS>=0.8 | 235 | 57 | +8.8% | +3.9% | 7.2% | -34% | +4.4% | +3.40% (1.56) | +4.07% (n=14) | +17.8% | -27% | 0.92 | +24.6% / 1.26 | -9.7% | +28.8% | +11.8% |
| EPS surprise>20%, reaction>=15%, volume>=2x, RS>=0.8 | 167 | 58 | +9.1% | +4.0% | 8.4% | -33% | +4.4% | +1.52% (0.63) | —% (n=4) | +14.8% | -21% | 0.90 | +17.7% / 1.13 | -2.0% | +28.8% | +10.2% |
| jump>=8%, trail 15% | 995 | 45 | +4.0% | -2.7% | 5.2% | -52% | +2.3% | +0.09% (0.09) | -1.57% (n=114) | +15.7% | -48% | 0.63 | +22.3% / 0.80 | -17.6% | +27.6% | +9.9% |
| jump>=8%, trail 25% | 995 | 51 | +5.3% | +0.6% | 6.7% | -61% | +3.0% | +0.68% (0.58) | -1.49% (n=114) | +15.8% | -68% | 0.62 | +22.7% / 0.80 | -11.8% | +16.9% | +11.8% |
| jump>=15%, trail 15% | 538 | 43 | +4.7% | -4.6% | 6.7% | -52% | +2.3% | -0.16% (-0.11) | -4.77% (n=23) | +17.7% | -38% | 0.70 | +21.3% / 0.79 | -2.7% | +27.6% | +11.4% |
| jump>=15%, trail 25% | 538 | 47 | +6.6% | -2.2% | 9.1% | -61% | +3.0% | +1.27% (0.69) | -4.98% (n=23) | +14.4% | -60% | 0.57 | +19.5% / 0.69 | -12.8% | +16.9% | +6.1% |

Pre-registered gates: excess vs random entries t >= 2 (train+val); portfolio beats SPY on train+val CAGR and Sharpe; positive excess among 2015 large caps; CAGR without the 3 best stocks >= SPY's; max drawdown >= -50%.

**Chosen: none — no rocket variant passed every gate**

| variant | passes | failed gates |
|---|---|---|
| EPS surprise>0%, reaction>=5% | ❌ | beats_random_entries_same_stocks, beats_spy_train_val, holds_in_2015_largecaps, without_top3_beats_spy |
| EPS surprise>0%, reaction>=10% | ❌ | beats_random_entries_same_stocks |
| EPS surprise>10%, reaction>=5% | ❌ | beats_random_entries_same_stocks, holds_in_2015_largecaps, without_top3_beats_spy |
| EPS surprise>10%, reaction>=10% | ❌ | beats_random_entries_same_stocks |
| EPS surprise>20%, reaction>=10%, volume>=2x, RS>=0.8 | ❌ | beats_random_entries_same_stocks, without_top3_beats_spy |
| EPS surprise>20%, reaction>=15%, volume>=2x, RS>=0.8 | ❌ | beats_random_entries_same_stocks, holds_in_2015_largecaps, without_top3_beats_spy |
| jump>=8%, trail 15% | ❌ | beats_random_entries_same_stocks, beats_spy_train_val, holds_in_2015_largecaps, without_top3_beats_spy |
| jump>=8%, trail 25% | ❌ | beats_random_entries_same_stocks, beats_spy_train_val, holds_in_2015_largecaps, without_top3_beats_spy, drawdown_tolerable |
| jump>=15%, trail 15% | ❌ | beats_random_entries_same_stocks, beats_spy_train_val, holds_in_2015_largecaps, without_top3_beats_spy |
| jump>=15%, trail 25% | ❌ | beats_random_entries_same_stocks, beats_spy_train_val, holds_in_2015_largecaps, without_top3_beats_spy, drawdown_tolerable |

## Mean R by year (all universe, fixed exit)

| group | policy | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| combined | all | +0.96 | -0.43 | +0.30 | +1.07 | +0.03 | -0.44 | +0.53 | +0.42 | +0.23 | +0.01 |
| combined | SPY>200d & stock>200d | +1.01 | -0.42 | +0.03 | +0.94 | -0.03 | -0.79 | +0.38 | +0.42 | +0.19 | +0.05 |
| combined | SPY>200d & stock>200d & RS>=0.8 | +1.02 | -0.27 | +0.35 | +1.46 | -0.41 | -0.36 | +0.35 | +0.60 | +0.83 | +0.38 |
| combined | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | +1.12 | -0.13 | +0.45 | +1.36 | -0.52 | -0.07 | +0.30 | +0.46 | +0.81 | +0.59 |
| combined | score>=70 & SPY>200d & stock>200d | +0.97 | +0.65 | +0.42 | +1.15 | -0.54 | -0.96 | +0.43 | +0.69 | +0.52 | +0.14 |
| combined | score>=70 & SPY>200d & stock>200d & RS>=0.8 | +0.53 | +1.33 | +0.61 | +1.08 | -0.53 | -1.15 | +0.41 | +1.00 | +0.70 | +0.22 |
| baseline_random | all | +1.01 | +0.14 | +0.49 | +1.17 | +0.17 | -0.24 | +0.55 | +0.48 | +0.23 | +0.15 |
| baseline_random | SPY>200d & stock>200d | +1.13 | -0.20 | +0.42 | +1.19 | +0.14 | -0.73 | +0.32 | +0.51 | +0.17 | +0.11 |
| baseline_random | SPY>200d & stock>200d & RS>=0.8 | +1.07 | +0.04 | +0.37 | +1.63 | -0.23 | -0.51 | +0.34 | +0.53 | +0.35 | +0.11 |
| baseline_random | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | +0.86 | +0.17 | +0.43 | +1.35 | -0.23 | -0.37 | +0.43 | +0.54 | +0.45 | +0.15 |