# Strategy research

277 symbols with data (2 failed), 10 years of daily bars. Control group: 105 stocks that were already large caps in 2015. Primary cost 20 bps per side (USD account: courtage + slippage; 40 bps ≈ trading from a SEK account). Validation from 2023-03-12, out-of-sample (OOS) from 2025-01-11. Setups invalidated at the next open (skipped): 1303.

Portfolio: max 8 positions, max 3 new per day, 1% risk per trade, max 25% of equity per position, no leverage, marked to market daily. 'vs random' = share of 40 random-order portfolios from the same eligible trades that this ranking beat.

## Portfolio — universe: all

SPY buy-and-hold: +14.4%/yr, max DD -34%, Sharpe 0.81 · train+val Sharpe 0.79 · OOS +15.2%/yr, Sharpe 0.91

| rule set | trades/yr | exposure | win% | avgR | CAGR | max DD | Sharpe | train+val Sharpe | OOS CAGR | OOS Sharpe | vs random |
|---|---|---|---|---|---|---|---|---|---|---|---|
| random picks (reference) | 73.3 | 87% | 23 | +0.31 | +15.1% | -63% | 0.62 | 0.74 | -4.5% | -0.01 | — |
| random picks, trend filter | 64.4 | 78% | 23 | +0.33 | +14.6% | -37% | 0.64 | 0.87 | -6.7% | -0.07 | — |
| RS leaders, trend filter | 70.6 | 69% | 22 | +0.41 | +21.5% | -43% | 0.76 | 0.97 | +0.4% | 0.19 | 100% |
| RS leaders near 52w high | 63.2 | 76% | 24 | +0.44 | +20.1% | -44% | 0.76 | 0.87 | +11.0% | 0.47 | 95% |
| signals score>=70, trend | 47.8 | 62% | 20 | +0.25 | +8.9% | -35% | 0.51 | 0.66 | -5.7% | -0.14 | 15% |
| signals score>=70, trend, RS top 20% | 41.8 | 50% | 22 | +0.55 | +19.6% | -33% | 0.92 | 1.03 | +5.5% | 0.35 | 95% |
| signals, trend, RS top 20% | 78.5 | 78% | 21 | +0.63 | +36.0% | -48% | 1.06 | 1.17 | +23.2% | 0.72 | 100% |
| signals, trend, RS top 20%, near 52w high | 75.3 | 79% | 21 | +0.49 | +25.1% | -32% | 0.90 | 1.00 | +22.6% | 0.74 | 95% |

Cost sensitivity (full-period CAGR / Sharpe):

| rule set | 20 bps | 40 bps | 70 bps |
|---|---|---|---|
| RS leaders, trend filter | +21.5% / 0.76 | +18.0% / 0.67 | +12.9% / 0.54 |
| RS leaders near 52w high | +20.1% / 0.76 | +12.9% / 0.55 | +7.8% / 0.40 |
| signals score>=70, trend | +8.9% / 0.51 | +6.0% / 0.38 | +2.0% / 0.20 |
| signals score>=70, trend, RS top 20% | +19.6% / 0.92 | +17.0% / 0.82 | +13.2% / 0.67 |
| signals, trend, RS top 20% | +36.0% / 1.06 | +30.7% / 0.94 | +22.7% / 0.76 |
| signals, trend, RS top 20%, near 52w high | +25.1% / 0.90 | +19.9% / 0.76 | +12.7% / 0.55 |

Exit variant (stop 2.5 x ATR instead of 1.5 x ATR / structural):

| rule set | CAGR | max DD | Sharpe | OOS Sharpe |
|---|---|---|---|---|
| random picks (reference) | +15.6% | -39% | 0.80 | -0.11 |
| random picks, trend filter | +15.0% | -39% | 0.81 | 0.88 |
| RS leaders, trend filter | +21.1% | -25% | 0.99 | 0.29 |
| RS leaders near 52w high | +17.9% | -34% | 0.83 | 0.42 |
| signals score>=70, trend | +12.7% | -28% | 0.79 | -0.09 |
| signals score>=70, trend, RS top 20% | +16.1% | -27% | 0.96 | 0.30 |
| signals, trend, RS top 20% | +16.7% | -36% | 0.81 | 0.68 |
| signals, trend, RS top 20%, near 52w high | +17.6% | -25% | 0.85 | 0.32 |

### Per trade — universe: all (one position per symbol, t over monthly means)

