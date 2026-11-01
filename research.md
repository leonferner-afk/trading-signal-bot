# Strategy research

278 symbols with data (1 failed), 10 years of daily bars. Control group: 105 stocks that were already large caps in 2015. Primary cost 20 bps per side (USD account: courtage + slippage; 40 bps ≈ trading from a SEK account). Validation from 2023-02-25, out-of-sample (OOS) from 2024-12-27. Setups invalidated at the next open (skipped): 1300.

Portfolio: max 8 positions, max 3 new per day, 1% risk per trade, max 25% of equity per position, no leverage, marked to market daily. 'vs random' = share of 40 random-order portfolios from the same eligible trades that this ranking beat.

## Portfolio — universe: all

SPY buy-and-hold: +14.9%/yr, max DD -34%, Sharpe 0.84 · train+val Sharpe 0.83 · OOS +15.2%/yr, Sharpe 0.92

| rule set | trades/yr | exposure | win% | avgR | CAGR | max DD | Sharpe | train+val Sharpe | OOS CAGR | OOS Sharpe | vs random |
|---|---|---|---|---|---|---|---|---|---|---|---|
| random picks (reference) | 79.7 | 86% | 21 | +0.22 | +6.6% | -61% | 0.36 | 0.58 | -14.3% | -0.33 | — |
| random picks, trend filter | 63.1 | 78% | 22 | +0.35 | +13.8% | -40% | 0.64 | 0.64 | +12.4% | 0.56 | — |
| RS leaders, trend filter | 73.1 | 66% | 23 | +0.40 | +21.5% | -42% | 0.75 | 0.94 | -4.8% | 0.07 | 97% |
| RS leaders near 52w high | 65.4 | 76% | 25 | +0.62 | +32.6% | -34% | 1.06 | 1.19 | +24.4% | 0.75 | 100% |
| signals score>=70, trend | 46.7 | 63% | 22 | +0.32 | +11.7% | -35% | 0.63 | 0.77 | +0.3% | 0.13 | 30% |
| signals score>=70, trend, RS top 20% | 41.5 | 50% | 22 | +0.49 | +18.6% | -33% | 0.88 | 0.99 | +7.7% | 0.44 | 72% |
| signals, trend, RS top 20% | 77.1 | 78% | 22 | +0.70 | +38.9% | -48% | 1.12 | 1.31 | +18.6% | 0.63 | 100% |
| signals, trend, RS top 20%, near 52w high | 75.0 | 79% | 22 | +0.53 | +29.1% | -32% | 1.00 | 1.18 | +20.4% | 0.70 | 100% |

Cost sensitivity (full-period CAGR / Sharpe):

| rule set | 20 bps | 40 bps | 70 bps |
|---|---|---|---|
| RS leaders, trend filter | +21.5% / 0.75 | +17.9% / 0.66 | +12.6% / 0.52 |
| RS leaders near 52w high | +32.6% / 1.06 | +28.2% / 0.95 | +21.4% / 0.78 |
| signals score>=70, trend | +11.7% / 0.63 | +8.7% / 0.50 | +4.8% / 0.33 |
| signals score>=70, trend, RS top 20% | +18.6% / 0.88 | +16.1% / 0.78 | +12.3% / 0.63 |
| signals, trend, RS top 20% | +38.9% / 1.12 | +33.2% / 1.00 | +26.5% / 0.85 |
| signals, trend, RS top 20%, near 52w high | +29.1% / 1.00 | +23.8% / 0.86 | +17.0% / 0.67 |

Exit variant (stop 2.5 x ATR instead of 1.5 x ATR / structural):

| rule set | CAGR | max DD | Sharpe | OOS Sharpe |
|---|---|---|---|---|
| random picks (reference) | +14.1% | -32% | 0.74 | -0.42 |
| random picks, trend filter | +13.8% | -35% | 0.76 | 0.37 |
| RS leaders, trend filter | +18.6% | -27% | 0.88 | 0.69 |
| RS leaders near 52w high | +24.5% | -24% | 1.07 | 0.34 |
| signals score>=70, trend | +12.3% | -28% | 0.77 | -0.09 |
| signals score>=70, trend, RS top 20% | +17.1% | -28% | 1.00 | 0.32 |
| signals, trend, RS top 20% | +18.1% | -36% | 0.86 | 0.41 |
| signals, trend, RS top 20%, near 52w high | +16.3% | -26% | 0.80 | 0.43 |

### Per trade — universe: all (one position per symbol, t over monthly means)

