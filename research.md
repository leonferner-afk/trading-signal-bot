# Strategy research

278 symbols with data (1 failed), 10 years of daily bars. Control group: 105 stocks that were already large caps in 2015. Primary cost 20 bps per side (USD account: courtage + slippage; 40 bps ≈ trading from a SEK account). Validation from 2023-02-11, out-of-sample (OOS) from 2024-12-13. Setups invalidated at the next open (skipped): 1304.

Portfolio: max 8 positions, max 3 new per day, 1% risk per trade, max 25% of equity per position, no leverage, marked to market daily. 'vs random' = share of 40 random-order portfolios from the same eligible trades that this ranking beat.

## Portfolio — universe: all

SPY buy-and-hold: +15.0%/yr, max DD -34%, Sharpe 0.85 · train+val Sharpe 0.83 · OOS +15.1%/yr, Sharpe 0.91

| rule set | trades/yr | exposure | win% | avgR | CAGR | max DD | Sharpe | train+val Sharpe | OOS CAGR | OOS Sharpe | vs random |
|---|---|---|---|---|---|---|---|---|---|---|---|
| random picks (reference) | 78.0 | 87% | 22 | +0.27 | +10.3% | -54% | 0.48 | 0.73 | -16.8% | -0.41 | — |
| random picks, trend filter | 65.0 | 78% | 22 | +0.32 | +15.6% | -42% | 0.71 | 0.85 | +15.3% | 0.61 | — |
| RS leaders, trend filter | 73.4 | 66% | 22 | +0.37 | +19.5% | -42% | 0.72 | 0.85 | -2.1% | 0.13 | 90% |
| RS leaders near 52w high | 65.4 | 76% | 26 | +0.69 | +34.3% | -34% | 1.11 | 1.24 | +12.5% | 0.50 | 100% |
| signals score>=70, trend | 45.8 | 63% | 21 | +0.34 | +12.0% | -35% | 0.64 | 0.74 | -1.5% | 0.04 | 17% |
| signals score>=70, trend, RS top 20% | 41.0 | 51% | 22 | +0.54 | +19.7% | -33% | 0.92 | 1.01 | +7.4% | 0.41 | 70% |
| signals, trend, RS top 20% | 77.7 | 78% | 22 | +0.71 | +38.8% | -48% | 1.13 | 1.30 | +12.5% | 0.48 | 100% |
| signals, trend, RS top 20%, near 52w high | 74.2 | 78% | 22 | +0.52 | +28.7% | -32% | 1.00 | 1.15 | +15.1% | 0.55 | 97% |

Cost sensitivity (full-period CAGR / Sharpe):

| rule set | 20 bps | 40 bps | 70 bps |
|---|---|---|---|
| RS leaders, trend filter | +19.5% / 0.72 | +15.9% / 0.63 | +10.7% / 0.48 |
| RS leaders near 52w high | +34.3% / 1.11 | +29.8% / 1.00 | +23.3% / 0.84 |
| signals score>=70, trend | +12.0% / 0.64 | +9.1% / 0.52 | +5.3% / 0.35 |
| signals score>=70, trend, RS top 20% | +19.7% / 0.92 | +17.2% / 0.82 | +13.5% / 0.67 |
| signals, trend, RS top 20% | +38.8% / 1.13 | +33.4% / 1.01 | +26.2% / 0.85 |
| signals, trend, RS top 20%, near 52w high | +28.7% / 1.00 | +23.4% / 0.86 | +16.6% / 0.67 |

Exit variant (stop 2.5 x ATR instead of 1.5 x ATR / structural):

| rule set | CAGR | max DD | Sharpe | OOS Sharpe |
|---|---|---|---|---|
| random picks (reference) | +10.4% | -42% | 0.58 | -0.05 |
| random picks, trend filter | +13.0% | -36% | 0.75 | 0.68 |
| RS leaders, trend filter | +17.7% | -28% | 0.86 | 0.84 |
| RS leaders near 52w high | +25.1% | -24% | 1.11 | 0.24 |
| signals score>=70, trend | +11.9% | -29% | 0.75 | -0.18 |
| signals score>=70, trend, RS top 20% | +17.1% | -28% | 1.00 | 0.31 |
| signals, trend, RS top 20% | +17.7% | -36% | 0.85 | 0.33 |
| signals, trend, RS top 20%, near 52w high | +16.7% | -24% | 0.82 | 0.22 |

### Per trade — universe: all (one position per symbol, t over monthly means)

