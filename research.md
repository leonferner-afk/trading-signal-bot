# Strategy research

278 symbols with data (1 failed), 10 years of daily bars. Control group: 105 stocks that were already large caps in 2015. Primary cost 20 bps per side (USD account: courtage + slippage; 40 bps ≈ trading from a SEK account). Validation from 2023-03-04, out-of-sample (OOS) from 2025-01-03. Setups invalidated at the next open (skipped): 1311.

Portfolio: max 8 positions, max 3 new per day, 1% risk per trade, max 25% of equity per position, no leverage, marked to market daily. 'vs random' = share of 40 random-order portfolios from the same eligible trades that this ranking beat.

## Portfolio — universe: all

SPY buy-and-hold: +14.4%/yr, max DD -34%, Sharpe 0.81 · train+val Sharpe 0.8 · OOS +13.7%/yr, Sharpe 0.84

| rule set | trades/yr | exposure | win% | avgR | CAGR | max DD | Sharpe | train+val Sharpe | OOS CAGR | OOS Sharpe | vs random |
|---|---|---|---|---|---|---|---|---|---|---|---|
| random picks (reference) | 80.4 | 84% | 20 | +0.14 | +7.7% | -54% | 0.40 | 0.74 | -21.9% | -0.63 | — |
| random picks, trend filter | 63.5 | 77% | 22 | +0.31 | +13.8% | -51% | 0.64 | 0.82 | -6.8% | -0.12 | — |
| RS leaders, trend filter | 73.6 | 66% | 23 | +0.40 | +21.4% | -42% | 0.75 | 0.93 | -4.3% | 0.06 | 100% |
| RS leaders near 52w high | 66.1 | 76% | 25 | +0.60 | +30.9% | -42% | 1.02 | 1.17 | +12.3% | 0.49 | 100% |
| signals score>=70, trend | 47.4 | 63% | 21 | +0.28 | +9.5% | -35% | 0.53 | 0.68 | -4.5% | -0.09 | 35% |
| signals score>=70, trend, RS top 20% | 41.7 | 50% | 22 | +0.48 | +17.9% | -33% | 0.85 | 0.96 | +4.2% | 0.30 | 78% |
| signals, trend, RS top 20% | 77.2 | 78% | 22 | +0.72 | +36.6% | -48% | 1.07 | 1.26 | +18.5% | 0.61 | 100% |
| signals, trend, RS top 20%, near 52w high | 73.9 | 79% | 22 | +0.56 | +31.1% | -32% | 1.05 | 1.25 | +17.9% | 0.62 | 100% |

Cost sensitivity (full-period CAGR / Sharpe):

| rule set | 20 bps | 40 bps | 70 bps |
|---|---|---|---|
| RS leaders, trend filter | +21.4% / 0.75 | +17.7% / 0.66 | +12.4% / 0.52 |
| RS leaders near 52w high | +30.9% / 1.02 | +26.5% / 0.91 | +19.7% / 0.73 |
| signals score>=70, trend | +9.5% / 0.53 | +6.6% / 0.40 | +2.7% / 0.23 |
| signals score>=70, trend, RS top 20% | +17.9% / 0.85 | +15.3% / 0.75 | +11.6% / 0.60 |
| signals, trend, RS top 20% | +36.6% / 1.07 | +31.2% / 0.95 | +24.4% / 0.80 |
| signals, trend, RS top 20%, near 52w high | +31.1% / 1.05 | +25.7% / 0.91 | +18.8% / 0.72 |

Exit variant (stop 2.5 x ATR instead of 1.5 x ATR / structural):

| rule set | CAGR | max DD | Sharpe | OOS Sharpe |
|---|---|---|---|---|
| random picks (reference) | +9.0% | -49% | 0.51 | -0.23 |
| random picks, trend filter | +7.0% | -46% | 0.45 | -0.09 |
| RS leaders, trend filter | +19.1% | -27% | 0.90 | 0.45 |
| RS leaders near 52w high | +23.5% | -24% | 1.04 | 0.27 |
| signals score>=70, trend | +11.2% | -28% | 0.71 | -0.24 |
| signals score>=70, trend, RS top 20% | +16.8% | -28% | 0.98 | 0.24 |
| signals, trend, RS top 20% | +18.6% | -36% | 0.88 | 0.42 |
| signals, trend, RS top 20%, near 52w high | +15.1% | -26% | 0.75 | 0.39 |

### Per trade — universe: all (one position per symbol, t over monthly means)

