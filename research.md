# Strategy research

278 symbols with data (1 failed), 10 years of daily bars. Control group: 105 stocks that were already large caps in 2015. Primary cost 20 bps per side (USD account: courtage + slippage; 40 bps ≈ trading from a SEK account). Validation from 2023-02-18, out-of-sample (OOS) from 2024-12-20. Setups invalidated at the next open (skipped): 1305.

Portfolio: max 8 positions, max 3 new per day, 1% risk per trade, max 25% of equity per position, no leverage, marked to market daily. 'vs random' = share of 40 random-order portfolios from the same eligible trades that this ranking beat.

## Portfolio — universe: all

SPY buy-and-hold: +15.0%/yr, max DD -34%, Sharpe 0.85 · train+val Sharpe 0.81 · OOS +15.9%/yr, Sharpe 0.97

| rule set | trades/yr | exposure | win% | avgR | CAGR | max DD | Sharpe | train+val Sharpe | OOS CAGR | OOS Sharpe | vs random |
|---|---|---|---|---|---|---|---|---|---|---|---|
| random picks (reference) | 77.2 | 86% | 22 | +0.26 | +9.4% | -62% | 0.45 | 0.50 | -8.0% | -0.12 | — |
| random picks, trend filter | 67.8 | 77% | 22 | +0.32 | +11.2% | -51% | 0.54 | 0.81 | -2.1% | 0.06 | — |
| RS leaders, trend filter | 74.3 | 66% | 22 | +0.36 | +19.2% | -42% | 0.71 | 0.81 | -1.1% | 0.14 | 93% |
| RS leaders near 52w high | 66.1 | 76% | 26 | +0.69 | +33.9% | -34% | 1.10 | 1.16 | +24.2% | 0.74 | 100% |
| signals score>=70, trend | 46.7 | 63% | 22 | +0.32 | +11.9% | -35% | 0.64 | 0.70 | +0.7% | 0.15 | 33% |
| signals score>=70, trend, RS top 20% | 41.5 | 50% | 22 | +0.50 | +19.1% | -33% | 0.90 | 0.95 | +9.0% | 0.49 | 75% |
| signals, trend, RS top 20% | 78.6 | 78% | 22 | +0.70 | +38.8% | -48% | 1.12 | 1.26 | +18.3% | 0.62 | 100% |
| signals, trend, RS top 20%, near 52w high | 75.2 | 78% | 22 | +0.53 | +28.9% | -32% | 1.01 | 1.13 | +18.7% | 0.65 | 100% |

Cost sensitivity (full-period CAGR / Sharpe):

| rule set | 20 bps | 40 bps | 70 bps |
|---|---|---|---|
| RS leaders, trend filter | +19.2% / 0.71 | +15.6% / 0.61 | +10.4% / 0.47 |
| RS leaders near 52w high | +33.9% / 1.10 | +29.4% / 0.99 | +22.9% / 0.82 |
| signals score>=70, trend | +11.9% / 0.64 | +9.0% / 0.51 | +5.0% / 0.34 |
| signals score>=70, trend, RS top 20% | +19.1% / 0.90 | +16.5% / 0.80 | +12.8% / 0.65 |
| signals, trend, RS top 20% | +38.8% / 1.12 | +32.6% / 0.99 | +25.6% / 0.83 |
| signals, trend, RS top 20%, near 52w high | +28.9% / 1.01 | +23.7% / 0.87 | +16.9% / 0.67 |

Exit variant (stop 2.5 x ATR instead of 1.5 x ATR / structural):

| rule set | CAGR | max DD | Sharpe | OOS Sharpe |
|---|---|---|---|---|
| random picks (reference) | +1.9% | -39% | 0.20 | -0.70 |
| random picks, trend filter | +17.1% | -33% | 0.96 | 0.35 |
| RS leaders, trend filter | +18.3% | -28% | 0.88 | 0.68 |
| RS leaders near 52w high | +25.6% | -24% | 1.13 | 0.42 |
| signals score>=70, trend | +12.3% | -28% | 0.77 | -0.05 |
| signals score>=70, trend, RS top 20% | +17.4% | -28% | 1.02 | 0.40 |
| signals, trend, RS top 20% | +18.4% | -36% | 0.87 | 0.44 |
| signals, trend, RS top 20%, near 52w high | +16.6% | -26% | 0.81 | 0.44 |

### Per trade — universe: all (one position per symbol, t over monthly means)

