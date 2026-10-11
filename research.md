# Strategy research

278 symbols with data (1 failed), 10 years of daily bars. Control group: 105 stocks that were already large caps in 2015. Primary cost 20 bps per side (USD account: courtage + slippage; 40 bps ≈ trading from a SEK account). Validation from 2023-02-04, out-of-sample (OOS) from 2024-12-06. Setups invalidated at the next open (skipped): 1307.

Portfolio: max 8 positions, max 3 new per day, 1% risk per trade, max 25% of equity per position, no leverage, marked to market daily. 'vs random' = share of 40 random-order portfolios from the same eligible trades that this ranking beat.

## Portfolio — universe: all

SPY buy-and-hold: +15.1%/yr, max DD -34%, Sharpe 0.85 · train+val Sharpe 0.83 · OOS +15.9%/yr, Sharpe 0.96

| rule set | trades/yr | exposure | win% | avgR | CAGR | max DD | Sharpe | train+val Sharpe | OOS CAGR | OOS Sharpe | vs random |
|---|---|---|---|---|---|---|---|---|---|---|---|
| random picks (reference) | 77.5 | 86% | 21 | +0.21 | +7.5% | -66% | 0.40 | 0.58 | -22.9% | -0.65 | — |
| random picks, trend filter | 68.9 | 77% | 22 | +0.33 | +16.9% | -44% | 0.73 | 0.91 | -4.1% | 0.04 | — |
| RS leaders, trend filter | 74.2 | 66% | 23 | +0.39 | +21.2% | -42% | 0.76 | 0.84 | +8.7% | 0.39 | 95% |
| RS leaders near 52w high | 65.7 | 76% | 26 | +0.71 | +36.4% | -34% | 1.16 | 1.24 | +25.3% | 0.76 | 100% |
| signals score>=70, trend | 45.9 | 63% | 22 | +0.34 | +12.1% | -35% | 0.65 | 0.78 | +2.5% | 0.22 | 25% |
| signals score>=70, trend, RS top 20% | 41.0 | 51% | 23 | +0.55 | +19.9% | -33% | 0.93 | 1.07 | +13.1% | 0.63 | 65% |
| signals, trend, RS top 20% | 78.5 | 78% | 21 | +0.66 | +36.4% | -48% | 1.08 | 1.14 | +21.9% | 0.67 | 97% |
| signals, trend, RS top 20%, near 52w high | 75.7 | 78% | 22 | +0.53 | +28.1% | -32% | 0.99 | 1.09 | +29.3% | 0.86 | 100% |

Cost sensitivity (full-period CAGR / Sharpe):

| rule set | 20 bps | 40 bps | 70 bps |
|---|---|---|---|
| RS leaders, trend filter | +21.2% / 0.76 | +17.5% / 0.66 | +12.2% / 0.52 |
| RS leaders near 52w high | +36.4% / 1.16 | +31.8% / 1.05 | +25.2% / 0.89 |
| signals score>=70, trend | +12.1% / 0.65 | +9.2% / 0.52 | +5.3% / 0.35 |
| signals score>=70, trend, RS top 20% | +19.9% / 0.93 | +17.4% / 0.83 | +13.7% / 0.69 |
| signals, trend, RS top 20% | +36.4% / 1.08 | +30.4% / 0.94 | +23.3% / 0.78 |
| signals, trend, RS top 20%, near 52w high | +28.1% / 0.99 | +22.8% / 0.84 | +15.8% / 0.65 |

Exit variant (stop 2.5 x ATR instead of 1.5 x ATR / structural):

| rule set | CAGR | max DD | Sharpe | OOS Sharpe |
|---|---|---|---|---|
| random picks (reference) | +12.2% | -41% | 0.65 | -0.25 |
| random picks, trend filter | +16.9% | -35% | 0.92 | 0.73 |
| RS leaders, trend filter | +19.8% | -28% | 0.94 | 0.47 |
| RS leaders near 52w high | +25.9% | -24% | 1.13 | 0.70 |
| signals score>=70, trend | +11.9% | -29% | 0.75 | -0.05 |
| signals score>=70, trend, RS top 20% | +17.5% | -28% | 1.02 | 0.55 |
| signals, trend, RS top 20% | +19.1% | -36% | 0.90 | 0.74 |
| signals, trend, RS top 20%, near 52w high | +16.0% | -26% | 0.79 | 0.69 |

### Per trade — universe: all (one position per symbol, t over monthly means)