| group | exit | policy | n | win% | avgR | medR | t | excess vs random (t) | ≥+50% | OOS n | OOS avgR |
|---|---|---|---|---|---|---|---|---|---|---|---|
| breakout | fixed | all | 6539 | 17 | +0.269 | -1.11 | 1.11 | -0.337 (-4.06) | 3.2% | 1485 | -0.026 |
| breakout | fixed | SPY>200d & stock>200d | 5187 | 16 | +0.216 | -1.12 | 0.40 | -0.228 (-3.28) | 2.9% | 1201 | -0.032 |
| breakout | fixed | SPY>200d & stock>200d & RS>=0.8 | 2147 | 17 | +0.389 | -1.08 | 1.33 | -0.197 (-1.90) | 5.4% | 516 | +0.410 |
| breakout | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1752 | 18 | +0.425 | -1.08 | 1.26 | -0.108 (-0.91) | 4.3% | 395 | +0.592 |
| breakout | fixed | score>=70 & SPY>200d & stock>200d | 745 | 22 | +0.440 | -1.00 | 2.01 | -0.000 (-0.00) | 5.9% | 140 | +0.261 |
| breakout | fixed | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 455 | 23 | +0.557 | -0.98 | 2.50 | +0.069 (0.34) | 7.7% | 92 | +0.404 |
| momentum | fixed | all | 5421 | 22 | +0.254 | -1.04 | 1.76 | -0.306 (-4.11) | 3.6% | 1232 | +0.035 |
| momentum | fixed | SPY>200d & stock>200d | 4789 | 22 | +0.288 | -1.04 | 1.77 | -0.102 (-1.63) | 3.5% | 1115 | +0.055 |
| momentum | fixed | SPY>200d & stock>200d & RS>=0.8 | 1947 | 22 | +0.368 | -1.02 | 2.14 | -0.105 (-1.32) | 6.2% | 462 | +0.208 |
| momentum | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1607 | 23 | +0.378 | -1.04 | 2.11 | -0.036 (-0.42) | 4.5% | 369 | +0.195 |
| momentum | fixed | score>=70 & SPY>200d & stock>200d | 157 | 24 | +0.541 | -0.92 | 1.99 | +0.307 (1.14) | 12.7% | 38 | +0.918 |
| momentum | fixed | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 98 | 24 | +0.694 | -0.90 | 1.80 | +0.260 (0.71) | 15.3% | 27 | +0.911 |
| combined | fixed | all | 8230 | 19 | +0.261 | -1.08 | 1.49 | -0.319 (-4.59) | 3.3% | 1854 | +0.087 |
| combined | fixed | SPY>200d & stock>200d | 6782 | 19 | +0.225 | -1.08 | 0.78 | -0.187 (-3.18) | 3.1% | 1557 | +0.061 |
| combined | fixed | SPY>200d & stock>200d & RS>=0.8 | 2830 | 20 | +0.387 | -1.04 | 1.87 | -0.140 (-1.78) | 5.4% | 678 | +0.445 |
| combined | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 2330 | 21 | +0.395 | -1.05 | 1.84 | -0.058 (-0.69) | 4.3% | 524 | +0.536 |
| combined | fixed | score>=70 & SPY>200d & stock>200d | 822 | 23 | +0.463 | -0.98 | 1.77 | -0.011 (-0.08) | 6.6% | 163 | +0.305 |
| combined | fixed | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 502 | 23 | +0.564 | -0.96 | 2.15 | +0.012 (0.06) | 8.6% | 108 | +0.415 |
| baseline_random | fixed | all | 17866 | 24 | +0.349 | -1.02 | 4.89 | — (—) | 5.0% | 4067 | +0.235 |
| baseline_random | fixed | SPY>200d & stock>200d | 11303 | 23 | +0.321 | -1.04 | 2.98 | — (—) | 3.6% | 2584 | +0.151 |
| baseline_random | fixed | SPY>200d & stock>200d & RS>=0.8 | 4617 | 23 | +0.360 | -1.03 | 3.31 | — (—) | 6.2% | 1125 | +0.192 |
| baseline_random | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 3154 | 23 | +0.417 | -1.04 | 3.00 | — (—) | 4.0% | 694 | +0.284 |
| breakout | wide | all | 5256 | 33 | +0.295 | -0.95 | 3.12 | -0.168 (-3.03) | 5.5% | 1185 | +0.239 |
| breakout | wide | SPY>200d & stock>200d | 4226 | 33 | +0.303 | -0.96 | 2.20 | -0.071 (-1.45) | 5.0% | 965 | +0.250 |
| breakout | wide | SPY>200d & stock>200d & RS>=0.8 | 1794 | 34 | +0.417 | -0.93 | 2.50 | -0.104 (-1.67) | 9.0% | 431 | +0.341 |
| breakout | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1492 | 34 | +0.452 | -0.93 | 2.85 | -0.039 (-0.55) | 7.3% | 335 | +0.312 |
| breakout | wide | score>=70 & SPY>200d & stock>200d | 718 | 32 | +0.372 | -0.91 | 2.19 | -0.045 (-0.41) | 9.0% | 134 | +0.142 |
| breakout | wide | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 433 | 33 | +0.466 | -0.90 | 2.74 | +0.029 (0.19) | 11.6% | 88 | +0.216 |
| momentum | wide | all | 4506 | 32 | +0.264 | -0.98 | 2.76 | -0.183 (-3.16) | 4.8% | 1000 | +0.137 |
| momentum | wide | SPY>200d & stock>200d | 3996 | 33 | +0.305 | -0.98 | 2.84 | -0.024 (-0.47) | 4.7% | 909 | +0.162 |
| momentum | wide | SPY>200d & stock>200d & RS>=0.8 | 1644 | 33 | +0.344 | -0.96 | 2.34 | -0.116 (-1.97) | 7.9% | 389 | +0.223 |
| momentum | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1387 | 33 | +0.325 | -0.97 | 2.10 | -0.114 (-1.77) | 5.7% | 311 | +0.234 |
| momentum | wide | score>=70 & SPY>200d & stock>200d | 141 | 30 | +0.298 | -0.88 | 1.22 | -0.003 (-0.01) | 14.9% | 35 | +0.618 |
| momentum | wide | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 84 | 30 | +0.418 | -0.80 | 1.31 | -0.017 (-0.07) | 19.1% | 25 | +0.689 |
| combined | wide | all | 6265 | 33 | +0.280 | -0.97 | 3.09 | -0.179 (-3.50) | 5.1% | 1398 | +0.208 |
| combined | wide | SPY>200d & stock>200d | 5229 | 33 | +0.301 | -0.98 | 2.36 | -0.067 (-1.56) | 4.8% | 1193 | +0.211 |
| combined | wide | SPY>200d & stock>200d & RS>=0.8 | 2270 | 33 | +0.367 | -0.95 | 2.42 | -0.111 (-2.04) | 8.2% | 545 | +0.309 |
| combined | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1900 | 33 | +0.380 | -0.95 | 2.61 | -0.066 (-1.09) | 6.5% | 424 | +0.299 |
| combined | wide | score>=70 & SPY>200d & stock>200d | 779 | 32 | +0.363 | -0.91 | 1.74 | -0.077 (-0.75) | 9.1% | 153 | +0.216 |
| combined | wide | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 466 | 33 | +0.447 | -0.89 | 2.22 | -0.047 (-0.35) | 12.0% | 101 | +0.295 |
| baseline_random | wide | all | 12443 | 35 | +0.320 | -0.94 | 5.32 | — (—) | 6.3% | 2704 | +0.282 |
| baseline_random | wide | SPY>200d & stock>200d | 8123 | 34 | +0.315 | -0.97 | 3.45 | — (—) | 4.8% | 1846 | +0.178 |
| baseline_random | wide | SPY>200d & stock>200d & RS>=0.8 | 3423 | 33 | +0.347 | -0.97 | 3.80 | — (—) | 8.2% | 813 | +0.242 |
| baseline_random | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 2502 | 35 | +0.412 | -0.97 | 3.81 | — (—) | 5.8% | 540 | +0.355 |