| group | exit | policy | n | win% | avgR | medR | t | excess vs random (t) | ≥+50% | OOS n | OOS avgR |
|---|---|---|---|---|---|---|---|---|---|---|---|
| breakout | fixed | all | 6481 | 17 | +0.289 | -1.11 | 1.27 | -0.312 (-3.72) | 3.2% | 1434 | -0.015 |
| breakout | fixed | SPY>200d & stock>200d | 5140 | 16 | +0.242 | -1.12 | 0.62 | -0.202 (-2.86) | 3.0% | 1157 | -0.003 |
| breakout | fixed | SPY>200d & stock>200d & RS>=0.8 | 2128 | 18 | +0.436 | -1.08 | 1.67 | -0.162 (-1.52) | 5.5% | 501 | +0.459 |
| breakout | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1737 | 18 | +0.480 | -1.08 | 1.64 | -0.055 (-0.45) | 4.4% | 384 | +0.643 |
| breakout | fixed | score>=70 & SPY>200d & stock>200d | 746 | 22 | +0.482 | -1.00 | 2.40 | +0.094 (0.59) | 5.9% | 140 | +0.292 |
| breakout | fixed | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 454 | 23 | +0.600 | -0.97 | 2.77 | +0.200 (0.86) | 7.7% | 92 | +0.448 |
| momentum | fixed | all | 5363 | 22 | +0.270 | -1.04 | 1.88 | -0.287 (-3.78) | 3.6% | 1186 | +0.034 |
| momentum | fixed | SPY>200d & stock>200d | 4736 | 22 | +0.308 | -1.04 | 1.94 | -0.083 (-1.30) | 3.5% | 1076 | +0.060 |
| momentum | fixed | SPY>200d & stock>200d & RS>=0.8 | 1920 | 22 | +0.385 | -1.02 | 2.13 | -0.119 (-1.49) | 6.3% | 445 | +0.217 |
| momentum | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1585 | 22 | +0.392 | -1.03 | 2.06 | -0.051 (-0.58) | 4.6% | 355 | +0.190 |
| momentum | fixed | score>=70 & SPY>200d & stock>200d | 155 | 24 | +0.559 | -0.92 | 2.03 | +0.320 (1.16) | 12.9% | 38 | +0.903 |
| momentum | fixed | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 96 | 25 | +0.731 | -0.88 | 1.87 | +0.279 (0.75) | 15.6% | 27 | +0.905 |
| combined | fixed | all | 8153 | 19 | +0.277 | -1.08 | 1.60 | -0.302 (-4.33) | 3.3% | 1787 | +0.091 |
| combined | fixed | SPY>200d & stock>200d | 6718 | 19 | +0.245 | -1.08 | 0.94 | -0.170 (-2.88) | 3.1% | 1500 | +0.076 |
| combined | fixed | SPY>200d & stock>200d & RS>=0.8 | 2803 | 20 | +0.412 | -1.04 | 1.96 | -0.144 (-1.80) | 5.5% | 659 | +0.474 |
| combined | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 2307 | 20 | +0.422 | -1.05 | 1.95 | -0.053 (-0.62) | 4.3% | 509 | +0.561 |
| combined | fixed | score>=70 & SPY>200d & stock>200d | 821 | 23 | +0.504 | -0.98 | 2.22 | +0.085 (0.59) | 6.6% | 163 | +0.329 |
| combined | fixed | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 499 | 23 | +0.610 | -0.95 | 2.49 | +0.139 (0.64) | 8.6% | 108 | +0.452 |
| baseline_random | fixed | all | 17861 | 24 | +0.346 | -1.01 | 4.88 | — (—) | 4.9% | 4098 | +0.212 |
| baseline_random | fixed | SPY>200d & stock>200d | 11338 | 23 | +0.321 | -1.04 | 3.03 | — (—) | 3.5% | 2588 | +0.161 |
| baseline_random | fixed | SPY>200d & stock>200d & RS>=0.8 | 4581 | 23 | +0.378 | -1.03 | 3.41 | — (—) | 6.2% | 1111 | +0.215 |
| baseline_random | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 3122 | 23 | +0.440 | -1.04 | 3.09 | — (—) | 4.0% | 680 | +0.309 |
| breakout | wide | all | 5210 | 33 | +0.303 | -0.95 | 3.17 | -0.162 (-2.94) | 5.5% | 1138 | +0.244 |
| breakout | wide | SPY>200d & stock>200d | 4192 | 33 | +0.314 | -0.96 | 2.27 | -0.068 (-1.40) | 5.1% | 930 | +0.259 |
| breakout | wide | SPY>200d & stock>200d & RS>=0.8 | 1780 | 34 | +0.439 | -0.93 | 2.71 | -0.099 (-1.65) | 9.2% | 418 | +0.381 |
| breakout | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1481 | 35 | +0.471 | -0.92 | 3.09 | -0.027 (-0.39) | 7.4% | 326 | +0.338 |
| breakout | wide | score>=70 & SPY>200d & stock>200d | 719 | 33 | +0.391 | -0.91 | 2.58 | +0.006 (0.05) | 9.0% | 133 | +0.154 |
| breakout | wide | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 432 | 34 | +0.482 | -0.89 | 3.01 | +0.051 (0.34) | 11.6% | 87 | +0.239 |
| momentum | wide | all | 4464 | 32 | +0.270 | -0.98 | 2.73 | -0.185 (-3.23) | 4.8% | 959 | +0.137 |
| momentum | wide | SPY>200d & stock>200d | 3959 | 33 | +0.313 | -0.98 | 2.86 | -0.028 (-0.55) | 4.7% | 874 | +0.167 |
| momentum | wide | SPY>200d & stock>200d & RS>=0.8 | 1623 | 32 | +0.355 | -0.96 | 2.34 | -0.133 (-2.23) | 8.0% | 373 | +0.231 |
| momentum | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1367 | 32 | +0.337 | -0.97 | 2.08 | -0.127 (-1.97) | 5.8% | 296 | +0.242 |
| momentum | wide | score>=70 & SPY>200d & stock>200d | 139 | 31 | +0.318 | -0.88 | 1.35 | +0.008 (0.04) | 15.1% | 33 | +0.723 |
| momentum | wide | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 82 | 32 | +0.458 | -0.80 | 1.45 | -0.014 (-0.06) | 19.5% | 23 | +0.856 |
| combined | wide | all | 6210 | 33 | +0.285 | -0.97 | 3.09 | -0.178 (-3.48) | 5.2% | 1345 | +0.208 |
| combined | wide | SPY>200d & stock>200d | 5188 | 33 | +0.307 | -0.98 | 2.40 | -0.068 (-1.57) | 4.8% | 1153 | +0.212 |
| combined | wide | SPY>200d & stock>200d & RS>=0.8 | 2254 | 33 | +0.377 | -0.95 | 2.49 | -0.119 (-2.18) | 8.3% | 533 | +0.320 |
| combined | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1883 | 33 | +0.390 | -0.95 | 2.68 | -0.068 (-1.15) | 6.6% | 412 | +0.306 |
| combined | wide | score>=70 & SPY>200d & stock>200d | 778 | 33 | +0.383 | -0.91 | 2.19 | -0.024 (-0.24) | 9.1% | 150 | +0.237 |
| combined | wide | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 463 | 33 | +0.467 | -0.89 | 2.55 | -0.020 (-0.14) | 12.1% | 98 | +0.336 |
| baseline_random | wide | all | 12419 | 35 | +0.320 | -0.94 | 5.33 | — (—) | 6.2% | 2751 | +0.260 |
| baseline_random | wide | SPY>200d & stock>200d | 8115 | 34 | +0.323 | -0.97 | 3.54 | — (—) | 4.7% | 1839 | +0.189 |
| baseline_random | wide | SPY>200d & stock>200d & RS>=0.8 | 3397 | 34 | +0.369 | -0.96 | 3.95 | — (—) | 8.3% | 799 | +0.259 |
| baseline_random | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 2479 | 35 | +0.433 | -0.97 | 3.96 | — (—) | 5.8% | 521 | +0.384 |