| group | exit | policy | n | win% | avgR | medR | t | excess vs random (t) | ≥+50% | OOS n | OOS avgR |
|---|---|---|---|---|---|---|---|---|---|---|---|
| breakout | fixed | all | 6493 | 17 | +0.287 | -1.11 | 1.31 | -0.312 (-3.72) | 3.2% | 1438 | +0.004 |
| breakout | fixed | SPY>200d & stock>200d | 5151 | 16 | +0.238 | -1.12 | 0.64 | -0.204 (-2.89) | 3.0% | 1161 | +0.009 |
| breakout | fixed | SPY>200d & stock>200d & RS>=0.8 | 2130 | 18 | +0.430 | -1.08 | 1.72 | -0.165 (-1.55) | 5.5% | 500 | +0.489 |
| breakout | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1739 | 18 | +0.470 | -1.08 | 1.66 | -0.066 (-0.54) | 4.4% | 382 | +0.675 |
| breakout | fixed | score>=70 & SPY>200d & stock>200d | 747 | 22 | +0.467 | -1.00 | 2.42 | +0.079 (0.52) | 6.0% | 139 | +0.327 |
| breakout | fixed | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 454 | 23 | +0.575 | -0.98 | 2.62 | +0.083 (0.41) | 7.9% | 91 | +0.489 |
| momentum | fixed | all | 5382 | 22 | +0.274 | -1.04 | 1.98 | -0.279 (-3.62) | 3.6% | 1201 | +0.057 |
| momentum | fixed | SPY>200d & stock>200d | 4755 | 22 | +0.313 | -1.04 | 2.04 | -0.073 (-1.12) | 3.5% | 1089 | +0.088 |
| momentum | fixed | SPY>200d & stock>200d & RS>=0.8 | 1935 | 23 | +0.390 | -1.02 | 2.24 | -0.113 (-1.42) | 6.2% | 454 | +0.259 |
| momentum | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1597 | 23 | +0.396 | -1.03 | 2.16 | -0.048 (-0.56) | 4.6% | 362 | +0.226 |
| momentum | fixed | score>=70 & SPY>200d & stock>200d | 156 | 24 | +0.555 | -0.91 | 2.07 | +0.325 (1.18) | 12.8% | 38 | +0.932 |
| momentum | fixed | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 97 | 25 | +0.719 | -0.88 | 1.88 | +0.260 (0.69) | 15.5% | 27 | +0.932 |
| combined | fixed | all | 8175 | 19 | +0.277 | -1.07 | 1.66 | -0.300 (-4.30) | 3.3% | 1803 | +0.113 |
| combined | fixed | SPY>200d & stock>200d | 6739 | 19 | +0.245 | -1.08 | 1.01 | -0.167 (-2.82) | 3.1% | 1514 | +0.098 |
| combined | fixed | SPY>200d & stock>200d & RS>=0.8 | 2812 | 20 | +0.414 | -1.04 | 2.04 | -0.144 (-1.80) | 5.5% | 661 | +0.513 |
| combined | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 2316 | 21 | +0.420 | -1.05 | 2.00 | -0.058 (-0.68) | 4.3% | 510 | +0.597 |
| combined | fixed | score>=70 & SPY>200d & stock>200d | 823 | 23 | +0.490 | -0.98 | 2.23 | +0.069 (0.50) | 6.7% | 162 | +0.366 |
| combined | fixed | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 500 | 23 | +0.585 | -0.95 | 2.31 | +0.028 (0.15) | 8.8% | 107 | +0.493 |
| baseline_random | fixed | all | 17873 | 25 | +0.349 | -1.02 | 4.92 | — (—) | 4.9% | 4108 | +0.221 |
| baseline_random | fixed | SPY>200d & stock>200d | 11324 | 23 | +0.325 | -1.04 | 3.05 | — (—) | 3.5% | 2585 | +0.168 |
| baseline_random | fixed | SPY>200d & stock>200d & RS>=0.8 | 4593 | 23 | +0.381 | -1.03 | 3.49 | — (—) | 6.2% | 1117 | +0.243 |
| baseline_random | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 3134 | 24 | +0.441 | -1.04 | 3.20 | — (—) | 4.0% | 689 | +0.333 |
| breakout | wide | all | 5222 | 34 | +0.305 | -0.95 | 3.25 | -0.161 (-2.88) | 5.5% | 1146 | +0.264 |
| breakout | wide | SPY>200d & stock>200d | 4199 | 33 | +0.317 | -0.96 | 2.37 | -0.065 (-1.32) | 5.1% | 934 | +0.284 |
| breakout | wide | SPY>200d & stock>200d & RS>=0.8 | 1784 | 34 | +0.441 | -0.93 | 2.79 | -0.097 (-1.55) | 9.1% | 418 | +0.415 |
| breakout | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1485 | 35 | +0.472 | -0.92 | 3.16 | -0.028 (-0.41) | 7.4% | 325 | +0.366 |
| breakout | wide | score>=70 & SPY>200d & stock>200d | 720 | 33 | +0.387 | -0.91 | 2.73 | +0.018 (0.16) | 9.2% | 133 | +0.179 |
| breakout | wide | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 432 | 33 | +0.473 | -0.90 | 2.84 | +0.027 (0.18) | 11.8% | 87 | +0.252 |
| momentum | wide | all | 4481 | 32 | +0.272 | -0.98 | 2.82 | -0.183 (-3.15) | 4.8% | 975 | +0.156 |
| momentum | wide | SPY>200d & stock>200d | 3976 | 33 | +0.316 | -0.98 | 2.96 | -0.025 (-0.47) | 4.7% | 889 | +0.188 |
| momentum | wide | SPY>200d & stock>200d & RS>=0.8 | 1636 | 33 | +0.362 | -0.96 | 2.48 | -0.123 (-2.04) | 7.9% | 383 | +0.272 |
| momentum | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1378 | 33 | +0.341 | -0.97 | 2.20 | -0.120 (-1.86) | 5.7% | 304 | +0.273 |
| momentum | wide | score>=70 & SPY>200d & stock>200d | 140 | 31 | +0.324 | -0.88 | 1.47 | +0.031 (0.17) | 15.0% | 34 | +0.736 |
| momentum | wide | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 83 | 33 | +0.463 | -0.81 | 1.56 | +0.004 (0.02) | 19.3% | 24 | +0.858 |
| combined | wide | all | 6227 | 33 | +0.287 | -0.97 | 3.18 | -0.177 (-3.41) | 5.1% | 1360 | +0.228 |
| combined | wide | SPY>200d & stock>200d | 5201 | 33 | +0.309 | -0.98 | 2.51 | -0.065 (-1.48) | 4.8% | 1165 | +0.234 |
| combined | wide | SPY>200d & stock>200d & RS>=0.8 | 2258 | 33 | +0.384 | -0.95 | 2.63 | -0.110 (-1.98) | 8.3% | 533 | +0.366 |
| combined | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1890 | 34 | +0.394 | -0.94 | 2.80 | -0.063 (-1.08) | 6.6% | 414 | +0.343 |
| combined | wide | score>=70 & SPY>200d & stock>200d | 780 | 33 | +0.380 | -0.91 | 2.36 | -0.011 (-0.11) | 9.2% | 151 | +0.265 |
| combined | wide | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 464 | 33 | +0.460 | -0.89 | 2.41 | -0.038 (-0.27) | 12.3% | 99 | +0.351 |
| baseline_random | wide | all | 12438 | 35 | +0.320 | -0.94 | 5.40 | — (—) | 6.3% | 2761 | +0.270 |
| baseline_random | wide | SPY>200d & stock>200d | 8118 | 34 | +0.322 | -0.97 | 3.58 | — (—) | 4.7% | 1837 | +0.197 |
| baseline_random | wide | SPY>200d & stock>200d & RS>=0.8 | 3405 | 34 | +0.367 | -0.97 | 4.01 | — (—) | 8.3% | 804 | +0.283 |
| baseline_random | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 2490 | 35 | +0.429 | -0.97 | 4.05 | — (—) | 5.8% | 528 | +0.405 |

