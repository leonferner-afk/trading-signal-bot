# Strategy research

277 symbols with data (2 failed), 10 years of daily bars. Control group: 105 stocks that were already large caps in 2015. Primary cost 20 bps per side (USD account: courtage + slippage; 40 bps ≈ trading from a SEK account). Validation from 2023-03-05, out-of-sample (OOS) from 2025-01-04. Setups invalidated at the next open (skipped): 1302.

Portfolio: max 8 positions, max 3 new per day, 1% risk per trade, max 25% of equity per position, no leverage, marked to market daily. 'vs random' = share of 40 random-order portfolios from the same eligible trades that this ranking beat.

## Portfolio — universe: all

SPY buy-and-hold: +14.7%/yr, max DD -34%, Sharpe 0.83 · train+val Sharpe 0.81 · OOS +14.8%/yr, Sharpe 0.89

| rule set | trades/yr | exposure | win% | avgR | CAGR | max DD | Sharpe | train+val Sharpe | OOS CAGR | OOS Sharpe | vs random |
|---|---|---|---|---|---|---|---|---|---|---|---|
| random picks (reference) | 79.8 | 87% | 20 | +0.11 | +6.1% | -66% | 0.35 | 0.65 | -24.8% | -0.76 | — |
| random picks, trend filter | 69.5 | 77% | 21 | +0.28 | +11.7% | -50% | 0.54 | 0.74 | -4.6% | 0.01 | — |
| RS leaders, trend filter | 70.1 | 68% | 23 | +0.43 | +22.6% | -43% | 0.79 | 1.01 | -3.8% | 0.08 | 100% |
| RS leaders near 52w high | 62.8 | 76% | 24 | +0.46 | +20.9% | -44% | 0.78 | 0.94 | +12.0% | 0.51 | 100% |
| signals score>=70, trend | 47.1 | 62% | 21 | +0.29 | +9.8% | -35% | 0.55 | 0.74 | -5.9% | -0.13 | 10% |
| signals score>=70, trend, RS top 20% | 41.9 | 50% | 22 | +0.54 | +19.6% | -33% | 0.92 | 1.05 | +4.8% | 0.32 | 88% |
| signals, trend, RS top 20% | 78.0 | 78% | 22 | +0.66 | +38.0% | -48% | 1.10 | 1.27 | +22.9% | 0.72 | 100% |
| signals, trend, RS top 20%, near 52w high | 75.4 | 78% | 22 | +0.53 | +28.4% | -32% | 0.98 | 1.18 | +18.7% | 0.65 | 100% |

Cost sensitivity (full-period CAGR / Sharpe):

| rule set | 20 bps | 40 bps | 70 bps |
|---|---|---|---|
| RS leaders, trend filter | +22.6% / 0.79 | +19.1% / 0.70 | +14.1% / 0.56 |
| RS leaders near 52w high | +20.9% / 0.78 | +13.6% / 0.58 | +8.3% / 0.42 |
| signals score>=70, trend | +9.8% / 0.55 | +6.9% / 0.42 | +3.0% / 0.24 |
| signals score>=70, trend, RS top 20% | +19.6% / 0.92 | +17.0% / 0.82 | +13.2% / 0.67 |
| signals, trend, RS top 20% | +38.0% / 1.10 | +32.7% / 0.99 | +24.9% / 0.81 |
| signals, trend, RS top 20%, near 52w high | +28.4% / 0.98 | +23.0% / 0.84 | +15.4% / 0.63 |

Exit variant (stop 2.5 x ATR instead of 1.5 x ATR / structural):

| rule set | CAGR | max DD | Sharpe | OOS Sharpe |
|---|---|---|---|---|
| random picks (reference) | +9.5% | -55% | 0.54 | -0.12 |
| random picks, trend filter | +10.4% | -38% | 0.61 | 0.71 |
| RS leaders, trend filter | +22.1% | -25% | 1.03 | 0.43 |
| RS leaders near 52w high | +18.0% | -34% | 0.84 | 0.65 |
| signals score>=70, trend | +12.6% | -28% | 0.78 | -0.13 |
| signals score>=70, trend, RS top 20% | +16.7% | -27% | 0.99 | 0.28 |
| signals, trend, RS top 20% | +14.8% | -36% | 0.73 | 0.57 |
| signals, trend, RS top 20%, near 52w high | +18.7% | -24% | 0.89 | 0.29 |

### Per trade — universe: all (one position per symbol, t over monthly means)