| group | exit | policy | n | win% | avgR | medR | t | excess vs random (t) | ≥+50% | OOS n | OOS avgR |
|---|---|---|---|---|---|---|---|---|---|---|---|
| breakout | fixed | all | 6504 | 17 | +0.283 | -1.11 | 1.29 | -0.327 (-3.88) | 3.2% | 1449 | +0.002 |
| breakout | fixed | SPY>200d & stock>200d | 5157 | 16 | +0.228 | -1.12 | 0.58 | -0.224 (-3.19) | 3.0% | 1167 | +0.009 |
| breakout | fixed | SPY>200d & stock>200d & RS>=0.8 | 2133 | 18 | +0.406 | -1.08 | 1.52 | -0.198 (-1.90) | 5.4% | 503 | +0.467 |
| breakout | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1741 | 18 | +0.445 | -1.08 | 1.48 | -0.093 (-0.78) | 4.4% | 384 | +0.666 |
| breakout | fixed | score>=70 & SPY>200d & stock>200d | 747 | 22 | +0.465 | -1.00 | 2.43 | +0.065 (0.43) | 5.9% | 139 | +0.312 |
| breakout | fixed | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 454 | 23 | +0.567 | -0.98 | 2.56 | +0.072 (0.35) | 7.7% | 91 | +0.450 |
| momentum | fixed | all | 5394 | 22 | +0.262 | -1.04 | 1.89 | -0.303 (-4.02) | 3.6% | 1204 | +0.054 |
| momentum | fixed | SPY>200d & stock>200d | 4765 | 22 | +0.300 | -1.04 | 1.94 | -0.099 (-1.55) | 3.4% | 1090 | +0.085 |
| momentum | fixed | SPY>200d & stock>200d & RS>=0.8 | 1938 | 22 | +0.372 | -1.02 | 2.12 | -0.134 (-1.64) | 6.2% | 453 | +0.238 |
| momentum | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1599 | 23 | +0.381 | -1.03 | 2.07 | -0.061 (-0.69) | 4.6% | 361 | +0.227 |
| momentum | fixed | score>=70 & SPY>200d & stock>200d | 156 | 24 | +0.556 | -0.91 | 2.07 | +0.329 (1.19) | 12.8% | 37 | +0.993 |
| momentum | fixed | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 97 | 25 | +0.721 | -0.88 | 1.89 | +0.269 (0.71) | 15.5% | 26 | +1.018 |
| combined | fixed | all | 8189 | 19 | +0.274 | -1.07 | 1.65 | -0.313 (-4.46) | 3.3% | 1813 | +0.112 |
| combined | fixed | SPY>200d & stock>200d | 6750 | 19 | +0.237 | -1.08 | 0.96 | -0.185 (-3.11) | 3.1% | 1521 | +0.096 |
| combined | fixed | SPY>200d & stock>200d & RS>=0.8 | 2818 | 20 | +0.396 | -1.04 | 1.93 | -0.162 (-2.05) | 5.5% | 663 | +0.490 |
| combined | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 2320 | 21 | +0.405 | -1.05 | 1.91 | -0.070 (-0.84) | 4.3% | 511 | +0.593 |
| combined | fixed | score>=70 & SPY>200d & stock>200d | 823 | 23 | +0.488 | -0.98 | 2.23 | +0.053 (0.39) | 6.6% | 161 | +0.363 |
| combined | fixed | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 500 | 23 | +0.578 | -0.96 | 2.26 | +0.021 (0.11) | 8.6% | 106 | +0.476 |
| baseline_random | fixed | all | 17829 | 25 | +0.358 | -1.02 | 4.96 | — (—) | 5.0% | 4038 | +0.246 |
| baseline_random | fixed | SPY>200d & stock>200d | 11269 | 23 | +0.335 | -1.04 | 3.09 | — (—) | 3.6% | 2563 | +0.171 |
| baseline_random | fixed | SPY>200d & stock>200d & RS>=0.8 | 4592 | 23 | +0.381 | -1.03 | 3.48 | — (—) | 6.2% | 1114 | +0.242 |
| baseline_random | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 3131 | 24 | +0.437 | -1.04 | 3.13 | — (—) | 4.0% | 684 | +0.326 |
| breakout | wide | all | 5229 | 34 | +0.302 | -0.95 | 3.23 | -0.169 (-3.01) | 5.5% | 1155 | +0.265 |
| breakout | wide | SPY>200d & stock>200d | 4202 | 33 | +0.312 | -0.96 | 2.32 | -0.070 (-1.43) | 5.1% | 937 | +0.286 |
| breakout | wide | SPY>200d & stock>200d & RS>=0.8 | 1786 | 34 | +0.428 | -0.93 | 2.63 | -0.112 (-1.77) | 9.1% | 419 | +0.389 |
| breakout | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1486 | 35 | +0.463 | -0.93 | 3.02 | -0.037 (-0.54) | 7.4% | 325 | +0.357 |
| breakout | wide | score>=70 & SPY>200d & stock>200d | 720 | 33 | +0.386 | -0.91 | 2.74 | +0.017 (0.15) | 9.0% | 133 | +0.173 |
| breakout | wide | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 432 | 33 | +0.468 | -0.90 | 2.76 | +0.016 (0.10) | 11.6% | 87 | +0.224 |
| momentum | wide | all | 4488 | 32 | +0.267 | -0.98 | 2.79 | -0.190 (-3.25) | 4.8% | 978 | +0.154 |
| momentum | wide | SPY>200d & stock>200d | 3981 | 33 | +0.310 | -0.98 | 2.92 | -0.029 (-0.54) | 4.6% | 890 | +0.186 |
| momentum | wide | SPY>200d & stock>200d & RS>=0.8 | 1637 | 33 | +0.352 | -0.96 | 2.44 | -0.125 (-2.07) | 7.9% | 383 | +0.251 |
| momentum | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1379 | 33 | +0.334 | -0.97 | 2.18 | -0.118 (-1.85) | 5.7% | 304 | +0.267 |
| momentum | wide | score>=70 & SPY>200d & stock>200d | 140 | 31 | +0.321 | -0.88 | 1.44 | +0.028 (0.15) | 15.0% | 34 | +0.722 |
| momentum | wide | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 83 | 33 | +0.458 | -0.81 | 1.52 | -0.002 (-0.01) | 19.3% | 24 | +0.839 |
| combined | wide | all | 6240 | 33 | +0.285 | -0.97 | 3.17 | -0.182 (-3.53) | 5.1% | 1370 | +0.227 |
| combined | wide | SPY>200d & stock>200d | 5211 | 33 | +0.307 | -0.98 | 2.48 | -0.068 (-1.55) | 4.8% | 1170 | +0.236 |
| combined | wide | SPY>200d & stock>200d & RS>=0.8 | 2262 | 33 | +0.377 | -0.95 | 2.55 | -0.117 (-2.08) | 8.2% | 535 | +0.345 |
| combined | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1893 | 34 | +0.390 | -0.95 | 2.72 | -0.067 (-1.13) | 6.6% | 415 | +0.334 |
| combined | wide | score>=70 & SPY>200d & stock>200d | 780 | 33 | +0.379 | -0.91 | 2.35 | -0.013 (-0.13) | 9.1% | 151 | +0.258 |
| combined | wide | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 464 | 33 | +0.454 | -0.89 | 2.35 | -0.047 (-0.34) | 12.1% | 99 | +0.326 |
| baseline_random | wide | all | 12435 | 36 | +0.326 | -0.94 | 5.40 | — (—) | 6.3% | 2696 | +0.292 |
| baseline_random | wide | SPY>200d & stock>200d | 8119 | 34 | +0.324 | -0.97 | 3.54 | — (—) | 4.7% | 1836 | +0.200 |
| baseline_random | wide | SPY>200d & stock>200d & RS>=0.8 | 3413 | 34 | +0.362 | -0.96 | 3.98 | — (—) | 8.3% | 808 | +0.280 |
| baseline_random | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 2492 | 35 | +0.425 | -0.97 | 4.00 | — (—) | 5.8% | 528 | +0.406 |