## Portfolio — universe: largecap_2015

SPY buy-and-hold: +15.0%/yr, max DD -34%, Sharpe 0.85 · train+val Sharpe 0.81 · OOS +15.9%/yr, Sharpe 0.97

| rule set | trades/yr | exposure | win% | avgR | CAGR | max DD | Sharpe | train+val Sharpe | OOS CAGR | OOS Sharpe | vs random |
|---|---|---|---|---|---|---|---|---|---|---|---|
| random picks (reference) | 45.3 | 88% | 25 | +0.28 | +7.7% | -34% | 0.57 | 0.51 | -7.6% | -0.41 | — |
| random picks, trend filter | 35.1 | 75% | 23 | +0.28 | +5.7% | -25% | 0.52 | 0.72 | -6.0% | -0.39 | — |
| RS leaders, trend filter | 42.1 | 76% | 23 | +0.25 | +7.1% | -36% | 0.46 | 0.57 | -0.1% | 0.10 | 75% |
| RS leaders near 52w high | 40.7 | 76% | 22 | +0.21 | +3.7% | -29% | 0.30 | 0.33 | +1.9% | 0.19 | 30% |
| signals score>=70, trend | 15.0 | 36% | 23 | +0.27 | +2.8% | -16% | 0.34 | 0.27 | +4.9% | 0.55 | 40% |
| signals score>=70, trend, RS top 20% | 10.8 | 25% | 22 | +0.34 | +2.4% | -19% | 0.33 | 0.33 | +2.4% | 0.36 | 15% |
| signals, trend, RS top 20% | 41.9 | 78% | 21 | +0.29 | +6.1% | -30% | 0.46 | 0.52 | +2.9% | 0.26 | 70% |
| signals, trend, RS top 20%, near 52w high | 42.6 | 78% | 20 | +0.27 | +6.7% | -33% | 0.50 | 0.58 | +2.4% | 0.23 | 82% |

Cost sensitivity (full-period CAGR / Sharpe):

| rule set | 20 bps | 40 bps | 70 bps |
|---|---|---|---|
| RS leaders, trend filter | +7.1% / 0.46 | +4.2% / 0.32 | -0.2% / 0.10 |
| RS leaders near 52w high | +3.7% / 0.30 | +0.7% / 0.13 | -4.0% / -0.13 |
| signals score>=70, trend | +2.8% / 0.34 | +1.4% / 0.20 | -0.6% / -0.01 |
| signals score>=70, trend, RS top 20% | +2.4% / 0.33 | +1.3% / 0.20 | -0.1% / 0.02 |
| signals, trend, RS top 20% | +6.1% / 0.46 | +2.8% / 0.25 | -2.0% / -0.04 |
| signals, trend, RS top 20%, near 52w high | +6.7% / 0.50 | +3.4% / 0.29 | -1.6% / -0.02 |

Exit variant (stop 2.5 x ATR instead of 1.5 x ATR / structural):

| rule set | CAGR | max DD | Sharpe | OOS Sharpe |
|---|---|---|---|---|
| random picks (reference) | +7.0% | -23% | 0.53 | 1.57 |
| random picks, trend filter | +2.8% | -33% | 0.30 | 0.86 |
| RS leaders, trend filter | +10.6% | -25% | 0.68 | 0.47 |
| RS leaders near 52w high | +12.5% | -22% | 0.78 | 0.36 |
| signals score>=70, trend | +1.6% | -16% | 0.23 | 0.54 |
| signals score>=70, trend, RS top 20% | +2.9% | -17% | 0.41 | 0.44 |
| signals, trend, RS top 20% | +7.1% | -21% | 0.53 | 0.21 |
| signals, trend, RS top 20%, near 52w high | +6.1% | -27% | 0.48 | 0.35 |

### Per trade — universe: largecap_2015 (one position per symbol, t over monthly means)