## Portfolio — universe: largecap_2015

SPY buy-and-hold: +15.0%/yr, max DD -34%, Sharpe 0.85 · train+val Sharpe 0.83 · OOS +15.1%/yr, Sharpe 0.91

| rule set | trades/yr | exposure | win% | avgR | CAGR | max DD | Sharpe | train+val Sharpe | OOS CAGR | OOS Sharpe | vs random |
|---|---|---|---|---|---|---|---|---|---|---|---|
| random picks (reference) | 41.5 | 88% | 26 | +0.28 | +7.5% | -25% | 0.54 | 0.66 | +3.0% | 0.28 | — |
| random picks, trend filter | 36.1 | 76% | 22 | +0.16 | +4.3% | -29% | 0.40 | 0.47 | +0.9% | 0.13 | — |
| RS leaders, trend filter | 42.3 | 76% | 23 | +0.24 | +7.1% | -36% | 0.47 | 0.59 | -0.5% | 0.08 | 65% |
| RS leaders near 52w high | 40.9 | 76% | 22 | +0.21 | +3.6% | -29% | 0.30 | 0.35 | +1.0% | 0.15 | 40% |
| signals score>=70, trend | 14.7 | 36% | 23 | +0.27 | +2.8% | -16% | 0.34 | 0.34 | +4.5% | 0.50 | 20% |
| signals score>=70, trend, RS top 20% | 10.7 | 25% | 22 | +0.35 | +2.4% | -19% | 0.34 | 0.41 | +2.4% | 0.35 | 15% |
| signals, trend, RS top 20% | 42.1 | 78% | 20 | +0.28 | +5.5% | -30% | 0.42 | 0.50 | +1.8% | 0.19 | 57% |
| signals, trend, RS top 20%, near 52w high | 42.1 | 78% | 20 | +0.27 | +6.4% | -33% | 0.48 | 0.57 | +2.0% | 0.21 | 68% |

Cost sensitivity (full-period CAGR / Sharpe):

| rule set | 20 bps | 40 bps | 70 bps |
|---|---|---|---|
| RS leaders, trend filter | +7.1% / 0.47 | +4.2% / 0.32 | -0.2% / 0.10 |
| RS leaders near 52w high | +3.6% / 0.30 | +0.6% / 0.13 | -4.1% / -0.14 |
| signals score>=70, trend | +2.8% / 0.34 | +1.4% / 0.20 | -0.6% / -0.01 |
| signals score>=70, trend, RS top 20% | +2.4% / 0.34 | +1.4% / 0.21 | -0.1% / 0.03 |
| signals, trend, RS top 20% | +5.5% / 0.42 | +2.1% / 0.22 | -2.8% / -0.09 |
| signals, trend, RS top 20%, near 52w high | +6.4% / 0.48 | +3.0% / 0.28 | -1.8% / -0.03 |

Exit variant (stop 2.5 x ATR instead of 1.5 x ATR / structural):

| rule set | CAGR | max DD | Sharpe | OOS Sharpe |
|---|---|---|---|---|
| random picks (reference) | +9.3% | -22% | 0.69 | 0.48 |
| random picks, trend filter | +6.1% | -30% | 0.54 | 0.98 |
| RS leaders, trend filter | +10.4% | -25% | 0.67 | 0.39 |
| RS leaders near 52w high | +12.3% | -22% | 0.77 | 0.34 |
| signals score>=70, trend | +1.6% | -16% | 0.23 | 0.48 |
| signals score>=70, trend, RS top 20% | +2.9% | -17% | 0.41 | 0.41 |
| signals, trend, RS top 20% | +6.8% | -21% | 0.52 | 0.17 |
| signals, trend, RS top 20%, near 52w high | +6.2% | -27% | 0.49 | 0.27 |

### Per trade — universe: largecap_2015 (one position per symbol, t over monthly means)