| group | exit | policy | n | win% | avgR | medR | t | excess vs random (t) | ≥+50% | OOS n | OOS avgR |
|---|---|---|---|---|---|---|---|---|---|---|---|
| breakout | fixed | all | 6481 | 17 | +0.292 | -1.11 | 1.33 | -0.310 (-3.67) | 3.2% | 1431 | +0.021 |
| breakout | fixed | SPY>200d & stock>200d | 5139 | 17 | +0.245 | -1.12 | 0.68 | -0.203 (-2.91) | 3.0% | 1150 | +0.047 |
| breakout | fixed | SPY>200d & stock>200d & RS>=0.8 | 2123 | 18 | +0.443 | -1.08 | 1.82 | -0.157 (-1.49) | 5.5% | 497 | +0.569 |
| breakout | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1735 | 18 | +0.480 | -1.08 | 1.86 | -0.044 (-0.35) | 4.4% | 382 | +0.767 |
| breakout | fixed | score>=70 & SPY>200d & stock>200d | 748 | 22 | +0.481 | -1.00 | 2.37 | +0.066 (0.44) | 5.9% | 145 | +0.278 |
| breakout | fixed | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 455 | 23 | +0.600 | -0.98 | 2.82 | +0.127 (0.61) | 7.7% | 96 | +0.434 |
| momentum | fixed | all | 5375 | 22 | +0.272 | -1.04 | 1.94 | -0.287 (-3.81) | 3.6% | 1194 | +0.028 |
| momentum | fixed | SPY>200d & stock>200d | 4747 | 22 | +0.311 | -1.04 | 2.01 | -0.084 (-1.34) | 3.5% | 1081 | +0.058 |
| momentum | fixed | SPY>200d & stock>200d & RS>=0.8 | 1920 | 23 | +0.403 | -1.02 | 2.29 | -0.110 (-1.40) | 6.3% | 442 | +0.268 |
| momentum | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1587 | 23 | +0.410 | -1.03 | 2.27 | -0.046 (-0.53) | 4.6% | 353 | +0.239 |
| momentum | fixed | score>=70 & SPY>200d & stock>200d | 154 | 24 | +0.567 | -0.91 | 2.08 | +0.326 (1.17) | 13.0% | 38 | +0.894 |
| momentum | fixed | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 95 | 25 | +0.748 | -0.88 | 1.92 | +0.280 (0.74) | 15.8% | 26 | +0.976 |
| combined | fixed | all | 8155 | 19 | +0.278 | -1.08 | 1.66 | -0.300 (-4.27) | 3.3% | 1791 | +0.114 |
| combined | fixed | SPY>200d & stock>200d | 6720 | 19 | +0.247 | -1.08 | 1.02 | -0.169 (-2.90) | 3.1% | 1502 | +0.108 |
| combined | fixed | SPY>200d & stock>200d & RS>=0.8 | 2798 | 21 | +0.424 | -1.04 | 2.12 | -0.138 (-1.77) | 5.5% | 652 | +0.604 |
| combined | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 2306 | 21 | +0.429 | -1.05 | 2.15 | -0.047 (-0.54) | 4.3% | 504 | +0.656 |
| combined | fixed | score>=70 & SPY>200d & stock>200d | 822 | 23 | +0.505 | -0.98 | 2.19 | +0.058 (0.43) | 6.6% | 168 | +0.314 |
| combined | fixed | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 499 | 24 | +0.613 | -0.96 | 2.51 | +0.068 (0.36) | 8.6% | 111 | +0.452 |
| baseline_random | fixed | all | 17818 | 25 | +0.351 | -1.02 | 4.93 | — (—) | 5.0% | 4102 | +0.219 |
| baseline_random | fixed | SPY>200d & stock>200d | 11304 | 23 | +0.327 | -1.04 | 3.10 | — (—) | 3.6% | 2596 | +0.173 |
| baseline_random | fixed | SPY>200d & stock>200d & RS>=0.8 | 4576 | 23 | +0.392 | -1.03 | 3.55 | — (—) | 6.3% | 1108 | +0.277 |
| baseline_random | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 3121 | 24 | +0.455 | -1.04 | 3.32 | — (—) | 4.0% | 679 | +0.361 |
| breakout | wide | all | 5211 | 34 | +0.307 | -0.95 | 3.22 | -0.164 (-2.96) | 5.5% | 1139 | +0.256 |
| breakout | wide | SPY>200d & stock>200d | 4192 | 33 | +0.319 | -0.96 | 2.35 | -0.067 (-1.37) | 5.1% | 925 | +0.283 |
| breakout | wide | SPY>200d & stock>200d & RS>=0.8 | 1778 | 35 | +0.451 | -0.93 | 2.92 | -0.093 (-1.53) | 9.2% | 415 | +0.444 |
| breakout | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1481 | 35 | +0.478 | -0.92 | 3.36 | -0.016 (-0.23) | 7.4% | 324 | +0.393 |
| breakout | wide | score>=70 & SPY>200d & stock>200d | 721 | 33 | +0.390 | -0.91 | 2.67 | +0.008 (0.07) | 9.0% | 138 | +0.160 |
| breakout | wide | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 433 | 34 | +0.483 | -0.90 | 3.02 | +0.035 (0.23) | 11.6% | 90 | +0.264 |
| momentum | wide | all | 4471 | 32 | +0.274 | -0.98 | 2.82 | -0.184 (-3.20) | 4.8% | 964 | +0.145 |
| momentum | wide | SPY>200d & stock>200d | 3966 | 33 | +0.318 | -0.98 | 2.95 | -0.026 (-0.51) | 4.7% | 878 | +0.170 |
| momentum | wide | SPY>200d & stock>200d & RS>=0.8 | 1623 | 33 | +0.372 | -0.96 | 2.50 | -0.127 (-2.11) | 8.0% | 370 | +0.277 |
| momentum | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1369 | 33 | +0.353 | -0.97 | 2.29 | -0.116 (-1.81) | 5.8% | 294 | +0.285 |
| momentum | wide | score>=70 & SPY>200d & stock>200d | 138 | 32 | +0.338 | -0.88 | 1.52 | +0.041 (0.22) | 15.2% | 33 | +0.764 |
| momentum | wide | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 81 | 33 | +0.494 | -0.81 | 1.63 | +0.013 (0.05) | 19.8% | 22 | +1.008 |
| combined | wide | all | 6206 | 33 | +0.291 | -0.97 | 3.20 | -0.175 (-3.41) | 5.2% | 1347 | +0.217 |
| combined | wide | SPY>200d & stock>200d | 5184 | 33 | +0.315 | -0.97 | 2.53 | -0.062 (-1.45) | 4.8% | 1152 | +0.228 |
| combined | wide | SPY>200d & stock>200d & RS>=0.8 | 2248 | 33 | +0.394 | -0.95 | 2.69 | -0.111 (-2.04) | 8.3% | 527 | +0.382 |
| combined | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1880 | 34 | +0.404 | -0.95 | 2.92 | -0.057 (-0.97) | 6.6% | 408 | +0.359 |
| combined | wide | score>=70 & SPY>200d & stock>200d | 780 | 33 | +0.384 | -0.91 | 2.29 | -0.021 (-0.20) | 9.1% | 156 | +0.241 |
| combined | wide | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 464 | 34 | +0.472 | -0.89 | 2.58 | -0.032 (-0.23) | 12.1% | 101 | +0.371 |
| baseline_random | wide | all | 12419 | 36 | +0.321 | -0.94 | 5.38 | — (—) | 6.3% | 2759 | +0.265 |
| baseline_random | wide | SPY>200d & stock>200d | 8114 | 34 | +0.323 | -0.97 | 3.60 | — (—) | 4.7% | 1851 | +0.200 |
| baseline_random | wide | SPY>200d & stock>200d & RS>=0.8 | 3395 | 34 | +0.380 | -0.96 | 4.09 | — (—) | 8.4% | 797 | +0.322 |
| baseline_random | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 2485 | 35 | +0.437 | -0.97 | 4.13 | — (—) | 5.8% | 521 | +0.430 |