| group | exit | policy | n | win% | avgR | medR | t | excess vs random (t) | ≥+50% | OOS n | OOS avgR |
|---|---|---|---|---|---|---|---|---|---|---|---|
| breakout | fixed | all | 2271 | 17 | +0.086 | -1.16 | -0.44 | -0.434 (-3.61) | 0.2% | 448 | -0.195 |
| breakout | fixed | SPY>200d & stock>200d | 1863 | 16 | +0.012 | -1.17 | -0.54 | -0.255 (-2.49) | 0.1% | 373 | -0.185 |
| breakout | fixed | SPY>200d & stock>200d & RS>=0.8 | 761 | 18 | +0.285 | -1.12 | 1.24 | +0.029 (0.13) | 0.1% | 158 | +0.045 |
| breakout | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 713 | 18 | +0.313 | -1.12 | 1.33 | +0.078 (0.36) | 0.1% | 153 | +0.169 |
| breakout | fixed | score>=70 & SPY>200d & stock>200d | 159 | 22 | +0.192 | -1.02 | 0.97 | -0.061 (-0.22) | 0.0% | 26 | +0.533 |
| breakout | fixed | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 104 | 21 | +0.218 | -1.01 | 1.07 | -0.047 (-0.13) | 0.0% | 14 | +0.550 |
| momentum | fixed | all | 2177 | 22 | +0.193 | -1.09 | 1.27 | -0.250 (-2.55) | 0.1% | 444 | +0.017 |
| momentum | fixed | SPY>200d & stock>200d | 1943 | 23 | +0.231 | -1.10 | 1.10 | -0.065 (-0.71) | 0.1% | 409 | +0.078 |
| momentum | fixed | SPY>200d & stock>200d & RS>=0.8 | 835 | 23 | +0.245 | -1.07 | 0.38 | -0.221 (-2.00) | 0.0% | 176 | +0.111 |
| momentum | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 793 | 23 | +0.231 | -1.08 | 0.21 | -0.210 (-1.87) | 0.0% | 171 | +0.149 |
| momentum | fixed | score>=70 & SPY>200d & stock>200d | 16 | 19 | +0.073 | -0.97 | 0.36 | -0.022 (-0.03) | 0.0% | 4 | -0.965 |
| momentum | fixed | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 9 | 22 | +0.762 | -0.89 | 0.70 | -0.192 (-0.18) | 0.0% | 3 | -0.864 |
| combined | fixed | all | 3084 | 20 | +0.133 | -1.12 | 0.27 | -0.345 (-3.58) | 0.2% | 607 | -0.084 |
| combined | fixed | SPY>200d & stock>200d | 2634 | 20 | +0.103 | -1.12 | -0.02 | -0.175 (-2.12) | 0.1% | 523 | -0.046 |
| combined | fixed | SPY>200d & stock>200d & RS>=0.8 | 1131 | 21 | +0.221 | -1.08 | 0.26 | -0.194 (-1.77) | 0.0% | 227 | -0.016 |
| combined | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1072 | 20 | +0.216 | -1.09 | 0.32 | -0.155 (-1.47) | 0.0% | 221 | +0.076 |
| combined | fixed | score>=70 & SPY>200d & stock>200d | 171 | 22 | +0.221 | -1.02 | 1.11 | -0.051 (-0.19) | 0.0% | 30 | +0.334 |
| combined | fixed | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 111 | 22 | +0.301 | -0.98 | 1.31 | -0.015 (-0.05) | 0.0% | 17 | +0.300 |
| baseline_random | fixed | all | 7372 | 25 | +0.306 | -1.05 | 4.32 | — (—) | 0.7% | 1491 | +0.263 |
| baseline_random | fixed | SPY>200d & stock>200d | 4822 | 23 | +0.249 | -1.08 | 2.43 | — (—) | 0.3% | 969 | +0.182 |
| baseline_random | fixed | SPY>200d & stock>200d & RS>=0.8 | 1928 | 24 | +0.308 | -1.06 | 2.39 | — (—) | 0.4% | 428 | +0.156 |
| baseline_random | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1713 | 24 | +0.298 | -1.07 | 2.12 | — (—) | 0.2% | 367 | +0.191 |
| breakout | wide | all | 1936 | 34 | +0.189 | -0.99 | 1.56 | -0.241 (-3.22) | 0.3% | 373 | +0.150 |
| breakout | wide | SPY>200d & stock>200d | 1589 | 34 | +0.208 | -1.00 | 1.63 | -0.043 (-0.62) | 0.2% | 312 | +0.207 |
| breakout | wide | SPY>200d & stock>200d & RS>=0.8 | 674 | 34 | +0.268 | -0.97 | 1.27 | -0.140 (-1.63) | 0.0% | 136 | +0.106 |
| breakout | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 636 | 33 | +0.271 | -0.96 | 1.36 | -0.091 (-1.06) | 0.0% | 131 | +0.142 |
| breakout | wide | score>=70 & SPY>200d & stock>200d | 159 | 32 | +0.172 | -0.93 | 0.62 | -0.129 (-0.69) | 0.0% | 26 | +0.449 |
| breakout | wide | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 104 | 32 | +0.306 | -0.93 | 1.20 | -0.119 (-0.49) | 0.0% | 14 | +0.616 |
| momentum | wide | all | 1855 | 32 | +0.194 | -1.02 | 1.93 | -0.204 (-2.70) | 0.1% | 371 | +0.104 |
| momentum | wide | SPY>200d & stock>200d | 1655 | 33 | +0.240 | -1.02 | 2.10 | +0.008 (0.11) | 0.1% | 344 | +0.144 |
| momentum | wide | SPY>200d & stock>200d & RS>=0.8 | 721 | 34 | +0.263 | -0.99 | 1.32 | -0.138 (-1.82) | 0.0% | 154 | +0.007 |
| momentum | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 685 | 34 | +0.270 | -0.99 | 1.53 | -0.079 (-0.99) | 0.0% | 151 | +0.039 |
| momentum | wide | score>=70 & SPY>200d & stock>200d | 15 | 27 | -0.012 | -0.94 | 0.29 | -0.019 (-0.04) | 0.0% | 4 | -0.876 |
| momentum | wide | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 8 | 38 | +0.684 | -0.58 | 0.88 | -0.146 (-0.23) | 0.0% | 3 | -0.784 |
| combined | wide | all | 2447 | 33 | +0.184 | -1.01 | 1.76 | -0.229 (-3.30) | 0.3% | 475 | +0.140 |
| combined | wide | SPY>200d & stock>200d | 2102 | 33 | +0.203 | -1.02 | 1.81 | -0.033 (-0.56) | 0.1% | 419 | +0.183 |
| combined | wide | SPY>200d & stock>200d & RS>=0.8 | 922 | 34 | +0.273 | -0.99 | 1.53 | -0.111 (-1.71) | 0.0% | 187 | +0.033 |
| combined | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 876 | 34 | +0.276 | -0.99 | 1.58 | -0.060 (-0.98) | 0.0% | 183 | +0.065 |
| combined | wide | score>=70 & SPY>200d & stock>200d | 170 | 32 | +0.175 | -0.93 | 0.80 | -0.112 (-0.62) | 0.0% | 30 | +0.273 |
| combined | wide | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 110 | 32 | +0.342 | -0.92 | 1.35 | -0.111 (-0.48) | 0.0% | 17 | +0.369 |
| baseline_random | wide | all | 5207 | 37 | +0.308 | -0.94 | 5.22 | — (—) | 0.8% | 1003 | +0.335 |
| baseline_random | wide | SPY>200d & stock>200d | 3503 | 35 | +0.260 | -0.99 | 3.01 | — (—) | 0.2% | 710 | +0.242 |
| baseline_random | wide | SPY>200d & stock>200d & RS>=0.8 | 1479 | 36 | +0.314 | -0.98 | 3.02 | — (—) | 0.4% | 313 | +0.194 |
| baseline_random | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1328 | 35 | +0.312 | -0.99 | 2.80 | — (—) | 0.3% | 270 | +0.220 |