## Portfolio — universe: largecap_2015

SPY buy-and-hold: +14.9%/yr, max DD -34%, Sharpe 0.84 · train+val Sharpe 0.83 · OOS +15.2%/yr, Sharpe 0.92

| rule set | trades/yr | exposure | win% | avgR | CAGR | max DD | Sharpe | train+val Sharpe | OOS CAGR | OOS Sharpe | vs random |
|---|---|---|---|---|---|---|---|---|---|---|---|
| random picks (reference) | 41.4 | 88% | 25 | +0.24 | +4.2% | -35% | 0.34 | 0.28 | +10.1% | 0.66 | — |
| random picks, trend filter | 35.0 | 76% | 25 | +0.27 | +5.3% | -26% | 0.45 | 0.46 | +3.3% | 0.29 | — |
| RS leaders, trend filter | 42.2 | 76% | 23 | +0.24 | +7.0% | -36% | 0.45 | 0.56 | -0.1% | 0.10 | 60% |
| RS leaders near 52w high | 40.8 | 76% | 22 | +0.21 | +3.6% | -29% | 0.29 | 0.33 | +1.7% | 0.18 | 30% |
| signals score>=70, trend | 15.0 | 36% | 23 | +0.28 | +3.0% | -16% | 0.36 | 0.30 | +5.8% | 0.63 | 42% |
| signals score>=70, trend, RS top 20% | 10.8 | 25% | 22 | +0.34 | +2.4% | -19% | 0.33 | 0.37 | +2.5% | 0.37 | 10% |
| signals, trend, RS top 20% | 41.8 | 78% | 21 | +0.33 | +6.3% | -30% | 0.46 | 0.53 | +4.3% | 0.34 | 62% |
| signals, trend, RS top 20%, near 52w high | 43.0 | 78% | 21 | +0.32 | +7.1% | -33% | 0.52 | 0.61 | +4.2% | 0.33 | 75% |

Cost sensitivity (full-period CAGR / Sharpe):

| rule set | 20 bps | 40 bps | 70 bps |
|---|---|---|---|
| RS leaders, trend filter | +7.0% / 0.45 | +4.0% / 0.30 | -0.3% / 0.08 |
| RS leaders near 52w high | +3.6% / 0.29 | +0.6% / 0.12 | -4.1% / -0.14 |
| signals score>=70, trend | +3.0% / 0.36 | +1.6% / 0.22 | -0.4% / 0.00 |
| signals score>=70, trend, RS top 20% | +2.4% / 0.33 | +1.4% / 0.21 | -0.1% / 0.02 |
| signals, trend, RS top 20% | +6.3% / 0.46 | +3.0% / 0.26 | -1.9% / -0.04 |
| signals, trend, RS top 20%, near 52w high | +7.1% / 0.52 | +3.7% / 0.31 | -1.2% / 0.00 |

Exit variant (stop 2.5 x ATR instead of 1.5 x ATR / structural):

| rule set | CAGR | max DD | Sharpe | OOS Sharpe |
|---|---|---|---|---|
| random picks (reference) | +11.7% | -16% | 0.85 | 0.35 |
| random picks, trend filter | +10.5% | -17% | 0.87 | 0.60 |
| RS leaders, trend filter | +10.5% | -25% | 0.66 | 0.41 |
| RS leaders near 52w high | +12.1% | -22% | 0.76 | 0.35 |
| signals score>=70, trend | +1.8% | -16% | 0.25 | 0.64 |
| signals score>=70, trend, RS top 20% | +2.9% | -17% | 0.41 | 0.45 |
| signals, trend, RS top 20% | +7.3% | -21% | 0.54 | 0.39 |
| signals, trend, RS top 20%, near 52w high | +6.7% | -27% | 0.51 | 0.47 |

### Per trade — universe: largecap_2015 (one position per symbol, t over monthly means)