| group | exit | policy | n | win% | avgR | medR | t | excess vs random (t) | ≥+50% | OOS n | OOS avgR |
|---|---|---|---|---|---|---|---|---|---|---|---|
| breakout | fixed | all | 6492 | 17 | +0.272 | -1.11 | 1.10 | -0.344 (-4.33) | 3.2% | 1473 | -0.008 |
| breakout | fixed | SPY>200d & stock>200d | 5142 | 16 | +0.216 | -1.12 | 0.36 | -0.251 (-3.44) | 2.9% | 1185 | -0.004 |
| breakout | fixed | SPY>200d & stock>200d & RS>=0.8 | 2137 | 17 | +0.391 | -1.08 | 1.27 | -0.183 (-1.76) | 5.3% | 515 | +0.412 |
| breakout | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1741 | 18 | +0.429 | -1.08 | 1.25 | -0.100 (-0.85) | 4.2% | 393 | +0.604 |
| breakout | fixed | score>=70 & SPY>200d & stock>200d | 737 | 22 | +0.458 | -1.00 | 2.18 | +0.015 (0.10) | 6.0% | 137 | +0.293 |
| breakout | fixed | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 451 | 23 | +0.573 | -0.98 | 2.54 | +0.109 (0.54) | 7.8% | 90 | +0.441 |
| momentum | fixed | all | 5397 | 22 | +0.250 | -1.04 | 1.63 | -0.324 (-4.48) | 3.5% | 1233 | +0.042 |
| momentum | fixed | SPY>200d & stock>200d | 4767 | 22 | +0.284 | -1.04 | 1.64 | -0.134 (-2.18) | 3.4% | 1116 | +0.072 |
| momentum | fixed | SPY>200d & stock>200d & RS>=0.8 | 1934 | 22 | +0.368 | -1.02 | 1.98 | -0.104 (-1.27) | 6.1% | 468 | +0.221 |
| momentum | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1594 | 23 | +0.373 | -1.03 | 1.88 | -0.056 (-0.63) | 4.4% | 373 | +0.201 |
| momentum | fixed | score>=70 & SPY>200d & stock>200d | 157 | 23 | +0.524 | -0.92 | 1.90 | +0.277 (1.04) | 12.7% | 39 | +0.794 |
| momentum | fixed | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 97 | 25 | +0.715 | -0.89 | 1.81 | +0.271 (0.73) | 15.5% | 27 | +0.911 |
| combined | fixed | all | 8187 | 19 | +0.268 | -1.07 | 1.45 | -0.328 (-5.05) | 3.3% | 1854 | +0.094 |
| combined | fixed | SPY>200d & stock>200d | 6741 | 19 | +0.229 | -1.08 | 0.73 | -0.211 (-3.57) | 3.0% | 1553 | +0.077 |
| combined | fixed | SPY>200d & stock>200d & RS>=0.8 | 2813 | 20 | +0.402 | -1.04 | 1.82 | -0.124 (-1.58) | 5.4% | 680 | +0.457 |
| combined | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 2313 | 21 | +0.413 | -1.05 | 1.79 | -0.053 (-0.66) | 4.2% | 525 | +0.550 |
| combined | fixed | score>=70 & SPY>200d & stock>200d | 815 | 23 | +0.474 | -0.98 | 1.89 | -0.004 (-0.03) | 6.6% | 161 | +0.307 |
| combined | fixed | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 498 | 23 | +0.579 | -0.96 | 2.19 | +0.040 (0.22) | 8.6% | 106 | +0.448 |
| baseline_random | fixed | all | 17552 | 25 | +0.358 | -1.02 | 4.96 | — (—) | 5.0% | 4066 | +0.232 |
| baseline_random | fixed | SPY>200d & stock>200d | 11061 | 23 | +0.336 | -1.04 | 3.21 | — (—) | 3.6% | 2537 | +0.180 |
| baseline_random | fixed | SPY>200d & stock>200d & RS>=0.8 | 4556 | 23 | +0.342 | -1.03 | 3.27 | — (—) | 6.2% | 1107 | +0.194 |
| baseline_random | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 3102 | 23 | +0.400 | -1.04 | 2.92 | — (—) | 3.8% | 686 | +0.270 |
| breakout | wide | all | 5233 | 33 | +0.295 | -0.95 | 3.04 | -0.155 (-3.29) | 5.5% | 1180 | +0.249 |
| breakout | wide | SPY>200d & stock>200d | 4200 | 33 | +0.306 | -0.96 | 2.16 | -0.073 (-1.64) | 5.0% | 955 | +0.270 |
| breakout | wide | SPY>200d & stock>200d & RS>=0.8 | 1784 | 34 | +0.430 | -0.93 | 2.49 | -0.076 (-1.30) | 8.9% | 431 | +0.346 |
| breakout | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1481 | 35 | +0.469 | -0.92 | 2.90 | +0.009 (0.14) | 7.2% | 332 | +0.330 |
| breakout | wide | score>=70 & SPY>200d & stock>200d | 709 | 33 | +0.392 | -0.91 | 2.47 | -0.007 (-0.07) | 9.2% | 131 | +0.183 |
| breakout | wide | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 428 | 34 | +0.484 | -0.89 | 2.82 | +0.061 (0.41) | 11.7% | 86 | +0.257 |
| momentum | wide | all | 4483 | 32 | +0.264 | -0.98 | 2.60 | -0.178 (-3.21) | 4.7% | 1001 | +0.144 |
| momentum | wide | SPY>200d & stock>200d | 3975 | 33 | +0.305 | -0.98 | 2.69 | -0.044 (-0.91) | 4.5% | 910 | +0.170 |
| momentum | wide | SPY>200d & stock>200d & RS>=0.8 | 1628 | 33 | +0.352 | -0.96 | 2.29 | -0.111 (-1.86) | 7.7% | 394 | +0.226 |
| momentum | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1372 | 33 | +0.332 | -0.97 | 1.99 | -0.097 (-1.55) | 5.5% | 315 | +0.236 |
| momentum | wide | score>=70 & SPY>200d & stock>200d | 140 | 29 | +0.294 | -0.88 | 1.20 | -0.018 (-0.10) | 15.0% | 36 | +0.537 |
| momentum | wide | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 82 | 30 | +0.445 | -0.83 | 1.29 | -0.042 (-0.17) | 19.5% | 25 | +0.684 |
| combined | wide | all | 6242 | 33 | +0.278 | -0.97 | 2.92 | -0.174 (-3.88) | 5.1% | 1399 | +0.213 |
| combined | wide | SPY>200d & stock>200d | 5203 | 33 | +0.299 | -0.98 | 2.24 | -0.075 (-1.92) | 4.7% | 1189 | +0.222 |
| combined | wide | SPY>200d & stock>200d & RS>=0.8 | 2253 | 33 | +0.376 | -0.95 | 2.40 | -0.101 (-1.92) | 8.1% | 548 | +0.315 |
| combined | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1883 | 34 | +0.390 | -0.95 | 2.58 | -0.040 (-0.76) | 6.4% | 424 | +0.312 |
| combined | wide | score>=70 & SPY>200d & stock>200d | 771 | 33 | +0.378 | -0.90 | 2.00 | -0.036 (-0.39) | 9.2% | 151 | +0.237 |
| combined | wide | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 461 | 33 | +0.464 | -0.89 | 2.27 | -0.026 (-0.20) | 12.2% | 99 | +0.332 |
| baseline_random | wide | all | 12302 | 36 | +0.325 | -0.95 | 5.16 | — (—) | 6.2% | 2794 | +0.262 |
| baseline_random | wide | SPY>200d & stock>200d | 8154 | 34 | +0.310 | -0.97 | 3.53 | — (—) | 4.6% | 1873 | +0.193 |
| baseline_random | wide | SPY>200d & stock>200d & RS>=0.8 | 3409 | 33 | +0.338 | -0.97 | 3.59 | — (—) | 8.1% | 816 | +0.249 |
| baseline_random | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 2503 | 34 | +0.374 | -0.98 | 3.29 | — (—) | 5.1% | 545 | +0.289 |

## Portfolio — universe: largecap_2015

SPY buy-and-hold: +14.4%/yr, max DD -34%, Sharpe 0.81 · train+val Sharpe 0.79 · OOS +15.2%/yr, Sharpe 0.91