| group | exit | policy | n | win% | avgR | medR | t | excess vs random (t) | ≥+50% | OOS n | OOS avgR |
|---|---|---|---|---|---|---|---|---|---|---|---|
| breakout | fixed | all | 6502 | 17 | +0.285 | -1.11 | 1.40 | -0.315 (-3.77) | 3.2% | 1479 | -0.003 |
| breakout | fixed | SPY>200d & stock>200d | 5157 | 16 | +0.234 | -1.12 | 0.77 | -0.212 (-2.65) | 2.9% | 1194 | -0.004 |
| breakout | fixed | SPY>200d & stock>200d & RS>=0.8 | 2143 | 17 | +0.401 | -1.08 | 1.47 | -0.173 (-1.68) | 5.3% | 517 | +0.410 |
| breakout | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1746 | 18 | +0.440 | -1.08 | 1.40 | -0.091 (-0.79) | 4.2% | 395 | +0.592 |
| breakout | fixed | score>=70 & SPY>200d & stock>200d | 740 | 22 | +0.452 | -1.00 | 2.13 | +0.006 (0.04) | 5.9% | 138 | +0.281 |
| breakout | fixed | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 452 | 23 | +0.570 | -0.98 | 2.53 | +0.110 (0.54) | 7.7% | 91 | +0.422 |
| momentum | fixed | all | 5392 | 22 | +0.256 | -1.04 | 1.80 | -0.321 (-4.50) | 3.6% | 1224 | +0.050 |
| momentum | fixed | SPY>200d & stock>200d | 4764 | 22 | +0.289 | -1.04 | 1.80 | -0.131 (-2.15) | 3.4% | 1107 | +0.071 |
| momentum | fixed | SPY>200d & stock>200d & RS>=0.8 | 1934 | 22 | +0.370 | -1.02 | 2.18 | -0.090 (-1.07) | 6.2% | 463 | +0.231 |
| momentum | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1595 | 23 | +0.378 | -1.03 | 2.12 | -0.033 (-0.37) | 4.5% | 370 | +0.219 |
| momentum | fixed | score>=70 & SPY>200d & stock>200d | 155 | 23 | +0.544 | -0.92 | 1.90 | +0.279 (1.05) | 12.9% | 37 | +0.890 |
| momentum | fixed | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 97 | 25 | +0.715 | -0.89 | 1.81 | +0.271 (0.73) | 15.5% | 27 | +0.911 |
| combined | fixed | all | 8199 | 19 | +0.273 | -1.07 | 1.68 | -0.314 (-4.65) | 3.3% | 1849 | +0.099 |
| combined | fixed | SPY>200d & stock>200d | 6756 | 19 | +0.238 | -1.08 | 1.02 | -0.190 (-3.02) | 3.0% | 1550 | +0.074 |
| combined | fixed | SPY>200d & stock>200d & RS>=0.8 | 2818 | 20 | +0.410 | -1.04 | 2.05 | -0.109 (-1.37) | 5.4% | 678 | +0.461 |
| combined | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 2318 | 21 | +0.423 | -1.05 | 2.03 | -0.032 (-0.40) | 4.2% | 524 | +0.556 |
| combined | fixed | score>=70 & SPY>200d & stock>200d | 816 | 23 | +0.472 | -0.98 | 1.84 | -0.013 (-0.10) | 6.6% | 160 | +0.313 |
| combined | fixed | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 499 | 23 | +0.576 | -0.96 | 2.18 | +0.040 (0.21) | 8.6% | 107 | +0.431 |
| baseline_random | fixed | all | 17518 | 25 | +0.364 | -1.03 | 5.13 | — (—) | 5.1% | 4031 | +0.278 |
| baseline_random | fixed | SPY>200d & stock>200d | 11067 | 23 | +0.337 | -1.04 | 3.34 | — (—) | 3.6% | 2530 | +0.193 |
| baseline_random | fixed | SPY>200d & stock>200d & RS>=0.8 | 4551 | 23 | +0.350 | -1.03 | 3.43 | — (—) | 6.3% | 1108 | +0.204 |
| baseline_random | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 3098 | 23 | +0.407 | -1.04 | 3.04 | — (—) | 3.9% | 684 | +0.274 |
| breakout | wide | all | 5236 | 33 | +0.299 | -0.95 | 3.23 | -0.155 (-3.31) | 5.4% | 1183 | +0.254 |
| breakout | wide | SPY>200d & stock>200d | 4207 | 33 | +0.308 | -0.96 | 2.32 | -0.076 (-1.72) | 4.9% | 962 | +0.265 |
| breakout | wide | SPY>200d & stock>200d & RS>=0.8 | 1788 | 34 | +0.429 | -0.93 | 2.54 | -0.079 (-1.32) | 8.9% | 432 | +0.350 |
| breakout | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1485 | 35 | +0.467 | -0.92 | 2.96 | +0.007 (0.11) | 7.2% | 335 | +0.326 |
| breakout | wide | score>=70 & SPY>200d & stock>200d | 712 | 33 | +0.385 | -0.91 | 2.40 | -0.017 (-0.16) | 9.1% | 132 | +0.170 |
| breakout | wide | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 429 | 34 | +0.479 | -0.90 | 2.78 | +0.065 (0.43) | 11.7% | 87 | +0.233 |
| momentum | wide | all | 4487 | 32 | +0.264 | -0.98 | 2.77 | -0.178 (-3.25) | 4.8% | 994 | +0.153 |
| momentum | wide | SPY>200d & stock>200d | 3980 | 33 | +0.304 | -0.98 | 2.84 | -0.047 (-0.97) | 4.6% | 903 | +0.178 |
| momentum | wide | SPY>200d & stock>200d & RS>=0.8 | 1631 | 33 | +0.351 | -0.96 | 2.48 | -0.098 (-1.67) | 7.8% | 390 | +0.242 |
| momentum | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1375 | 33 | +0.331 | -0.97 | 2.21 | -0.081 (-1.31) | 5.6% | 312 | +0.253 |
| momentum | wide | score>=70 & SPY>200d & stock>200d | 138 | 30 | +0.313 | -0.88 | 1.24 | -0.011 (-0.06) | 15.2% | 34 | +0.628 |
| momentum | wide | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 82 | 32 | +0.457 | -0.80 | 1.36 | -0.016 (-0.07) | 19.5% | 25 | +0.724 |
| combined | wide | all | 6249 | 33 | +0.281 | -0.97 | 3.14 | -0.172 (-3.84) | 5.1% | 1397 | +0.221 |
| combined | wide | SPY>200d & stock>200d | 5214 | 33 | +0.302 | -0.98 | 2.42 | -0.076 (-1.95) | 4.7% | 1190 | +0.224 |
| combined | wide | SPY>200d & stock>200d & RS>=0.8 | 2259 | 33 | +0.374 | -0.95 | 2.51 | -0.098 (-1.87) | 8.2% | 547 | +0.322 |
| combined | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1890 | 34 | +0.388 | -0.95 | 2.73 | -0.035 (-0.64) | 6.5% | 426 | +0.313 |
| combined | wide | score>=70 & SPY>200d & stock>200d | 772 | 33 | +0.376 | -0.90 | 1.96 | -0.043 (-0.47) | 9.2% | 150 | +0.242 |
| combined | wide | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 462 | 33 | +0.462 | -0.88 | 2.30 | -0.014 (-0.11) | 12.1% | 100 | +0.321 |
| baseline_random | wide | all | 12278 | 36 | +0.330 | -0.95 | 5.37 | — (—) | 6.3% | 2763 | +0.300 |
| baseline_random | wide | SPY>200d & stock>200d | 8145 | 34 | +0.312 | -0.97 | 3.72 | — (—) | 4.7% | 1859 | +0.200 |
| baseline_random | wide | SPY>200d & stock>200d & RS>=0.8 | 3402 | 34 | +0.341 | -0.97 | 3.69 | — (—) | 8.2% | 813 | +0.254 |
| baseline_random | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 2501 | 34 | +0.373 | -0.98 | 3.38 | — (—) | 5.2% | 545 | +0.289 |

## Portfolio — universe: largecap_2015

SPY buy-and-hold: +14.7%/yr, max DD -34%, Sharpe 0.83 · train+val Sharpe 0.81 · OOS +14.8%/yr, Sharpe 0.89