## Portfolio — universe: largecap_2015

SPY buy-and-hold: +15.1%/yr, max DD -34%, Sharpe 0.85 · train+val Sharpe 0.83 · OOS +15.9%/yr, Sharpe 0.96

| rule set | trades/yr | exposure | win% | avgR | CAGR | max DD | Sharpe | train+val Sharpe | OOS CAGR | OOS Sharpe | vs random |
|---|---|---|---|---|---|---|---|---|---|---|---|
| random picks (reference) | 44.3 | 87% | 24 | +0.11 | +4.0% | -36% | 0.33 | 0.40 | -2.2% | -0.05 | — |
| random picks, trend filter | 35.9 | 75% | 24 | +0.30 | +7.8% | -26% | 0.62 | 0.66 | +6.5% | 0.53 | — |
| RS leaders, trend filter | 42.3 | 76% | 23 | +0.24 | +7.6% | -36% | 0.49 | 0.63 | +5.0% | 0.34 | 72% |
| RS leaders near 52w high | 40.9 | 76% | 22 | +0.19 | +3.4% | -29% | 0.28 | 0.38 | +2.8% | 0.24 | 33% |
| signals score>=70, trend | 14.7 | 36% | 23 | +0.27 | +2.8% | -16% | 0.34 | 0.37 | +4.5% | 0.50 | 33% |
| signals score>=70, trend, RS top 20% | 10.7 | 25% | 22 | +0.35 | +2.4% | -19% | 0.34 | 0.45 | +2.4% | 0.35 | 5% |
| signals, trend, RS top 20% | 42.3 | 78% | 21 | +0.27 | +5.1% | -30% | 0.40 | 0.50 | -1.4% | 0.01 | 68% |
| signals, trend, RS top 20%, near 52w high | 42.7 | 78% | 20 | +0.24 | +6.1% | -33% | 0.47 | 0.59 | -1.1% | 0.03 | 78% |

Cost sensitivity (full-period CAGR / Sharpe):

| rule set | 20 bps | 40 bps | 70 bps |
|---|---|---|---|
| RS leaders, trend filter | +7.6% / 0.49 | +4.7% / 0.34 | +0.3% / 0.12 |
| RS leaders near 52w high | +3.4% / 0.28 | +0.3% / 0.11 | -4.3% / -0.16 |
| signals score>=70, trend | +2.8% / 0.34 | +1.4% / 0.20 | -0.6% / -0.01 |
| signals score>=70, trend, RS top 20% | +2.4% / 0.34 | +1.4% / 0.21 | -0.1% / 0.03 |
| signals, trend, RS top 20% | +5.1% / 0.40 | +1.7% / 0.19 | -3.2% / -0.11 |
| signals, trend, RS top 20%, near 52w high | +6.1% / 0.47 | +2.8% / 0.26 | -2.1% / -0.05 |

Exit variant (stop 2.5 x ATR instead of 1.5 x ATR / structural):

| rule set | CAGR | max DD | Sharpe | OOS Sharpe |
|---|---|---|---|---|
| random picks (reference) | +9.0% | -27% | 0.66 | 1.10 |
| random picks, trend filter | +6.7% | -26% | 0.59 | 0.19 |
| RS leaders, trend filter | +11.7% | -25% | 0.73 | 0.42 |
| RS leaders near 52w high | +12.9% | -22% | 0.79 | 0.27 |
| signals score>=70, trend | +1.5% | -16% | 0.22 | 0.44 |
| signals score>=70, trend, RS top 20% | +2.9% | -17% | 0.41 | 0.41 |
| signals, trend, RS top 20% | +6.3% | -21% | 0.48 | 0.00 |
| signals, trend, RS top 20%, near 52w high | +5.5% | -27% | 0.44 | 0.04 |

### Per trade — universe: largecap_2015 (one position per symbol, t over monthly means)