| rule set | trades/yr | exposure | win% | avgR | CAGR | max DD | Sharpe | train+val Sharpe | OOS CAGR | OOS Sharpe | vs random |
|---|---|---|---|---|---|---|---|---|---|---|---|
| random picks (reference) | 41.5 | 88% | 24 | +0.12 | +3.4% | -36% | 0.28 | 0.16 | +13.4% | 0.90 | — |
| random picks, trend filter | 34.5 | 76% | 24 | +0.22 | +6.3% | -32% | 0.52 | 0.32 | +17.8% | 1.10 | — |
| RS leaders, trend filter | 40.3 | 77% | 26 | +0.44 | +12.8% | -32% | 0.70 | 0.74 | +9.4% | 0.51 | 100% |
| RS leaders near 52w high | 40.8 | 76% | 25 | +0.48 | +15.4% | -20% | 0.85 | 0.78 | +14.6% | 0.78 | 100% |
| signals score>=70, trend | 14.5 | 36% | 23 | +0.29 | +3.1% | -16% | 0.36 | 0.36 | +2.4% | 0.28 | 38% |
| signals score>=70, trend, RS top 20% | 10.7 | 25% | 22 | +0.35 | +2.4% | -19% | 0.33 | 0.35 | +1.4% | 0.22 | 5% |
| signals, trend, RS top 20% | 41.0 | 78% | 21 | +0.30 | +6.4% | -30% | 0.46 | 0.49 | +4.8% | 0.37 | 42% |
| signals, trend, RS top 20%, near 52w high | 42.1 | 78% | 21 | +0.30 | +7.0% | -33% | 0.51 | 0.56 | +4.6% | 0.35 | 68% |

Cost sensitivity (full-period CAGR / Sharpe):

| rule set | 20 bps | 40 bps | 70 bps |
|---|---|---|---|
| RS leaders, trend filter | +12.8% / 0.70 | +9.7% / 0.56 | +5.2% / 0.35 |
| RS leaders near 52w high | +15.4% / 0.85 | +12.1% / 0.69 | +6.6% / 0.42 |
| signals score>=70, trend | +3.1% / 0.36 | +1.8% / 0.23 | -0.2% / 0.02 |
| signals score>=70, trend, RS top 20% | +2.4% / 0.33 | +1.4% / 0.20 | -0.1% / 0.03 |
| signals, trend, RS top 20% | +6.4% / 0.46 | +3.1% / 0.26 | -1.7% / -0.03 |
| signals, trend, RS top 20%, near 52w high | +7.0% / 0.51 | +3.7% / 0.31 | -1.1% / -0.00 |

Exit variant (stop 2.5 x ATR instead of 1.5 x ATR / structural):

| rule set | CAGR | max DD | Sharpe | OOS Sharpe |
|---|---|---|---|---|
| random picks (reference) | +12.8% | -26% | 0.88 | 1.40 |
| random picks, trend filter | +5.2% | -22% | 0.47 | 1.10 |
| RS leaders, trend filter | +13.2% | -21% | 0.82 | 0.47 |
| RS leaders near 52w high | +9.8% | -20% | 0.65 | 0.14 |
| signals score>=70, trend | +1.7% | -16% | 0.24 | 0.55 |
| signals score>=70, trend, RS top 20% | +3.0% | -17% | 0.42 | 0.46 |
| signals, trend, RS top 20% | +7.7% | -21% | 0.55 | 0.35 |
| signals, trend, RS top 20%, near 52w high | +6.9% | -27% | 0.51 | 0.42 |

### Per trade — universe: largecap_2015 (one position per symbol, t over monthly means)