## Portfolio — universe: largecap_2015

SPY buy-and-hold: +14.4%/yr, max DD -34%, Sharpe 0.81 · train+val Sharpe 0.8 · OOS +13.7%/yr, Sharpe 0.84

| rule set | trades/yr | exposure | win% | avgR | CAGR | max DD | Sharpe | train+val Sharpe | OOS CAGR | OOS Sharpe | vs random |
|---|---|---|---|---|---|---|---|---|---|---|---|
| random picks (reference) | 41.6 | 88% | 29 | +0.61 | +18.2% | -17% | 1.18 | 1.26 | +5.5% | 0.43 | — |
| random picks, trend filter | 33.8 | 77% | 26 | +0.42 | +9.9% | -24% | 0.79 | 1.04 | +2.1% | 0.21 | — |
| RS leaders, trend filter | 42.8 | 76% | 23 | +0.22 | +6.5% | -36% | 0.43 | 0.54 | -0.3% | 0.09 | 62% |
| RS leaders near 52w high | 41.1 | 76% | 22 | +0.19 | +3.1% | -29% | 0.26 | 0.29 | +1.7% | 0.18 | 28% |
| signals score>=70, trend | 15.0 | 36% | 23 | +0.25 | +2.5% | -16% | 0.30 | 0.28 | +3.0% | 0.34 | 30% |
| signals score>=70, trend, RS top 20% | 10.9 | 25% | 22 | +0.32 | +2.2% | -19% | 0.30 | 0.33 | +1.4% | 0.22 | 20% |
| signals, trend, RS top 20% | 41.3 | 78% | 21 | +0.31 | +6.0% | -30% | 0.44 | 0.49 | +3.2% | 0.27 | 50% |
| signals, trend, RS top 20%, near 52w high | 42.3 | 78% | 21 | +0.31 | +6.7% | -33% | 0.49 | 0.55 | +3.1% | 0.27 | 78% |

Cost sensitivity (full-period CAGR / Sharpe):

| rule set | 20 bps | 40 bps | 70 bps |
|---|---|---|---|
| RS leaders, trend filter | +6.5% / 0.43 | +3.5% / 0.28 | -0.8% / 0.06 |
| RS leaders near 52w high | +3.1% / 0.26 | +0.1% / 0.09 | -4.7% / -0.17 |
| signals score>=70, trend | +2.5% / 0.30 | +1.1% / 0.16 | -0.8% / -0.05 |
| signals score>=70, trend, RS top 20% | +2.2% / 0.30 | +1.1% / 0.17 | -0.4% / -0.01 |
| signals, trend, RS top 20% | +6.0% / 0.44 | +2.7% / 0.24 | -2.1% / -0.05 |
| signals, trend, RS top 20%, near 52w high | +6.7% / 0.49 | +3.4% / 0.29 | -1.5% / -0.02 |

Exit variant (stop 2.5 x ATR instead of 1.5 x ATR / structural):

| rule set | CAGR | max DD | Sharpe | OOS Sharpe |
|---|---|---|---|---|
| random picks (reference) | +10.1% | -20% | 0.72 | 0.54 |
| random picks, trend filter | +8.2% | -17% | 0.69 | -0.01 |
| RS leaders, trend filter | +10.5% | -25% | 0.67 | 0.10 |
| RS leaders near 52w high | +12.5% | -22% | 0.78 | 0.08 |
| signals score>=70, trend | +1.6% | -16% | 0.22 | 0.48 |
| signals score>=70, trend, RS top 20% | +2.8% | -17% | 0.40 | 0.41 |
| signals, trend, RS top 20% | +8.1% | -21% | 0.58 | 0.31 |
| signals, trend, RS top 20%, near 52w high | +7.4% | -27% | 0.55 | 0.40 |

### Per trade — universe: largecap_2015 (one position per symbol, t over monthly means)