| group | exit | policy | n | win% | avgR | medR | t | excess vs random (t) | ≥+50% | OOS n | OOS avgR |
|---|---|---|---|---|---|---|---|---|---|---|---|
| breakout | fixed | all | 2256 | 17 | +0.083 | -1.16 | -0.51 | -0.421 (-3.51) | 0.2% | 433 | -0.220 |
| breakout | fixed | SPY>200d & stock>200d | 1848 | 16 | +0.010 | -1.18 | -0.60 | -0.245 (-2.39) | 0.1% | 358 | -0.204 |
| breakout | fixed | SPY>200d & stock>200d & RS>=0.8 | 754 | 18 | +0.293 | -1.12 | 1.26 | +0.059 (0.27) | 0.1% | 151 | +0.078 |
| breakout | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 707 | 18 | +0.318 | -1.12 | 1.34 | +0.106 (0.49) | 0.1% | 147 | +0.188 |
| breakout | fixed | score>=70 & SPY>200d & stock>200d | 158 | 22 | +0.188 | -1.02 | 0.94 | -0.053 (-0.19) | 0.0% | 26 | +0.486 |
| breakout | fixed | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 104 | 21 | +0.218 | -1.01 | 1.07 | -0.044 (-0.12) | 0.0% | 15 | +0.482 |
| momentum | fixed | all | 2171 | 22 | +0.171 | -1.10 | 0.97 | -0.263 (-2.79) | 0.1% | 428 | -0.068 |
| momentum | fixed | SPY>200d & stock>200d | 1936 | 22 | +0.208 | -1.10 | 0.79 | -0.086 (-0.98) | 0.1% | 393 | -0.009 |
| momentum | fixed | SPY>200d & stock>200d & RS>=0.8 | 827 | 22 | +0.235 | -1.08 | 0.25 | -0.219 (-2.03) | 0.0% | 165 | +0.073 |
| momentum | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 785 | 22 | +0.220 | -1.08 | 0.08 | -0.209 (-1.90) | 0.0% | 160 | +0.110 |
| momentum | fixed | score>=70 & SPY>200d & stock>200d | 15 | 20 | +0.106 | -1.03 | 0.39 | +0.037 (0.05) | 0.0% | 3 | -1.150 |
| momentum | fixed | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 8 | 25 | +0.909 | -0.90 | 0.74 | +0.039 (0.03) | 0.0% | 2 | -1.090 |
| combined | fixed | all | 3066 | 19 | +0.120 | -1.12 | 0.06 | -0.347 (-3.64) | 0.2% | 583 | -0.157 |
| combined | fixed | SPY>200d & stock>200d | 2616 | 19 | +0.088 | -1.13 | -0.25 | -0.183 (-2.28) | 0.1% | 500 | -0.126 |
| combined | fixed | SPY>200d & stock>200d & RS>=0.8 | 1121 | 20 | +0.218 | -1.08 | 0.25 | -0.178 (-1.64) | 0.0% | 214 | -0.029 |
| combined | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1063 | 20 | +0.208 | -1.09 | 0.28 | -0.143 (-1.36) | 0.0% | 209 | +0.052 |
| combined | fixed | score>=70 & SPY>200d & stock>200d | 169 | 22 | +0.222 | -1.02 | 1.10 | -0.034 (-0.13) | 0.0% | 29 | +0.316 |
| combined | fixed | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 110 | 22 | +0.308 | -0.99 | 1.33 | +0.023 (0.07) | 0.0% | 17 | +0.297 |
| baseline_random | fixed | all | 7391 | 25 | +0.288 | -1.05 | 4.08 | — (—) | 0.7% | 1501 | +0.202 |
| baseline_random | fixed | SPY>200d & stock>200d | 4831 | 23 | +0.232 | -1.08 | 2.24 | — (—) | 0.3% | 966 | +0.149 |
| baseline_random | fixed | SPY>200d & stock>200d & RS>=0.8 | 1929 | 24 | +0.296 | -1.06 | 2.25 | — (—) | 0.4% | 426 | +0.086 |
| baseline_random | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1715 | 24 | +0.289 | -1.07 | 1.98 | — (—) | 0.2% | 366 | +0.129 |
| breakout | wide | all | 1930 | 33 | +0.182 | -1.00 | 1.39 | -0.236 (-3.16) | 0.3% | 360 | +0.117 |
| breakout | wide | SPY>200d & stock>200d | 1585 | 33 | +0.200 | -1.00 | 1.45 | -0.038 (-0.55) | 0.2% | 300 | +0.177 |
| breakout | wide | SPY>200d & stock>200d & RS>=0.8 | 670 | 33 | +0.268 | -0.97 | 1.17 | -0.136 (-1.58) | 0.0% | 132 | +0.070 |
| breakout | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 633 | 33 | +0.269 | -0.97 | 1.24 | -0.090 (-1.04) | 0.0% | 128 | +0.101 |
| breakout | wide | score>=70 & SPY>200d & stock>200d | 158 | 32 | +0.165 | -0.93 | 0.54 | -0.120 (-0.64) | 0.0% | 26 | +0.380 |
| breakout | wide | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 104 | 32 | +0.306 | -0.93 | 1.20 | -0.113 (-0.47) | 0.0% | 15 | +0.530 |
| momentum | wide | all | 1844 | 32 | +0.185 | -1.02 | 1.76 | -0.203 (-2.74) | 0.1% | 354 | +0.044 |
| momentum | wide | SPY>200d & stock>200d | 1645 | 33 | +0.231 | -1.02 | 1.94 | +0.009 (0.13) | 0.1% | 329 | +0.079 |
| momentum | wide | SPY>200d & stock>200d & RS>=0.8 | 714 | 33 | +0.259 | -0.99 | 1.23 | -0.134 (-1.77) | 0.0% | 145 | -0.031 |
| momentum | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 678 | 33 | +0.265 | -0.99 | 1.39 | -0.082 (-1.03) | 0.0% | 142 | -0.003 |
| momentum | wide | score>=70 & SPY>200d & stock>200d | 14 | 29 | +0.005 | -0.99 | 0.33 | +0.046 (0.09) | 0.0% | 3 | -1.085 |
| momentum | wide | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 7 | 43 | +0.817 | -0.91 | 0.92 | -0.009 (-0.01) | 0.0% | 2 | -1.053 |
| combined | wide | all | 2434 | 33 | +0.177 | -1.01 | 1.59 | -0.225 (-3.26) | 0.3% | 454 | +0.093 |
| combined | wide | SPY>200d & stock>200d | 2089 | 33 | +0.196 | -1.02 | 1.65 | -0.026 (-0.46) | 0.1% | 399 | +0.135 |
| combined | wide | SPY>200d & stock>200d & RS>=0.8 | 915 | 34 | +0.273 | -0.99 | 1.48 | -0.101 (-1.55) | 0.0% | 180 | -0.013 |
| combined | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 869 | 33 | +0.275 | -0.99 | 1.51 | -0.055 (-0.89) | 0.0% | 176 | +0.016 |
| combined | wide | score>=70 & SPY>200d & stock>200d | 168 | 32 | +0.172 | -0.93 | 0.74 | -0.097 (-0.54) | 0.0% | 29 | +0.228 |
| combined | wide | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 109 | 32 | +0.348 | -0.92 | 1.37 | -0.087 (-0.38) | 0.0% | 17 | +0.343 |
| baseline_random | wide | all | 5223 | 37 | +0.289 | -0.95 | 4.91 | — (—) | 0.8% | 1012 | +0.271 |
| baseline_random | wide | SPY>200d & stock>200d | 3504 | 34 | +0.244 | -1.00 | 2.76 | — (—) | 0.2% | 708 | +0.204 |
| baseline_random | wide | SPY>200d & stock>200d & RS>=0.8 | 1479 | 36 | +0.307 | -0.98 | 2.88 | — (—) | 0.4% | 312 | +0.155 |
| baseline_random | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1327 | 35 | +0.309 | -0.99 | 2.67 | — (—) | 0.3% | 267 | +0.198 |