| group | exit | policy | n | win% | avgR | medR | t | excess vs random (t) | ≥+50% | OOS n | OOS avgR |
|---|---|---|---|---|---|---|---|---|---|---|---|
| breakout | fixed | all | 2274 | 17 | +0.090 | -1.16 | -0.39 | -0.443 (-3.68) | 0.2% | 452 | -0.172 |
| breakout | fixed | SPY>200d & stock>200d | 1865 | 16 | +0.018 | -1.17 | -0.48 | -0.266 (-2.58) | 0.1% | 376 | -0.151 |
| breakout | fixed | SPY>200d & stock>200d & RS>=0.8 | 760 | 19 | +0.292 | -1.12 | 1.27 | +0.029 (0.13) | 0.1% | 158 | +0.076 |
| breakout | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 712 | 18 | +0.320 | -1.12 | 1.36 | +0.074 (0.34) | 0.1% | 153 | +0.200 |
| breakout | fixed | score>=70 & SPY>200d & stock>200d | 159 | 22 | +0.201 | -1.02 | 1.04 | -0.065 (-0.23) | 0.0% | 26 | +0.589 |
| breakout | fixed | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 104 | 21 | +0.218 | -1.01 | 1.07 | -0.059 (-0.17) | 0.0% | 14 | +0.550 |
| momentum | fixed | all | 2184 | 22 | +0.182 | -1.09 | 1.19 | -0.275 (-2.90) | 0.1% | 448 | +0.046 |
| momentum | fixed | SPY>200d & stock>200d | 1950 | 23 | +0.220 | -1.10 | 1.01 | -0.095 (-1.07) | 0.1% | 413 | +0.112 |
| momentum | fixed | SPY>200d & stock>200d & RS>=0.8 | 837 | 23 | +0.235 | -1.07 | 0.26 | -0.245 (-2.25) | 0.0% | 177 | +0.163 |
| momentum | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 795 | 23 | +0.221 | -1.08 | 0.09 | -0.238 (-2.15) | 0.0% | 172 | +0.199 |
| momentum | fixed | score>=70 & SPY>200d & stock>200d | 16 | 19 | +0.084 | -0.97 | 0.37 | -0.013 (-0.02) | 0.0% | 4 | -0.923 |
| momentum | fixed | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 9 | 22 | +0.781 | -0.89 | 0.72 | -0.171 (-0.16) | 0.0% | 3 | -0.808 |
| combined | fixed | all | 3091 | 20 | +0.131 | -1.12 | 0.28 | -0.359 (-3.76) | 0.2% | 613 | -0.059 |
| combined | fixed | SPY>200d & stock>200d | 2641 | 20 | +0.102 | -1.12 | -0.01 | -0.193 (-2.35) | 0.1% | 529 | -0.013 |
| combined | fixed | SPY>200d & stock>200d & RS>=0.8 | 1133 | 21 | +0.223 | -1.08 | 0.27 | -0.202 (-1.86) | 0.0% | 229 | +0.027 |
| combined | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1074 | 20 | +0.216 | -1.09 | 0.33 | -0.167 (-1.58) | 0.0% | 223 | +0.117 |
| combined | fixed | score>=70 & SPY>200d & stock>200d | 171 | 22 | +0.231 | -1.02 | 1.15 | -0.064 (-0.24) | 0.0% | 30 | +0.387 |
| combined | fixed | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 111 | 22 | +0.303 | -0.98 | 1.32 | -0.024 (-0.07) | 0.0% | 17 | +0.310 |
| baseline_random | fixed | all | 7326 | 26 | +0.325 | -1.05 | 4.42 | — (—) | 0.7% | 1450 | +0.316 |
| baseline_random | fixed | SPY>200d & stock>200d | 4793 | 23 | +0.270 | -1.08 | 2.56 | — (—) | 0.3% | 966 | +0.210 |
| baseline_random | fixed | SPY>200d & stock>200d & RS>=0.8 | 1925 | 24 | +0.319 | -1.06 | 2.45 | — (—) | 0.4% | 421 | +0.194 |
| baseline_random | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1710 | 24 | +0.311 | -1.07 | 2.21 | — (—) | 0.2% | 362 | +0.237 |
| breakout | wide | all | 1939 | 34 | +0.191 | -0.99 | 1.59 | -0.244 (-3.28) | 0.3% | 376 | +0.177 |
| breakout | wide | SPY>200d & stock>200d | 1591 | 34 | +0.212 | -1.00 | 1.65 | -0.050 (-0.71) | 0.2% | 314 | +0.242 |
| breakout | wide | SPY>200d & stock>200d & RS>=0.8 | 674 | 33 | +0.268 | -0.97 | 1.28 | -0.146 (-1.72) | 0.0% | 136 | +0.138 |
| breakout | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 636 | 33 | +0.272 | -0.97 | 1.40 | -0.096 (-1.13) | 0.0% | 131 | +0.184 |
| breakout | wide | score>=70 & SPY>200d & stock>200d | 159 | 32 | +0.180 | -0.93 | 0.71 | -0.117 (-0.61) | 0.0% | 26 | +0.504 |
| breakout | wide | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 104 | 32 | +0.306 | -0.93 | 1.20 | -0.127 (-0.53) | 0.0% | 14 | +0.616 |
| momentum | wide | all | 1857 | 33 | +0.195 | -1.02 | 1.97 | -0.207 (-2.80) | 0.1% | 373 | +0.137 |
| momentum | wide | SPY>200d & stock>200d | 1657 | 33 | +0.242 | -1.02 | 2.14 | +0.002 (0.04) | 0.1% | 346 | +0.183 |
| momentum | wide | SPY>200d & stock>200d & RS>=0.8 | 723 | 34 | +0.265 | -0.99 | 1.36 | -0.141 (-1.87) | 0.0% | 155 | +0.059 |
| momentum | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 687 | 34 | +0.272 | -0.99 | 1.57 | -0.084 (-1.07) | 0.0% | 152 | +0.089 |
| momentum | wide | score>=70 & SPY>200d & stock>200d | 15 | 27 | -0.005 | -0.94 | 0.31 | +0.004 (0.01) | 0.0% | 4 | -0.850 |
| momentum | wide | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 8 | 38 | +0.697 | -0.53 | 0.89 | -0.131 (-0.21) | 0.0% | 3 | -0.751 |
| combined | wide | all | 2451 | 33 | +0.189 | -1.01 | 1.82 | -0.230 (-3.36) | 0.3% | 478 | +0.171 |
| combined | wide | SPY>200d & stock>200d | 2106 | 33 | +0.209 | -1.02 | 1.88 | -0.035 (-0.61) | 0.1% | 422 | +0.218 |
| combined | wide | SPY>200d & stock>200d & RS>=0.8 | 926 | 34 | +0.278 | -0.98 | 1.56 | -0.115 (-1.77) | 0.0% | 189 | +0.073 |
| combined | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 880 | 34 | +0.281 | -0.99 | 1.63 | -0.065 (-1.06) | 0.0% | 185 | +0.107 |
| combined | wide | score>=70 & SPY>200d & stock>200d | 170 | 32 | +0.185 | -0.93 | 0.87 | -0.105 (-0.57) | 0.0% | 30 | +0.324 |
| combined | wide | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 110 | 32 | +0.343 | -0.92 | 1.36 | -0.116 (-0.51) | 0.0% | 17 | +0.375 |
| baseline_random | wide | all | 5198 | 37 | +0.320 | -0.94 | 5.26 | — (—) | 0.8% | 972 | +0.368 |
| baseline_random | wide | SPY>200d & stock>200d | 3503 | 35 | +0.273 | -0.99 | 3.07 | — (—) | 0.2% | 712 | +0.268 |
| baseline_random | wide | SPY>200d & stock>200d & RS>=0.8 | 1483 | 36 | +0.323 | -0.98 | 3.07 | — (—) | 0.4% | 313 | +0.236 |
| baseline_random | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1332 | 36 | +0.320 | -0.99 | 2.87 | — (—) | 0.3% | 270 | +0.270 |