| group | exit | policy | n | win% | avgR | medR | t | excess vs random (t) | ≥+50% | OOS n | OOS avgR |
|---|---|---|---|---|---|---|---|---|---|---|---|
| breakout | fixed | all | 2282 | 17 | +0.076 | -1.16 | -0.54 | -0.521 (-4.55) | 0.2% | 470 | -0.191 |
| breakout | fixed | SPY>200d & stock>200d | 1871 | 16 | +0.004 | -1.18 | -0.64 | -0.301 (-2.68) | 0.1% | 393 | -0.191 |
| breakout | fixed | SPY>200d & stock>200d & RS>=0.8 | 762 | 18 | +0.274 | -1.12 | 1.18 | +0.067 (0.32) | 0.1% | 163 | +0.021 |
| breakout | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 714 | 18 | +0.301 | -1.12 | 1.26 | +0.132 (0.61) | 0.1% | 158 | +0.140 |
| breakout | fixed | score>=70 & SPY>200d & stock>200d | 157 | 22 | +0.200 | -1.02 | 1.11 | +0.013 (0.04) | 0.0% | 27 | +0.414 |
| breakout | fixed | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 104 | 21 | +0.223 | -1.01 | 1.09 | +0.011 (0.03) | 0.0% | 15 | +0.442 |
| momentum | fixed | all | 2205 | 22 | +0.177 | -1.09 | 0.96 | -0.359 (-3.92) | 0.1% | 472 | +0.051 |
| momentum | fixed | SPY>200d & stock>200d | 1970 | 23 | +0.213 | -1.10 | 0.75 | -0.116 (-1.38) | 0.1% | 436 | +0.112 |
| momentum | fixed | SPY>200d & stock>200d & RS>=0.8 | 840 | 22 | +0.225 | -1.07 | 0.17 | -0.155 (-1.43) | 0.0% | 184 | +0.123 |
| momentum | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 797 | 22 | +0.212 | -1.07 | 0.02 | -0.123 (-1.09) | 0.0% | 178 | +0.165 |
| momentum | fixed | score>=70 & SPY>200d & stock>200d | 17 | 18 | -0.036 | -1.06 | 0.18 | -0.191 (-0.28) | 0.0% | 5 | -1.131 |
| momentum | fixed | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 9 | 22 | +0.681 | -0.91 | 0.62 | +0.110 (0.11) | 0.0% | 3 | -1.108 |
| combined | fixed | all | 3101 | 20 | +0.129 | -1.12 | 0.10 | -0.438 (-4.62) | 0.2% | 640 | -0.065 |
| combined | fixed | SPY>200d & stock>200d | 2648 | 20 | +0.099 | -1.13 | -0.21 | -0.221 (-2.63) | 0.1% | 553 | -0.029 |
| combined | fixed | SPY>200d & stock>200d & RS>=0.8 | 1130 | 20 | +0.221 | -1.08 | 0.25 | -0.128 (-1.27) | 0.0% | 235 | -0.011 |
| combined | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1070 | 20 | +0.217 | -1.08 | 0.32 | -0.067 (-0.67) | 0.0% | 228 | +0.082 |
| combined | fixed | score>=70 & SPY>200d & stock>200d | 170 | 22 | +0.218 | -1.02 | 1.22 | +0.023 (0.09) | 0.0% | 32 | +0.172 |
| combined | fixed | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 111 | 22 | +0.299 | -1.00 | 1.35 | +0.100 (0.29) | 0.0% | 18 | +0.183 |
| baseline_random | fixed | all | 7076 | 26 | +0.365 | -1.05 | 4.81 | — (—) | 0.7% | 1397 | +0.429 |
| baseline_random | fixed | SPY>200d & stock>200d | 4649 | 24 | +0.277 | -1.08 | 2.70 | — (—) | 0.3% | 949 | +0.298 |
| baseline_random | fixed | SPY>200d & stock>200d & RS>=0.8 | 1898 | 24 | +0.238 | -1.09 | 1.79 | — (—) | 0.4% | 418 | +0.038 |
| baseline_random | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1721 | 23 | +0.204 | -1.09 | 1.33 | — (—) | 0.2% | 361 | +0.141 |
| breakout | wide | all | 1949 | 33 | +0.187 | -0.99 | 1.42 | -0.236 (-3.44) | 0.3% | 393 | +0.160 |
| breakout | wide | SPY>200d & stock>200d | 1600 | 33 | +0.208 | -1.00 | 1.46 | -0.056 (-0.90) | 0.2% | 330 | +0.212 |
| breakout | wide | SPY>200d & stock>200d & RS>=0.8 | 676 | 33 | +0.263 | -0.97 | 1.15 | -0.071 (-0.87) | 0.0% | 140 | +0.122 |
| breakout | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 638 | 33 | +0.269 | -0.96 | 1.27 | -0.031 (-0.37) | 0.0% | 135 | +0.171 |
| breakout | wide | score>=70 & SPY>200d & stock>200d | 157 | 32 | +0.197 | -0.92 | 0.99 | -0.104 (-0.54) | 0.0% | 27 | +0.447 |
| breakout | wide | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 104 | 33 | +0.321 | -0.92 | 1.31 | -0.030 (-0.14) | 0.0% | 15 | +0.596 |
| momentum | wide | all | 1871 | 33 | +0.196 | -1.02 | 1.82 | -0.200 (-2.78) | 0.1% | 392 | +0.142 |
| momentum | wide | SPY>200d & stock>200d | 1670 | 33 | +0.242 | -1.02 | 1.98 | -0.034 (-0.58) | 0.1% | 364 | +0.182 |
| momentum | wide | SPY>200d & stock>200d & RS>=0.8 | 724 | 34 | +0.255 | -0.99 | 1.21 | -0.096 (-1.39) | 0.0% | 161 | +0.037 |
| momentum | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 687 | 34 | +0.263 | -0.99 | 1.42 | -0.038 (-0.50) | 0.0% | 157 | +0.070 |
| momentum | wide | score>=70 & SPY>200d & stock>200d | 16 | 25 | -0.020 | -0.93 | 0.27 | -0.059 (-0.13) | 0.0% | 5 | -0.729 |
| momentum | wide | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 8 | 38 | +0.680 | -0.59 | 0.87 | +0.122 (0.16) | 0.0% | 3 | -0.796 |
| combined | wide | all | 2463 | 33 | +0.184 | -1.01 | 1.60 | -0.225 (-3.51) | 0.3% | 497 | +0.165 |
| combined | wide | SPY>200d & stock>200d | 2114 | 33 | +0.202 | -1.02 | 1.62 | -0.059 (-1.19) | 0.1% | 438 | +0.205 |
| combined | wide | SPY>200d & stock>200d & RS>=0.8 | 922 | 34 | +0.268 | -0.98 | 1.42 | -0.050 (-0.83) | 0.0% | 192 | +0.067 |
| combined | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 875 | 34 | +0.272 | -0.99 | 1.52 | +0.001 (0.02) | 0.0% | 187 | +0.104 |
| combined | wide | score>=70 & SPY>200d & stock>200d | 169 | 32 | +0.198 | -0.91 | 1.18 | -0.078 (-0.43) | 0.0% | 32 | +0.263 |
| combined | wide | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 110 | 33 | +0.356 | -0.91 | 1.46 | -0.005 (-0.02) | 0.0% | 18 | +0.364 |
| baseline_random | wide | all | 5074 | 38 | +0.333 | -0.94 | 4.92 | — (—) | 0.8% | 997 | +0.395 |
| baseline_random | wide | SPY>200d & stock>200d | 3517 | 35 | +0.274 | -0.98 | 3.10 | — (—) | 0.3% | 725 | +0.293 |
| baseline_random | wide | SPY>200d & stock>200d & RS>=0.8 | 1481 | 35 | +0.239 | -1.01 | 2.34 | — (—) | 0.4% | 319 | +0.096 |
| baseline_random | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1353 | 33 | +0.209 | -1.01 | 2.03 | — (—) | 0.3% | 282 | +0.204 |

## Momentum rotation — universe: all (from 2018-02-26, 20 bps per side)

| benchmark | CAGR | max DD | Sharpe | train+val Sharpe | OOS CAGR | OOS Sharpe |
|---|---|---|---|---|---|---|
| SPY buy-and-hold | +13.6% | -34% | 0.77 | 0.74 | +15.2% | 0.91 |
| equal-weight universe (no costs) | +24.7% | -42% | 0.97 | 0.98 | +22.6% | 0.94 |