## Momentum rotation — universe: all (from 2018-01-18, 20 bps per side)

| benchmark | CAGR | max DD | Sharpe | train+val Sharpe | OOS CAGR | OOS Sharpe |
|---|---|---|---|---|---|---|
| SPY buy-and-hold | +14.2% | -34% | 0.80 | 0.76 | +15.9% | 0.96 |
| equal-weight universe (no costs) | +26.1% | -42% | 1.01 | 1.01 | +23.7% | 0.98 |

| rule set | trades/yr | exposure | win% | avg trade | avg days | CAGR | max DD | Sharpe | train+val Sharpe | OOS CAGR | OOS Sharpe | vs random | CAGR @40 / @70 bps | without best stock |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| top5, in RS>=0.8, out RS<0.5 | 10 | 92% | 41 | +25.2% | 108 | +29.3% | -75% | 0.72 | 0.66 | +48.1% | 0.89 | 75% | +28.4% / +27.0% | SE: +28.9%, Sharpe 0.72 |
| top5, in RS>=0.8, out RS<0.5, stop -20% | 15 | 92% | 34 | +16.1% | 73 | +26.2% | -70% | 0.69 | 0.70 | +23.7% | 0.65 | 60% | +25.0% / +23.1% | RKLB: +21.7%, Sharpe 0.63 |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d | 21 | 80% | 38 | +6.6% | 48 | +15.3% | -74% | 0.53 | 0.71 | -22.2% | -0.10 | 15% | +13.6% / +11.0% | MARA: +12.8%, Sharpe 0.49 |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | 25 | 80% | 35 | +3.5% | 39 | +9.1% | -71% | 0.42 | 0.51 | -8.7% | 0.14 | 15% | +7.2% / +4.3% | CELH: +14.8%, Sharpe 0.52 |
| top5, in RS>=0.8, out RS<0.7 | 12 | 93% | 46 | +13.3% | 94 | +21.2% | -76% | 0.62 | 0.56 | +35.0% | 0.77 | 35% | +20.1% / +18.5% | ENPH: +21.3%, Sharpe 0.62 |
| top5, in RS>=0.8, out RS<0.7, stop -20% | 17 | 93% | 37 | +11.8% | 66 | +24.6% | -77% | 0.66 | 0.53 | +63.4% | 1.04 | 35% | +23.1% / +20.9% | ENPH: +20.7%, Sharpe 0.61 |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d | 22 | 80% | 40 | +4.5% | 45 | +12.0% | -77% | 0.48 | 0.57 | -8.7% | 0.22 | 20% | +10.1% / +7.3% | TSLA: +17.9%, Sharpe 0.57 |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | 27 | 80% | 36 | +3.7% | 37 | +10.0% | -68% | 0.44 | 0.46 | +4.5% | 0.39 | 10% | +7.9% / +4.8% | CELH: +5.8%, Sharpe 0.37 |
| top8, in RS>=0.8, out RS<0.5 | 16 | 92% | 39 | +21.6% | 107 | +34.7% | -69% | 0.84 | 0.88 | +28.2% | 0.71 | 85% | +33.9% / +32.6% | SE: +33.3%, Sharpe 0.81 |
| top8, in RS>=0.8, out RS<0.5, stop -20% | 23 | 92% | 34 | +14.6% | 72 | +30.8% | -62% | 0.77 | 0.83 | +20.3% | 0.61 | 90% | +25.1% / +23.1% | SE: +25.9%, Sharpe 0.70 |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d | 30 | 80% | 39 | +9.6% | 52 | +31.6% | -58% | 0.80 | 0.86 | +20.6% | 0.61 | 90% | +29.9% / +27.3% | APP: +24.5%, Sharpe 0.69 |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | 36 | 80% | 35 | +6.7% | 42 | +26.3% | -67% | 0.72 | 0.75 | +21.1% | 0.62 | 70% | +24.4% / +21.7% | NIO: +27.6%, Sharpe 0.74 |
| top8, in RS>=0.8, out RS<0.7 | 19 | 92% | 50 | +22.9% | 94 | +39.7% | -58% | 0.87 | 0.90 | +36.4% | 0.80 | 95% | +38.5% / +36.5% | MARA: +29.0%, Sharpe 0.75 |
| top8, in RS>=0.8, out RS<0.7, stop -20% | 28 | 91% | 33 | +15.5% | 63 | +28.5% | -71% | 0.72 | 0.70 | +32.7% | 0.75 | 60% | +27.0% / +24.9% | MARA: +24.5%, Sharpe 0.67 |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d | 32 | 80% | 41 | +8.0% | 48 | +24.2% | -54% | 0.68 | 0.74 | +11.4% | 0.48 | 65% | +22.3% / +19.6% | MARA: +23.2%, Sharpe 0.68 |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | 40 | 80% | 34 | +9.3% | 38 | +28.6% | -63% | 0.73 | 0.78 | +13.0% | 0.51 | 85% | +26.3% / +23.0% | MARA: +27.0%, Sharpe 0.71 |
| top8, in RS>=0.8, out RS<0.5, 12-1 month momentum | 18 | 91% | 33 | +20.4% | 100 | +26.5% | -63% | 0.72 | 0.69 | +39.5% | 0.83 | 70% | +25.6% / +24.1% | SE: +23.9%, Sharpe 0.68 |
| top8, in RS>=0.8, out RS<0.5, monthly | 11 | 94% | 39 | +49.3% | 150 | +37.5% | -63% | 0.87 | 0.81 | +59.8% | 1.04 | 75% | +36.8% / +35.8% | ENPH: +34.4%, Sharpe 0.84 |
| top8, in RS>=0.8, out RS<0.5, volatility-adjusted | 14 | 93% | 46 | +26.5% | 124 | +36.3% | -45% | 0.95 | 0.95 | +50.1% | 0.98 | 95% | +35.4% / +34.1% | RKLB: +30.3%, Sharpe 0.84 |