| rule set | trades/yr | exposure | win% | avgR | CAGR | max DD | Sharpe | train+val Sharpe | OOS CAGR | OOS Sharpe | vs random |
|---|---|---|---|---|---|---|---|---|---|---|---|
| random picks (reference) | 46.4 | 87% | 24 | +0.23 | +7.3% | -38% | 0.52 | 0.58 | +0.8% | 0.13 | — |
| random picks, trend filter | 36.7 | 75% | 24 | +0.20 | +4.5% | -30% | 0.39 | 0.65 | -14.1% | -0.97 | — |
| RS leaders, trend filter | 40.5 | 77% | 26 | +0.43 | +12.6% | -32% | 0.70 | 0.77 | +8.5% | 0.49 | 97% |
| RS leaders near 52w high | 41.1 | 76% | 25 | +0.47 | +14.7% | -20% | 0.83 | 0.77 | +14.9% | 0.78 | 100% |
| signals score>=70, trend | 14.7 | 36% | 23 | +0.27 | +3.0% | -16% | 0.36 | 0.36 | +3.0% | 0.34 | 30% |
| signals score>=70, trend, RS top 20% | 10.9 | 25% | 22 | +0.32 | +2.2% | -19% | 0.31 | 0.35 | +1.4% | 0.22 | 3% |
| signals, trend, RS top 20% | 41.5 | 78% | 22 | +0.33 | +6.5% | -30% | 0.48 | 0.52 | +4.5% | 0.35 | 47% |
| signals, trend, RS top 20%, near 52w high | 42.6 | 78% | 22 | +0.33 | +7.2% | -33% | 0.53 | 0.59 | +4.3% | 0.34 | 75% |

Cost sensitivity (full-period CAGR / Sharpe):

| rule set | 20 bps | 40 bps | 70 bps |
|---|---|---|---|
| RS leaders, trend filter | +12.6% / 0.70 | +9.4% / 0.56 | +4.9% / 0.34 |
| RS leaders near 52w high | +14.7% / 0.83 | +11.4% / 0.67 | +6.7% / 0.44 |
| signals score>=70, trend | +3.0% / 0.36 | +1.6% / 0.22 | -0.4% / 0.01 |
| signals score>=70, trend, RS top 20% | +2.2% / 0.31 | +1.1% / 0.18 | -0.4% / -0.00 |
| signals, trend, RS top 20% | +6.5% / 0.48 | +3.2% / 0.28 | -1.6% / -0.01 |
| signals, trend, RS top 20%, near 52w high | +7.2% / 0.53 | +3.9% / 0.32 | -1.0% / 0.02 |

Exit variant (stop 2.5 x ATR instead of 1.5 x ATR / structural):

| rule set | CAGR | max DD | Sharpe | OOS Sharpe |
|---|---|---|---|---|
| random picks (reference) | +14.8% | -21% | 1.03 | 2.00 |
| random picks, trend filter | +11.6% | -21% | 0.94 | 1.51 |
| RS leaders, trend filter | +12.5% | -21% | 0.79 | 0.44 |
| RS leaders near 52w high | +8.9% | -20% | 0.60 | 0.15 |
| signals score>=70, trend | +2.1% | -16% | 0.29 | 0.55 |
| signals score>=70, trend, RS top 20% | +2.7% | -17% | 0.39 | 0.45 |
| signals, trend, RS top 20% | +8.3% | -21% | 0.60 | 0.41 |
| signals, trend, RS top 20%, near 52w high | +7.6% | -27% | 0.57 | 0.50 |

### Per trade — universe: largecap_2015 (one position per symbol, t over monthly means)