| rule set | trades/yr | exposure | win% | avg trade | avg days | CAGR | max DD | Sharpe | train+val Sharpe | OOS CAGR | OOS Sharpe | vs random | CAGR @40 / @70 bps | without best stock |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| top5, in RS>=0.8, out RS<0.5 | 10 | 93% | 41 | +19.4% | 111 | +16.1% | -80% | 0.55 | 0.44 | +46.4% | 0.88 | 30% | +15.3% / +14.1% | SE: +21.2%, Sharpe 0.62 |
| top5, in RS>=0.8, out RS<0.5, stop -20% | 15 | 92% | 34 | +20.2% | 77 | +27.8% | -71% | 0.70 | 0.76 | +13.0% | 0.52 | 65% | +26.6% / +24.7% | SE: +23.5%, Sharpe 0.65 |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d | 21 | 81% | 37 | +5.7% | 48 | +8.2% | -74% | 0.41 | 0.59 | -22.1% | -0.10 | 15% | +6.5% / +4.0% | MARA: +4.6%, Sharpe 0.34 |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | 26 | 80% | 34 | +3.7% | 39 | +7.5% | -71% | 0.40 | 0.52 | -13.8% | 0.05 | 5% | +5.6% / +2.8% | CELH: +13.2%, Sharpe 0.50 |
| top5, in RS>=0.8, out RS<0.7 | 12 | 93% | 43 | +13.4% | 93 | +18.4% | -76% | 0.58 | 0.48 | +52.1% | 0.93 | 55% | +17.4% / +15.7% | ENPH: +16.8%, Sharpe 0.56 |
| top5, in RS>=0.8, out RS<0.7, stop -20% | 18 | 92% | 33 | +10.0% | 63 | +17.8% | -77% | 0.57 | 0.46 | +56.8% | 0.99 | 45% | +16.3% / +14.1% | VKTX: +11.6%, Sharpe 0.48 |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d | 23 | 80% | 36 | +2.6% | 44 | +2.7% | -79% | 0.32 | 0.37 | -2.6% | 0.27 | 0% | +0.9% / -1.6% | TSLA: +8.7%, Sharpe 0.43 |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | 28 | 80% | 32 | +2.9% | 36 | +4.2% | -73% | 0.34 | 0.39 | -1.6% | 0.28 | 10% | +2.1% / -0.8% | CELH: +3.0%, Sharpe 0.32 |
| top8, in RS>=0.8, out RS<0.5 | 17 | 92% | 41 | +21.4% | 106 | +27.2% | -69% | 0.73 | 0.78 | +21.8% | 0.63 | 65% | +26.3% / +25.0% | SE: +26.1%, Sharpe 0.70 |
| top8, in RS>=0.8, out RS<0.5, stop -20% | 24 | 92% | 35 | +14.9% | 73 | +26.1% | -62% | 0.70 | 0.78 | +14.9% | 0.55 | 80% | +24.9% / +23.0% | SE: +21.2%, Sharpe 0.63 |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d | 30 | 80% | 39 | +9.2% | 53 | +24.8% | -58% | 0.69 | 0.76 | +14.4% | 0.53 | 80% | +23.1% / +20.6% | APP: +18.1%, Sharpe 0.58 |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | 37 | 80% | 35 | +7.2% | 43 | +23.3% | -67% | 0.67 | 0.73 | +16.8% | 0.56 | 70% | +21.4% / +18.7% | NIO: +24.4%, Sharpe 0.69 |
| top8, in RS>=0.8, out RS<0.7 | 19 | 92% | 49 | +19.0% | 95 | +29.9% | -60% | 0.75 | 0.75 | +40.5% | 0.85 | 75% | +28.8% / +27.1% | MARA: +24.6%, Sharpe 0.68 |
| top8, in RS>=0.8, out RS<0.7, stop -20% | 28 | 91% | 33 | +16.0% | 64 | +24.8% | -72% | 0.67 | 0.65 | +37.6% | 0.81 | 60% | +23.2% / +21.0% | MARA: +16.4%, Sharpe 0.55 |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d | 33 | 80% | 40 | +7.4% | 48 | +16.9% | -55% | 0.56 | 0.63 | +10.5% | 0.46 | 30% | +15.1% / +12.4% | MARA: +17.7%, Sharpe 0.58 |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | 40 | 80% | 34 | +9.7% | 39 | +24.9% | -64% | 0.67 | 0.74 | +14.2% | 0.52 | 85% | +22.7% / +19.4% | MARA: +20.7%, Sharpe 0.61 |
| top8, in RS>=0.8, out RS<0.5, 12-1 month momentum | 19 | 92% | 32 | +19.7% | 96 | +22.5% | -62% | 0.65 | 0.69 | +21.3% | 0.62 | 60% | +21.5% / +20.0% | SE: +18.5%, Sharpe 0.59 |
| top8, in RS>=0.8, out RS<0.5, monthly | 12 | 94% | 42 | +49.0% | 154 | +35.8% | -55% | 0.85 | 0.84 | +54.7% | 0.97 | 85% | +35.1% / +34.1% | ENPH: +29.8%, Sharpe 0.77 |
| top8, in RS>=0.8, out RS<0.5, volatility-adjusted | 15 | 93% | 49 | +27.0% | 127 | +32.5% | -47% | 0.88 | 0.96 | +36.8% | 0.83 | 100% | +31.6% / +30.3% | RKLB: +31.1%, Sharpe 0.86 |
| top8, in RS>=0.8, out RS<0.5, max 2/sector | 16 | 92% | 41 | +26.3% | 109 | +37.6% | -56% | 0.88 | 0.95 | +28.9% | 0.72 | 100% | +36.9% / +35.5% | SE: +36.5%, Sharpe 0.83 |
| top8, in RS>=0.8, out RS<0.5, max 3/sector | 17 | 94% | 42 | +24.9% | 108 | +31.6% | -58% | 0.78 | 0.84 | +26.7% | 0.69 | 90% | +30.6% / +29.3% | SE: +29.0%, Sharpe 0.74 |
| top8, in RS>=0.8, out RS<0.5, sell below 50d | 61 | 87% | 35 | +10.0% | 28 | +45.7% | -60% | 0.96 | 1.15 | +11.4% | 0.47 | 100% | +41.7% / +36.0% | MARA: +34.9%, Sharpe 0.84 |
| top8, in RS>=0.8, out RS<0.5, sell below 50d after +30% over 200d | 58 | 88% | 38 | +10.6% | 30 | +31.6% | -59% | 0.80 | 0.96 | +10.9% | 0.47 | 95% | +28.0% / +22.9% | MARA: +33.0%, Sharpe 0.82 |

## Momentum rotation — universe: largecap_2015 (from 2018-02-26, 20 bps per side)

| benchmark | CAGR | max DD | Sharpe | train+val Sharpe | OOS CAGR | OOS Sharpe |
|---|---|---|---|---|---|---|
| SPY buy-and-hold | +13.6% | -34% | 0.77 | 0.74 | +15.2% | 0.91 |
| equal-weight universe (no costs) | +14.2% | -37% | 0.81 | 0.71 | +19.4% | 1.35 |