| group | exit | policy | n | win% | avgR | medR | t | excess vs random (t) | ≥+50% | OOS n | OOS avgR |
|---|---|---|---|---|---|---|---|---|---|---|---|
| breakout | fixed | all | 2259 | 17 | +0.088 | -1.16 | -0.44 | -0.426 (-3.57) | 0.2% | 438 | -0.196 |
| breakout | fixed | SPY>200d & stock>200d | 1852 | 16 | +0.015 | -1.17 | -0.52 | -0.248 (-2.44) | 0.1% | 365 | -0.183 |
| breakout | fixed | SPY>200d & stock>200d & RS>=0.8 | 757 | 18 | +0.288 | -1.12 | 1.22 | +0.039 (0.18) | 0.1% | 155 | +0.045 |
| breakout | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 709 | 18 | +0.316 | -1.12 | 1.31 | +0.087 (0.40) | 0.1% | 150 | +0.171 |
| breakout | fixed | score>=70 & SPY>200d & stock>200d | 158 | 22 | +0.188 | -1.02 | 0.94 | -0.059 (-0.21) | 0.0% | 26 | +0.486 |
| breakout | fixed | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 104 | 21 | +0.218 | -1.01 | 1.07 | -0.030 (-0.09) | 0.0% | 15 | +0.482 |
| momentum | fixed | all | 2161 | 22 | +0.186 | -1.10 | 1.19 | -0.254 (-2.68) | 0.1% | 428 | +0.003 |
| momentum | fixed | SPY>200d & stock>200d | 1927 | 22 | +0.224 | -1.10 | 1.00 | -0.075 (-0.85) | 0.1% | 394 | +0.062 |
| momentum | fixed | SPY>200d & stock>200d & RS>=0.8 | 827 | 22 | +0.234 | -1.08 | 0.23 | -0.227 (-2.05) | 0.0% | 166 | +0.109 |
| momentum | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 785 | 22 | +0.218 | -1.08 | 0.06 | -0.217 (-1.93) | 0.0% | 161 | +0.146 |
| momentum | fixed | score>=70 & SPY>200d & stock>200d | 15 | 20 | +0.106 | -1.03 | 0.39 | +0.036 (0.05) | 0.0% | 3 | -1.150 |
| momentum | fixed | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 8 | 25 | +0.909 | -0.90 | 0.74 | +0.039 (0.03) | 0.0% | 2 | -1.090 |
| combined | fixed | all | 3065 | 20 | +0.130 | -1.12 | 0.23 | -0.343 (-3.60) | 0.2% | 588 | -0.100 |
| combined | fixed | SPY>200d & stock>200d | 2616 | 20 | +0.100 | -1.13 | -0.09 | -0.178 (-2.22) | 0.1% | 506 | -0.066 |
| combined | fixed | SPY>200d & stock>200d & RS>=0.8 | 1125 | 20 | +0.218 | -1.08 | 0.22 | -0.186 (-1.70) | 0.0% | 219 | -0.028 |
| combined | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1066 | 20 | +0.212 | -1.09 | 0.29 | -0.148 (-1.39) | 0.0% | 213 | +0.065 |
| combined | fixed | score>=70 & SPY>200d & stock>200d | 169 | 22 | +0.222 | -1.02 | 1.10 | -0.039 (-0.15) | 0.0% | 29 | +0.316 |
| combined | fixed | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 110 | 22 | +0.308 | -0.99 | 1.33 | +0.037 (0.11) | 0.0% | 17 | +0.297 |
| baseline_random | fixed | all | 7392 | 25 | +0.300 | -1.05 | 4.26 | — (—) | 0.7% | 1497 | +0.260 |
| baseline_random | fixed | SPY>200d & stock>200d | 4837 | 23 | +0.244 | -1.08 | 2.40 | — (—) | 0.3% | 969 | +0.193 |
| baseline_random | fixed | SPY>200d & stock>200d & RS>=0.8 | 1939 | 24 | +0.295 | -1.06 | 2.30 | — (—) | 0.4% | 427 | +0.133 |
| baseline_random | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1724 | 23 | +0.286 | -1.07 | 2.04 | — (—) | 0.2% | 366 | +0.175 |
| breakout | wide | all | 1927 | 33 | +0.191 | -1.00 | 1.55 | -0.236 (-3.18) | 0.3% | 364 | +0.146 |
| breakout | wide | SPY>200d & stock>200d | 1583 | 33 | +0.208 | -1.00 | 1.60 | -0.043 (-0.61) | 0.2% | 306 | +0.195 |
| breakout | wide | SPY>200d & stock>200d & RS>=0.8 | 671 | 33 | +0.272 | -0.97 | 1.26 | -0.143 (-1.66) | 0.0% | 135 | +0.075 |
| breakout | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 633 | 33 | +0.276 | -0.97 | 1.37 | -0.096 (-1.11) | 0.0% | 130 | +0.117 |
| breakout | wide | score>=70 & SPY>200d & stock>200d | 158 | 32 | +0.170 | -0.93 | 0.58 | -0.125 (-0.66) | 0.0% | 26 | +0.405 |
| breakout | wide | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 104 | 32 | +0.306 | -0.93 | 1.20 | -0.130 (-0.53) | 0.0% | 15 | +0.530 |
| momentum | wide | all | 1838 | 32 | +0.193 | -1.02 | 1.92 | -0.199 (-2.67) | 0.1% | 356 | +0.094 |
| momentum | wide | SPY>200d & stock>200d | 1639 | 33 | +0.240 | -1.02 | 2.09 | +0.009 (0.13) | 0.1% | 331 | +0.131 |
| momentum | wide | SPY>200d & stock>200d & RS>=0.8 | 712 | 34 | +0.263 | -0.99 | 1.32 | -0.141 (-1.87) | 0.0% | 146 | -0.005 |
| momentum | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 676 | 34 | +0.270 | -0.99 | 1.51 | -0.086 (-1.10) | 0.0% | 143 | +0.026 |
| momentum | wide | score>=70 & SPY>200d & stock>200d | 14 | 29 | +0.005 | -0.99 | 0.33 | +0.051 (0.10) | 0.0% | 3 | -1.085 |
| momentum | wide | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 7 | 43 | +0.817 | -0.91 | 0.92 | -0.009 (-0.01) | 0.0% | 2 | -1.053 |
| combined | wide | all | 2430 | 33 | +0.187 | -1.01 | 1.77 | -0.223 (-3.24) | 0.3% | 459 | +0.134 |
| combined | wide | SPY>200d & stock>200d | 2086 | 33 | +0.205 | -1.02 | 1.81 | -0.029 (-0.51) | 0.1% | 405 | +0.170 |
| combined | wide | SPY>200d & stock>200d & RS>=0.8 | 915 | 34 | +0.281 | -0.99 | 1.57 | -0.108 (-1.65) | 0.0% | 183 | +0.007 |
| combined | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 868 | 34 | +0.285 | -0.99 | 1.64 | -0.059 (-0.95) | 0.0% | 178 | +0.043 |
| combined | wide | score>=70 & SPY>200d & stock>200d | 168 | 32 | +0.176 | -0.93 | 0.79 | -0.102 (-0.56) | 0.0% | 29 | +0.251 |
| combined | wide | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 109 | 32 | +0.348 | -0.92 | 1.37 | -0.104 (-0.44) | 0.0% | 17 | +0.343 |
| baseline_random | wide | all | 5213 | 37 | +0.305 | -0.94 | 5.15 | — (—) | 0.8% | 1009 | +0.328 |
| baseline_random | wide | SPY>200d & stock>200d | 3499 | 35 | +0.261 | -0.99 | 2.99 | — (—) | 0.2% | 710 | +0.249 |
| baseline_random | wide | SPY>200d & stock>200d & RS>=0.8 | 1477 | 36 | +0.321 | -0.98 | 3.04 | — (—) | 0.4% | 314 | +0.184 |
| baseline_random | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1327 | 35 | +0.321 | -0.99 | 2.87 | — (—) | 0.3% | 269 | +0.224 |