## Momentum rotation — universe: all (from 2018-02-01, 20 bps per side)

| benchmark | CAGR | max DD | Sharpe | train+val Sharpe | OOS CAGR | OOS Sharpe |
|---|---|---|---|---|---|---|
| SPY buy-and-hold | +13.8% | -34% | 0.78 | 0.73 | +15.9% | 0.97 |
| equal-weight universe (no costs) | +25.4% | -42% | 0.99 | 0.98 | +24.5% | 1.01 |

| rule set | trades/yr | exposure | win% | avg trade | avg days | CAGR | max DD | Sharpe | train+val Sharpe | OOS CAGR | OOS Sharpe | vs random | CAGR @40 / @70 bps | without best stock |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| top5, in RS>=0.8, out RS<0.5 | 10 | 93% | 38 | +18.6% | 109 | +18.5% | -80% | 0.58 | 0.48 | +44.4% | 0.86 | 25% | +17.7% / +16.5% | SE: +25.5%, Sharpe 0.67 |
| top5, in RS>=0.8, out RS<0.5, stop -20% | 15 | 92% | 32 | +20.7% | 74 | +31.1% | -66% | 0.75 | 0.79 | +19.5% | 0.60 | 90% | +29.8% / +27.9% | SE: +25.7%, Sharpe 0.69 |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d | 21 | 81% | 38 | +6.3% | 48 | +11.9% | -74% | 0.48 | 0.67 | -24.0% | -0.14 | 15% | +10.2% / +7.7% | MARA: +8.9%, Sharpe 0.42 |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | 25 | 80% | 34 | +4.6% | 39 | +10.4% | -71% | 0.45 | 0.55 | -9.2% | 0.14 | 5% | +8.4% / +5.5% | CELH: +16.2%, Sharpe 0.54 |
| top5, in RS>=0.8, out RS<0.7 | 12 | 93% | 45 | +12.9% | 93 | +17.9% | -76% | 0.57 | 0.51 | +32.0% | 0.75 | 25% | +16.8% / +15.3% | ENPH: +18.5%, Sharpe 0.58 |
| top5, in RS>=0.8, out RS<0.7, stop -20% | 18 | 92% | 36 | +11.2% | 64 | +22.3% | -77% | 0.63 | 0.49 | +61.3% | 1.02 | 55% | +20.8% / +18.6% | VKTX: +17.2%, Sharpe 0.56 |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d | 22 | 80% | 39 | +4.0% | 45 | +8.8% | -77% | 0.43 | 0.49 | -7.8% | 0.23 | 20% | +7.0% / +4.3% | TSLA: +14.5%, Sharpe 0.52 |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | 27 | 80% | 35 | +4.4% | 37 | +10.2% | -68% | 0.45 | 0.47 | +2.2% | 0.35 | 20% | +8.1% / +5.1% | CELH: +6.0%, Sharpe 0.37 |
| top8, in RS>=0.8, out RS<0.5 | 16 | 92% | 42 | +23.0% | 108 | +33.7% | -70% | 0.82 | 0.86 | +27.5% | 0.70 | 80% | +32.7% / +31.3% | SE: +31.2%, Sharpe 0.78 |
| top8, in RS>=0.8, out RS<0.5, stop -20% | 23 | 92% | 36 | +16.1% | 74 | +28.9% | -62% | 0.74 | 0.80 | +17.8% | 0.58 | 80% | +27.6% / +25.7% | SE: +23.6%, Sharpe 0.66 |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d | 30 | 80% | 39 | +9.7% | 53 | +29.6% | -58% | 0.77 | 0.82 | +19.0% | 0.59 | 95% | +27.9% / +25.3% | APP: +22.6%, Sharpe 0.66 |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | 37 | 80% | 35 | +7.6% | 43 | +26.2% | -67% | 0.72 | 0.75 | +20.8% | 0.62 | 70% | +24.3% / +21.5% | NIO: +27.5%, Sharpe 0.74 |
| top8, in RS>=0.8, out RS<0.7 | 19 | 92% | 48 | +19.6% | 95 | +35.6% | -57% | 0.82 | 0.84 | +33.9% | 0.77 | 85% | +34.5% / +32.8% | MARA: +26.0%, Sharpe 0.70 |
| top8, in RS>=0.8, out RS<0.7, stop -20% | 27 | 92% | 34 | +16.6% | 64 | +28.9% | -71% | 0.72 | 0.70 | +32.9% | 0.76 | 75% | +27.4% / +25.2% | MARA: +21.5%, Sharpe 0.63 |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d | 33 | 80% | 41 | +8.1% | 49 | +22.6% | -54% | 0.65 | 0.71 | +9.4% | 0.45 | 50% | +20.7% / +18.0% | MARA: +20.5%, Sharpe 0.63 |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | 40 | 80% | 34 | +10.1% | 39 | +28.4% | -63% | 0.72 | 0.78 | +11.3% | 0.48 | 90% | +26.1% / +22.8% | MARA: +25.8%, Sharpe 0.69 |
| top8, in RS>=0.8, out RS<0.5, 12-1 month momentum | 18 | 91% | 32 | +20.1% | 99 | +23.8% | -63% | 0.68 | 0.68 | +28.7% | 0.71 | 65% | +22.8% / +21.3% | SE: +19.7%, Sharpe 0.61 |
| top8, in RS>=0.8, out RS<0.5, monthly | 11 | 95% | 39 | +49.3% | 150 | +33.8% | -63% | 0.82 | 0.77 | +49.1% | 0.93 | 70% | +33.1% / +32.1% | ENPH: +30.8%, Sharpe 0.78 |
| top8, in RS>=0.8, out RS<0.5, volatility-adjusted | 15 | 93% | 46 | +26.6% | 125 | +37.3% | -47% | 0.96 | 0.99 | +45.3% | 0.93 | 100% | +36.4% / +35.0% | RKLB: +31.1%, Sharpe 0.86 |