| rule set | trades/yr | exposure | win% | avg trade | avg days | CAGR | max DD | Sharpe | train+val Sharpe | OOS CAGR | OOS Sharpe | vs random | CAGR @40 / @70 bps | without best stock |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| top5, in RS>=0.8, out RS<0.5 | 10 | 95% | 49 | +9.0% | 115 | +15.4% | -36% | 0.68 | 0.59 | +28.4% | 0.98 | 100% | +14.5% / +13.2% | DVN: +12.1%, Sharpe 0.59 |
| top5, in RS>=0.8, out RS<0.5, stop -20% | 11 | 94% | 51 | +8.9% | 111 | +15.7% | -36% | 0.70 | 0.61 | +28.2% | 0.97 | 100% | +14.8% / +13.5% | DVN: +12.7%, Sharpe 0.61 |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d | 20 | 81% | 47 | +3.1% | 50 | +10.5% | -26% | 0.56 | 0.58 | +9.7% | 0.48 | 90% | +8.7% / +6.2% | AVGO: +10.7%, Sharpe 0.59 |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | 20 | 81% | 48 | +3.1% | 50 | +10.6% | -26% | 0.56 | 0.59 | +9.8% | 0.48 | 75% | +8.9% / +6.3% | AVGO: +10.8%, Sharpe 0.59 |
| top5, in RS>=0.8, out RS<0.7 | 14 | 94% | 47 | +4.8% | 84 | +11.3% | -36% | 0.54 | 0.53 | +14.6% | 0.59 | 100% | +10.2% / +8.5% | INTC: +9.6%, Sharpe 0.50 |
| top5, in RS>=0.8, out RS<0.7, stop -20% | 14 | 95% | 47 | +5.4% | 82 | +13.5% | -33% | 0.61 | 0.62 | +14.2% | 0.58 | 100% | +12.3% / +10.5% | INTC: +12.1%, Sharpe 0.59 |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d | 23 | 81% | 46 | +2.4% | 44 | +9.0% | -29% | 0.50 | 0.59 | +2.9% | 0.24 | 100% | +7.1% / +4.2% | AVGO: +7.8%, Sharpe 0.46 |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | 23 | 81% | 46 | +2.4% | 44 | +9.1% | -29% | 0.50 | 0.60 | +2.7% | 0.23 | 100% | +7.1% / +4.3% | AVGO: +8.0%, Sharpe 0.47 |
| top8, in RS>=0.8, out RS<0.5 | 17 | 94% | 47 | +8.2% | 112 | +15.1% | -29% | 0.73 | 0.66 | +22.7% | 0.97 | 100% | +14.2% / +12.9% | DVN: +12.8%, Sharpe 0.66 |
| top8, in RS>=0.8, out RS<0.5, stop -20% | 18 | 94% | 46 | +6.8% | 105 | +13.5% | -29% | 0.67 | 0.60 | +21.3% | 0.92 | 100% | +12.6% / +11.2% | DVN: +11.3%, Sharpe 0.60 |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d | 30 | 80% | 45 | +2.6% | 52 | +8.6% | -28% | 0.53 | 0.53 | +8.7% | 0.51 | 95% | +7.0% / +4.6% | DVN: +7.9%, Sharpe 0.50 |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | 31 | 80% | 44 | +2.5% | 51 | +8.3% | -27% | 0.52 | 0.51 | +8.6% | 0.51 | 80% | +6.7% / +4.3% | DVN: +7.8%, Sharpe 0.50 |
| top8, in RS>=0.8, out RS<0.7 | 22 | 93% | 48 | +4.5% | 82 | +12.4% | -26% | 0.64 | 0.62 | +15.1% | 0.72 | 95% | +11.2% / +9.5% | META: +9.5%, Sharpe 0.52 |
| top8, in RS>=0.8, out RS<0.7, stop -20% | 23 | 93% | 47 | +4.5% | 79 | +11.9% | -29% | 0.62 | 0.59 | +14.4% | 0.70 | 100% | +10.7% / +8.8% | AVGO: +9.6%, Sharpe 0.53 |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d | 35 | 80% | 47 | +2.0% | 45 | +8.2% | -29% | 0.52 | 0.54 | +6.8% | 0.43 | 95% | +6.4% / +3.7% | AVGO: +7.6%, Sharpe 0.49 |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | 36 | 80% | 47 | +1.9% | 45 | +8.0% | -29% | 0.50 | 0.52 | +6.7% | 0.42 | 95% | +6.1% / +3.4% | AVGO: +7.4%, Sharpe 0.48 |
| top8, in RS>=0.8, out RS<0.5, 12-1 month momentum | 19 | 90% | 33 | +3.1% | 93 | +4.7% | -40% | 0.32 | 0.37 | +0.6% | 0.13 | 25% | +3.8% / +2.5% | GE: +3.1%, Sharpe 0.25 |
| top8, in RS>=0.8, out RS<0.5, monthly | 13 | 94% | 50 | +9.8% | 144 | +12.4% | -27% | 0.62 | 0.62 | +12.7% | 0.60 | 100% | +13.2% / +12.2% | DVN: +12.2%, Sharpe 0.61 |
| top8, in RS>=0.8, out RS<0.5, volatility-adjusted | 16 | 93% | 55 | +6.6% | 114 | +12.5% | -23% | 0.73 | 0.67 | +15.8% | 0.99 | 95% | +11.7% / +10.4% | GE: +9.8%, Sharpe 0.60 |
| top8, in RS>=0.8, out RS<0.5, max 2/sector | 18 | 93% | 44 | +6.3% | 106 | +11.2% | -30% | 0.59 | 0.50 | +20.1% | 0.86 | 95% | +10.3% / +8.9% | DVN: +9.4%, Sharpe 0.52 |
| top8, in RS>=0.8, out RS<0.5, max 3/sector | 17 | 94% | 45 | +7.2% | 107 | +13.4% | -29% | 0.67 | 0.59 | +21.6% | 0.91 | 95% | +12.5% / +11.2% | DVN: +11.7%, Sharpe 0.61 |
| top8, in RS>=0.8, out RS<0.5, sell below 50d | 63 | 87% | 36 | +0.8% | 28 | +5.8% | -25% | 0.40 | 0.51 | -2.0% | -0.01 | 50% | +2.7% / -1.8% | DVN: +4.4%, Sharpe 0.33 |
| top8, in RS>=0.8, out RS<0.5, sell below 50d after +30% over 200d | 33 | 90% | 45 | +2.5% | 54 | +9.2% | -26% | 0.56 | 0.60 | +5.4% | 0.38 | 90% | +7.5% / +4.9% | AVGO: +8.8%, Sharpe 0.54 |

## Rotation: pre-registered selection (2015 large caps, train+validation only)

Gates: train+val Sharpe > SPY's, ranking beats >= 90% of random selections, CAGR without the single best stock >= SPY's, max drawdown at most 10 points worse than SPY's.

**Chosen: none — no rule set passed every gate**