## Momentum rotation — universe: all (from 2018-01-25, 20 bps per side)

| benchmark | CAGR | max DD | Sharpe | train+val Sharpe | OOS CAGR | OOS Sharpe |
|---|---|---|---|---|---|---|
| SPY buy-and-hold | +13.8% | -34% | 0.77 | 0.74 | +15.1% | 0.91 |
| equal-weight universe (no costs) | +25.2% | -42% | 0.98 | 1.00 | +22.5% | 0.94 |

| rule set | trades/yr | exposure | win% | avg trade | avg days | CAGR | max DD | Sharpe | train+val Sharpe | OOS CAGR | OOS Sharpe | vs random | CAGR @40 / @70 bps | without best stock |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| top5, in RS>=0.8, out RS<0.5 | 11 | 92% | 40 | +25.0% | 108 | +25.1% | -75% | 0.67 | 0.63 | +39.7% | 0.81 | 55% | +24.2% / +22.9% | SE: +24.8%, Sharpe 0.66 |
| top5, in RS>=0.8, out RS<0.5, stop -20% | 15 | 92% | 32 | +19.9% | 75 | +27.7% | -71% | 0.70 | 0.73 | +19.3% | 0.60 | 80% | +26.4% / +24.5% | SE: +25.7%, Sharpe 0.68 |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d | 21 | 81% | 38 | +6.3% | 49 | +11.8% | -74% | 0.47 | 0.68 | -26.3% | -0.19 | 20% | +10.1% / +7.6% | MARA: +8.9%, Sharpe 0.42 |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | 25 | 80% | 34 | +4.2% | 39 | +9.7% | -71% | 0.44 | 0.55 | -12.3% | 0.08 | 10% | +7.8% / +4.9% | CELH: +15.5%, Sharpe 0.53 |
| top5, in RS>=0.8, out RS<0.7 | 12 | 93% | 46 | +12.9% | 93 | +17.8% | -76% | 0.57 | 0.53 | +29.1% | 0.71 | 0% | +16.8% / +15.3% | ENPH: +17.9%, Sharpe 0.57 |
| top5, in RS>=0.8, out RS<0.7, stop -20% | 18 | 92% | 36 | +11.6% | 65 | +22.5% | -77% | 0.63 | 0.51 | +57.5% | 0.99 | 55% | +21.0% / +18.8% | VKTX: +15.4%, Sharpe 0.54 |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d | 22 | 80% | 40 | +4.2% | 45 | +9.4% | -77% | 0.44 | 0.53 | -9.9% | 0.20 | 20% | +7.6% / +4.9% | TSLA: +15.2%, Sharpe 0.53 |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | 27 | 80% | 36 | +4.3% | 37 | +10.5% | -68% | 0.45 | 0.49 | +0.1% | 0.32 | 25% | +8.4% / +5.3% | CELH: +6.3%, Sharpe 0.38 |
| top8, in RS>=0.8, out RS<0.5 | 16 | 92% | 38 | +22.0% | 107 | +31.4% | -64% | 0.79 | 0.84 | +24.3% | 0.66 | 70% | +30.5% / +29.0% | SE: +28.5%, Sharpe 0.74 |
| top8, in RS>=0.8, out RS<0.5, stop -20% | 24 | 92% | 34 | +15.2% | 73 | +27.9% | -62% | 0.73 | 0.80 | +16.6% | 0.57 | 70% | +26.6% / +24.6% | SE: +22.6%, Sharpe 0.64 |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d | 30 | 80% | 38 | +9.0% | 52 | +27.1% | -58% | 0.73 | 0.79 | +16.6% | 0.56 | 75% | +25.4% / +22.9% | APP: +20.2%, Sharpe 0.62 |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | 36 | 80% | 35 | +7.2% | 42 | +25.0% | -67% | 0.70 | 0.75 | +18.3% | 0.58 | 85% | +23.2% / +20.4% | NIO: +26.3%, Sharpe 0.72 |
| top8, in RS>=0.8, out RS<0.7 | 19 | 92% | 49 | +19.3% | 95 | +34.9% | -57% | 0.81 | 0.85 | +30.3% | 0.73 | 95% | +33.8% / +32.2% | MARA: +26.3%, Sharpe 0.71 |
| top8, in RS>=0.8, out RS<0.7, stop -20% | 27 | 91% | 34 | +16.2% | 64 | +27.8% | -71% | 0.71 | 0.71 | +30.1% | 0.73 | 80% | +26.4% / +24.2% | MARA: +20.6%, Sharpe 0.61 |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d | 32 | 80% | 41 | +7.7% | 48 | +21.1% | -54% | 0.63 | 0.71 | +5.9% | 0.40 | 40% | +19.3% / +16.6% | MARA: +18.8%, Sharpe 0.60 |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | 40 | 80% | 34 | +9.8% | 38 | +27.4% | -63% | 0.71 | 0.79 | +8.0% | 0.43 | 90% | +25.2% / +21.9% | MARA: +24.2%, Sharpe 0.67 |
| top8, in RS>=0.8, out RS<0.5, 12-1 month momentum | 18 | 91% | 32 | +19.9% | 99 | +23.2% | -63% | 0.67 | 0.67 | +28.4% | 0.70 | 70% | +22.3% / +20.9% | SE: +19.4%, Sharpe 0.60 |
| top8, in RS>=0.8, out RS<0.5, monthly | 11 | 94% | 39 | +49.3% | 150 | +34.4% | -63% | 0.83 | 0.79 | +49.9% | 0.94 | 70% | +33.8% / +32.8% | ENPH: +31.4%, Sharpe 0.79 |
| top8, in RS>=0.8, out RS<0.5, volatility-adjusted | 14 | 93% | 45 | +25.9% | 125 | +29.5% | -53% | 0.83 | 0.81 | +45.0% | 0.93 | 95% | +32.9% / +31.6% | RKLB: +23.8%, Sharpe 0.72 |