| group | exit | policy | n | win% | avgR | medR | t | excess vs random (t) | ≥+50% | OOS n | OOS avgR |
|---|---|---|---|---|---|---|---|---|---|---|---|
| breakout | fixed | all | 2294 | 17 | +0.076 | -1.16 | -0.53 | -0.449 (-3.75) | 0.2% | 471 | -0.228 |
| breakout | fixed | SPY>200d & stock>200d | 1884 | 16 | -0.001 | -1.17 | -0.64 | -0.274 (-2.64) | 0.1% | 395 | -0.236 |
| breakout | fixed | SPY>200d & stock>200d & RS>=0.8 | 767 | 18 | +0.272 | -1.12 | 1.19 | +0.035 (0.16) | 0.1% | 165 | -0.007 |
| breakout | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 719 | 18 | +0.299 | -1.12 | 1.27 | +0.074 (0.34) | 0.1% | 160 | +0.110 |
| breakout | fixed | score>=70 & SPY>200d & stock>200d | 159 | 21 | +0.181 | -1.02 | 0.89 | -0.101 (-0.37) | 0.0% | 27 | +0.414 |
| breakout | fixed | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 105 | 21 | +0.206 | -1.01 | 1.01 | -0.081 (-0.23) | 0.0% | 15 | +0.442 |
| momentum | fixed | all | 2202 | 22 | +0.172 | -1.09 | 1.10 | -0.273 (-2.88) | 0.1% | 468 | +0.003 |
| momentum | fixed | SPY>200d & stock>200d | 1967 | 23 | +0.208 | -1.10 | 0.90 | -0.094 (-1.05) | 0.1% | 432 | +0.060 |
| momentum | fixed | SPY>200d & stock>200d & RS>=0.8 | 843 | 23 | +0.218 | -1.07 | 0.17 | -0.227 (-2.12) | 0.0% | 182 | +0.095 |
| momentum | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 800 | 22 | +0.205 | -1.08 | 0.03 | -0.222 (-2.04) | 0.0% | 176 | +0.137 |
| momentum | fixed | score>=70 & SPY>200d & stock>200d | 16 | 19 | +0.028 | -1.05 | 0.28 | -0.066 (-0.09) | 0.0% | 4 | -1.149 |
| momentum | fixed | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 9 | 22 | +0.681 | -0.91 | 0.62 | -0.195 (-0.18) | 0.0% | 3 | -1.108 |
| combined | fixed | all | 3111 | 20 | +0.118 | -1.12 | 0.13 | -0.364 (-3.83) | 0.2% | 636 | -0.107 |
| combined | fixed | SPY>200d & stock>200d | 2658 | 20 | +0.086 | -1.13 | -0.22 | -0.202 (-2.45) | 0.1% | 550 | -0.079 |
| combined | fixed | SPY>200d & stock>200d & RS>=0.8 | 1139 | 20 | +0.200 | -1.08 | 0.11 | -0.196 (-1.80) | 0.0% | 235 | -0.042 |
| combined | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1079 | 20 | +0.195 | -1.09 | 0.18 | -0.165 (-1.56) | 0.0% | 228 | +0.051 |
| combined | fixed | score>=70 & SPY>200d & stock>200d | 171 | 22 | +0.207 | -1.02 | 1.05 | -0.084 (-0.32) | 0.0% | 31 | +0.212 |
| combined | fixed | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 112 | 21 | +0.283 | -1.00 | 1.27 | -0.015 (-0.04) | 0.0% | 18 | +0.183 |
| baseline_random | fixed | all | 7316 | 25 | +0.317 | -1.05 | 4.33 | — (—) | 0.7% | 1457 | +0.309 |
| baseline_random | fixed | SPY>200d & stock>200d | 4793 | 23 | +0.255 | -1.08 | 2.43 | — (—) | 0.3% | 977 | +0.179 |
| baseline_random | fixed | SPY>200d & stock>200d & RS>=0.8 | 1931 | 23 | +0.287 | -1.07 | 2.23 | — (—) | 0.4% | 427 | +0.120 |
| baseline_random | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1718 | 23 | +0.285 | -1.07 | 2.05 | — (—) | 0.2% | 368 | +0.183 |
| breakout | wide | all | 1956 | 33 | +0.182 | -0.99 | 1.44 | -0.250 (-3.36) | 0.3% | 394 | +0.127 |
| breakout | wide | SPY>200d & stock>200d | 1608 | 33 | +0.198 | -1.00 | 1.45 | -0.059 (-0.85) | 0.2% | 332 | +0.169 |
| breakout | wide | SPY>200d & stock>200d & RS>=0.8 | 679 | 33 | +0.256 | -0.97 | 1.19 | -0.132 (-1.54) | 0.0% | 142 | +0.082 |
| breakout | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 641 | 33 | +0.262 | -0.96 | 1.32 | -0.087 (-1.01) | 0.0% | 137 | +0.133 |
| breakout | wide | score>=70 & SPY>200d & stock>200d | 159 | 31 | +0.173 | -0.92 | 0.70 | -0.118 (-0.61) | 0.0% | 27 | +0.403 |
| breakout | wide | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 105 | 31 | +0.300 | -0.92 | 1.17 | -0.121 (-0.50) | 0.0% | 15 | +0.549 |
| momentum | wide | all | 1869 | 33 | +0.194 | -1.02 | 1.97 | -0.199 (-2.67) | 0.1% | 388 | +0.107 |
| momentum | wide | SPY>200d & stock>200d | 1668 | 33 | +0.240 | -1.02 | 2.12 | +0.010 (0.15) | 0.1% | 360 | +0.147 |
| momentum | wide | SPY>200d & stock>200d & RS>=0.8 | 727 | 34 | +0.258 | -0.99 | 1.34 | -0.118 (-1.57) | 0.0% | 159 | +0.011 |
| momentum | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 690 | 34 | +0.267 | -0.99 | 1.54 | -0.067 (-0.84) | 0.0% | 155 | +0.043 |
| momentum | wide | score>=70 & SPY>200d & stock>200d | 15 | 27 | -0.013 | -0.94 | 0.29 | +0.017 (0.04) | 0.0% | 4 | -0.879 |
| momentum | wide | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 8 | 38 | +0.682 | -0.58 | 0.87 | -0.062 (-0.10) | 0.0% | 3 | -0.789 |
| combined | wide | all | 2465 | 33 | +0.181 | -1.01 | 1.70 | -0.233 (-3.39) | 0.3% | 494 | +0.134 |
| combined | wide | SPY>200d & stock>200d | 2117 | 33 | +0.199 | -1.02 | 1.71 | -0.041 (-0.72) | 0.1% | 436 | +0.169 |
| combined | wide | SPY>200d & stock>200d & RS>=0.8 | 928 | 34 | +0.269 | -0.98 | 1.48 | -0.098 (-1.52) | 0.0% | 193 | +0.028 |
| combined | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 881 | 34 | +0.274 | -0.99 | 1.57 | -0.053 (-0.85) | 0.0% | 188 | +0.067 |
| combined | wide | score>=70 & SPY>200d & stock>200d | 170 | 31 | +0.177 | -0.92 | 0.91 | -0.094 (-0.50) | 0.0% | 31 | +0.237 |
| combined | wide | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 111 | 32 | +0.336 | -0.92 | 1.35 | -0.095 (-0.41) | 0.0% | 18 | +0.326 |
| baseline_random | wide | all | 5186 | 37 | +0.314 | -0.94 | 5.15 | — (—) | 0.8% | 977 | +0.354 |
| baseline_random | wide | SPY>200d & stock>200d | 3494 | 35 | +0.264 | -0.99 | 2.95 | — (—) | 0.2% | 718 | +0.235 |
| baseline_random | wide | SPY>200d & stock>200d & RS>=0.8 | 1484 | 35 | +0.297 | -0.98 | 2.84 | — (—) | 0.4% | 318 | +0.169 |
| baseline_random | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1333 | 35 | +0.303 | -0.99 | 2.69 | — (—) | 0.3% | 275 | +0.221 |

## Momentum rotation — universe: all (from 2018-02-15, 20 bps per side)

| benchmark | CAGR | max DD | Sharpe | train+val Sharpe | OOS CAGR | OOS Sharpe |
|---|---|---|---|---|---|---|
| SPY buy-and-hold | +13.8% | -34% | 0.78 | 0.75 | +13.7% | 0.84 |
| equal-weight universe (no costs) | +25.3% | -42% | 0.99 | 0.99 | +21.5% | 0.90 |