## Momentum rotation — universe: largecap_2015 (from 2018-02-01, 20 bps per side)

| benchmark | CAGR | max DD | Sharpe | train+val Sharpe | OOS CAGR | OOS Sharpe |
|---|---|---|---|---|---|---|
| SPY buy-and-hold | +13.8% | -34% | 0.78 | 0.73 | +15.9% | 0.97 |
| equal-weight universe (no costs) | +13.8% | -37% | 0.79 | 0.69 | +18.6% | 1.32 |

| rule set | trades/yr | exposure | win% | avg trade | avg days | CAGR | max DD | Sharpe | train+val Sharpe | OOS CAGR | OOS Sharpe | vs random | CAGR @40 / @70 bps | without best stock |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| top5, in RS>=0.8, out RS<0.5 | 10 | 95% | 50 | +9.6% | 116 | +16.2% | -36% | 0.71 | 0.64 | +25.7% | 0.91 | 90% | +15.3% / +14.0% | DVN: +12.8%, Sharpe 0.61 |
| top5, in RS>=0.8, out RS<0.5, stop -20% | 10 | 94% | 52 | +9.3% | 112 | +16.4% | -36% | 0.72 | 0.65 | +25.5% | 0.90 | 85% | +15.4% / +14.1% | DVN: +13.1%, Sharpe 0.62 |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d | 20 | 81% | 48 | +3.3% | 50 | +11.3% | -26% | 0.59 | 0.64 | +7.8% | 0.41 | 90% | +9.6% / +7.0% | AVGO: +11.4%, Sharpe 0.62 |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | 20 | 81% | 48 | +3.3% | 50 | +11.3% | -26% | 0.59 | 0.64 | +7.8% | 0.42 | 100% | +9.6% / +7.0% | AVGO: +11.4%, Sharpe 0.61 |
| top5, in RS>=0.8, out RS<0.7 | 14 | 94% | 49 | +5.3% | 85 | +12.4% | -36% | 0.57 | 0.56 | +15.6% | 0.61 | 100% | +11.2% / +9.5% | INTC: +10.4%, Sharpe 0.54 |
| top5, in RS>=0.8, out RS<0.7, stop -20% | 14 | 95% | 49 | +5.8% | 83 | +14.4% | -33% | 0.64 | 0.65 | +15.1% | 0.60 | 100% | +13.2% / +11.4% | INTC: +12.8%, Sharpe 0.61 |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d | 22 | 81% | 47 | +2.7% | 45 | +10.1% | -29% | 0.54 | 0.63 | +4.3% | 0.29 | 90% | +8.2% / +5.4% | AVGO: +8.9%, Sharpe 0.50 |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | 23 | 81% | 48 | +2.6% | 44 | +10.0% | -29% | 0.54 | 0.63 | +4.1% | 0.28 | 95% | +8.0% / +5.2% | AVGO: +8.9%, Sharpe 0.50 |
| top8, in RS>=0.8, out RS<0.5 | 17 | 94% | 46 | +8.9% | 112 | +16.1% | -29% | 0.76 | 0.70 | +22.6% | 0.96 | 100% | +15.2% / +13.9% | DVN: +14.0%, Sharpe 0.70 |
| top8, in RS>=0.8, out RS<0.5, stop -20% | 17 | 93% | 47 | +7.6% | 107 | +14.9% | -29% | 0.72 | 0.66 | +21.0% | 0.92 | 100% | +14.0% / +12.6% | DVN: +12.5%, Sharpe 0.65 |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d | 31 | 80% | 45 | +2.9% | 52 | +9.2% | -28% | 0.56 | 0.56 | +8.2% | 0.49 | 100% | +7.6% / +5.2% | DVN: +8.7%, Sharpe 0.54 |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | 31 | 80% | 45 | +2.8% | 51 | +9.2% | -28% | 0.55 | 0.56 | +8.1% | 0.49 | 100% | +7.6% / +5.2% | DVN: +8.7%, Sharpe 0.54 |
| top8, in RS>=0.8, out RS<0.7 | 22 | 93% | 50 | +5.0% | 82 | +13.1% | -26% | 0.67 | 0.65 | +14.3% | 0.70 | 95% | +12.0% / +10.2% | META: +10.2%, Sharpe 0.55 |
| top8, in RS>=0.8, out RS<0.7, stop -20% | 23 | 93% | 48 | +5.0% | 80 | +12.8% | -29% | 0.65 | 0.64 | +13.7% | 0.67 | 95% | +11.6% / +9.8% | AVGO: +10.4%, Sharpe 0.56 |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d | 35 | 80% | 48 | +2.2% | 45 | +8.9% | -29% | 0.55 | 0.58 | +6.1% | 0.39 | 100% | +7.1% / +4.4% | AVGO: +8.3%, Sharpe 0.52 |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | 35 | 80% | 48 | +2.2% | 45 | +8.8% | -29% | 0.54 | 0.58 | +5.9% | 0.39 | 100% | +7.0% / +4.3% | AVGO: +8.3%, Sharpe 0.52 |
| top8, in RS>=0.8, out RS<0.5, 12-1 month momentum | 19 | 90% | 34 | +3.4% | 95 | +5.4% | -40% | 0.35 | 0.40 | +1.6% | 0.18 | 20% | +4.5% / +3.2% | GE: +3.8%, Sharpe 0.28 |
| top8, in RS>=0.8, out RS<0.5, monthly | 12 | 94% | 49 | +9.5% | 146 | +13.0% | -26% | 0.64 | 0.60 | +16.4% | 0.75 | 95% | +12.3% / +12.9% | DVN: +12.8%, Sharpe 0.63 |
| top8, in RS>=0.8, out RS<0.5, volatility-adjusted | 16 | 93% | 54 | +6.8% | 115 | +12.6% | -22% | 0.73 | 0.68 | +14.6% | 0.93 | 100% | +11.8% / +10.5% | GE: +9.7%, Sharpe 0.59 |