## Momentum rotation — universe: largecap_2015 (from 2018-01-25, 20 bps per side)

| benchmark | CAGR | max DD | Sharpe | train+val Sharpe | OOS CAGR | OOS Sharpe |
|---|---|---|---|---|---|---|
| SPY buy-and-hold | +13.8% | -34% | 0.77 | 0.74 | +15.1% | 0.91 |
| equal-weight universe (no costs) | +13.6% | -37% | 0.78 | 0.71 | +16.6% | 1.19 |

| rule set | trades/yr | exposure | win% | avg trade | avg days | CAGR | max DD | Sharpe | train+val Sharpe | OOS CAGR | OOS Sharpe | vs random | CAGR @40 / @70 bps | without best stock |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| top5, in RS>=0.8, out RS<0.5 | 10 | 95% | 49 | +7.8% | 114 | +15.8% | -36% | 0.69 | 0.60 | +26.8% | 0.93 | 100% | +14.9% / +13.6% | DVN: +12.3%, Sharpe 0.59 |
| top5, in RS>=0.8, out RS<0.5, stop -20% | 10 | 94% | 51 | +7.7% | 110 | +15.9% | -36% | 0.70 | 0.61 | +26.5% | 0.93 | 90% | +15.1% / +13.8% | DVN: +12.7%, Sharpe 0.61 |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d | 20 | 81% | 47 | +3.0% | 50 | +10.9% | -26% | 0.57 | 0.60 | +8.7% | 0.44 | 95% | +9.2% / +6.7% | AVGO: +11.0%, Sharpe 0.59 |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | 20 | 81% | 48 | +3.0% | 49 | +10.9% | -25% | 0.57 | 0.60 | +8.7% | 0.45 | 85% | +9.2% / +6.6% | AVGO: +10.9%, Sharpe 0.59 |
| top5, in RS>=0.8, out RS<0.7 | 14 | 94% | 48 | +3.9% | 83 | +11.7% | -36% | 0.55 | 0.54 | +15.2% | 0.60 | 95% | +10.6% / +8.9% | META: +9.7%, Sharpe 0.49 |
| top5, in RS>=0.8, out RS<0.7, stop -20% | 14 | 95% | 48 | +4.4% | 81 | +13.7% | -33% | 0.61 | 0.63 | +14.6% | 0.59 | 100% | +12.6% / +10.8% | META: +13.2%, Sharpe 0.60 |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d | 22 | 81% | 47 | +2.3% | 44 | +9.4% | -29% | 0.52 | 0.61 | +3.8% | 0.27 | 95% | +7.5% / +4.8% | AVGO: +8.3%, Sharpe 0.48 |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | 23 | 81% | 47 | +2.2% | 43 | +9.4% | -29% | 0.51 | 0.61 | +3.6% | 0.27 | 100% | +7.5% / +4.7% | AVGO: +8.3%, Sharpe 0.48 |
| top8, in RS>=0.8, out RS<0.5 | 17 | 94% | 46 | +6.9% | 108 | +14.4% | -29% | 0.70 | 0.61 | +22.9% | 0.97 | 100% | +13.5% / +12.2% | DVN: +12.4%, Sharpe 0.64 |
| top8, in RS>=0.8, out RS<0.5, stop -20% | 18 | 93% | 46 | +5.7% | 103 | +13.2% | -29% | 0.66 | 0.56 | +21.8% | 0.94 | 100% | +12.3% / +11.0% | DVN: +11.0%, Sharpe 0.58 |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d | 31 | 80% | 45 | +2.3% | 51 | +7.8% | -28% | 0.49 | 0.47 | +8.8% | 0.52 | 60% | +6.2% / +3.9% | DVN: +7.2%, Sharpe 0.47 |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | 31 | 80% | 44 | +2.3% | 51 | +7.8% | -27% | 0.49 | 0.47 | +8.7% | 0.51 | 55% | +6.2% / +3.8% | DVN: +7.2%, Sharpe 0.47 |
| top8, in RS>=0.8, out RS<0.7 | 22 | 93% | 48 | +3.9% | 81 | +11.9% | -26% | 0.62 | 0.60 | +13.9% | 0.68 | 100% | +10.8% / +9.0% | META: +9.0%, Sharpe 0.50 |
| top8, in RS>=0.8, out RS<0.7, stop -20% | 23 | 93% | 48 | +3.9% | 78 | +11.6% | -29% | 0.61 | 0.59 | +13.3% | 0.66 | 100% | +10.4% / +8.6% | AVGO: +9.3%, Sharpe 0.51 |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d | 35 | 80% | 47 | +1.8% | 45 | +7.7% | -29% | 0.49 | 0.52 | +5.4% | 0.36 | 90% | +5.9% / +3.2% | AVGO: +7.1%, Sharpe 0.46 |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | 35 | 80% | 47 | +1.8% | 44 | +7.7% | -29% | 0.48 | 0.52 | +5.3% | 0.35 | 90% | +5.8% / +3.1% | AVGO: +7.1%, Sharpe 0.46 |
| top8, in RS>=0.8, out RS<0.5, 12-1 month momentum | 18 | 90% | 34 | +3.1% | 97 | +5.8% | -40% | 0.37 | 0.41 | +0.9% | 0.15 | 30% | +5.0% / +3.7% | GE: +4.3%, Sharpe 0.31 |
| top8, in RS>=0.8, out RS<0.5, monthly | 12 | 94% | 49 | +9.5% | 146 | +13.0% | -26% | 0.64 | 0.59 | +15.7% | 0.72 | 95% | +12.3% / +12.9% | DVN: +12.8%, Sharpe 0.63 |
| top8, in RS>=0.8, out RS<0.5, volatility-adjusted | 16 | 93% | 54 | +6.5% | 115 | +11.7% | -23% | 0.69 | 0.65 | +13.9% | 0.90 | 100% | +10.9% / +9.7% | GE: +8.8%, Sharpe 0.55 |