## Momentum rotation — universe: all (from 2018-02-08, 20 bps per side)

| benchmark | CAGR | max DD | Sharpe | train+val Sharpe | OOS CAGR | OOS Sharpe |
|---|---|---|---|---|---|---|
| SPY buy-and-hold | +14.9% | -34% | 0.83 | 0.82 | +15.2% | 0.92 |
| equal-weight universe (no costs) | +26.6% | -42% | 1.03 | 1.04 | +24.1% | 1.00 |

| rule set | trades/yr | exposure | win% | avg trade | avg days | CAGR | max DD | Sharpe | train+val Sharpe | OOS CAGR | OOS Sharpe | vs random | CAGR @40 / @70 bps | without best stock |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| top5, in RS>=0.8, out RS<0.5 | 10 | 93% | 38 | +18.1% | 108 | +17.7% | -79% | 0.57 | 0.48 | +46.4% | 0.88 | 20% | +16.9% / +15.7% | SE: +23.4%, Sharpe 0.65 |
| top5, in RS>=0.8, out RS<0.5, stop -20% | 15 | 92% | 33 | +21.1% | 76 | +34.9% | -62% | 0.80 | 0.88 | +18.4% | 0.59 | 80% | +31.7% / +29.8% | SE: +27.8%, Sharpe 0.71 |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d | 21 | 81% | 38 | +6.0% | 48 | +10.1% | -74% | 0.45 | 0.64 | -23.6% | -0.13 | 15% | +8.4% / +5.9% | MARA: +7.1%, Sharpe 0.38 |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | 25 | 80% | 35 | +4.3% | 39 | +10.8% | -71% | 0.45 | 0.58 | -10.3% | 0.12 | 10% | +8.8% / +5.9% | CELH: +16.6%, Sharpe 0.55 |
| top5, in RS>=0.8, out RS<0.7 | 12 | 93% | 45 | +12.5% | 93 | +16.9% | -76% | 0.56 | 0.54 | +20.1% | 0.62 | 10% | +15.9% / +14.4% | ENPH: +17.6%, Sharpe 0.57 |
| top5, in RS>=0.8, out RS<0.7, stop -20% | 17 | 92% | 36 | +11.2% | 65 | +21.5% | -77% | 0.62 | 0.54 | +47.5% | 0.90 | 55% | +20.0% / +17.8% | VKTX: +15.3%, Sharpe 0.53 |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d | 22 | 80% | 39 | +3.7% | 45 | +7.2% | -77% | 0.40 | 0.53 | -18.3% | 0.04 | 10% | +5.4% / +2.8% | TSLA: +12.9%, Sharpe 0.50 |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | 27 | 80% | 35 | +4.2% | 37 | +10.7% | -68% | 0.45 | 0.55 | -7.4% | 0.20 | 15% | +8.6% / +5.6% | CELH: +6.5%, Sharpe 0.38 |
| top8, in RS>=0.8, out RS<0.5 | 16 | 92% | 39 | +22.1% | 107 | +30.6% | -69% | 0.78 | 0.83 | +26.8% | 0.69 | 75% | +29.7% / +28.4% | SE: +28.2%, Sharpe 0.73 |
| top8, in RS>=0.8, out RS<0.5, stop -20% | 23 | 92% | 35 | +15.8% | 74 | +28.7% | -62% | 0.74 | 0.82 | +17.5% | 0.58 | 75% | +27.4% / +25.5% | SE: +24.0%, Sharpe 0.66 |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d | 30 | 80% | 39 | +9.3% | 53 | +27.8% | -58% | 0.74 | 0.81 | +18.9% | 0.59 | 75% | +26.1% / +23.6% | APP: +20.9%, Sharpe 0.63 |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | 36 | 80% | 35 | +7.4% | 42 | +26.7% | -67% | 0.73 | 0.79 | +20.2% | 0.61 | 85% | +24.8% / +22.0% | NIO: +27.9%, Sharpe 0.74 |
| top8, in RS>=0.8, out RS<0.7 | 19 | 92% | 48 | +19.8% | 95 | +36.1% | -58% | 0.83 | 0.91 | +22.9% | 0.64 | 95% | +38.8% / +33.3% | MARA: +27.2%, Sharpe 0.72 |
| top8, in RS>=0.8, out RS<0.7, stop -20% | 27 | 91% | 34 | +17.0% | 64 | +30.7% | -71% | 0.75 | 0.80 | +21.8% | 0.63 | 75% | +29.3% / +27.1% | MARA: +22.8%, Sharpe 0.65 |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d | 33 | 80% | 42 | +7.9% | 48 | +21.6% | -54% | 0.64 | 0.75 | +1.4% | 0.33 | 50% | +19.8% / +17.1% | MARA: +19.6%, Sharpe 0.61 |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | 40 | 80% | 34 | +10.0% | 39 | +29.2% | -63% | 0.73 | 0.85 | +3.8% | 0.36 | 90% | +26.9% / +23.6% | MARA: +25.6%, Sharpe 0.69 |
| top8, in RS>=0.8, out RS<0.5, 12-1 month momentum | 18 | 92% | 32 | +19.9% | 99 | +23.2% | -63% | 0.67 | 0.69 | +28.0% | 0.70 | 60% | +22.3% / +20.9% | SE: +18.7%, Sharpe 0.59 |
| top8, in RS>=0.8, out RS<0.5, monthly | 11 | 94% | 42 | +51.1% | 153 | +34.6% | -64% | 0.83 | 0.80 | +53.0% | 0.97 | 70% | +34.0% / +33.0% | ENPH: +34.2%, Sharpe 0.83 |
| top8, in RS>=0.8, out RS<0.5, volatility-adjusted | 14 | 93% | 46 | +25.5% | 125 | +33.4% | -45% | 0.90 | 0.97 | +40.1% | 0.87 | 100% | +32.5% / +31.2% | RKLB: +27.3%, Sharpe 0.79 |
| top8, in RS>=0.8, out RS<0.5, max 2/sector | 17 | 91% | 41 | +30.7% | 109 | +39.5% | -66% | 0.85 | 0.88 | +33.5% | 0.77 | 90% | +38.4% / +37.0% | GME: +36.5%, Sharpe 0.87 |
| top8, in RS>=0.8, out RS<0.5, max 3/sector | 16 | 94% | 43 | +26.8% | 110 | +35.6% | -58% | 0.84 | 0.91 | +30.6% | 0.73 | 80% | +34.7% / +33.4% | SE: +31.1%, Sharpe 0.77 |