## Momentum rotation — universe: largecap_2015 (from 2018-01-18, 20 bps per side)

| benchmark | CAGR | max DD | Sharpe | train+val Sharpe | OOS CAGR | OOS Sharpe |
|---|---|---|---|---|---|---|
| SPY buy-and-hold | +14.2% | -34% | 0.80 | 0.76 | +15.9% | 0.96 |
| equal-weight universe (no costs) | +13.4% | -37% | 0.77 | 0.73 | +13.9% | 1.02 |

| rule set | trades/yr | exposure | win% | avg trade | avg days | CAGR | max DD | Sharpe | train+val Sharpe | OOS CAGR | OOS Sharpe | vs random | CAGR @40 / @70 bps | without best stock |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| top5, in RS>=0.8, out RS<0.5 | 10 | 95% | 47 | +7.0% | 115 | +14.8% | -36% | 0.67 | 0.53 | +31.9% | 1.07 | 95% | +14.0% / +12.7% | DVN: +11.9%, Sharpe 0.58 |
| top5, in RS>=0.8, out RS<0.5, stop -20% | 10 | 94% | 51 | +7.2% | 111 | +15.5% | -36% | 0.69 | 0.57 | +31.7% | 1.06 | 95% | +14.6% / +13.3% | DVN: +12.5%, Sharpe 0.60 |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d | 20 | 81% | 47 | +2.8% | 50 | +10.7% | -25% | 0.57 | 0.57 | +12.0% | 0.56 | 85% | +9.0% / +6.5% | AVGO: +10.6%, Sharpe 0.58 |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | 20 | 81% | 48 | +2.8% | 49 | +11.0% | -25% | 0.58 | 0.58 | +12.1% | 0.56 | 100% | +9.3% / +6.8% | AVGO: +10.8%, Sharpe 0.59 |
| top5, in RS>=0.8, out RS<0.7 | 14 | 94% | 48 | +3.5% | 82 | +11.9% | -36% | 0.56 | 0.53 | +17.6% | 0.67 | 100% | +10.8% / +9.1% | META: +10.1%, Sharpe 0.50 |
| top5, in RS>=0.8, out RS<0.7, stop -20% | 14 | 95% | 48 | +4.1% | 80 | +14.0% | -33% | 0.62 | 0.62 | +16.9% | 0.65 | 100% | +12.8% / +11.0% | META: +13.6%, Sharpe 0.62 |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d | 23 | 81% | 47 | +2.1% | 44 | +9.2% | -29% | 0.51 | 0.59 | +4.0% | 0.28 | 100% | +7.3% / +4.5% | AVGO: +8.1%, Sharpe 0.47 |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | 23 | 81% | 47 | +2.1% | 43 | +9.2% | -29% | 0.51 | 0.59 | +3.9% | 0.27 | 100% | +7.2% / +4.4% | AVGO: +8.1%, Sharpe 0.47 |
| top8, in RS>=0.8, out RS<0.5 | 17 | 94% | 46 | +6.8% | 110 | +14.5% | -29% | 0.71 | 0.60 | +25.7% | 1.07 | 100% | +13.6% / +12.3% | DVN: +12.5%, Sharpe 0.64 |
| top8, in RS>=0.8, out RS<0.5, stop -20% | 17 | 94% | 46 | +5.6% | 104 | +13.4% | -29% | 0.67 | 0.57 | +23.9% | 1.02 | 100% | +12.5% / +11.2% | DVN: +11.2%, Sharpe 0.59 |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d | 31 | 80% | 44 | +2.3% | 51 | +8.0% | -27% | 0.50 | 0.46 | +10.4% | 0.59 | 70% | +6.3% / +4.0% | DVN: +7.2%, Sharpe 0.47 |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | 31 | 80% | 44 | +2.3% | 51 | +8.1% | -27% | 0.50 | 0.47 | +10.3% | 0.59 | 75% | +6.4% / +4.1% | DVN: +7.4%, Sharpe 0.48 |
| top8, in RS>=0.8, out RS<0.7 | 22 | 93% | 48 | +3.6% | 80 | +11.8% | -26% | 0.61 | 0.60 | +13.7% | 0.67 | 100% | +10.6% / +8.8% | META: +8.9%, Sharpe 0.50 |
| top8, in RS>=0.8, out RS<0.7, stop -20% | 23 | 93% | 47 | +3.7% | 78 | +11.5% | -29% | 0.60 | 0.59 | +13.1% | 0.65 | 95% | +10.3% / +8.5% | AVGO: +9.1%, Sharpe 0.50 |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d | 35 | 80% | 47 | +1.7% | 45 | +7.4% | -29% | 0.47 | 0.52 | +4.7% | 0.33 | 90% | +5.6% / +2.9% | AVGO: +6.8%, Sharpe 0.45 |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | 35 | 80% | 47 | +1.7% | 44 | +7.4% | -29% | 0.47 | 0.52 | +4.5% | 0.32 | 90% | +5.5% / +2.9% | AVGO: +6.8%, Sharpe 0.45 |
| top8, in RS>=0.8, out RS<0.5, 12-1 month momentum | 19 | 90% | 33 | +2.7% | 93 | +5.8% | -40% | 0.37 | 0.38 | +4.2% | 0.30 | 25% | +4.9% / +3.6% | GE: +4.2%, Sharpe 0.30 |
| top8, in RS>=0.8, out RS<0.5, monthly | 12 | 93% | 49 | +9.5% | 146 | +13.4% | -26% | 0.65 | 0.60 | +18.7% | 0.82 | 95% | +12.7% / +13.3% | DVN: +13.2%, Sharpe 0.64 |
| top8, in RS>=0.8, out RS<0.5, volatility-adjusted | 16 | 93% | 54 | +6.7% | 116 | +12.1% | -23% | 0.71 | 0.68 | +13.0% | 0.84 | 100% | +11.2% / +10.0% | GE: +9.1%, Sharpe 0.56 |