| group | exit | policy | n | win% | avgR | medR | t | excess vs random (t) | ≥+50% | OOS n | OOS avgR |
|---|---|---|---|---|---|---|---|---|---|---|---|
| breakout | fixed | all | 2291 | 17 | +0.081 | -1.16 | -0.53 | -0.525 (-4.63) | 0.2% | 470 | -0.204 |
| breakout | fixed | SPY>200d & stock>200d | 1883 | 16 | +0.002 | -1.17 | -0.66 | -0.310 (-2.83) | 0.1% | 395 | -0.212 |
| breakout | fixed | SPY>200d & stock>200d & RS>=0.8 | 767 | 18 | +0.274 | -1.12 | 1.19 | +0.070 (0.33) | 0.1% | 165 | +0.001 |
| breakout | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 719 | 18 | +0.301 | -1.12 | 1.28 | +0.133 (0.63) | 0.1% | 160 | +0.118 |
| breakout | fixed | score>=70 & SPY>200d & stock>200d | 159 | 21 | +0.183 | -1.02 | 0.96 | -0.050 (-0.18) | 0.0% | 27 | +0.414 |
| breakout | fixed | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 104 | 21 | +0.222 | -1.01 | 1.08 | +0.023 (0.06) | 0.0% | 15 | +0.442 |
| momentum | fixed | all | 2201 | 22 | +0.174 | -1.09 | 1.10 | -0.351 (-3.83) | 0.1% | 468 | +0.031 |
| momentum | fixed | SPY>200d & stock>200d | 1967 | 23 | +0.210 | -1.10 | 0.90 | -0.110 (-1.30) | 0.1% | 432 | +0.090 |
| momentum | fixed | SPY>200d & stock>200d & RS>=0.8 | 842 | 23 | +0.220 | -1.07 | 0.16 | -0.155 (-1.44) | 0.0% | 182 | +0.134 |
| momentum | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 799 | 22 | +0.207 | -1.08 | 0.03 | -0.121 (-1.06) | 0.0% | 176 | +0.179 |
| momentum | fixed | score>=70 & SPY>200d & stock>200d | 16 | 19 | +0.028 | -1.05 | 0.28 | -0.122 (-0.17) | 0.0% | 4 | -1.149 |
| momentum | fixed | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 9 | 22 | +0.681 | -0.91 | 0.62 | +0.095 (0.09) | 0.0% | 3 | -1.108 |
| combined | fixed | all | 3111 | 20 | +0.122 | -1.12 | 0.13 | -0.440 (-4.70) | 0.2% | 636 | -0.086 |
| combined | fixed | SPY>200d & stock>200d | 2659 | 20 | +0.090 | -1.13 | -0.21 | -0.229 (-2.76) | 0.1% | 550 | -0.055 |
| combined | fixed | SPY>200d & stock>200d & RS>=0.8 | 1139 | 20 | +0.206 | -1.08 | 0.15 | -0.141 (-1.46) | 0.0% | 235 | -0.018 |
| combined | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1079 | 20 | +0.201 | -1.09 | 0.23 | -0.081 (-0.84) | 0.0% | 228 | +0.077 |
| combined | fixed | score>=70 & SPY>200d & stock>200d | 171 | 22 | +0.209 | -1.02 | 1.12 | -0.027 (-0.11) | 0.0% | 31 | +0.212 |
| combined | fixed | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 111 | 22 | +0.298 | -1.00 | 1.34 | +0.112 (0.32) | 0.0% | 18 | +0.183 |
| baseline_random | fixed | all | 7088 | 26 | +0.363 | -1.05 | 4.85 | — (—) | 0.7% | 1404 | +0.457 |
| baseline_random | fixed | SPY>200d & stock>200d | 4658 | 24 | +0.275 | -1.08 | 2.76 | — (—) | 0.3% | 944 | +0.293 |
| baseline_random | fixed | SPY>200d & stock>200d & RS>=0.8 | 1902 | 23 | +0.233 | -1.09 | 1.78 | — (—) | 0.4% | 419 | +0.049 |
| baseline_random | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1724 | 23 | +0.198 | -1.09 | 1.33 | — (—) | 0.2% | 361 | +0.152 |
| breakout | wide | all | 1955 | 33 | +0.188 | -0.99 | 1.52 | -0.230 (-3.37) | 0.3% | 393 | +0.158 |
| breakout | wide | SPY>200d & stock>200d | 1608 | 33 | +0.203 | -1.00 | 1.53 | -0.062 (-1.01) | 0.2% | 332 | +0.199 |
| breakout | wide | SPY>200d & stock>200d & RS>=0.8 | 679 | 33 | +0.263 | -0.97 | 1.26 | -0.062 (-0.77) | 0.0% | 142 | +0.112 |
| breakout | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 641 | 33 | +0.269 | -0.96 | 1.40 | -0.024 (-0.28) | 0.0% | 137 | +0.164 |
| breakout | wide | score>=70 & SPY>200d & stock>200d | 159 | 32 | +0.179 | -0.92 | 0.70 | -0.166 (-0.88) | 0.0% | 27 | +0.432 |
| breakout | wide | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 104 | 32 | +0.316 | -0.92 | 1.27 | -0.032 (-0.14) | 0.0% | 15 | +0.564 |
| momentum | wide | all | 1869 | 33 | +0.194 | -1.02 | 1.99 | -0.184 (-2.54) | 0.1% | 389 | +0.131 |
| momentum | wide | SPY>200d & stock>200d | 1669 | 33 | +0.239 | -1.02 | 2.14 | -0.026 (-0.43) | 0.1% | 361 | +0.172 |
| momentum | wide | SPY>200d & stock>200d & RS>=0.8 | 726 | 34 | +0.260 | -0.99 | 1.38 | -0.082 (-1.20) | 0.0% | 159 | +0.041 |
| momentum | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 689 | 34 | +0.269 | -0.99 | 1.60 | -0.026 (-0.34) | 0.0% | 155 | +0.074 |
| momentum | wide | score>=70 & SPY>200d & stock>200d | 15 | 33 | +0.006 | -0.94 | 0.33 | -0.037 (-0.08) | 0.0% | 4 | -0.808 |
| momentum | wide | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 8 | 50 | +0.718 | -0.44 | 0.92 | +0.144 (0.19) | 0.0% | 3 | -0.695 |
| combined | wide | all | 2465 | 33 | +0.186 | -1.01 | 1.77 | -0.214 (-3.34) | 0.3% | 495 | +0.159 |
| combined | wide | SPY>200d & stock>200d | 2118 | 33 | +0.203 | -1.02 | 1.79 | -0.055 (-1.12) | 0.1% | 437 | +0.195 |
| combined | wide | SPY>200d & stock>200d & RS>=0.8 | 928 | 34 | +0.275 | -0.98 | 1.55 | -0.042 (-0.70) | 0.0% | 193 | +0.055 |
| combined | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 881 | 34 | +0.280 | -0.99 | 1.63 | +0.005 (0.08) | 0.0% | 188 | +0.095 |
| combined | wide | score>=70 & SPY>200d & stock>200d | 170 | 32 | +0.184 | -0.92 | 0.92 | -0.140 (-0.78) | 0.0% | 31 | +0.272 |
| combined | wide | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 110 | 33 | +0.354 | -0.91 | 1.45 | +0.001 (0.00) | 0.0% | 18 | +0.354 |
| baseline_random | wide | all | 5080 | 38 | +0.330 | -0.95 | 4.92 | — (—) | 0.8% | 992 | +0.418 |
| baseline_random | wide | SPY>200d & stock>200d | 3517 | 35 | +0.273 | -0.99 | 3.20 | — (—) | 0.3% | 718 | +0.280 |
| baseline_random | wide | SPY>200d & stock>200d & RS>=0.8 | 1483 | 35 | +0.239 | -1.01 | 2.41 | — (—) | 0.4% | 319 | +0.105 |
| baseline_random | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1354 | 33 | +0.213 | -1.01 | 2.13 | — (—) | 0.3% | 282 | +0.211 |

## Momentum rotation — universe: all (from 2018-02-16, 20 bps per side)

| benchmark | CAGR | max DD | Sharpe | train+val Sharpe | OOS CAGR | OOS Sharpe |
|---|---|---|---|---|---|---|
| SPY buy-and-hold | +14.1% | -34% | 0.79 | 0.76 | +14.8% | 0.89 |
| equal-weight universe (no costs) | +25.8% | -42% | 1.00 | 1.01 | +22.2% | 0.93 |