| rule set | passes | train+val Sharpe | failed gates |
|---|---|---|---|
| top5, in RS>=0.8, out RS<0.5 | ❌ | 0.59 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top5, in RS>=0.8, out RS<0.5, stop -20% | ❌ | 0.61 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d | ❌ | 0.58 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | ❌ | 0.59 | train_val_sharpe_beats_spy, ranking_beats_random, without_best_stock_beats_spy |
| top5, in RS>=0.8, out RS<0.7 | ❌ | 0.53 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top5, in RS>=0.8, out RS<0.7, stop -20% | ❌ | 0.62 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d | ❌ | 0.59 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | ❌ | 0.60 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5 | ❌ | 0.66 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5, stop -20% | ❌ | 0.60 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d | ❌ | 0.53 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | ❌ | 0.51 | train_val_sharpe_beats_spy, ranking_beats_random, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.7 | ❌ | 0.62 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.7, stop -20% | ❌ | 0.59 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d | ❌ | 0.54 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | ❌ | 0.52 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5, 12-1 month momentum | ❌ | 0.37 | train_val_sharpe_beats_spy, ranking_beats_random, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5, monthly | ❌ | 0.62 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5, volatility-adjusted | ❌ | 0.67 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5, max 2/sector | ❌ | 0.50 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5, max 3/sector | ❌ | 0.59 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5, sell below 50d | ❌ | 0.51 | train_val_sharpe_beats_spy, ranking_beats_random, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5, sell below 50d after +30% over 200d | ❌ | 0.60 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |

Calendar-year returns (2015 large caps, 20 bps per side):

| | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|---|---|---|---|
| SPY | -8% | +31% | +18% | +29% | -18% | +26% | +25% | +18% | +9% |
| equal-weight group | -8% | +29% | +14% | +31% | -4% | +16% | +16% | +17% | +18% |
| top5, in RS>=0.8, out RS<0.5 | -4% | +14% | +12% | +22% | +0% | +11% | +37% | +15% | +35% |
| top5, in RS>=0.8, out RS<0.5, stop -20% | -4% | +14% | +12% | +22% | -0% | +14% | +36% | +14% | +35% |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d | +0% | +3% | +16% | +21% | -1% | +21% | +19% | +9% | +6% |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | +1% | +3% | +16% | +22% | -1% | +21% | +19% | +9% | +6% |
| top5, in RS>=0.8, out RS<0.7 | -6% | +8% | +7% | +21% | -4% | +19% | +30% | -2% | +32% |
| top5, in RS>=0.8, out RS<0.7, stop -20% | -5% | +7% | +9% | +22% | +10% | +21% | +30% | -2% | +32% |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d | +0% | -3% | +8% | +21% | -2% | +22% | +29% | -5% | +12% |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | +1% | -3% | +8% | +21% | -2% | +22% | +29% | -5% | +12% |
| top8, in RS>=0.8, out RS<0.5 | -7% | +8% | +17% | +28% | +0% | +23% | +27% | +22% | +19% |
| top8, in RS>=0.8, out RS<0.5, stop -20% | -10% | +8% | +11% | +33% | +1% | +20% | +22% | +23% | +16% |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d | +2% | -5% | +11% | +30% | -2% | +14% | +13% | +14% | +2% |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | -0% | -4% | +11% | +30% | -2% | +14% | +13% | +14% | +1% |
| top8, in RS>=0.8, out RS<0.7 | -7% | +9% | +17% | +18% | +2% | +20% | +25% | +6% | +22% |
| top8, in RS>=0.8, out RS<0.7, stop -20% | -8% | +6% | +13% | +18% | +6% | +21% | +25% | +5% | +22% |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d | +1% | +2% | +12% | +18% | -4% | +9% | +24% | +2% | +11% |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | -0% | +2% | +12% | +18% | -4% | +9% | +24% | +1% | +11% |
| top8, in RS>=0.8, out RS<0.5, 12-1 month momentum | -15% | +10% | +2% | +24% | -12% | +2% | +41% | -1% | +1% |
| top8, in RS>=0.8, out RS<0.5, monthly | -0% | +12% | +16% | +19% | -5% | +26% | +23% | +5% | +16% |
| top8, in RS>=0.8, out RS<0.5, volatility-adjusted | -2% | +17% | +3% | +22% | -8% | +18% | +38% | +20% | +9% |
| top8, in RS>=0.8, out RS<0.5, max 2/sector | -10% | +8% | +4% | +29% | -0% | +19% | +17% | +10% | +26% |
| top8, in RS>=0.8, out RS<0.5, max 3/sector | -9% | +8% | +10% | +29% | -1% | +24% | +22% | +18% | +21% |
| top8, in RS>=0.8, out RS<0.5, sell below 50d | -7% | +3% | +28% | +21% | +6% | +7% | +4% | +2% | -7% |
| top8, in RS>=0.8, out RS<0.5, sell below 50d after +30% over 200d | -8% | +10% | +26% | +13% | +6% | +22% | +7% | +6% | +2% |

## Rockets (from 2016-12-07, 20 bps per side, 10 slots x 10%, max 3 new per day)

Rocket day: close >= +jump vs previous close, volume >= 3x the 20-day average, close in the top quarter of the day's range, price >= $5, 20-day dollar volume >= $5M. Buy next open; sell next open after a close more than `trail` below the highest close, or after 40 sessions. 'Random' = same stocks, same liquidity filter, same exit, random dates.

SPY: +14.6%/yr, max DD -34%, Sharpe 0.84 · train+val +14.4%/yr, Sharpe 0.83