## Rotation: pre-registered selection (2015 large caps, train+validation only)

Gates: train+val Sharpe > SPY's, ranking beats >= 90% of random selections, CAGR without the single best stock >= SPY's, max drawdown at most 10 points worse than SPY's.

**Chosen: none — no rule set passed every gate**

| rule set | passes | train+val Sharpe | failed gates |
|---|---|---|---|
| top5, in RS>=0.8, out RS<0.5 | ❌ | 0.53 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top5, in RS>=0.8, out RS<0.5, stop -20% | ❌ | 0.57 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d | ❌ | 0.57 | train_val_sharpe_beats_spy, ranking_beats_random, without_best_stock_beats_spy |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | ❌ | 0.58 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top5, in RS>=0.8, out RS<0.7 | ❌ | 0.53 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top5, in RS>=0.8, out RS<0.7, stop -20% | ❌ | 0.62 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d | ❌ | 0.59 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | ❌ | 0.59 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5 | ❌ | 0.60 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5, stop -20% | ❌ | 0.57 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d | ❌ | 0.46 | train_val_sharpe_beats_spy, ranking_beats_random, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | ❌ | 0.47 | train_val_sharpe_beats_spy, ranking_beats_random, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.7 | ❌ | 0.60 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.7, stop -20% | ❌ | 0.59 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d | ❌ | 0.52 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | ❌ | 0.52 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5, 12-1 month momentum | ❌ | 0.38 | train_val_sharpe_beats_spy, ranking_beats_random, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5, monthly | ❌ | 0.60 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5, volatility-adjusted | ❌ | 0.68 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |

Calendar-year returns (2015 large caps, 20 bps per side):

| | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|---|---|---|---|
| SPY | -9% | +31% | +18% | +29% | -18% | +26% | +25% | +18% | +15% |
| equal-weight group | -10% | +29% | +14% | +31% | -4% | +16% | +16% | +17% | +13% |
| top5, in RS>=0.8, out RS<0.5 | -13% | +8% | +14% | +21% | +0% | +11% | +37% | +15% | +48% |
| top5, in RS>=0.8, out RS<0.5, stop -20% | -11% | +8% | +14% | +22% | -0% | +14% | +36% | +14% | +48% |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d | -6% | +3% | +16% | +21% | -1% | +21% | +19% | +9% | +16% |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | -5% | +3% | +16% | +22% | -1% | +21% | +19% | +9% | +16% |
| top5, in RS>=0.8, out RS<0.7 | -11% | +8% | +7% | +21% | -4% | +19% | +30% | -2% | +46% |
| top5, in RS>=0.8, out RS<0.7, stop -20% | -11% | +7% | +9% | +22% | +10% | +21% | +30% | -2% | +46% |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d | -5% | -3% | +8% | +21% | -2% | +22% | +29% | -5% | +21% |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | -5% | -3% | +8% | +21% | -2% | +22% | +29% | -5% | +21% |
| top8, in RS>=0.8, out RS<0.5 | -17% | +8% | +17% | +28% | +0% | +23% | +27% | +22% | +27% |
| top8, in RS>=0.8, out RS<0.5, stop -20% | -16% | +8% | +11% | +33% | +1% | +20% | +22% | +23% | +24% |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d | -8% | -5% | +11% | +30% | -2% | +14% | +13% | +14% | +8% |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | -8% | -4% | +11% | +30% | -2% | +14% | +13% | +14% | +7% |
| top8, in RS>=0.8, out RS<0.7 | -14% | +9% | +17% | +18% | +2% | +20% | +25% | +6% | +26% |
| top8, in RS>=0.8, out RS<0.7, stop -20% | -14% | +6% | +13% | +18% | +6% | +21% | +25% | +5% | +26% |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d | -7% | +2% | +12% | +18% | -4% | +9% | +24% | +2% | +13% |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | -7% | +2% | +12% | +18% | -4% | +9% | +24% | +1% | +13% |
| top8, in RS>=0.8, out RS<0.5, 12-1 month momentum | -14% | +10% | +2% | +24% | -12% | +2% | +41% | -1% | +9% |
| top8, in RS>=0.8, out RS<0.5, monthly | -3% | +12% | +16% | +19% | -5% | +26% | +23% | +5% | +29% |
| top8, in RS>=0.8, out RS<0.5, volatility-adjusted | -6% | +16% | +3% | +22% | -8% | +18% | +38% | +20% | +10% |

## Rockets (from 2016-10-31, 20 bps per side, 10 slots x 10%, max 3 new per day)