| rule set | trades/yr | exposure | win% | avg trade | avg days | CAGR | max DD | Sharpe | train+val Sharpe | OOS CAGR | OOS Sharpe | vs random | CAGR @40 / @70 bps | without best stock |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| top5, in RS>=0.8, out RS<0.5 | 11 | 93% | 38 | +17.6% | 109 | +14.9% | -79% | 0.53 | 0.45 | +32.7% | 0.75 | 20% | +14.1% / +12.8% | SE: +20.3%, Sharpe 0.60 |
| top5, in RS>=0.8, out RS<0.5, stop -20% | 16 | 91% | 31 | +16.8% | 72 | +19.4% | -77% | 0.59 | 0.61 | +9.9% | 0.48 | 55% | +18.1% / +16.2% | SE: +22.7%, Sharpe 0.64 |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d | 21 | 81% | 37 | +5.5% | 48 | +7.9% | -74% | 0.41 | 0.61 | -28.8% | -0.24 | 10% | +6.2% / +3.7% | MARA: +5.0%, Sharpe 0.35 |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | 26 | 80% | 34 | +3.6% | 39 | +7.1% | -71% | 0.39 | 0.50 | -15.2% | 0.03 | 15% | +5.1% / +2.3% | CELH: +12.7%, Sharpe 0.49 |
| top5, in RS>=0.8, out RS<0.7 | 13 | 93% | 44 | +12.0% | 93 | +14.3% | -76% | 0.52 | 0.53 | +13.8% | 0.55 | 20% | +13.3% / +11.8% | ENPH: +15.2%, Sharpe 0.53 |
| top5, in RS>=0.8, out RS<0.7, stop -20% | 18 | 92% | 35 | +10.1% | 64 | +18.3% | -77% | 0.58 | 0.50 | +39.2% | 0.82 | 60% | +16.9% / +14.7% | VKTX: +11.5%, Sharpe 0.48 |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d | 22 | 80% | 39 | +3.2% | 45 | +5.1% | -77% | 0.36 | 0.52 | -23.8% | -0.07 | 5% | +3.3% / +0.7% | TSLA: +10.6%, Sharpe 0.46 |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | 27 | 80% | 34 | +3.5% | 37 | +7.1% | -68% | 0.39 | 0.50 | -13.7% | 0.09 | 20% | +5.0% / +2.0% | CELH: +3.0%, Sharpe 0.32 |
| top8, in RS>=0.8, out RS<0.5 | 17 | 92% | 42 | +21.9% | 108 | +28.4% | -70% | 0.74 | 0.81 | +15.6% | 0.55 | 60% | +27.4% / +26.1% | SE: +26.4%, Sharpe 0.71 |
| top8, in RS>=0.8, out RS<0.5, stop -20% | 24 | 92% | 35 | +14.7% | 73 | +25.2% | -62% | 0.69 | 0.76 | +10.0% | 0.48 | 70% | +23.9% / +22.0% | SE: +20.2%, Sharpe 0.61 |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d | 30 | 80% | 39 | +9.2% | 53 | +25.1% | -58% | 0.70 | 0.78 | +9.6% | 0.45 | 80% | +23.4% / +20.9% | APP: +18.4%, Sharpe 0.59 |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | 37 | 80% | 35 | +7.0% | 42 | +21.8% | -67% | 0.65 | 0.71 | +9.4% | 0.45 | 70% | +19.9% / +17.1% | NIO: +23.0%, Sharpe 0.66 |
| top8, in RS>=0.8, out RS<0.7 | 19 | 92% | 48 | +18.7% | 94 | +31.2% | -57% | 0.76 | 0.84 | +16.5% | 0.57 | 75% | +30.1% / +30.6% | MARA: +23.7%, Sharpe 0.67 |
| top8, in RS>=0.8, out RS<0.7, stop -20% | 28 | 91% | 33 | +15.7% | 63 | +24.4% | -71% | 0.66 | 0.70 | +15.2% | 0.55 | 55% | +22.9% / +20.8% | MARA: +19.1%, Sharpe 0.59 |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d | 33 | 80% | 41 | +7.6% | 49 | +18.2% | -54% | 0.58 | 0.71 | -4.9% | 0.22 | 40% | +16.4% / +13.8% | MARA: +16.2%, Sharpe 0.55 |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | 41 | 80% | 34 | +9.6% | 39 | +23.9% | -63% | 0.66 | 0.78 | -3.6% | 0.24 | 80% | +21.7% / +18.4% | MARA: +21.7%, Sharpe 0.63 |
| top8, in RS>=0.8, out RS<0.5, 12-1 month momentum | 19 | 91% | 33 | +19.1% | 97 | +18.7% | -63% | 0.59 | 0.60 | +18.6% | 0.59 | 55% | +17.8% / +16.3% | SE: +16.6%, Sharpe 0.56 |
| top8, in RS>=0.8, out RS<0.5, monthly | 12 | 94% | 42 | +48.8% | 152 | +32.5% | -64% | 0.80 | 0.78 | +40.2% | 0.84 | 70% | +31.9% / +30.9% | ENPH: +32.0%, Sharpe 0.80 |
| top8, in RS>=0.8, out RS<0.5, volatility-adjusted | 15 | 93% | 46 | +25.1% | 124 | +30.8% | -47% | 0.85 | 0.94 | +26.0% | 0.69 | 95% | +29.9% / +28.6% | RKLB: +25.6%, Sharpe 0.76 |
| top8, in RS>=0.8, out RS<0.5, max 2/sector | 17 | 91% | 42 | +29.8% | 108 | +36.2% | -65% | 0.81 | 0.82 | +29.7% | 0.73 | 80% | +35.2% / +33.7% | GME: +33.5%, Sharpe 0.82 |
| top8, in RS>=0.8, out RS<0.5, max 3/sector | 16 | 94% | 44 | +25.3% | 110 | +32.0% | -58% | 0.79 | 0.86 | +20.5% | 0.61 | 80% | +31.1% / +29.8% | SE: +27.6%, Sharpe 0.72 |
| top8, in RS>=0.8, out RS<0.5, sell below 50d | 61 | 87% | 36 | +10.0% | 28 | +45.6% | -60% | 0.96 | 1.24 | -14.7% | 0.04 | 100% | +41.6% / +35.9% | MARA: +34.8%, Sharpe 0.84 |
| top8, in RS>=0.8, out RS<0.5, sell below 50d after +30% over 200d | 58 | 88% | 38 | +10.5% | 30 | +31.3% | -59% | 0.80 | 1.03 | -11.7% | 0.09 | 100% | +27.7% / +22.6% | MARA: +32.6%, Sharpe 0.82 |