## Rotation: pre-registered selection (2015 large caps, train+validation only)

Gates: train+val Sharpe > SPY's, ranking beats >= 90% of random selections, CAGR without the single best stock >= SPY's, max drawdown at most 10 points worse than SPY's.

**Chosen: none — no rule set passed every gate**

| rule set | passes | train+val Sharpe | failed gates |
|---|---|---|---|
| top5, in RS>=0.8, out RS<0.5 | ❌ | 0.60 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top5, in RS>=0.8, out RS<0.5, stop -20% | ❌ | 0.61 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d | ❌ | 0.60 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | ❌ | 0.60 | train_val_sharpe_beats_spy, ranking_beats_random, without_best_stock_beats_spy |
| top5, in RS>=0.8, out RS<0.7 | ❌ | 0.54 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top5, in RS>=0.8, out RS<0.7, stop -20% | ❌ | 0.63 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d | ❌ | 0.61 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | ❌ | 0.61 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5 | ❌ | 0.61 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5, stop -20% | ❌ | 0.56 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d | ❌ | 0.47 | train_val_sharpe_beats_spy, ranking_beats_random, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | ❌ | 0.47 | train_val_sharpe_beats_spy, ranking_beats_random, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.7 | ❌ | 0.60 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.7, stop -20% | ❌ | 0.59 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d | ❌ | 0.52 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | ❌ | 0.52 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5, 12-1 month momentum | ❌ | 0.41 | train_val_sharpe_beats_spy, ranking_beats_random, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5, monthly | ❌ | 0.59 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5, volatility-adjusted | ❌ | 0.65 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |

Calendar-year returns (2015 large caps, 20 bps per side):

| | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|---|---|---|---|
| SPY | -10% | +31% | +18% | +29% | -18% | +26% | +25% | +18% | +13% |
| equal-weight group | -11% | +29% | +14% | +31% | -4% | +16% | +16% | +17% | +16% |
| top5, in RS>=0.8, out RS<0.5 | -4% | +14% | +12% | +21% | +0% | +11% | +37% | +15% | +38% |
| top5, in RS>=0.8, out RS<0.5, stop -20% | -5% | +14% | +12% | +22% | -0% | +14% | +36% | +14% | +38% |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d | +0% | +3% | +16% | +21% | -1% | +21% | +19% | +9% | +10% |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | -1% | +3% | +16% | +22% | -1% | +21% | +19% | +9% | +10% |
| top5, in RS>=0.8, out RS<0.7 | -6% | +8% | +7% | +21% | -4% | +19% | +30% | -2% | +36% |
| top5, in RS>=0.8, out RS<0.7, stop -20% | -5% | +7% | +9% | +22% | +10% | +21% | +30% | -2% | +35% |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d | +1% | -3% | +8% | +21% | -2% | +22% | +29% | -5% | +16% |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | +1% | -3% | +8% | +21% | -2% | +22% | +29% | -5% | +16% |
| top8, in RS>=0.8, out RS<0.5 | -14% | +8% | +17% | +28% | +0% | +23% | +27% | +22% | +22% |
| top8, in RS>=0.8, out RS<0.5, stop -20% | -14% | +8% | +11% | +33% | +1% | +20% | +22% | +23% | +19% |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d | -6% | -5% | +11% | +30% | -2% | +14% | +13% | +14% | +4% |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | -7% | -4% | +11% | +30% | -2% | +14% | +13% | +14% | +4% |
| top8, in RS>=0.8, out RS<0.7 | -11% | +9% | +17% | +18% | +2% | +20% | +25% | +6% | +23% |
| top8, in RS>=0.8, out RS<0.7, stop -20% | -11% | +6% | +13% | +18% | +6% | +21% | +25% | +5% | +23% |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d | -4% | +2% | +12% | +18% | -4% | +9% | +24% | +2% | +12% |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | -4% | +2% | +12% | +18% | -4% | +9% | +24% | +1% | +12% |
| top8, in RS>=0.8, out RS<0.5, 12-1 month momentum | -14% | +13% | +3% | +24% | -12% | +2% | +41% | -1% | +5% |
| top8, in RS>=0.8, out RS<0.5, monthly | -3% | +12% | +16% | +19% | -5% | +26% | +23% | +5% | +26% |
| top8, in RS>=0.8, out RS<0.5, volatility-adjusted | -8% | +16% | +3% | +22% | -8% | +18% | +38% | +20% | +9% |

## Rockets (from 2016-11-07, 20 bps per side, 10 slots x 10%, max 3 new per day)