| variant | trades | win% | avg trade | median | ≥+50% | worst | random avg | excess vs random t (train+val) | 2015 large caps excess | CAGR | max DD | Sharpe | train+val CAGR / Sharpe | OOS CAGR | random-entry portfolio CAGR | without top 3 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| EPS surprise>0%, reaction>=5% | 1909 | 54 | +4.6% | +1.9% | 4.3% | -51% | +4.2% | -0.31% (-0.48) | -0.12% (n=566) | +8.3% | -41% | 0.48 | +10.8% / 0.58 | -2.9% | +21.3% | +8.3% |
| EPS surprise>0%, reaction>=10% | 929 | 54 | +6.2% | +2.0% | 6.1% | -51% | +4.2% | +0.85% (0.83) | +1.31% (n=131) | +21.7% | -40% | 0.92 | +22.1% / 0.96 | +13.1% | +21.3% | +22.8% |
| EPS surprise>10%, reaction>=5% | 1271 | 53 | +5.0% | +2.0% | 5.1% | -51% | +4.2% | +0.65% (0.80) | -0.47% (n=272) | +13.6% | -44% | 0.65 | +20.6% / 0.91 | -15.9% | +21.3% | +12.0% |
| EPS surprise>10%, reaction>=10% | 718 | 53 | +6.6% | +1.9% | 6.6% | -51% | +4.2% | +1.74% (1.44) | +1.56% (n=73) | +17.0% | -45% | 0.75 | +25.2% / 1.01 | -15.8% | +21.3% | +15.2% |
| EPS surprise>20%, reaction>=10%, volume>=2x, RS>=0.8 | 235 | 57 | +9.0% | +3.3% | 7.2% | -34% | +4.2% | +3.69% (1.72) | +3.49% (n=15) | +18.7% | -25% | 0.95 | +24.8% / 1.24 | -7.7% | +21.3% | +12.5% |
| EPS surprise>20%, reaction>=15%, volume>=2x, RS>=0.8 | 167 | 58 | +9.3% | +3.9% | 8.4% | -33% | +4.2% | +1.85% (0.77) | —% (n=4) | +15.2% | -21% | 0.92 | +18.6% / 1.15 | -1.5% | +21.3% | +10.6% |
| EPS surprise>20%, reaction>=10%, volume>=2x, RS>=0.8, trail 10% | 236 | 43 | +3.5% | -2.8% | 3.4% | -21% | +4.2% | -2.23% (-1.39) | +1.47% (n=15) | +7.4% | -20% | 0.67 | +10.6% / 0.90 | -5.2% | +21.3% | +4.6% |
| EPS surprise>20%, reaction>=10%, volume>=2x, RS>=0.8, trail 15% | 235 | 51 | +7.1% | +0.1% | 4.7% | -28% | +4.2% | +2.48% (1.27) | +2.83% (n=15) | +15.1% | -17% | 0.95 | +19.2% / 1.16 | -1.3% | +21.3% | +10.5% |
| EPS surprise>20%, reaction>=10%, volume>=2x, RS>=0.8, take-profit +30% | 235 | 60 | +6.7% | +5.5% | 0.4% | -34% | +4.2% | +2.34% (1.27) | +3.91% (n=15) | +14.3% | -22% | 0.90 | +19.2% / 1.19 | -4.4% | +21.3% | +11.9% |
| EPS surprise>20%, reaction>=10%, volume>=2x, RS>=0.8, take-profit +50% | 235 | 57 | +7.2% | +3.3% | 10.2% | -34% | +4.2% | +2.42% (1.25) | +5.27% (n=15) | +15.3% | -25% | 0.88 | +20.2% / 1.14 | -5.9% | +21.3% | +11.8% |
| EPS surprise>20%, reaction>=10%, volume>=2x, RS>=0.8, trail 15%, take-profit +30% | 235 | 51 | +5.7% | +0.1% | 0.4% | -28% | +4.2% | +1.50% (0.88) | +3.15% (n=15) | +12.3% | -17% | 0.94 | +15.8% / 1.16 | -0.7% | +21.3% | +10.0% |
| EPS surprise>0%, reaction>=10%, max 5 days | 948 | 50 | +0.3% | +0.1% | 0.1% | -29% | +4.2% | -4.30% (-3.95) | -2.44% (n=134) | +0.0% | -28% | 0.06 | +3.9% / 0.40 | -15.2% | +21.3% | -1.0% |
| EPS surprise>0%, reaction>=10%, max 10 days | 940 | 55 | +0.9% | +1.3% | 0.6% | -51% | +4.2% | -3.43% (-3.19) | -1.48% (n=133) | +7.7% | -27% | 0.54 | +9.1% / 0.64 | +1.9% | +21.3% | +4.5% |
| EPS surprise>0%, reaction>=10%, max 20 days | 934 | 55 | +1.9% | +1.4% | 0.9% | -51% | +4.2% | -2.58% (-2.92) | -0.49% (n=132) | +9.9% | -24% | 0.61 | +11.9% / 0.70 | +1.3% | +21.3% | +8.5% |
| jump>=8%, trail 15% | 983 | 45 | +3.9% | -2.7% | 5.2% | -52% | +2.2% | -0.42% (-0.41) | -1.40% (n=114) | +13.9% | -48% | 0.58 | +22.0% / 0.79 | -14.8% | +17.2% | +7.5% |
| jump>=8%, trail 25% | 981 | 51 | +5.4% | +0.6% | 6.7% | -61% | +2.9% | +0.17% (0.14) | -1.31% (n=114) | +14.7% | -69% | 0.58 | +21.3% / 0.76 | -10.4% | +16.9% | +10.8% |
| jump>=15%, trail 15% | 533 | 42 | +4.5% | -4.8% | 6.8% | -52% | +2.2% | -1.06% (-0.74) | -4.25% (n=24) | +16.7% | -37% | 0.67 | +19.9% / 0.75 | +5.3% | +17.2% | +10.4% |
| jump>=15%, trail 25% | 533 | 47 | +6.5% | -2.4% | 9.2% | -61% | +2.9% | +0.40% (0.22) | -4.48% (n=24) | +13.2% | -58% | 0.54 | +18.8% / 0.67 | -6.7% | +16.9% | +5.3% |

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
| combined | all | +0.90 | -0.45 | +0.34 | +1.09 | +0.03 | -0.44 | +0.54 | +0.42 | +0.23 | -0.08 |
| combined | SPY>200d & stock>200d | +0.99 | -0.44 | +0.08 | +0.92 | -0.03 | -0.79 | +0.39 | +0.43 | +0.18 | -0.07 |
| combined | SPY>200d & stock>200d & RS>=0.8 | +1.05 | -0.24 | +0.42 | +1.45 | -0.41 | -0.36 | +0.42 | +0.62 | +0.84 | +0.02 |
| combined | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | +1.11 | -0.10 | +0.54 | +1.34 | -0.52 | -0.07 | +0.39 | +0.47 | +0.81 | +0.24 |
| combined | score>=70 & SPY>200d & stock>200d | +0.67 | +0.65 | +0.45 | +1.15 | -0.54 | -0.96 | +0.48 | +0.69 | +0.54 | -0.11 |
| combined | score>=70 & SPY>200d & stock>200d & RS>=0.8 | +0.22 | +1.33 | +0.61 | +1.08 | -0.53 | -1.15 | +0.47 | +1.00 | +0.72 | -0.07 |
| baseline_random | all | +1.51 | +0.13 | +0.63 | +0.87 | +0.22 | -0.24 | +0.56 | +0.44 | +0.36 | +0.09 |
| baseline_random | SPY>200d & stock>200d | +1.47 | -0.23 | +0.51 | +1.14 | +0.16 | -0.68 | +0.33 | +0.37 | +0.26 | +0.06 |
| baseline_random | SPY>200d & stock>200d & RS>=0.8 | +1.24 | +0.01 | +0.58 | +1.36 | -0.19 | -0.38 | +0.48 | +0.42 | +0.46 | -0.12 |
| baseline_random | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | +1.08 | +0.26 | +0.61 | +1.12 | -0.15 | -0.34 | +0.58 | +0.44 | +0.58 | -0.08 |