## Rotation: pre-registered selection (2015 large caps, train+validation only)

Gates: train+val Sharpe > SPY's, ranking beats >= 90% of random selections, CAGR without the single best stock >= SPY's, max drawdown at most 10 points worse than SPY's.

**Chosen: none — no rule set passed every gate**

| rule set | passes | train+val Sharpe | failed gates |
|---|---|---|---|
| top5, in RS>=0.8, out RS<0.5 | ❌ | 0.64 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top5, in RS>=0.8, out RS<0.5, stop -20% | ❌ | 0.65 | train_val_sharpe_beats_spy, ranking_beats_random, without_best_stock_beats_spy |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d | ❌ | 0.64 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | ❌ | 0.64 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top5, in RS>=0.8, out RS<0.7 | ❌ | 0.56 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top5, in RS>=0.8, out RS<0.7, stop -20% | ❌ | 0.65 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d | ❌ | 0.63 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | ❌ | 0.63 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5 | ❌ | 0.70 | train_val_sharpe_beats_spy |
| top8, in RS>=0.8, out RS<0.5, stop -20% | ❌ | 0.66 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d | ❌ | 0.56 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | ❌ | 0.56 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.7 | ❌ | 0.65 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.7, stop -20% | ❌ | 0.64 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d | ❌ | 0.58 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | ❌ | 0.58 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5, 12-1 month momentum | ❌ | 0.40 | train_val_sharpe_beats_spy, ranking_beats_random, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5, monthly | ❌ | 0.60 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5, volatility-adjusted | ❌ | 0.68 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |

Calendar-year returns (2015 large caps, 20 bps per side):

| | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|---|---|---|---|
| SPY | -10% | +31% | +18% | +29% | -18% | +26% | +25% | +18% | +12% |
| equal-weight group | -10% | +29% | +14% | +31% | -4% | +16% | +16% | +17% | +17% |
| top5, in RS>=0.8, out RS<0.5 | +2% | +14% | +12% | +22% | +0% | +11% | +37% | +15% | +34% |
| top5, in RS>=0.8, out RS<0.5, stop -20% | +1% | +14% | +12% | +22% | -0% | +14% | +36% | +14% | +34% |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d | +6% | +3% | +16% | +21% | -1% | +21% | +19% | +9% | +7% |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | +6% | +3% | +16% | +22% | -1% | +21% | +19% | +9% | +7% |
| top5, in RS>=0.8, out RS<0.7 | +2% | +8% | +7% | +21% | -4% | +19% | +30% | -2% | +33% |
| top5, in RS>=0.8, out RS<0.7, stop -20% | +1% | +7% | +9% | +22% | +10% | +21% | +30% | -2% | +33% |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d | +8% | -3% | +8% | +21% | -2% | +22% | +29% | -5% | +14% |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | +8% | -3% | +8% | +21% | -2% | +22% | +29% | -5% | +14% |
| top8, in RS>=0.8, out RS<0.5 | -0% | +7% | +17% | +28% | +0% | +23% | +27% | +22% | +20% |
| top8, in RS>=0.8, out RS<0.5, stop -20% | -1% | +8% | +11% | +33% | +1% | +20% | +22% | +23% | +17% |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d | +7% | -5% | +11% | +30% | -2% | +14% | +13% | +14% | +2% |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | +6% | -4% | +11% | +30% | -2% | +14% | +13% | +14% | +2% |
| top8, in RS>=0.8, out RS<0.7 | -1% | +9% | +17% | +18% | +2% | +20% | +25% | +6% | +22% |
| top8, in RS>=0.8, out RS<0.7, stop -20% | -1% | +6% | +13% | +18% | +6% | +21% | +25% | +5% | +21% |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d | +8% | +2% | +12% | +18% | -4% | +9% | +24% | +2% | +10% |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | +7% | +2% | +12% | +18% | -4% | +9% | +24% | +1% | +10% |
| top8, in RS>=0.8, out RS<0.5, 12-1 month momentum | -13% | +10% | +2% | +24% | -12% | +2% | +41% | -1% | +4% |
| top8, in RS>=0.8, out RS<0.5, monthly | -3% | +12% | +16% | +19% | -5% | +26% | +23% | +5% | +26% |
| top8, in RS>=0.8, out RS<0.5, volatility-adjusted | -2% | +17% | +3% | +22% | -8% | +18% | +38% | +20% | +8% |

## Rockets (from 2016-11-14, 20 bps per side, 10 slots x 10%, max 3 new per day)