Rocket day: close >= +jump vs previous close, volume >= 3x the 20-day average, close in the top quarter of the day's range, price >= $5, 20-day dollar volume >= $5M. Buy next open; sell next open after a close more than `trail` below the highest close, or after 40 sessions. 'Random' = same stocks, same liquidity filter, same exit, random dates.

SPY: +15.6%/yr, max DD -34%, Sharpe 0.89 · train+val +15.7%/yr, Sharpe 0.89

| variant | trades | win% | avg trade | median | ≥+50% | worst | random avg | excess vs random t (train+val) | 2015 large caps excess | CAGR | max DD | Sharpe | train+val CAGR / Sharpe | OOS CAGR | random-entry portfolio CAGR | without top 3 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| EPS surprise>0%, reaction>=5% | 1890 | 54 | +4.6% | +2.0% | 4.3% | -51% | +4.3% | -0.34% (-0.52) | -0.26% (n=557) | +6.8% | -41% | 0.41 | +10.4% / 0.56 | -4.5% | +16.1% | +6.8% |
| EPS surprise>0%, reaction>=10% | 917 | 54 | +6.3% | +2.0% | 6.2% | -51% | +4.3% | +0.77% (0.76) | +1.65% (n=128) | +21.9% | -42% | 0.93 | +23.9% / 1.01 | +14.6% | +16.1% | +21.5% |
| EPS surprise>10%, reaction>=5% | 1262 | 53 | +5.0% | +2.1% | 5.1% | -51% | +4.3% | +0.62% (0.75) | -0.66% (n=266) | +12.7% | -44% | 0.62 | +20.5% / 0.92 | -18.8% | +16.1% | +10.9% |
| EPS surprise>10%, reaction>=10% | 710 | 53 | +6.7% | +2.6% | 6.6% | -51% | +4.3% | +1.66% (1.37) | +1.82% (n=70) | +17.5% | -45% | 0.76 | +26.3% / 1.05 | -16.1% | +16.1% | +15.5% |
| EPS surprise>20%, reaction>=10%, volume>=2x, RS>=0.8 | 235 | 57 | +8.8% | +3.9% | 7.2% | -34% | +4.3% | +3.29% (1.53) | +3.91% (n=14) | +17.8% | -27% | 0.92 | +25.1% / 1.27 | -9.0% | +16.1% | +11.8% |
| EPS surprise>20%, reaction>=15%, volume>=2x, RS>=0.8 | 167 | 58 | +9.1% | +4.0% | 8.4% | -33% | +4.3% | +1.46% (0.61) | —% (n=4) | +14.8% | -21% | 0.90 | +18.6% / 1.17 | -1.2% | +16.1% | +10.2% |
| jump>=8%, trail 15% | 1001 | 46 | +4.0% | -2.6% | 5.3% | -52% | +2.3% | +0.00% (0.00) | -1.48% (n=115) | +15.3% | -48% | 0.62 | +22.6% / 0.81 | -15.9% | +9.7% | +9.6% |
| jump>=8%, trail 25% | 1000 | 51 | +5.4% | +0.6% | 6.8% | -61% | +3.0% | +0.51% (0.45) | -1.45% (n=115) | +14.9% | -68% | 0.59 | +21.5% / 0.77 | -8.5% | +12.6% | +10.9% |
| jump>=15%, trail 15% | 542 | 43 | +4.8% | -4.5% | 6.8% | -52% | +2.3% | -0.22% (-0.16) | -4.51% (n=23) | +18.4% | -38% | 0.71 | +22.0% / 0.80 | +1.5% | +9.7% | +12.1% |
| jump>=15%, trail 25% | 541 | 47 | +6.7% | -1.9% | 9.2% | -61% | +3.0% | +1.14% (0.63) | -4.75% (n=23) | +14.9% | -60% | 0.58 | +20.2% / 0.71 | -9.4% | +12.6% | +6.6% |

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
| combined | all | +0.95 | -0.43 | +0.34 | +1.07 | +0.03 | -0.44 | +0.53 | +0.42 | +0.23 | -0.05 |
| combined | SPY>200d & stock>200d | +1.03 | -0.42 | +0.08 | +0.94 | -0.03 | -0.79 | +0.38 | +0.42 | +0.19 | -0.03 |
| combined | SPY>200d & stock>200d & RS>=0.8 | +1.10 | -0.27 | +0.47 | +1.45 | -0.41 | -0.36 | +0.35 | +0.60 | +0.83 | +0.11 |
| combined | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | +1.22 | -0.13 | +0.59 | +1.35 | -0.52 | -0.07 | +0.30 | +0.46 | +0.81 | +0.35 |
| combined | score>=70 & SPY>200d & stock>200d | +1.10 | +0.65 | +0.42 | +1.14 | -0.54 | -0.96 | +0.43 | +0.69 | +0.52 | +0.10 |
| combined | score>=70 & SPY>200d & stock>200d & RS>=0.8 | +0.65 | +1.33 | +0.61 | +1.08 | -0.53 | -1.15 | +0.41 | +1.00 | +0.70 | +0.14 |
| baseline_random | all | +1.05 | +0.07 | +0.55 | +0.98 | +0.15 | -0.28 | +0.61 | +0.42 | +0.30 | +0.16 |
| baseline_random | SPY>200d & stock>200d | +1.14 | -0.22 | +0.52 | +0.85 | +0.17 | -0.78 | +0.26 | +0.42 | +0.21 | +0.14 |
| baseline_random | SPY>200d & stock>200d & RS>=0.8 | +1.42 | +0.12 | +0.66 | +1.15 | -0.24 | -0.74 | +0.47 | +0.51 | +0.39 | +0.05 |
| baseline_random | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | +1.30 | +0.28 | +0.75 | +0.96 | -0.29 | -0.63 | +0.55 | +0.60 | +0.64 | +0.01 |