| rule set | trades/yr | exposure | win% | avg trade | avg days | CAGR | max DD | Sharpe | train+val Sharpe | OOS CAGR | OOS Sharpe | vs random | CAGR @40 / @70 bps | without best stock |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| top5, in RS>=0.8, out RS<0.5 | 10 | 93% | 41 | +19.5% | 111 | +17.6% | -80% | 0.57 | 0.50 | +35.4% | 0.77 | 15% | +16.8% / +15.5% | SE: +21.9%, Sharpe 0.63 |
| top5, in RS>=0.8, out RS<0.5, stop -20% | 15 | 91% | 34 | +18.4% | 75 | +24.2% | -77% | 0.65 | 0.69 | +11.9% | 0.51 | 50% | +22.9% / +21.0% | SE: +25.6%, Sharpe 0.68 |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d | 21 | 81% | 37 | +5.8% | 48 | +9.6% | -74% | 0.44 | 0.64 | -27.4% | -0.21 | 20% | +7.9% / +5.3% | MARA: +6.0%, Sharpe 0.36 |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | 26 | 80% | 34 | +3.9% | 39 | +8.8% | -71% | 0.42 | 0.53 | -14.1% | 0.05 | 15% | +6.8% / +4.0% | CELH: +14.5%, Sharpe 0.52 |
| top5, in RS>=0.8, out RS<0.7 | 12 | 93% | 44 | +13.5% | 94 | +19.9% | -76% | 0.60 | 0.53 | +37.1% | 0.79 | 45% | +18.8% / +17.2% | ENPH: +18.1%, Sharpe 0.57 |
| top5, in RS>=0.8, out RS<0.7, stop -20% | 18 | 92% | 34 | +10.1% | 63 | +19.0% | -77% | 0.59 | 0.50 | +39.9% | 0.82 | 45% | +17.5% / +15.2% | VKTX: +11.7%, Sharpe 0.48 |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d | 23 | 80% | 37 | +2.7% | 44 | +4.2% | -79% | 0.34 | 0.46 | -19.8% | -0.01 | 0% | +2.4% / -0.2% | TSLA: +10.3%, Sharpe 0.45 |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | 28 | 80% | 33 | +3.1% | 36 | +5.4% | -73% | 0.36 | 0.45 | -13.8% | 0.09 | 10% | +3.3% / +0.3% | CELH: +4.3%, Sharpe 0.34 |
| top8, in RS>=0.8, out RS<0.5 | 17 | 92% | 42 | +21.4% | 106 | +28.2% | -69% | 0.74 | 0.81 | +16.8% | 0.56 | 70% | +27.3% / +25.9% | SE: +27.2%, Sharpe 0.72 |
| top8, in RS>=0.8, out RS<0.5, stop -20% | 24 | 92% | 35 | +14.6% | 73 | +25.8% | -62% | 0.70 | 0.78 | +11.1% | 0.50 | 55% | +24.5% / +22.5% | SE: +21.1%, Sharpe 0.62 |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d | 30 | 80% | 39 | +9.3% | 53 | +26.0% | -58% | 0.71 | 0.80 | +10.7% | 0.47 | 85% | +24.2% / +21.7% | APP: +19.2%, Sharpe 0.60 |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | 37 | 80% | 36 | +7.2% | 43 | +22.9% | -67% | 0.67 | 0.74 | +10.3% | 0.47 | 70% | +21.0% / +18.2% | NIO: +24.0%, Sharpe 0.68 |
| top8, in RS>=0.8, out RS<0.7 | 19 | 92% | 51 | +19.1% | 95 | +31.0% | -60% | 0.77 | 0.81 | +21.1% | 0.62 | 65% | +29.9% / +28.2% | MARA: +26.0%, Sharpe 0.71 |
| top8, in RS>=0.8, out RS<0.7, stop -20% | 28 | 91% | 34 | +15.7% | 63 | +25.0% | -72% | 0.67 | 0.71 | +15.6% | 0.56 | 45% | +23.5% / +21.2% | MARA: +18.7%, Sharpe 0.58 |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d | 33 | 80% | 41 | +7.5% | 48 | +18.0% | -55% | 0.58 | 0.69 | -5.0% | 0.22 | 45% | +16.2% / +13.6% | MARA: +19.1%, Sharpe 0.61 |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | 41 | 80% | 34 | +9.7% | 39 | +24.8% | -64% | 0.67 | 0.79 | -4.0% | 0.23 | 85% | +22.5% / +19.2% | MARA: +21.5%, Sharpe 0.62 |
| top8, in RS>=0.8, out RS<0.5, 12-1 month momentum | 19 | 91% | 34 | +19.9% | 97 | +22.0% | -62% | 0.65 | 0.67 | +20.0% | 0.61 | 60% | +21.0% / +19.5% | SE: +19.6%, Sharpe 0.61 |
| top8, in RS>=0.8, out RS<0.5, monthly | 12 | 94% | 42 | +49.0% | 154 | +36.6% | -55% | 0.87 | 0.85 | +51.8% | 0.95 | 85% | +36.0% / +35.0% | ENPH: +30.7%, Sharpe 0.78 |
| top8, in RS>=0.8, out RS<0.5, volatility-adjusted | 15 | 93% | 48 | +27.6% | 127 | +35.1% | -47% | 0.93 | 1.06 | +26.9% | 0.70 | 100% | +34.2% / +29.4% | RKLB: +32.7%, Sharpe 0.90 |
| top8, in RS>=0.8, out RS<0.5, max 2/sector | 17 | 91% | 43 | +30.5% | 109 | +38.3% | -65% | 0.83 | 0.85 | +32.4% | 0.76 | 95% | +37.2% / +35.3% | GME: +36.6%, Sharpe 0.87 |
| top8, in RS>=0.8, out RS<0.5, max 3/sector | 17 | 94% | 42 | +25.0% | 108 | +32.9% | -58% | 0.80 | 0.87 | +22.0% | 0.63 | 85% | +32.0% / +30.6% | SE: +30.1%, Sharpe 0.75 |
| top8, in RS>=0.8, out RS<0.5, sell below 50d | 61 | 87% | 36 | +10.0% | 28 | +47.2% | -60% | 0.98 | 1.26 | -14.1% | 0.05 | 100% | +43.2% / +37.4% | MARA: +36.3%, Sharpe 0.86 |
| top8, in RS>=0.8, out RS<0.5, sell below 50d after +30% over 200d | 58 | 88% | 38 | +10.6% | 30 | +32.8% | -59% | 0.82 | 1.06 | -11.2% | 0.10 | 95% | +29.2% / +24.0% | MARA: +34.1%, Sharpe 0.84 |

## Momentum rotation — universe: largecap_2015 (from 2018-02-16, 20 bps per side)

| benchmark | CAGR | max DD | Sharpe | train+val Sharpe | OOS CAGR | OOS Sharpe |
|---|---|---|---|---|---|---|
| SPY buy-and-hold | +14.1% | -34% | 0.79 | 0.76 | +14.8% | 0.89 |
| equal-weight universe (no costs) | +14.4% | -37% | 0.82 | 0.74 | +19.1% | 1.34 |