Rocket day: close >= +jump vs previous close, volume >= 3x the 20-day average, close in the top quarter of the day's range, price >= $5, 20-day dollar volume >= $5M. Buy next open; sell next open after a close more than `trail` below the highest close, or after 40 sessions. 'Random' = same stocks, same liquidity filter, same exit, random dates.

SPY: +15.3%/yr, max DD -34%, Sharpe 0.88 · train+val +15.0%/yr, Sharpe 0.86

| variant | trades | win% | avg trade | median | ≥+50% | worst | random avg | excess vs random t (train+val) | 2015 large caps excess | CAGR | max DD | Sharpe | train+val CAGR / Sharpe | OOS CAGR | random-entry portfolio CAGR | without top 3 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| EPS surprise>0%, reaction>=5% | 1902 | 54 | +4.6% | +1.9% | 4.3% | -51% | +4.3% | -0.34% (-0.53) | -0.31% (n=562) | +7.8% | -41% | 0.46 | +9.8% / 0.54 | -2.2% | +17.6% | +7.8% |
| EPS surprise>0%, reaction>=10% | 923 | 53 | +6.2% | +1.9% | 6.2% | -51% | +4.3% | +0.76% (0.75) | +1.68% (n=129) | +23.0% | -42% | 0.96 | +23.7% / 1.00 | +15.1% | +17.6% | +22.6% |
| EPS surprise>10%, reaction>=5% | 1267 | 53 | +5.0% | +2.0% | 5.1% | -51% | +4.3% | +0.62% (0.75) | -0.66% (n=268) | +13.5% | -44% | 0.66 | +19.9% / 0.90 | -14.3% | +17.6% | +11.7% |
| EPS surprise>10%, reaction>=10% | 714 | 53 | +6.6% | +2.2% | 6.6% | -51% | +4.3% | +1.66% (1.37) | +2.04% (n=71) | +17.1% | -45% | 0.74 | +26.1% / 1.04 | -17.7% | +17.6% | +15.1% |
| EPS surprise>20%, reaction>=10%, volume>=2x, RS>=0.8 | 236 | 57 | +8.8% | +3.6% | 7.2% | -34% | +4.3% | +3.28% (1.52) | +3.91% (n=14) | +17.8% | -27% | 0.92 | +24.5% / 1.24 | -9.0% | +17.6% | +11.8% |
| EPS surprise>20%, reaction>=15%, volume>=2x, RS>=0.8 | 168 | 58 | +9.1% | +4.0% | 8.3% | -33% | +4.3% | +1.45% (0.60) | —% (n=4) | +14.8% | -21% | 0.90 | +18.2% / 1.13 | -1.1% | +17.6% | +10.2% |
| jump>=8%, trail 15% | 1001 | 46 | +4.0% | -2.6% | 5.3% | -52% | +2.2% | -0.08% (-0.08) | -1.46% (n=114) | +15.2% | -48% | 0.62 | +22.5% / 0.80 | -14.3% | +18.8% | +9.4% |
| jump>=8%, trail 25% | 998 | 51 | +5.4% | +0.6% | 6.8% | -61% | +2.9% | +0.46% (0.40) | -1.39% (n=114) | +14.9% | -68% | 0.59 | +21.1% / 0.75 | -5.9% | +15.3% | +10.9% |
| jump>=15%, trail 15% | 542 | 43 | +4.7% | -4.5% | 6.8% | -52% | +2.2% | -0.46% (-0.32) | -4.51% (n=23) | +18.3% | -38% | 0.71 | +21.2% / 0.78 | +4.4% | +18.8% | +12.0% |
| jump>=15%, trail 25% | 540 | 47 | +6.6% | -2.2% | 9.3% | -61% | +2.9% | +0.95% (0.52) | -4.75% (n=23) | +14.7% | -60% | 0.57 | +20.7% / 0.72 | -7.0% | +15.3% | +6.4% |

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
| combined | all | +0.95 | -0.44 | +0.34 | +1.07 | +0.03 | -0.44 | +0.53 | +0.42 | +0.23 | -0.02 |
| combined | SPY>200d & stock>200d | +1.03 | -0.43 | +0.08 | +0.93 | -0.03 | -0.79 | +0.38 | +0.42 | +0.19 | +0.00 |
| combined | SPY>200d & stock>200d & RS>=0.8 | +1.03 | -0.26 | +0.47 | +1.45 | -0.41 | -0.36 | +0.35 | +0.60 | +0.83 | +0.15 |
| combined | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | +1.10 | -0.12 | +0.59 | +1.35 | -0.52 | -0.07 | +0.30 | +0.46 | +0.81 | +0.38 |
| combined | score>=70 & SPY>200d & stock>200d | +0.81 | +0.65 | +0.42 | +1.14 | -0.54 | -0.96 | +0.43 | +0.69 | +0.52 | +0.13 |
| combined | score>=70 & SPY>200d & stock>200d & RS>=0.8 | +0.17 | +1.33 | +0.61 | +1.08 | -0.53 | -1.15 | +0.41 | +1.00 | +0.70 | +0.17 |
| baseline_random | all | +1.20 | +0.06 | +0.55 | +0.98 | +0.15 | -0.28 | +0.61 | +0.42 | +0.30 | +0.18 |
| baseline_random | SPY>200d & stock>200d | +1.31 | -0.25 | +0.52 | +0.85 | +0.17 | -0.78 | +0.26 | +0.42 | +0.21 | +0.16 |
| baseline_random | SPY>200d & stock>200d & RS>=0.8 | +1.37 | +0.13 | +0.66 | +1.15 | -0.24 | -0.74 | +0.47 | +0.51 | +0.39 | +0.10 |
| baseline_random | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | +1.25 | +0.29 | +0.75 | +0.96 | -0.29 | -0.63 | +0.55 | +0.60 | +0.64 | +0.05 |