## Momentum rotation — universe: largecap_2015 (from 2018-02-08, 20 bps per side)

| benchmark | CAGR | max DD | Sharpe | train+val Sharpe | OOS CAGR | OOS Sharpe |
|---|---|---|---|---|---|---|
| SPY buy-and-hold | +14.9% | -34% | 0.83 | 0.82 | +15.2% | 0.92 |
| equal-weight universe (no costs) | +15.1% | -37% | 0.85 | 0.78 | +18.7% | 1.33 |

| rule set | trades/yr | exposure | win% | avg trade | avg days | CAGR | max DD | Sharpe | train+val Sharpe | OOS CAGR | OOS Sharpe | vs random | CAGR @40 / @70 bps | without best stock |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| top5, in RS>=0.8, out RS<0.5 | 10 | 95% | 51 | +9.8% | 116 | +16.7% | -36% | 0.73 | 0.67 | +25.7% | 0.91 | 95% | +15.8% / +14.5% | DVN: +13.3%, Sharpe 0.63 |
| top5, in RS>=0.8, out RS<0.5, stop -20% | 10 | 94% | 53 | +9.6% | 112 | +16.9% | -36% | 0.74 | 0.69 | +25.5% | 0.90 | 95% | +16.0% / +14.7% | DVN: +13.8%, Sharpe 0.65 |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d | 20 | 81% | 48 | +3.5% | 50 | +11.8% | -26% | 0.61 | 0.69 | +7.8% | 0.41 | 95% | +10.1% / +7.5% | AVGO: +11.9%, Sharpe 0.64 |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | 20 | 81% | 49 | +3.5% | 50 | +11.9% | -26% | 0.61 | 0.69 | +7.8% | 0.42 | 90% | +10.1% / +7.5% | AVGO: +12.0%, Sharpe 0.64 |
| top5, in RS>=0.8, out RS<0.7 | 14 | 94% | 49 | +5.4% | 85 | +12.8% | -36% | 0.59 | 0.60 | +14.7% | 0.59 | 100% | +11.6% / +9.8% | INTC: +11.0%, Sharpe 0.56 |
| top5, in RS>=0.8, out RS<0.7, stop -20% | 14 | 95% | 49 | +5.9% | 82 | +14.8% | -33% | 0.65 | 0.69 | +14.2% | 0.58 | 100% | +13.6% / +11.8% | INTC: +13.3%, Sharpe 0.64 |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d | 23 | 81% | 47 | +2.8% | 44 | +10.5% | -29% | 0.56 | 0.68 | +3.6% | 0.27 | 95% | +8.6% / +5.7% | AVGO: +9.3%, Sharpe 0.52 |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | 23 | 81% | 47 | +2.7% | 44 | +10.4% | -29% | 0.56 | 0.68 | +3.4% | 0.26 | 95% | +8.5% / +5.6% | AVGO: +9.4%, Sharpe 0.52 |
| top8, in RS>=0.8, out RS<0.5 | 17 | 94% | 47 | +8.7% | 112 | +15.9% | -29% | 0.76 | 0.71 | +22.4% | 0.95 | 95% | +15.0% / +13.7% | DVN: +13.8%, Sharpe 0.70 |
| top8, in RS>=0.8, out RS<0.5, stop -20% | 17 | 93% | 47 | +7.4% | 106 | +14.7% | -29% | 0.72 | 0.67 | +20.7% | 0.91 | 95% | +13.8% / +12.5% | DVN: +12.4%, Sharpe 0.65 |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d | 31 | 80% | 45 | +2.9% | 52 | +9.4% | -28% | 0.57 | 0.60 | +8.5% | 0.50 | 75% | +7.8% / +5.4% | DVN: +8.8%, Sharpe 0.55 |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | 31 | 80% | 45 | +2.9% | 51 | +9.4% | -27% | 0.57 | 0.60 | +8.4% | 0.50 | 80% | +7.8% / +5.4% | DVN: +8.8%, Sharpe 0.55 |
| top8, in RS>=0.8, out RS<0.7 | 22 | 93% | 50 | +4.9% | 82 | +13.5% | -26% | 0.69 | 0.68 | +15.2% | 0.73 | 100% | +12.3% / +10.5% | INTC: +12.2%, Sharpe 0.65 |
| top8, in RS>=0.8, out RS<0.7, stop -20% | 23 | 93% | 48 | +4.9% | 80 | +13.2% | -30% | 0.67 | 0.67 | +14.5% | 0.70 | 95% | +11.9% / +10.1% | AVGO: +10.8%, Sharpe 0.58 |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d | 35 | 80% | 48 | +2.2% | 45 | +9.2% | -29% | 0.57 | 0.62 | +6.8% | 0.42 | 95% | +7.4% / +4.7% | AVGO: +8.6%, Sharpe 0.54 |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | 35 | 80% | 48 | +2.2% | 45 | +9.2% | -29% | 0.56 | 0.61 | +6.6% | 0.42 | 100% | +7.3% / +4.6% | AVGO: +8.6%, Sharpe 0.54 |
| top8, in RS>=0.8, out RS<0.5, 12-1 month momentum | 19 | 90% | 34 | +3.5% | 94 | +5.9% | -40% | 0.38 | 0.44 | +1.4% | 0.17 | 15% | +5.0% / +3.7% | GE: +4.3%, Sharpe 0.31 |
| top8, in RS>=0.8, out RS<0.5, monthly | 12 | 93% | 50 | +9.8% | 146 | +12.5% | -27% | 0.63 | 0.66 | +10.8% | 0.54 | 100% | +13.4% / +12.4% | DVN: +12.4%, Sharpe 0.61 |
| top8, in RS>=0.8, out RS<0.5, volatility-adjusted | 16 | 93% | 58 | +7.5% | 116 | +13.9% | -23% | 0.80 | 0.77 | +14.8% | 0.94 | 100% | +13.1% / +11.9% | GE: +11.0%, Sharpe 0.66 |
| top8, in RS>=0.8, out RS<0.5, max 2/sector | 18 | 93% | 44 | +6.7% | 106 | +12.1% | -30% | 0.62 | 0.57 | +19.0% | 0.82 | 85% | +11.1% / +9.8% | DVN: +10.7%, Sharpe 0.58 |
| top8, in RS>=0.8, out RS<0.5, max 3/sector | 17 | 94% | 45 | +7.5% | 107 | +14.1% | -28% | 0.70 | 0.65 | +20.8% | 0.89 | 100% | +13.2% / +11.9% | DVN: +12.8%, Sharpe 0.66 |