| rule set | trades/yr | exposure | win% | avg trade | avg days | CAGR | max DD | Sharpe | train+val Sharpe | OOS CAGR | OOS Sharpe | vs random | CAGR @40 / @70 bps | without best stock |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| top5, in RS>=0.8, out RS<0.5 | 10 | 95% | 48 | +8.8% | 115 | +15.1% | -36% | 0.68 | 0.59 | +27.5% | 0.95 | 95% | +14.2% / +12.9% | DVN: +12.6%, Sharpe 0.61 |
| top5, in RS>=0.8, out RS<0.5, stop -20% | 10 | 94% | 52 | +8.9% | 112 | +15.6% | -36% | 0.69 | 0.62 | +27.3% | 0.94 | 100% | +14.7% / +13.4% | DVN: +13.1%, Sharpe 0.62 |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d | 20 | 81% | 48 | +3.2% | 50 | +11.1% | -26% | 0.59 | 0.64 | +8.6% | 0.44 | 95% | +9.4% / +6.8% | AVGO: +11.3%, Sharpe 0.61 |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | 20 | 81% | 48 | +3.2% | 50 | +11.1% | -25% | 0.59 | 0.64 | +8.7% | 0.44 | 85% | +9.4% / +6.8% | AVGO: +11.3%, Sharpe 0.61 |
| top5, in RS>=0.8, out RS<0.7 | 14 | 94% | 48 | +4.9% | 84 | +11.7% | -36% | 0.55 | 0.55 | +14.2% | 0.58 | 90% | +10.6% / +8.8% | INTC: +10.0%, Sharpe 0.52 |
| top5, in RS>=0.8, out RS<0.7, stop -20% | 14 | 95% | 48 | +5.5% | 82 | +13.8% | -33% | 0.62 | 0.64 | +13.9% | 0.57 | 95% | +12.6% / +10.8% | INTC: +12.4%, Sharpe 0.60 |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d | 23 | 81% | 46 | +2.5% | 45 | +9.3% | -30% | 0.51 | 0.62 | +2.4% | 0.22 | 100% | +7.3% / +4.5% | AVGO: +8.1%, Sharpe 0.47 |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | 23 | 81% | 46 | +2.4% | 44 | +9.2% | -30% | 0.51 | 0.61 | +2.2% | 0.22 | 100% | +7.2% / +4.4% | AVGO: +8.1%, Sharpe 0.47 |
| top8, in RS>=0.8, out RS<0.5 | 17 | 94% | 45 | +7.9% | 109 | +14.8% | -29% | 0.72 | 0.65 | +22.9% | 0.97 | 100% | +13.9% / +12.6% | DVN: +12.8%, Sharpe 0.65 |
| top8, in RS>=0.8, out RS<0.5, stop -20% | 18 | 93% | 45 | +6.7% | 104 | +13.6% | -29% | 0.67 | 0.61 | +21.1% | 0.91 | 100% | +12.7% / +11.3% | DVN: +11.4%, Sharpe 0.60 |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d | 31 | 80% | 44 | +2.5% | 52 | +8.3% | -28% | 0.51 | 0.52 | +8.9% | 0.52 | 65% | +6.7% / +4.3% | DVN: +7.8%, Sharpe 0.50 |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | 31 | 80% | 44 | +2.5% | 51 | +8.3% | -28% | 0.51 | 0.52 | +8.8% | 0.52 | 90% | +6.7% / +4.3% | DVN: +7.8%, Sharpe 0.50 |
| top8, in RS>=0.8, out RS<0.7 | 23 | 93% | 48 | +4.4% | 82 | +12.2% | -26% | 0.63 | 0.61 | +14.2% | 0.69 | 90% | +11.0% / +9.2% | META: +9.3%, Sharpe 0.51 |
| top8, in RS>=0.8, out RS<0.7, stop -20% | 23 | 93% | 47 | +4.5% | 80 | +11.8% | -29% | 0.62 | 0.60 | +13.5% | 0.66 | 100% | +10.6% / +8.8% | AVGO: +9.5%, Sharpe 0.52 |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d | 35 | 80% | 47 | +1.9% | 45 | +8.0% | -29% | 0.50 | 0.54 | +5.9% | 0.38 | 95% | +6.2% / +3.5% | AVGO: +7.4%, Sharpe 0.48 |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | 36 | 80% | 47 | +1.9% | 45 | +7.9% | -29% | 0.50 | 0.54 | +5.8% | 0.38 | 95% | +6.1% / +3.4% | AVGO: +7.4%, Sharpe 0.48 |
| top8, in RS>=0.8, out RS<0.5, 12-1 month momentum | 19 | 90% | 34 | +3.2% | 95 | +4.9% | -40% | 0.33 | 0.40 | -1.2% | 0.05 | 10% | +4.0% / +2.7% | GE: +3.3%, Sharpe 0.26 |
| top8, in RS>=0.8, out RS<0.5, monthly | 13 | 93% | 50 | +9.8% | 144 | +12.4% | -27% | 0.62 | 0.64 | +10.9% | 0.54 | 100% | +13.2% / +12.2% | DVN: +12.2%, Sharpe 0.61 |
| top8, in RS>=0.8, out RS<0.5, volatility-adjusted | 16 | 93% | 55 | +6.7% | 115 | +12.8% | -23% | 0.74 | 0.70 | +15.4% | 0.96 | 100% | +12.0% / +10.7% | GE: +10.0%, Sharpe 0.61 |
| top8, in RS>=0.8, out RS<0.5, max 2/sector | 18 | 93% | 45 | +6.6% | 106 | +11.9% | -30% | 0.62 | 0.55 | +19.7% | 0.84 | 95% | +11.0% / +9.6% | DVN: +9.8%, Sharpe 0.54 |
| top8, in RS>=0.8, out RS<0.5, max 3/sector | 18 | 94% | 44 | +7.1% | 105 | +13.5% | -28% | 0.67 | 0.61 | +21.1% | 0.89 | 100% | +12.6% / +11.3% | DVN: +11.7%, Sharpe 0.61 |
| top8, in RS>=0.8, out RS<0.5, sell below 50d | 63 | 87% | 36 | +0.9% | 28 | +6.3% | -25% | 0.42 | 0.57 | -3.9% | -0.11 | 50% | +3.1% / -1.4% | DVN: +4.9%, Sharpe 0.35 |
| top8, in RS>=0.8, out RS<0.5, sell below 50d after +30% over 200d | 33 | 90% | 46 | +2.7% | 54 | +10.0% | -25% | 0.59 | 0.66 | +4.3% | 0.32 | 95% | +8.2% / +5.6% | AVGO: +9.5%, Sharpe 0.57 |

## Rotation: pre-registered selection (2015 large caps, train+validation only)

Gates: train+val Sharpe > SPY's, ranking beats >= 90% of random selections, CAGR without the single best stock >= SPY's, max drawdown at most 10 points worse than SPY's.

**Chosen: none — no rule set passed every gate**

| rule set | passes | train+val Sharpe | failed gates |
|---|---|---|---|
| top5, in RS>=0.8, out RS<0.5 | ❌ | 0.59 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top5, in RS>=0.8, out RS<0.5, stop -20% | ❌ | 0.62 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d | ❌ | 0.64 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | ❌ | 0.64 | train_val_sharpe_beats_spy, ranking_beats_random, without_best_stock_beats_spy |
| top5, in RS>=0.8, out RS<0.7 | ❌ | 0.55 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top5, in RS>=0.8, out RS<0.7, stop -20% | ❌ | 0.64 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d | ❌ | 0.62 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | ❌ | 0.61 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5 | ❌ | 0.65 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5, stop -20% | ❌ | 0.61 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d | ❌ | 0.52 | train_val_sharpe_beats_spy, ranking_beats_random, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | ❌ | 0.52 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.7 | ❌ | 0.61 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.7, stop -20% | ❌ | 0.60 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d | ❌ | 0.54 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | ❌ | 0.54 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5, 12-1 month momentum | ❌ | 0.40 | train_val_sharpe_beats_spy, ranking_beats_random, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5, monthly | ❌ | 0.64 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5, volatility-adjusted | ❌ | 0.70 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5, max 2/sector | ❌ | 0.55 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5, max 3/sector | ❌ | 0.61 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5, sell below 50d | ❌ | 0.57 | train_val_sharpe_beats_spy, ranking_beats_random, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5, sell below 50d after +30% over 200d | ❌ | 0.66 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |

Calendar-year returns (2015 large caps, 20 bps per side):

| | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|---|---|---|---|
| SPY | -7% | +31% | +18% | +29% | -18% | +26% | +25% | +18% | +11% |
| equal-weight group | -7% | +29% | +14% | +31% | -4% | +16% | +16% | +17% | +19% |
| top5, in RS>=0.8, out RS<0.5 | -1% | +7% | +13% | +21% | +0% | +11% | +37% | +15% | +36% |
| top5, in RS>=0.8, out RS<0.5, stop -20% | -2% | +8% | +14% | +22% | -0% | +14% | +36% | +14% | +36% |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d | +5% | +3% | +16% | +21% | -1% | +21% | +19% | +9% | +7% |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | +4% | +3% | +16% | +22% | -1% | +21% | +19% | +9% | +7% |
| top5, in RS>=0.8, out RS<0.7 | -3% | +8% | +7% | +21% | -4% | +19% | +30% | -2% | +33% |
| top5, in RS>=0.8, out RS<0.7, stop -20% | -3% | +7% | +9% | +22% | +10% | +21% | +30% | -2% | +33% |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d | +3% | -3% | +8% | +21% | -2% | +22% | +29% | -5% | +12% |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | +2% | -3% | +8% | +21% | -2% | +22% | +29% | -5% | +12% |
| top8, in RS>=0.8, out RS<0.5 | -9% | +8% | +17% | +28% | +0% | +23% | +27% | +22% | +20% |
| top8, in RS>=0.8, out RS<0.5, stop -20% | -10% | +8% | +11% | +33% | +1% | +20% | +22% | +23% | +16% |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d | -1% | -5% | +11% | +30% | -2% | +14% | +13% | +14% | +2% |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | -1% | -4% | +11% | +30% | -2% | +14% | +13% | +14% | +2% |
| top8, in RS>=0.8, out RS<0.7 | -8% | +9% | +17% | +18% | +2% | +20% | +25% | +6% | +22% |
| top8, in RS>=0.8, out RS<0.7, stop -20% | -8% | +6% | +13% | +18% | +6% | +21% | +25% | +5% | +21% |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d | -0% | +2% | +12% | +18% | -4% | +9% | +24% | +2% | +11% |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | -0% | +2% | +12% | +18% | -4% | +9% | +24% | +1% | +11% |
| top8, in RS>=0.8, out RS<0.5, 12-1 month momentum | -14% | +10% | +2% | +24% | -12% | +2% | +41% | -1% | +0% |
| top8, in RS>=0.8, out RS<0.5, monthly | -0% | +12% | +16% | +19% | -5% | +26% | +23% | +5% | +16% |
| top8, in RS>=0.8, out RS<0.5, volatility-adjusted | -0% | +16% | +3% | +22% | -8% | +18% | +38% | +20% | +9% |
| top8, in RS>=0.8, out RS<0.5, max 2/sector | -5% | +7% | +4% | +29% | -0% | +19% | +17% | +10% | +27% |
| top8, in RS>=0.8, out RS<0.5, max 3/sector | -8% | +8% | +10% | +29% | -1% | +24% | +22% | +18% | +22% |
| top8, in RS>=0.8, out RS<0.5, sell below 50d | -3% | +3% | +28% | +21% | +6% | +7% | +4% | +2% | -8% |
| top8, in RS>=0.8, out RS<0.5, sell below 50d after +30% over 200d | -2% | +10% | +26% | +13% | +6% | +22% | +7% | +6% | +2% |

## Rockets (from 2016-11-30, 20 bps per side, 10 slots x 10%, max 3 new per day)

Rocket day: close >= +jump vs previous close, volume >= 3x the 20-day average, close in the top quarter of the day's range, price >= $5, 20-day dollar volume >= $5M. Buy next open; sell next open after a close more than `trail` below the highest close, or after 40 sessions. 'Random' = same stocks, same liquidity filter, same exit, random dates.

SPY: +15.0%/yr, max DD -34%, Sharpe 0.86 · train+val +15.0%/yr, Sharpe 0.86