## Momentum rotation — universe: largecap_2015 (from 2018-02-15, 20 bps per side)

| benchmark | CAGR | max DD | Sharpe | train+val Sharpe | OOS CAGR | OOS Sharpe |
|---|---|---|---|---|---|---|
| SPY buy-and-hold | +13.8% | -34% | 0.78 | 0.75 | +13.7% | 0.84 |
| equal-weight universe (no costs) | +14.2% | -37% | 0.81 | 0.73 | +17.9% | 1.26 |

| rule set | trades/yr | exposure | win% | avg trade | avg days | CAGR | max DD | Sharpe | train+val Sharpe | OOS CAGR | OOS Sharpe | vs random | CAGR @40 / @70 bps | without best stock |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| top5, in RS>=0.8, out RS<0.5 | 10 | 95% | 48 | +8.9% | 116 | +15.0% | -36% | 0.67 | 0.59 | +26.3% | 0.92 | 95% | +14.1% / +12.8% | DVN: +12.6%, Sharpe 0.61 |
| top5, in RS>=0.8, out RS<0.5, stop -20% | 10 | 94% | 52 | +8.9% | 112 | +15.4% | -36% | 0.69 | 0.62 | +26.1% | 0.91 | 90% | +14.5% / +13.2% | DVN: +13.0%, Sharpe 0.62 |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d | 20 | 81% | 48 | +3.2% | 50 | +11.0% | -26% | 0.58 | 0.64 | +7.4% | 0.40 | 100% | +9.2% / +6.7% | AVGO: +11.2%, Sharpe 0.61 |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | 20 | 81% | 48 | +3.2% | 50 | +11.0% | -26% | 0.58 | 0.64 | +7.5% | 0.40 | 100% | +9.2% / +6.7% | AVGO: +11.2%, Sharpe 0.61 |
| top5, in RS>=0.8, out RS<0.7 | 14 | 94% | 48 | +5.0% | 84 | +11.7% | -36% | 0.55 | 0.55 | +13.8% | 0.56 | 100% | +10.5% / +8.8% | INTC: +9.8%, Sharpe 0.51 |
| top5, in RS>=0.8, out RS<0.7, stop -20% | 14 | 95% | 48 | +5.5% | 82 | +13.7% | -33% | 0.61 | 0.63 | +13.5% | 0.56 | 100% | +12.5% / +10.7% | INTC: +12.2%, Sharpe 0.60 |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d | 23 | 81% | 46 | +2.5% | 45 | +9.2% | -30% | 0.51 | 0.62 | +1.8% | 0.20 | 95% | +7.2% / +4.4% | AVGO: +8.0%, Sharpe 0.47 |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | 23 | 81% | 46 | +2.4% | 44 | +9.0% | -30% | 0.50 | 0.61 | +1.6% | 0.19 | 100% | +7.1% / +4.2% | AVGO: +8.0%, Sharpe 0.46 |
| top8, in RS>=0.8, out RS<0.5 | 17 | 94% | 45 | +7.9% | 109 | +14.6% | -29% | 0.71 | 0.65 | +21.6% | 0.93 | 100% | +13.7% / +12.4% | DVN: +12.6%, Sharpe 0.65 |
| top8, in RS>=0.8, out RS<0.5, stop -20% | 18 | 93% | 45 | +6.7% | 104 | +13.3% | -29% | 0.67 | 0.61 | +19.7% | 0.87 | 100% | +12.4% / +11.1% | DVN: +11.1%, Sharpe 0.59 |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d | 31 | 80% | 44 | +2.5% | 52 | +8.1% | -28% | 0.51 | 0.52 | +7.6% | 0.46 | 65% | +6.5% / +4.1% | DVN: +7.7%, Sharpe 0.49 |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | 31 | 80% | 44 | +2.5% | 51 | +8.1% | -28% | 0.50 | 0.52 | +7.5% | 0.46 | 55% | +6.5% / +4.1% | DVN: +7.6%, Sharpe 0.49 |
| top8, in RS>=0.8, out RS<0.7 | 23 | 93% | 48 | +4.5% | 82 | +12.0% | -26% | 0.62 | 0.61 | +13.2% | 0.65 | 100% | +10.8% / +9.0% | META: +9.1%, Sharpe 0.51 |
| top8, in RS>=0.8, out RS<0.7, stop -20% | 23 | 93% | 47 | +4.5% | 80 | +11.7% | -29% | 0.61 | 0.60 | +12.6% | 0.63 | 95% | +10.4% / +8.6% | AVGO: +9.3%, Sharpe 0.52 |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d | 35 | 80% | 47 | +1.9% | 45 | +7.8% | -29% | 0.50 | 0.54 | +5.0% | 0.34 | 95% | +6.0% / +3.3% | AVGO: +7.2%, Sharpe 0.47 |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | 36 | 80% | 47 | +1.9% | 45 | +7.8% | -29% | 0.49 | 0.53 | +4.9% | 0.34 | 100% | +5.9% / +3.2% | AVGO: +7.2%, Sharpe 0.47 |
| top8, in RS>=0.8, out RS<0.5, 12-1 month momentum | 19 | 90% | 34 | +3.1% | 95 | +4.4% | -40% | 0.31 | 0.39 | -1.9% | 0.02 | 25% | +3.5% / +2.2% | GE: +2.9%, Sharpe 0.24 |
| top8, in RS>=0.8, out RS<0.5, monthly | 13 | 93% | 50 | +9.8% | 144 | +12.2% | -27% | 0.61 | 0.64 | +10.1% | 0.51 | 100% | +13.0% / +11.9% | DVN: +12.0%, Sharpe 0.60 |
| top8, in RS>=0.8, out RS<0.5, volatility-adjusted | 16 | 93% | 56 | +6.9% | 116 | +12.8% | -23% | 0.74 | 0.72 | +13.4% | 0.86 | 100% | +12.0% / +10.7% | GE: +10.0%, Sharpe 0.61 |
| top8, in RS>=0.8, out RS<0.5, max 2/sector | 18 | 93% | 44 | +6.2% | 104 | +11.1% | -30% | 0.58 | 0.52 | +18.5% | 0.80 | 90% | +10.2% / +8.8% | DVN: +9.7%, Sharpe 0.54 |
| top8, in RS>=0.8, out RS<0.5, max 3/sector | 18 | 94% | 44 | +7.1% | 106 | +13.3% | -28% | 0.67 | 0.61 | +19.9% | 0.86 | 95% | +12.4% / +11.1% | DVN: +11.5%, Sharpe 0.60 |
| top8, in RS>=0.8, out RS<0.5, sell below 50d | 63 | 87% | 36 | +0.9% | 28 | +6.1% | -25% | 0.41 | 0.56 | -4.3% | -0.13 | 50% | +3.0% / -1.5% | DVN: +4.7%, Sharpe 0.34 |
| top8, in RS>=0.8, out RS<0.5, sell below 50d after +30% over 200d | 33 | 90% | 45 | +2.7% | 54 | +9.9% | -25% | 0.59 | 0.66 | +3.7% | 0.29 | 80% | +8.1% / +5.5% | AVGO: +9.4%, Sharpe 0.57 |