## Rotation: pre-registered selection (2015 large caps, train+validation only)

Gates: train+val Sharpe > SPY's, ranking beats >= 90% of random selections, CAGR without the single best stock >= SPY's, max drawdown at most 10 points worse than SPY's.

**Chosen: none — no rule set passed every gate**

| rule set | passes | train+val Sharpe | failed gates |
|---|---|---|---|
| top5, in RS>=0.8, out RS<0.5 | ❌ | 0.67 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top5, in RS>=0.8, out RS<0.5, stop -20% | ❌ | 0.69 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d | ❌ | 0.69 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | ❌ | 0.69 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top5, in RS>=0.8, out RS<0.7 | ❌ | 0.60 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top5, in RS>=0.8, out RS<0.7, stop -20% | ❌ | 0.69 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d | ❌ | 0.68 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | ❌ | 0.68 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5 | ❌ | 0.71 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5, stop -20% | ❌ | 0.67 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d | ❌ | 0.60 | train_val_sharpe_beats_spy, ranking_beats_random, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | ❌ | 0.60 | train_val_sharpe_beats_spy, ranking_beats_random, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.7 | ❌ | 0.68 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.7, stop -20% | ❌ | 0.67 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d | ❌ | 0.62 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | ❌ | 0.61 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5, 12-1 month momentum | ❌ | 0.44 | train_val_sharpe_beats_spy, ranking_beats_random, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5, monthly | ❌ | 0.66 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5, volatility-adjusted | ❌ | 0.77 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5, max 2/sector | ❌ | 0.57 | train_val_sharpe_beats_spy, ranking_beats_random, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5, max 3/sector | ❌ | 0.65 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |

Calendar-year returns (2015 large caps, 20 bps per side):

| | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|---|---|---|---|
| SPY | -1% | +31% | +18% | +29% | -18% | +26% | +25% | +18% | +12% |
| equal-weight group | -2% | +29% | +14% | +31% | -4% | +16% | +16% | +17% | +18% |
| top5, in RS>=0.8, out RS<0.5 | +6% | +14% | +12% | +22% | +0% | +11% | +37% | +15% | +34% |
| top5, in RS>=0.8, out RS<0.5, stop -20% | +6% | +14% | +12% | +22% | -0% | +14% | +36% | +14% | +34% |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d | +10% | +3% | +16% | +21% | -1% | +21% | +19% | +9% | +7% |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | +10% | +3% | +16% | +22% | -1% | +21% | +19% | +9% | +7% |
| top5, in RS>=0.8, out RS<0.7 | +5% | +8% | +7% | +21% | -4% | +19% | +30% | -2% | +32% |
| top5, in RS>=0.8, out RS<0.7, stop -20% | +5% | +7% | +9% | +22% | +10% | +21% | +30% | -2% | +32% |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d | +12% | -3% | +8% | +21% | -2% | +22% | +29% | -5% | +13% |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | +12% | -3% | +8% | +21% | -2% | +22% | +29% | -5% | +13% |
| top8, in RS>=0.8, out RS<0.5 | -2% | +8% | +17% | +28% | +0% | +23% | +27% | +22% | +19% |
| top8, in RS>=0.8, out RS<0.5, stop -20% | -2% | +8% | +11% | +33% | +1% | +20% | +22% | +23% | +16% |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d | +8% | -5% | +11% | +30% | -2% | +14% | +13% | +14% | +2% |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | +8% | -4% | +11% | +30% | -2% | +14% | +13% | +14% | +2% |
| top8, in RS>=0.8, out RS<0.7 | +0% | +9% | +17% | +18% | +2% | +20% | +25% | +6% | +24% |
| top8, in RS>=0.8, out RS<0.7, stop -20% | +0% | +6% | +13% | +18% | +6% | +21% | +25% | +5% | +23% |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d | +9% | +2% | +12% | +18% | -4% | +9% | +24% | +2% | +12% |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | +9% | +2% | +12% | +18% | -4% | +9% | +24% | +1% | +12% |
| top8, in RS>=0.8, out RS<0.5, 12-1 month momentum | -11% | +10% | +2% | +24% | -12% | +2% | +41% | -1% | +6% |
| top8, in RS>=0.8, out RS<0.5, monthly | -0% | +12% | +16% | +19% | -5% | +26% | +23% | +5% | +18% |
| top8, in RS>=0.8, out RS<0.5, volatility-adjusted | +10% | +16% | +3% | +22% | -8% | +18% | +38% | +20% | +9% |
| top8, in RS>=0.8, out RS<0.5, max 2/sector | -4% | +8% | +4% | +29% | -0% | +19% | +17% | +10% | +26% |
| top8, in RS>=0.8, out RS<0.5, max 3/sector | -4% | +8% | +10% | +29% | -1% | +24% | +22% | +18% | +22% |