| variant | trades | win% | avg trade | median | ≥+50% | worst | random avg | excess vs random t (train+val) | 2015 large caps excess | CAGR | max DD | Sharpe | train+val CAGR / Sharpe | OOS CAGR | random-entry portfolio CAGR | without top 3 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| EPS surprise>0%, reaction>=5% | 1904 | 54 | +4.6% | +1.9% | 4.4% | -51% | +4.2% | -0.38% (-0.58) | -0.12% (n=564) | +7.4% | -40% | 0.45 | +10.2% / 0.57 | -3.8% | +14.4% | +7.4% |
| EPS surprise>0%, reaction>=10% | 925 | 53 | +6.2% | +1.6% | 6.3% | -51% | +4.2% | +0.81% (0.81) | +1.30% (n=130) | +21.5% | -41% | 0.92 | +22.3% / 0.97 | +13.6% | +14.4% | +22.8% |
| EPS surprise>10%, reaction>=5% | 1263 | 53 | +4.9% | +2.0% | 5.0% | -51% | +4.2% | +0.55% (0.69) | -0.50% (n=270) | +13.6% | -45% | 0.66 | +22.0% / 0.97 | -16.1% | +14.4% | +14.3% |
| EPS surprise>10%, reaction>=10% | 713 | 53 | +6.4% | +1.5% | 6.3% | -51% | +4.2% | +1.70% (1.40) | +1.54% (n=72) | +17.3% | -48% | 0.75 | +25.2% / 1.01 | -14.3% | +14.4% | +14.2% |
| EPS surprise>20%, reaction>=10%, volume>=2x, RS>=0.8 | 243 | 56 | +8.6% | +2.8% | 7.0% | -36% | +4.2% | +3.73% (1.74) | +3.49% (n=15) | +18.8% | -24% | 0.95 | +25.4% / 1.27 | -8.0% | +14.4% | +12.9% |
| EPS surprise>20%, reaction>=15%, volume>=2x, RS>=0.8 | 173 | 56 | +8.6% | +2.7% | 8.1% | -36% | +4.2% | +2.01% (0.86) | —% (n=4) | +14.8% | -24% | 0.89 | +19.8% / 1.20 | -6.2% | +14.4% | +9.5% |
| EPS surprise>20%, reaction>=10%, volume>=2x, RS>=0.8, trail 10% | 243 | 42 | +3.7% | -3.5% | 3.7% | -21% | +4.2% | -1.95% (-1.22) | +1.47% (n=15) | +8.4% | -16% | 0.74 | +11.1% / 0.93 | -2.7% | +14.4% | +4.6% |
| EPS surprise>20%, reaction>=10%, volume>=2x, RS>=0.8, trail 15% | 243 | 50 | +7.1% | +0.0% | 4.9% | -29% | +4.2% | +2.83% (1.46) | +2.83% (n=15) | +16.5% | -18% | 1.01 | +20.7% / 1.24 | +0.6% | +14.4% | +11.9% |
| EPS surprise>20%, reaction>=10%, volume>=2x, RS>=0.8, take-profit +30% | 243 | 58 | +5.9% | +4.5% | 0.4% | -36% | +4.2% | +2.40% (1.34) | +3.91% (n=15) | +12.0% | -23% | 0.77 | +17.8% / 1.11 | -9.8% | +14.4% | +10.0% |
| EPS surprise>20%, reaction>=10%, volume>=2x, RS>=0.8, take-profit +50% | 243 | 56 | +6.7% | +2.8% | 10.3% | -36% | +4.2% | +2.50% (1.31) | +5.27% (n=15) | +14.4% | -24% | 0.83 | +20.1% / 1.14 | -8.7% | +14.4% | +10.9% |
| EPS surprise>20%, reaction>=10%, volume>=2x, RS>=0.8, trail 15%, take-profit +30% | 243 | 50 | +5.2% | +0.0% | 0.4% | -29% | +4.2% | +1.71% (1.01) | +3.15% (n=15) | +11.7% | -17% | 0.89 | +15.8% / 1.16 | -3.6% | +14.4% | +9.4% |
| jump>=8%, trail 15% | 984 | 45 | +3.9% | -2.7% | 5.2% | -52% | +2.2% | -0.54% (-0.52) | -1.55% (n=115) | +13.8% | -48% | 0.58 | +22.2% / 0.80 | -16.6% | +13.7% | +7.4% |
| jump>=8%, trail 25% | 982 | 51 | +5.3% | +0.6% | 6.7% | -61% | +2.9% | +0.01% (0.01) | -1.46% (n=115) | +14.6% | -69% | 0.58 | +21.9% / 0.77 | -11.2% | +14.6% | +10.7% |
| jump>=15%, trail 15% | 533 | 42 | +4.5% | -4.8% | 6.8% | -52% | +2.2% | -1.04% (-0.73) | -4.25% (n=24) | +16.7% | -37% | 0.67 | +20.2% / 0.75 | +3.1% | +13.7% | +10.4% |
| jump>=15%, trail 25% | 533 | 47 | +6.5% | -2.4% | 9.2% | -61% | +2.9% | +0.38% (0.21) | -4.48% (n=24) | +13.2% | -58% | 0.54 | +19.6% / 0.70 | -8.3% | +14.6% | +5.3% |

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
| EPS surprise>20%, reaction>=10%, volume>=2x, RS>=0.8, trail 10% | ❌ | beats_random_entries_same_stocks, beats_spy_train_val, without_top3_beats_spy |
| EPS surprise>20%, reaction>=10%, volume>=2x, RS>=0.8, trail 15% | ❌ | beats_random_entries_same_stocks, without_top3_beats_spy |
| EPS surprise>20%, reaction>=10%, volume>=2x, RS>=0.8, take-profit +30% | ❌ | beats_random_entries_same_stocks, without_top3_beats_spy |
| EPS surprise>20%, reaction>=10%, volume>=2x, RS>=0.8, take-profit +50% | ❌ | beats_random_entries_same_stocks, without_top3_beats_spy |
| EPS surprise>20%, reaction>=10%, volume>=2x, RS>=0.8, trail 15%, take-profit +30% | ❌ | beats_random_entries_same_stocks, without_top3_beats_spy |
| jump>=8%, trail 15% | ❌ | beats_random_entries_same_stocks, beats_spy_train_val, holds_in_2015_largecaps, without_top3_beats_spy |
| jump>=8%, trail 25% | ❌ | beats_random_entries_same_stocks, beats_spy_train_val, holds_in_2015_largecaps, without_top3_beats_spy, drawdown_tolerable |
| jump>=15%, trail 15% | ❌ | beats_random_entries_same_stocks, beats_spy_train_val, holds_in_2015_largecaps, without_top3_beats_spy |
| jump>=15%, trail 25% | ❌ | beats_random_entries_same_stocks, beats_spy_train_val, holds_in_2015_largecaps, without_top3_beats_spy, drawdown_tolerable |

## Mean R by year (all universe, fixed exit)

| group | policy | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| combined | all | +0.98 | -0.44 | +0.34 | +1.06 | +0.03 | -0.44 | +0.54 | +0.43 | +0.23 | -0.06 |
| combined | SPY>200d & stock>200d | +1.07 | -0.43 | +0.08 | +0.92 | -0.03 | -0.79 | +0.39 | +0.43 | +0.18 | -0.06 |
| combined | SPY>200d & stock>200d & RS>=0.8 | +1.14 | -0.24 | +0.42 | +1.45 | -0.41 | -0.36 | +0.42 | +0.62 | +0.84 | +0.03 |
| combined | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | +1.22 | -0.10 | +0.54 | +1.34 | -0.52 | -0.07 | +0.39 | +0.47 | +0.81 | +0.27 |
| combined | score>=70 & SPY>200d & stock>200d | +0.58 | +0.65 | +0.45 | +1.14 | -0.54 | -0.96 | +0.48 | +0.69 | +0.54 | -0.07 |
| combined | score>=70 & SPY>200d & stock>200d & RS>=0.8 | +0.17 | +1.33 | +0.61 | +1.08 | -0.53 | -1.15 | +0.47 | +1.00 | +0.72 | -0.06 |
| baseline_random | all | +1.38 | +0.11 | +0.63 | +0.87 | +0.22 | -0.24 | +0.56 | +0.44 | +0.36 | +0.17 |
| baseline_random | SPY>200d & stock>200d | +1.36 | -0.25 | +0.51 | +1.14 | +0.16 | -0.68 | +0.33 | +0.37 | +0.26 | +0.08 |
| baseline_random | SPY>200d & stock>200d & RS>=0.8 | +1.31 | +0.02 | +0.58 | +1.36 | -0.19 | -0.38 | +0.48 | +0.42 | +0.46 | -0.09 |
| baseline_random | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | +1.20 | +0.23 | +0.61 | +1.12 | -0.15 | -0.34 | +0.58 | +0.44 | +0.58 | -0.06 |