## Rotation: pre-registered selection (2015 large caps, train+validation only)

Gates: train+val Sharpe > SPY's, ranking beats >= 90% of random selections, CAGR without the single best stock >= SPY's, max drawdown at most 10 points worse than SPY's.

**Chosen: none — no rule set passed every gate**

| rule set | passes | train+val Sharpe | failed gates |
|---|---|---|---|
| top5, in RS>=0.8, out RS<0.5 | ❌ | 0.59 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top5, in RS>=0.8, out RS<0.5, stop -20% | ❌ | 0.62 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d | ❌ | 0.64 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | ❌ | 0.64 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top5, in RS>=0.8, out RS<0.7 | ❌ | 0.55 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top5, in RS>=0.8, out RS<0.7, stop -20% | ❌ | 0.63 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d | ❌ | 0.62 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | ❌ | 0.61 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5 | ❌ | 0.65 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5, stop -20% | ❌ | 0.61 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d | ❌ | 0.52 | train_val_sharpe_beats_spy, ranking_beats_random, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | ❌ | 0.52 | train_val_sharpe_beats_spy, ranking_beats_random, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.7 | ❌ | 0.61 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.7, stop -20% | ❌ | 0.60 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d | ❌ | 0.54 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | ❌ | 0.53 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5, 12-1 month momentum | ❌ | 0.39 | train_val_sharpe_beats_spy, ranking_beats_random, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5, monthly | ❌ | 0.64 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5, volatility-adjusted | ❌ | 0.72 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5, max 2/sector | ❌ | 0.52 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5, max 3/sector | ❌ | 0.61 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5, sell below 50d | ❌ | 0.56 | train_val_sharpe_beats_spy, ranking_beats_random, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5, sell below 50d after +30% over 200d | ❌ | 0.66 | train_val_sharpe_beats_spy, ranking_beats_random, without_best_stock_beats_spy |

Calendar-year returns (2015 large caps, 20 bps per side):

| | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|---|---|---|---|
| SPY | -7% | +31% | +18% | +29% | -18% | +26% | +25% | +18% | +9% |
| equal-weight group | -7% | +29% | +14% | +31% | -4% | +16% | +16% | +17% | +17% |
| top5, in RS>=0.8, out RS<0.5 | -1% | +7% | +13% | +21% | +0% | +11% | +37% | +15% | +34% |
| top5, in RS>=0.8, out RS<0.5, stop -20% | -1% | +8% | +14% | +22% | -0% | +14% | +36% | +14% | +34% |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d | +6% | +3% | +16% | +21% | -1% | +21% | +19% | +9% | +5% |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | +5% | +3% | +16% | +22% | -1% | +21% | +19% | +9% | +5% |
| top5, in RS>=0.8, out RS<0.7 | -2% | +8% | +7% | +21% | -4% | +19% | +30% | -2% | +31% |
| top5, in RS>=0.8, out RS<0.7, stop -20% | -3% | +7% | +9% | +22% | +10% | +21% | +30% | -2% | +31% |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d | +3% | -3% | +8% | +21% | -2% | +22% | +29% | -5% | +10% |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | +3% | -3% | +8% | +21% | -2% | +22% | +29% | -5% | +10% |
| top8, in RS>=0.8, out RS<0.5 | -9% | +8% | +17% | +28% | +0% | +23% | +27% | +22% | +17% |
| top8, in RS>=0.8, out RS<0.5, stop -20% | -10% | +8% | +11% | +33% | +1% | +20% | +22% | +23% | +14% |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d | -1% | -5% | +11% | +30% | -2% | +14% | +13% | +14% | +1% |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | -1% | -4% | +11% | +30% | -2% | +14% | +13% | +14% | +0% |
| top8, in RS>=0.8, out RS<0.7 | -8% | +9% | +17% | +18% | +2% | +20% | +25% | +6% | +20% |
| top8, in RS>=0.8, out RS<0.7, stop -20% | -8% | +6% | +13% | +18% | +6% | +21% | +25% | +5% | +19% |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d | +0% | +2% | +12% | +18% | -4% | +9% | +24% | +2% | +9% |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | -0% | +2% | +12% | +18% | -4% | +9% | +24% | +1% | +9% |
| top8, in RS>=0.8, out RS<0.5, 12-1 month momentum | -15% | +10% | +2% | +24% | -12% | +2% | +41% | -1% | -2% |
| top8, in RS>=0.8, out RS<0.5, monthly | -0% | +12% | +16% | +19% | -5% | +26% | +23% | +5% | +14% |
| top8, in RS>=0.8, out RS<0.5, volatility-adjusted | +2% | +16% | +3% | +22% | -8% | +18% | +38% | +20% | +6% |
| top8, in RS>=0.8, out RS<0.5, max 2/sector | -10% | +8% | +4% | +29% | -0% | +19% | +17% | +10% | +25% |
| top8, in RS>=0.8, out RS<0.5, max 3/sector | -8% | +8% | +10% | +29% | -1% | +24% | +22% | +18% | +20% |
| top8, in RS>=0.8, out RS<0.5, sell below 50d | -3% | +3% | +28% | +21% | +6% | +7% | +4% | +2% | -9% |
| top8, in RS>=0.8, out RS<0.5, sell below 50d after +30% over 200d | -2% | +10% | +26% | +13% | +6% | +22% | +7% | +6% | +1% |