Rocket day: close >= +jump vs previous close, volume >= 3x the 20-day average, close in the top quarter of the day's range, price >= $5, 20-day dollar volume >= $5M. Buy next open; sell next open after a close more than `trail` below the highest close, or after 40 sessions. 'Random' = same stocks, same liquidity filter, same exit, random dates.

SPY: +15.8%/yr, max DD -34%, Sharpe 0.91 · train+val +15.8%/yr, Sharpe 0.89

| variant | trades | win% | avg trade | median | ≥+50% | worst | random avg | excess vs random t (train+val) | 2015 large caps excess | CAGR | max DD | Sharpe | train+val CAGR / Sharpe | OOS CAGR | random-entry portfolio CAGR | without top 3 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| EPS surprise>0%, reaction>=5% | 1885 | 54 | +4.7% | +2.0% | 4.4% | -51% | +4.4% | -0.34% (-0.54) | -0.19% (n=553) | +6.5% | -40% | 0.40 | +11.6% / 0.63 | -7.9% | +12.0% | +6.5% |
| EPS surprise>0%, reaction>=10% | 911 | 53 | +6.3% | +1.9% | 6.4% | -51% | +4.4% | +0.74% (0.75) | +1.45% (n=126) | +23.3% | -43% | 0.97 | +24.8% / 1.04 | +17.6% | +12.0% | +22.6% |
| EPS surprise>10%, reaction>=5% | 1256 | 54 | +5.1% | +2.4% | 5.0% | -51% | +4.4% | +0.55% (0.68) | -0.70% (n=264) | +13.1% | -45% | 0.64 | +22.7% / 0.99 | -19.0% | +12.0% | +13.4% |
| EPS surprise>10%, reaction>=10% | 704 | 53 | +6.7% | +2.2% | 6.4% | -51% | +4.4% | +1.61% (1.34) | +1.80% (n=69) | +18.7% | -48% | 0.80 | +27.0% / 1.06 | -13.4% | +12.0% | +15.4% |
| EPS surprise>20%, reaction>=10%, volume>=2x, RS>=0.8 | 240 | 56 | +8.7% | +3.2% | 7.1% | -36% | +4.4% | +3.57% (1.65) | +3.91% (n=14) | +18.2% | -27% | 0.93 | +24.2% / 1.25 | -7.1% | +12.0% | +12.1% |
| EPS surprise>20%, reaction>=15%, volume>=2x, RS>=0.8 | 171 | 56 | +8.7% | +2.8% | 8.2% | -36% | +4.4% | +1.87% (0.79) | —% (n=4) | +14.8% | -24% | 0.89 | +18.9% / 1.20 | -4.5% | +12.0% | +9.6% |
| jump>=8%, trail 15% | 997 | 45 | +4.0% | -2.7% | 5.2% | -52% | +2.3% | +0.08% (0.08) | -1.52% (n=114) | +15.7% | -48% | 0.63 | +23.2% / 0.82 | -16.1% | +19.8% | +9.9% |
| jump>=8%, trail 25% | 996 | 51 | +5.3% | +0.6% | 6.7% | -61% | +3.0% | +0.58% (0.50) | -1.48% (n=114) | +16.0% | -68% | 0.62 | +22.8% / 0.80 | -11.4% | +24.7% | +11.9% |
| jump>=15%, trail 15% | 540 | 43 | +4.7% | -4.6% | 6.7% | -52% | +2.3% | -0.13% (-0.09) | -4.51% (n=23) | +17.7% | -38% | 0.70 | +22.2% / 0.81 | -1.2% | +19.8% | +11.4% |
| jump>=15%, trail 25% | 539 | 47 | +6.6% | -1.9% | 9.1% | -61% | +3.0% | +1.19% (0.66) | -4.75% (n=23) | +14.6% | -60% | 0.57 | +20.4% / 0.72 | -11.1% | +24.7% | +6.3% |

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
| combined | all | +0.89 | -0.43 | +0.29 | +1.07 | +0.02 | -0.44 | +0.53 | +0.42 | +0.23 | +0.01 |
| combined | SPY>200d & stock>200d | +0.97 | -0.42 | +0.03 | +0.94 | -0.04 | -0.79 | +0.38 | +0.42 | +0.19 | +0.04 |
| combined | SPY>200d & stock>200d & RS>=0.8 | +1.05 | -0.27 | +0.35 | +1.46 | -0.42 | -0.36 | +0.35 | +0.60 | +0.83 | +0.34 |
| combined | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | +1.15 | -0.13 | +0.45 | +1.36 | -0.52 | -0.07 | +0.30 | +0.46 | +0.81 | +0.60 |
| combined | score>=70 & SPY>200d & stock>200d | +1.01 | +0.65 | +0.42 | +1.14 | -0.54 | -0.96 | +0.43 | +0.69 | +0.52 | +0.14 |
| combined | score>=70 & SPY>200d & stock>200d & RS>=0.8 | +0.58 | +1.33 | +0.61 | +1.08 | -0.53 | -1.15 | +0.41 | +1.00 | +0.70 | +0.23 |
| baseline_random | all | +1.11 | +0.06 | +0.55 | +0.98 | +0.15 | -0.28 | +0.61 | +0.42 | +0.30 | +0.20 |
| baseline_random | SPY>200d & stock>200d | +1.21 | -0.24 | +0.52 | +0.85 | +0.17 | -0.78 | +0.26 | +0.42 | +0.21 | +0.19 |
| baseline_random | SPY>200d & stock>200d & RS>=0.8 | +1.33 | +0.11 | +0.66 | +1.15 | -0.24 | -0.74 | +0.47 | +0.51 | +0.39 | +0.20 |
| baseline_random | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | +1.31 | +0.28 | +0.75 | +0.96 | -0.29 | -0.63 | +0.55 | +0.60 | +0.64 | +0.13 |