## Rockets (from 2016-11-21, 20 bps per side, 10 slots x 10%, max 3 new per day)

Rocket day: close >= +jump vs previous close, volume >= 3x the 20-day average, close in the top quarter of the day's range, price >= $5, 20-day dollar volume >= $5M. Buy next open; sell next open after a close more than `trail` below the highest close, or after 40 sessions. 'Random' = same stocks, same liquidity filter, same exit, random dates.

SPY: +15.1%/yr, max DD -34%, Sharpe 0.87 · train+val +15.2%/yr, Sharpe 0.87

| variant | trades | win% | avg trade | median | ≥+50% | worst | random avg | excess vs random t (train+val) | 2015 large caps excess | CAGR | max DD | Sharpe | train+val CAGR / Sharpe | OOS CAGR | random-entry portfolio CAGR | without top 3 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| EPS surprise>0%, reaction>=5% | 1907 | 54 | +4.6% | +1.9% | 4.3% | -51% | +4.3% | -0.33% (-0.51) | -0.15% (n=562) | +7.7% | -40% | 0.46 | +10.4% / 0.58 | -2.8% | +16.9% | +7.7% |
| EPS surprise>0%, reaction>=10% | 925 | 53 | +6.1% | +1.6% | 6.3% | -51% | +4.3% | +0.78% (0.78) | +1.57% (n=130) | +23.8% | -43% | 0.99 | +25.4% / 1.06 | +14.1% | +16.9% | +22.8% |
| EPS surprise>10%, reaction>=5% | 1268 | 53 | +5.0% | +2.1% | 5.0% | -51% | +4.3% | +0.64% (0.79) | -0.53% (n=268) | +13.3% | -45% | 0.65 | +22.1% / 0.98 | -15.8% | +16.9% | +14.0% |
| EPS surprise>10%, reaction>=10% | 714 | 53 | +6.4% | +1.6% | 6.3% | -51% | +4.3% | +1.68% (1.39) | +1.95% (n=72) | +18.4% | -48% | 0.78 | +26.8% / 1.05 | -13.5% | +16.9% | +15.1% |
| EPS surprise>20%, reaction>=10%, volume>=2x, RS>=0.8 | 243 | 56 | +8.5% | +2.8% | 7.0% | -36% | +4.3% | +3.55% (1.65) | +3.91% (n=14) | +17.7% | -27% | 0.91 | +25.0% / 1.25 | -9.1% | +16.9% | +11.7% |
| EPS surprise>20%, reaction>=15%, volume>=2x, RS>=0.8 | 174 | 56 | +8.3% | +2.7% | 8.1% | -36% | +4.3% | +1.85% (0.78) | —% (n=4) | +14.3% | -24% | 0.86 | +19.8% / 1.20 | -6.6% | +16.9% | +9.1% |
| jump>=8%, trail 15% | 1001 | 46 | +4.0% | -2.6% | 5.3% | -52% | +2.2% | -0.06% (-0.06) | -1.46% (n=115) | +15.4% | -48% | 0.62 | +23.8% / 0.84 | -13.5% | +15.7% | +9.7% |
| jump>=8%, trail 25% | 1000 | 51 | +5.4% | +0.6% | 6.8% | -61% | +2.9% | +0.52% (0.45) | -1.38% (n=115) | +15.1% | -68% | 0.60 | +21.8% / 0.77 | -8.4% | +19.6% | +11.1% |
| jump>=15%, trail 15% | 543 | 43 | +4.7% | -4.5% | 6.8% | -52% | +2.2% | -0.47% (-0.33) | -4.26% (n=24) | +18.3% | -38% | 0.71 | +22.2% / 0.81 | +4.4% | +15.7% | +12.0% |
| jump>=15%, trail 25% | 543 | 47 | +6.6% | -1.9% | 9.2% | -61% | +2.9% | +0.94% (0.52) | -4.50% (n=24) | +14.7% | -60% | 0.57 | +21.8% / 0.75 | -7.0% | +19.6% | +6.4% |

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
| combined | all | +0.94 | -0.44 | +0.30 | +1.11 | +0.02 | -0.44 | +0.53 | +0.42 | +0.23 | -0.04 |
| combined | SPY>200d & stock>200d | +1.01 | -0.43 | +0.03 | +0.94 | -0.04 | -0.79 | +0.38 | +0.42 | +0.19 | -0.02 |
| combined | SPY>200d & stock>200d & RS>=0.8 | +1.09 | -0.26 | +0.35 | +1.46 | -0.42 | -0.36 | +0.35 | +0.60 | +0.83 | +0.08 |
| combined | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | +1.17 | -0.12 | +0.45 | +1.36 | -0.53 | -0.07 | +0.30 | +0.46 | +0.81 | +0.34 |
| combined | score>=70 & SPY>200d & stock>200d | +0.81 | +0.65 | +0.42 | +1.14 | -0.54 | -0.96 | +0.43 | +0.69 | +0.52 | +0.10 |
| combined | score>=70 & SPY>200d & stock>200d & RS>=0.8 | +0.17 | +1.33 | +0.61 | +1.08 | -0.53 | -1.15 | +0.41 | +1.00 | +0.70 | +0.08 |
| baseline_random | all | +1.59 | +0.06 | +0.55 | +0.98 | +0.15 | -0.28 | +0.61 | +0.42 | +0.30 | +0.19 |
| baseline_random | SPY>200d & stock>200d | +1.76 | -0.25 | +0.52 | +0.86 | +0.16 | -0.78 | +0.27 | +0.42 | +0.21 | +0.14 |
| baseline_random | SPY>200d & stock>200d & RS>=0.8 | +1.58 | +0.11 | +0.65 | +1.17 | -0.25 | -0.74 | +0.47 | +0.51 | +0.41 | +0.06 |
| baseline_random | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | +1.43 | +0.27 | +0.73 | +0.94 | -0.29 | -0.63 | +0.55 | +0.60 | +0.65 | +0.00 |