## Rockets (from 2016-11-29, 20 bps per side, 10 slots x 10%, max 3 new per day)

Rocket day: close >= +jump vs previous close, volume >= 3x the 20-day average, close in the top quarter of the day's range, price >= $5, 20-day dollar volume >= $5M. Buy next open; sell next open after a close more than `trail` below the highest close, or after 40 sessions. 'Random' = same stocks, same liquidity filter, same exit, random dates.

SPY: +14.7%/yr, max DD -34%, Sharpe 0.85 · train+val +14.8%/yr, Sharpe 0.85

| variant | trades | win% | avg trade | median | ≥+50% | worst | random avg | excess vs random t (train+val) | 2015 large caps excess | CAGR | max DD | Sharpe | train+val CAGR / Sharpe | OOS CAGR | random-entry portfolio CAGR | without top 3 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| EPS surprise>0%, reaction>=5% | 1916 | 53 | +4.5% | +1.9% | 4.3% | -51% | +4.2% | -0.33% (-0.50) | -0.03% (n=564) | +7.3% | -40% | 0.44 | +9.8% / 0.55 | -3.8% | +15.9% | +7.3% |
| EPS surprise>0%, reaction>=10% | 933 | 53 | +6.0% | +1.5% | 6.2% | -51% | +4.2% | +0.82% (0.81) | +1.55% (n=130) | +22.9% | -43% | 0.96 | +23.6% / 0.99 | +13.6% | +15.9% | +21.9% |
| EPS surprise>10%, reaction>=5% | 1273 | 53 | +4.9% | +2.0% | 5.0% | -51% | +4.2% | +0.62% (0.75) | -0.39% (n=270) | +13.6% | -45% | 0.66 | +21.8% / 0.96 | -16.1% | +15.9% | +14.3% |
| EPS surprise>10%, reaction>=10% | 719 | 52 | +6.3% | +1.5% | 6.3% | -51% | +4.2% | +1.73% (1.41) | +1.92% (n=72) | +17.5% | -48% | 0.76 | +25.2% / 1.00 | -14.3% | +15.9% | +14.3% |
| EPS surprise>20%, reaction>=10%, volume>=2x, RS>=0.8 | 246 | 55 | +8.3% | +2.8% | 6.9% | -36% | +4.2% | +3.55% (1.64) | +3.91% (n=14) | +17.6% | -27% | 0.90 | +23.9% / 1.20 | -9.7% | +15.9% | +11.6% |
| EPS surprise>20%, reaction>=15%, volume>=2x, RS>=0.8 | 176 | 56 | +8.2% | +2.7% | 8.0% | -36% | +4.2% | +1.85% (0.78) | —% (n=4) | +14.4% | -24% | 0.86 | +18.8% / 1.15 | -6.2% | +15.9% | +9.2% |
| jump>=8%, trail 15% | 1000 | 45 | +4.0% | -2.6% | 5.3% | -52% | +2.2% | -0.13% (-0.12) | -1.47% (n=115) | +15.1% | -48% | 0.61 | +23.1% / 0.82 | -14.8% | +11.8% | +9.4% |
| jump>=8%, trail 25% | 998 | 51 | +5.4% | +0.6% | 6.8% | -61% | +2.9% | +0.45% (0.39) | -1.38% (n=115) | +14.9% | -68% | 0.59 | +21.5% / 0.76 | -9.4% | +13.2% | +10.9% |
| jump>=15%, trail 15% | 544 | 43 | +4.7% | -4.5% | 6.8% | -52% | +2.2% | -0.47% (-0.33) | -4.26% (n=24) | +18.1% | -38% | 0.70 | +21.6% / 0.79 | +3.4% | +11.8% | +11.8% |
| jump>=15%, trail 25% | 544 | 47 | +6.6% | -2.2% | 9.2% | -61% | +2.9% | +0.94% (0.52) | -4.50% (n=24) | +14.5% | -60% | 0.57 | +20.9% / 0.73 | -8.0% | +13.2% | +6.1% |

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
| combined | all | +0.91 | -0.44 | +0.29 | +1.07 | +0.02 | -0.44 | +0.53 | +0.42 | +0.23 | -0.09 |
| combined | SPY>200d & stock>200d | +0.99 | -0.43 | +0.03 | +0.94 | -0.04 | -0.79 | +0.37 | +0.42 | +0.19 | -0.09 |
| combined | SPY>200d & stock>200d & RS>=0.8 | +1.12 | -0.26 | +0.35 | +1.46 | -0.42 | -0.36 | +0.35 | +0.60 | +0.83 | +0.01 |
| combined | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | +1.21 | -0.12 | +0.45 | +1.36 | -0.52 | -0.07 | +0.30 | +0.46 | +0.81 | +0.24 |
| combined | score>=70 & SPY>200d & stock>200d | +0.54 | +0.65 | +0.42 | +1.15 | -0.54 | -0.96 | +0.43 | +0.69 | +0.52 | -0.04 |
| combined | score>=70 & SPY>200d & stock>200d & RS>=0.8 | +0.17 | +1.33 | +0.61 | +1.08 | -0.53 | -1.15 | +0.41 | +1.00 | +0.70 | -0.06 |
| baseline_random | all | +1.49 | +0.04 | +0.55 | +0.98 | +0.15 | -0.28 | +0.61 | +0.42 | +0.30 | +0.15 |
| baseline_random | SPY>200d & stock>200d | +1.62 | -0.27 | +0.52 | +0.86 | +0.16 | -0.78 | +0.27 | +0.42 | +0.21 | +0.08 |
| baseline_random | SPY>200d & stock>200d & RS>=0.8 | +1.33 | +0.11 | +0.65 | +1.17 | -0.25 | -0.74 | +0.47 | +0.51 | +0.41 | -0.06 |
| baseline_random | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | +1.26 | +0.27 | +0.73 | +0.94 | -0.29 | -0.63 | +0.55 | +0.60 | +0.65 | -0.09 |