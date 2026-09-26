# Strategy research

278 symbols with data (1 failed), 10 years of daily bars. Control group: 105 stocks that were already large caps in 2015. Primary cost 20 bps per side (USD account: courtage + slippage; 40 bps ≈ trading from a SEK account). Validation from 2023-01-21, out-of-sample (OOS) from 2024-11-22. Setups invalidated at the next open (skipped): 1320.

Portfolio: max 8 positions, max 3 new per day, 1% risk per trade, max 25% of equity per position, no leverage, marked to market daily. 'vs random' = share of 40 random-order portfolios from the same eligible trades that this ranking beat.

## Portfolio — universe: all

SPY buy-and-hold: +15.0%/yr, max DD -34%, Sharpe 0.85 · train+val Sharpe 0.81 · OOS +16.7%/yr, Sharpe 1.0

| rule set | trades/yr | exposure | win% | avgR | CAGR | max DD | Sharpe | train+val Sharpe | OOS CAGR | OOS Sharpe | vs random |
|---|---|---|---|---|---|---|---|---|---|---|---|
| random picks (reference) | 77.7 | 87% | 22 | +0.28 | +13.2% | -57% | 0.55 | 0.57 | +6.1% | 0.31 | — |
| random picks, trend filter | 64.4 | 78% | 23 | +0.43 | +19.5% | -36% | 0.81 | 0.99 | +1.1% | 0.20 | — |
| RS leaders, trend filter | 72.1 | 68% | 23 | +0.39 | +22.7% | -42% | 0.79 | 0.86 | +5.8% | 0.35 | 93% |
| RS leaders near 52w high | 65.9 | 76% | 26 | +0.62 | +29.4% | -34% | 1.00 | 1.05 | +34.1% | 0.93 | 100% |
| signals score>=70, trend | 47.0 | 63% | 21 | +0.30 | +10.6% | -35% | 0.59 | 0.73 | -5.2% | -0.05 | 12% |
| signals score>=70, trend, RS top 20% | 41.6 | 51% | 23 | +0.53 | +19.3% | -33% | 0.90 | 1.02 | +13.3% | 0.61 | 68% |
| signals, trend, RS top 20% | 77.9 | 78% | 22 | +0.69 | +37.4% | -48% | 1.09 | 1.15 | +44.9% | 1.07 | 95% |
| signals, trend, RS top 20%, near 52w high | 73.7 | 79% | 22 | +0.58 | +31.2% | -32% | 1.06 | 1.19 | +27.1% | 0.81 | 100% |

Cost sensitivity (full-period CAGR / Sharpe):

| rule set | 20 bps | 40 bps | 70 bps |
|---|---|---|---|
| RS leaders, trend filter | +22.7% / 0.79 | +19.1% / 0.70 | +13.1% / 0.54 |
| RS leaders near 52w high | +29.4% / 1.00 | +24.9% / 0.88 | +18.6% / 0.71 |
| signals score>=70, trend | +10.6% / 0.59 | +7.6% / 0.46 | +3.7% / 0.28 |
| signals score>=70, trend, RS top 20% | +19.3% / 0.90 | +16.7% / 0.80 | +12.9% / 0.66 |
| signals, trend, RS top 20% | +37.4% / 1.09 | +31.4% / 0.97 | +24.3% / 0.80 |
| signals, trend, RS top 20%, near 52w high | +31.2% / 1.06 | +25.8% / 0.92 | +18.8% / 0.72 |

Exit variant (stop 2.5 x ATR instead of 1.5 x ATR / structural):

| rule set | CAGR | max DD | Sharpe | OOS Sharpe |
|---|---|---|---|---|
| random picks (reference) | +2.1% | -41% | 0.20 | -0.19 |
| random picks, trend filter | +12.1% | -33% | 0.70 | 0.36 |
| RS leaders, trend filter | +23.0% | -29% | 1.01 | 0.87 |
| RS leaders near 52w high | +27.5% | -25% | 1.17 | 0.67 |
| signals score>=70, trend | +11.6% | -28% | 0.74 | -0.13 |
| signals score>=70, trend, RS top 20% | +17.2% | -28% | 1.01 | 0.70 |
| signals, trend, RS top 20% | +18.7% | -36% | 0.89 | 0.61 |
| signals, trend, RS top 20%, near 52w high | +16.7% | -26% | 0.82 | 0.47 |

### Per trade — universe: all (one position per symbol, t over monthly means)

| group | exit | policy | n | win% | avgR | medR | t | excess vs random (t) | ≥+50% | OOS n | OOS avgR |
|---|---|---|---|---|---|---|---|---|---|---|---|
| breakout | fixed | all | 6501 | 17 | +0.292 | -1.11 | 1.38 | -0.306 (-3.61) | 3.2% | 1458 | -0.005 |
| breakout | fixed | SPY>200d & stock>200d | 5161 | 17 | +0.245 | -1.12 | 0.73 | -0.201 (-2.87) | 3.0% | 1172 | +0.012 |
| breakout | fixed | SPY>200d & stock>200d & RS>=0.8 | 2134 | 18 | +0.436 | -1.08 | 1.77 | -0.176 (-1.67) | 5.4% | 511 | +0.541 |
| breakout | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1747 | 18 | +0.464 | -1.08 | 1.73 | -0.064 (-0.53) | 4.3% | 394 | +0.701 |
| breakout | fixed | score>=70 & SPY>200d & stock>200d | 754 | 22 | +0.484 | -1.00 | 2.48 | +0.083 (0.55) | 5.8% | 155 | +0.214 |
| breakout | fixed | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 458 | 23 | +0.615 | -0.97 | 2.97 | +0.146 (0.71) | 7.6% | 103 | +0.377 |
| momentum | fixed | all | 5388 | 22 | +0.265 | -1.04 | 1.92 | -0.292 (-3.93) | 3.6% | 1211 | +0.001 |
| momentum | fixed | SPY>200d & stock>200d | 4759 | 22 | +0.302 | -1.04 | 1.96 | -0.093 (-1.50) | 3.5% | 1096 | +0.025 |
| momentum | fixed | SPY>200d & stock>200d & RS>=0.8 | 1926 | 23 | +0.391 | -1.02 | 2.27 | -0.123 (-1.56) | 6.2% | 447 | +0.259 |
| momentum | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1592 | 23 | +0.398 | -1.03 | 2.21 | -0.050 (-0.58) | 4.6% | 359 | +0.234 |
| momentum | fixed | score>=70 & SPY>200d & stock>200d | 154 | 24 | +0.569 | -0.91 | 2.10 | +0.328 (1.18) | 13.0% | 39 | +0.974 |
| momentum | fixed | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 95 | 25 | +0.751 | -0.86 | 1.94 | +0.270 (0.71) | 15.8% | 27 | +1.088 |
| combined | fixed | all | 8181 | 19 | +0.275 | -1.07 | 1.69 | -0.299 (-4.25) | 3.3% | 1815 | +0.099 |
| combined | fixed | SPY>200d & stock>200d | 6746 | 19 | +0.244 | -1.08 | 1.04 | -0.171 (-2.92) | 3.0% | 1521 | +0.087 |
| combined | fixed | SPY>200d & stock>200d & RS>=0.8 | 2811 | 21 | +0.413 | -1.04 | 2.06 | -0.157 (-1.99) | 5.4% | 660 | +0.594 |
| combined | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 2319 | 21 | +0.412 | -1.05 | 2.00 | -0.068 (-0.81) | 4.3% | 515 | +0.608 |
| combined | fixed | score>=70 & SPY>200d & stock>200d | 828 | 23 | +0.508 | -0.98 | 2.31 | +0.073 (0.53) | 6.5% | 177 | +0.292 |
| combined | fixed | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 502 | 24 | +0.626 | -0.95 | 2.67 | +0.087 (0.46) | 8.6% | 117 | +0.457 |
| baseline_random | fixed | all | 17767 | 25 | +0.348 | -1.02 | 4.95 | — (—) | 4.9% | 4053 | +0.198 |
| baseline_random | fixed | SPY>200d & stock>200d | 11326 | 23 | +0.323 | -1.04 | 3.14 | — (—) | 3.5% | 2605 | +0.148 |
| baseline_random | fixed | SPY>200d & stock>200d & RS>=0.8 | 4576 | 23 | +0.389 | -1.03 | 3.64 | — (—) | 6.2% | 1113 | +0.275 |
| baseline_random | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 3139 | 24 | +0.441 | -1.04 | 3.18 | — (—) | 4.0% | 685 | +0.325 |
| breakout | wide | all | 5225 | 33 | +0.306 | -0.95 | 3.32 | -0.164 (-3.00) | 5.5% | 1155 | +0.237 |
| breakout | wide | SPY>200d & stock>200d | 4205 | 33 | +0.319 | -0.96 | 2.44 | -0.065 (-1.33) | 5.1% | 942 | +0.253 |
| breakout | wide | SPY>200d & stock>200d & RS>=0.8 | 1783 | 35 | +0.448 | -0.93 | 2.96 | -0.100 (-1.65) | 9.1% | 420 | +0.423 |
| breakout | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1487 | 35 | +0.474 | -0.93 | 3.33 | -0.024 (-0.35) | 7.4% | 332 | +0.385 |
| breakout | wide | score>=70 & SPY>200d & stock>200d | 727 | 33 | +0.392 | -0.91 | 2.56 | -0.007 (-0.06) | 8.9% | 148 | +0.186 |
| breakout | wide | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 436 | 34 | +0.496 | -0.89 | 3.02 | +0.030 (0.19) | 11.5% | 96 | +0.347 |
| momentum | wide | all | 4484 | 32 | +0.271 | -0.98 | 2.84 | -0.189 (-3.32) | 4.8% | 973 | +0.130 |
| momentum | wide | SPY>200d & stock>200d | 3980 | 33 | +0.314 | -0.98 | 2.95 | -0.029 (-0.57) | 4.7% | 889 | +0.149 |
| momentum | wide | SPY>200d & stock>200d & RS>=0.8 | 1629 | 33 | +0.367 | -0.96 | 2.56 | -0.130 (-2.14) | 7.9% | 373 | +0.257 |
| momentum | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1374 | 33 | +0.348 | -0.97 | 2.30 | -0.117 (-1.80) | 5.8% | 298 | +0.252 |
| momentum | wide | score>=70 & SPY>200d & stock>200d | 138 | 31 | +0.323 | -0.88 | 1.38 | +0.006 (0.04) | 15.2% | 33 | +0.703 |
| momentum | wide | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 81 | 32 | +0.470 | -0.81 | 1.49 | -0.031 (-0.12) | 19.8% | 22 | +0.917 |
| combined | wide | all | 6225 | 33 | +0.289 | -0.97 | 3.26 | -0.178 (-3.54) | 5.2% | 1366 | +0.201 |
| combined | wide | SPY>200d & stock>200d | 5199 | 33 | +0.314 | -0.97 | 2.60 | -0.061 (-1.45) | 4.8% | 1166 | +0.213 |
| combined | wide | SPY>200d & stock>200d & RS>=0.8 | 2254 | 33 | +0.391 | -0.95 | 2.73 | -0.119 (-2.18) | 8.3% | 531 | +0.373 |
| combined | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1886 | 34 | +0.399 | -0.95 | 2.87 | -0.066 (-1.14) | 6.6% | 414 | +0.346 |
| combined | wide | score>=70 & SPY>200d & stock>200d | 786 | 33 | +0.385 | -0.90 | 2.18 | -0.036 (-0.36) | 9.0% | 166 | +0.255 |
| combined | wide | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 467 | 33 | +0.483 | -0.89 | 2.58 | -0.039 (-0.28) | 12.0% | 107 | +0.433 |
| baseline_random | wide | all | 12395 | 35 | +0.319 | -0.94 | 5.50 | — (—) | 6.3% | 2737 | +0.245 |
| baseline_random | wide | SPY>200d & stock>200d | 8143 | 34 | +0.318 | -0.97 | 3.67 | — (—) | 4.6% | 1862 | +0.175 |
| baseline_random | wide | SPY>200d & stock>200d & RS>=0.8 | 3402 | 34 | +0.376 | -0.96 | 4.18 | — (—) | 8.3% | 799 | +0.312 |
| baseline_random | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 2491 | 35 | +0.430 | -0.97 | 4.00 | — (—) | 5.7% | 523 | +0.415 |

## Portfolio — universe: largecap_2015

SPY buy-and-hold: +15.0%/yr, max DD -34%, Sharpe 0.85 · train+val Sharpe 0.81 · OOS +16.7%/yr, Sharpe 1.0

| rule set | trades/yr | exposure | win% | avgR | CAGR | max DD | Sharpe | train+val Sharpe | OOS CAGR | OOS Sharpe | vs random |
|---|---|---|---|---|---|---|---|---|---|---|---|
| random picks (reference) | 45.7 | 88% | 22 | +0.11 | +5.4% | -33% | 0.40 | 0.34 | +4.5% | 0.34 | — |
| random picks, trend filter | 35.9 | 76% | 21 | +0.06 | +2.6% | -27% | 0.25 | 0.41 | -6.1% | -0.44 | — |
| RS leaders, trend filter | 41.6 | 76% | 23 | +0.25 | +7.6% | -36% | 0.48 | 0.60 | -1.2% | 0.04 | 80% |
| RS leaders near 52w high | 40.1 | 76% | 22 | +0.22 | +3.9% | -29% | 0.31 | 0.42 | -4.4% | -0.16 | 50% |
| signals score>=70, trend | 15.3 | 37% | 24 | +0.33 | +3.4% | -16% | 0.40 | 0.46 | +4.1% | 0.47 | 23% |
| signals score>=70, trend, RS top 20% | 11.0 | 26% | 23 | +0.38 | +2.7% | -19% | 0.37 | 0.50 | +2.0% | 0.31 | 0% |
| signals, trend, RS top 20% | 41.1 | 78% | 22 | +0.32 | +7.0% | -30% | 0.51 | 0.59 | +3.2% | 0.27 | 97% |
| signals, trend, RS top 20%, near 52w high | 42.1 | 78% | 21 | +0.31 | +7.5% | -33% | 0.55 | 0.68 | +2.2% | 0.21 | 90% |

Cost sensitivity (full-period CAGR / Sharpe):

| rule set | 20 bps | 40 bps | 70 bps |
|---|---|---|---|
| RS leaders, trend filter | +7.6% / 0.48 | +4.7% / 0.33 | +0.4% / 0.12 |
| RS leaders near 52w high | +3.9% / 0.31 | +1.0% / 0.14 | -3.7% / -0.12 |
| signals score>=70, trend | +3.4% / 0.40 | +2.0% / 0.26 | -0.0% / 0.05 |
| signals score>=70, trend, RS top 20% | +2.7% / 0.37 | +1.6% / 0.24 | +0.1% / 0.06 |
| signals, trend, RS top 20% | +7.0% / 0.51 | +3.7% / 0.31 | -1.1% / 0.01 |
| signals, trend, RS top 20%, near 52w high | +7.5% / 0.55 | +4.2% / 0.35 | -0.7% / 0.04 |

Exit variant (stop 2.5 x ATR instead of 1.5 x ATR / structural):

| rule set | CAGR | max DD | Sharpe | OOS Sharpe |
|---|---|---|---|---|
| random picks (reference) | +6.0% | -18% | 0.48 | -0.72 |
| random picks, trend filter | +0.7% | -27% | 0.12 | -0.77 |
| RS leaders, trend filter | +10.6% | -25% | 0.67 | 0.42 |
| RS leaders near 52w high | +11.8% | -22% | 0.74 | 0.13 |
| signals score>=70, trend | +2.1% | -16% | 0.28 | 0.41 |
| signals score>=70, trend, RS top 20% | +2.8% | -17% | 0.40 | 0.43 |
| signals, trend, RS top 20% | +7.7% | -21% | 0.57 | 0.61 |
| signals, trend, RS top 20%, near 52w high | +6.5% | -27% | 0.51 | 0.55 |

### Per trade — universe: largecap_2015 (one position per symbol, t over monthly means)

| group | exit | policy | n | win% | avgR | medR | t | excess vs random (t) | ≥+50% | OOS n | OOS avgR |
|---|---|---|---|---|---|---|---|---|---|---|---|
| breakout | fixed | all | 2273 | 17 | +0.078 | -1.16 | -0.37 | -0.407 (-3.36) | 0.2% | 437 | -0.200 |
| breakout | fixed | SPY>200d & stock>200d | 1866 | 16 | +0.000 | -1.18 | -0.48 | -0.234 (-2.26) | 0.1% | 362 | -0.183 |
| breakout | fixed | SPY>200d & stock>200d & RS>=0.8 | 761 | 19 | +0.291 | -1.12 | 1.36 | +0.056 (0.26) | 0.1% | 156 | +0.141 |
| breakout | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 714 | 18 | +0.301 | -1.12 | 1.38 | +0.086 (0.40) | 0.1% | 152 | +0.183 |
| breakout | fixed | score>=70 & SPY>200d & stock>200d | 163 | 21 | +0.195 | -1.02 | 0.96 | -0.057 (-0.21) | 0.0% | 27 | +0.444 |
| breakout | fixed | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 107 | 22 | +0.249 | -1.00 | 1.13 | -0.057 (-0.17) | 0.0% | 16 | +0.412 |
| momentum | fixed | all | 2177 | 22 | +0.173 | -1.10 | 1.05 | -0.260 (-2.78) | 0.1% | 432 | -0.076 |
| momentum | fixed | SPY>200d & stock>200d | 1942 | 22 | +0.210 | -1.10 | 0.89 | -0.082 (-0.95) | 0.1% | 396 | -0.016 |
| momentum | fixed | SPY>200d & stock>200d & RS>=0.8 | 832 | 23 | +0.241 | -1.08 | 0.32 | -0.226 (-2.06) | 0.0% | 170 | +0.044 |
| momentum | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 790 | 22 | +0.224 | -1.08 | 0.15 | -0.220 (-1.97) | 0.0% | 165 | +0.066 |
| momentum | fixed | score>=70 & SPY>200d & stock>200d | 15 | 20 | +0.106 | -1.03 | 0.39 | +0.025 (0.03) | 0.0% | 3 | -1.150 |
| momentum | fixed | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 8 | 25 | +0.909 | -0.90 | 0.74 | +0.039 (0.03) | 0.0% | 2 | -1.090 |
| combined | fixed | all | 3081 | 19 | +0.121 | -1.12 | 0.23 | -0.332 (-3.47) | 0.2% | 589 | -0.148 |
| combined | fixed | SPY>200d & stock>200d | 2631 | 19 | +0.087 | -1.13 | -0.07 | -0.169 (-2.11) | 0.1% | 505 | -0.118 |
| combined | fixed | SPY>200d & stock>200d & RS>=0.8 | 1128 | 20 | +0.227 | -1.08 | 0.37 | -0.176 (-1.62) | 0.0% | 221 | -0.021 |
| combined | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1070 | 20 | +0.209 | -1.09 | 0.32 | -0.157 (-1.50) | 0.0% | 216 | +0.013 |
| combined | fixed | score>=70 & SPY>200d & stock>200d | 174 | 22 | +0.227 | -1.02 | 1.12 | -0.038 (-0.15) | 0.0% | 30 | +0.284 |
| combined | fixed | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 113 | 22 | +0.334 | -0.98 | 1.39 | +0.009 (0.03) | 0.0% | 18 | +0.245 |
| baseline_random | fixed | all | 7345 | 25 | +0.294 | -1.06 | 4.13 | — (—) | 0.6% | 1464 | +0.188 |
| baseline_random | fixed | SPY>200d & stock>200d | 4833 | 23 | +0.237 | -1.09 | 2.31 | — (—) | 0.3% | 960 | +0.133 |
| baseline_random | fixed | SPY>200d & stock>200d & RS>=0.8 | 1925 | 24 | +0.309 | -1.07 | 2.36 | — (—) | 0.4% | 420 | +0.070 |
| baseline_random | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1715 | 24 | +0.304 | -1.07 | 2.12 | — (—) | 0.2% | 365 | +0.110 |
| breakout | wide | all | 1940 | 33 | +0.187 | -1.00 | 1.57 | -0.224 (-2.99) | 0.3% | 364 | +0.128 |
| breakout | wide | SPY>200d & stock>200d | 1595 | 33 | +0.203 | -1.00 | 1.63 | -0.029 (-0.41) | 0.2% | 304 | +0.183 |
| breakout | wide | SPY>200d & stock>200d & RS>=0.8 | 672 | 33 | +0.281 | -0.97 | 1.38 | -0.132 (-1.54) | 0.0% | 137 | +0.083 |
| breakout | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 635 | 33 | +0.279 | -0.97 | 1.43 | -0.093 (-1.10) | 0.0% | 133 | +0.092 |
| breakout | wide | score>=70 & SPY>200d & stock>200d | 163 | 31 | +0.160 | -0.92 | 0.51 | -0.143 (-0.78) | 0.0% | 27 | +0.350 |
| breakout | wide | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 107 | 32 | +0.322 | -0.91 | 1.27 | -0.133 (-0.55) | 0.0% | 16 | +0.516 |
| momentum | wide | all | 1849 | 32 | +0.192 | -1.02 | 1.91 | -0.192 (-2.60) | 0.1% | 356 | +0.055 |
| momentum | wide | SPY>200d & stock>200d | 1650 | 33 | +0.237 | -1.02 | 2.09 | +0.020 (0.30) | 0.1% | 330 | +0.090 |
| momentum | wide | SPY>200d & stock>200d & RS>=0.8 | 717 | 34 | +0.272 | -0.99 | 1.37 | -0.138 (-1.85) | 0.0% | 149 | -0.015 |
| momentum | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 681 | 34 | +0.277 | -0.99 | 1.50 | -0.091 (-1.17) | 0.0% | 146 | -0.001 |
| momentum | wide | score>=70 & SPY>200d & stock>200d | 14 | 29 | +0.005 | -0.99 | 0.33 | +0.043 (0.08) | 0.0% | 3 | -1.085 |
| momentum | wide | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 7 | 43 | +0.817 | -0.91 | 0.92 | -0.009 (-0.01) | 0.0% | 2 | -1.053 |
| combined | wide | all | 2441 | 33 | +0.184 | -1.01 | 1.80 | -0.210 (-3.07) | 0.3% | 460 | +0.104 |
| combined | wide | SPY>200d & stock>200d | 2095 | 33 | +0.204 | -1.02 | 1.88 | -0.012 (-0.20) | 0.1% | 404 | +0.148 |
| combined | wide | SPY>200d & stock>200d & RS>=0.8 | 917 | 34 | +0.290 | -0.99 | 1.70 | -0.097 (-1.48) | 0.0% | 185 | +0.009 |
| combined | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 871 | 34 | +0.290 | -0.99 | 1.69 | -0.057 (-0.91) | 0.0% | 181 | +0.024 |
| combined | wide | score>=70 & SPY>200d & stock>200d | 173 | 31 | +0.167 | -0.92 | 0.71 | -0.120 (-0.68) | 0.0% | 30 | +0.207 |
| combined | wide | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 112 | 32 | +0.362 | -0.91 | 1.45 | -0.107 (-0.46) | 0.0% | 18 | +0.342 |
| baseline_random | wide | all | 5193 | 37 | +0.293 | -0.94 | 4.99 | — (—) | 0.8% | 993 | +0.254 |
| baseline_random | wide | SPY>200d & stock>200d | 3510 | 34 | +0.246 | -1.00 | 2.83 | — (—) | 0.2% | 709 | +0.190 |
| baseline_random | wide | SPY>200d & stock>200d & RS>=0.8 | 1482 | 36 | +0.322 | -0.98 | 3.04 | — (—) | 0.4% | 311 | +0.136 |
| baseline_random | wide | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1334 | 35 | +0.324 | -0.99 | 2.88 | — (—) | 0.3% | 269 | +0.181 |

## Momentum rotation — universe: all (from 2018-01-03, 20 bps per side)

| benchmark | CAGR | max DD | Sharpe | train+val Sharpe | OOS CAGR | OOS Sharpe |
|---|---|---|---|---|---|---|
| SPY buy-and-hold | +14.5% | -34% | 0.81 | 0.76 | +16.7% | 1.00 |
| equal-weight universe (no costs) | +26.5% | -42% | 1.02 | 1.00 | +26.5% | 1.07 |

| rule set | trades/yr | exposure | win% | avg trade | avg days | CAGR | max DD | Sharpe | train+val Sharpe | OOS CAGR | OOS Sharpe | vs random | CAGR @40 / @70 bps | without best stock |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| top5, in RS>=0.8, out RS<0.5 | 10 | 93% | 37 | +15.8% | 107 | +19.0% | -79% | 0.59 | 0.48 | +46.2% | 0.88 | 20% | +18.2% / +17.0% | SE: +25.4%, Sharpe 0.67 |
| top5, in RS>=0.8, out RS<0.5, stop -20% | 16 | 92% | 29 | +17.3% | 68 | +28.5% | -66% | 0.71 | 0.71 | +26.6% | 0.69 | 65% | +27.3% / +25.5% | SE: +24.0%, Sharpe 0.66 |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d | 20 | 81% | 38 | +6.1% | 48 | +12.7% | -74% | 0.49 | 0.68 | -24.6% | -0.15 | 10% | +11.0% / +8.5% | MARA: +10.5%, Sharpe 0.45 |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | 26 | 80% | 33 | +3.4% | 37 | +8.1% | -71% | 0.41 | 0.50 | -10.4% | 0.11 | 5% | +6.1% / +3.2% | CELH: +13.8%, Sharpe 0.51 |
| top5, in RS>=0.8, out RS<0.7 | 12 | 93% | 45 | +11.8% | 93 | +18.5% | -76% | 0.58 | 0.52 | +32.5% | 0.75 | 20% | +17.5% / +16.0% | ENPH: +18.8%, Sharpe 0.58 |
| top5, in RS>=0.8, out RS<0.7, stop -20% | 18 | 92% | 33 | +8.9% | 60 | +18.8% | -77% | 0.58 | 0.44 | +58.5% | 0.99 | 15% | +17.2% / +14.8% | VKTX: +13.7%, Sharpe 0.51 |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d | 22 | 80% | 40 | +3.9% | 45 | +9.6% | -77% | 0.44 | 0.53 | -10.1% | 0.19 | 15% | +7.8% / +5.1% | TSLA: +15.4%, Sharpe 0.53 |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | 28 | 80% | 33 | +3.2% | 35 | +7.8% | -68% | 0.40 | 0.42 | +2.1% | 0.35 | 10% | +5.7% / +2.6% | CELH: +3.7%, Sharpe 0.33 |
| top8, in RS>=0.8, out RS<0.5 | 16 | 92% | 42 | +21.7% | 108 | +33.6% | -70% | 0.82 | 0.84 | +32.8% | 0.76 | 55% | +32.7% / +31.0% | SE: +31.2%, Sharpe 0.78 |
| top8, in RS>=0.8, out RS<0.5, stop -20% | 24 | 91% | 34 | +13.9% | 71 | +28.8% | -62% | 0.74 | 0.78 | +22.7% | 0.64 | 85% | +27.5% / +25.6% | SE: +23.4%, Sharpe 0.66 |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d | 30 | 80% | 39 | +9.4% | 52 | +30.7% | -58% | 0.79 | 0.81 | +27.6% | 0.71 | 85% | +29.0% / +26.5% | APP: +23.7%, Sharpe 0.68 |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | 37 | 80% | 35 | +7.0% | 42 | +27.2% | -67% | 0.74 | 0.73 | +29.6% | 0.73 | 85% | +25.3% / +22.5% | NIO: +28.5%, Sharpe 0.75 |
| top8, in RS>=0.8, out RS<0.7 | 19 | 92% | 49 | +18.9% | 95 | +36.8% | -57% | 0.84 | 0.86 | +35.7% | 0.79 | 75% | +35.6% / +34.0% | MARA: +31.0%, Sharpe 0.77 |
| top8, in RS>=0.8, out RS<0.7, stop -20% | 28 | 91% | 33 | +15.6% | 62 | +27.6% | -71% | 0.71 | 0.69 | +32.2% | 0.75 | 70% | +26.2% / +24.0% | MARA: +22.1%, Sharpe 0.64 |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d | 32 | 80% | 41 | +7.7% | 48 | +23.9% | -54% | 0.68 | 0.73 | +12.6% | 0.50 | 55% | +22.1% / +19.3% | MARA: +22.4%, Sharpe 0.66 |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | 40 | 80% | 33 | +9.6% | 38 | +29.0% | -63% | 0.73 | 0.79 | +14.5% | 0.53 | 75% | +26.7% / +23.4% | MARA: +27.1%, Sharpe 0.71 |
| top8, in RS>=0.8, out RS<0.5, 12-1 month momentum | 18 | 91% | 34 | +20.2% | 99 | +26.9% | -63% | 0.73 | 0.68 | +43.6% | 0.87 | 70% | +25.9% / +24.4% | SE: +24.6%, Sharpe 0.69 |
| top8, in RS>=0.8, out RS<0.5, monthly | 11 | 94% | 39 | +49.3% | 150 | +37.1% | -63% | 0.87 | 0.80 | +60.7% | 1.05 | 75% | +36.5% / +35.5% | ENPH: +34.1%, Sharpe 0.83 |
| top8, in RS>=0.8, out RS<0.5, volatility-adjusted | 14 | 93% | 46 | +26.8% | 125 | +38.3% | -45% | 0.98 | 0.96 | +60.5% | 1.10 | 100% | +37.4% / +36.1% | RKLB: +32.1%, Sharpe 0.88 |

## Momentum rotation — universe: largecap_2015 (from 2018-01-03, 20 bps per side)

| benchmark | CAGR | max DD | Sharpe | train+val Sharpe | OOS CAGR | OOS Sharpe |
|---|---|---|---|---|---|---|
| SPY buy-and-hold | +14.5% | -34% | 0.81 | 0.76 | +16.7% | 1.00 |
| equal-weight universe (no costs) | +13.8% | -37% | 0.79 | 0.75 | +13.7% | 1.01 |

| rule set | trades/yr | exposure | win% | avg trade | avg days | CAGR | max DD | Sharpe | train+val Sharpe | OOS CAGR | OOS Sharpe | vs random | CAGR @40 / @70 bps | without best stock |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| top5, in RS>=0.8, out RS<0.5 | 10 | 95% | 47 | +6.9% | 111 | +15.5% | -36% | 0.69 | 0.52 | +37.2% | 1.20 | 95% | +14.6% / +13.3% | GE: +14.9%, Sharpe 0.66 |
| top5, in RS>=0.8, out RS<0.5, stop -20% | 11 | 94% | 50 | +7.0% | 108 | +16.0% | -36% | 0.71 | 0.55 | +37.0% | 1.19 | 95% | +15.1% / +13.8% | GE: +16.3%, Sharpe 0.71 |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d | 20 | 81% | 47 | +2.8% | 49 | +11.2% | -26% | 0.59 | 0.56 | +15.0% | 0.66 | 75% | +9.4% / +6.9% | AVGO: +11.2%, Sharpe 0.61 |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | 20 | 81% | 47 | +2.8% | 49 | +11.2% | -26% | 0.59 | 0.56 | +15.1% | 0.66 | 85% | +9.4% / +6.9% | AVGO: +11.2%, Sharpe 0.60 |
| top5, in RS>=0.8, out RS<0.7 | 14 | 94% | 47 | +3.7% | 82 | +13.1% | -36% | 0.60 | 0.54 | +21.4% | 0.77 | 90% | +11.9% / +10.2% | META: +10.9%, Sharpe 0.53 |
| top5, in RS>=0.8, out RS<0.7, stop -20% | 14 | 95% | 47 | +4.3% | 80 | +15.1% | -33% | 0.66 | 0.63 | +20.8% | 0.76 | 100% | +13.9% / +12.1% | META: +14.5%, Sharpe 0.64 |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d | 23 | 81% | 46 | +2.2% | 44 | +10.1% | -29% | 0.54 | 0.61 | +6.2% | 0.36 | 100% | +8.2% / +5.4% | AVGO: +9.0%, Sharpe 0.51 |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | 23 | 81% | 46 | +2.2% | 43 | +10.1% | -29% | 0.54 | 0.61 | +6.0% | 0.35 | 100% | +8.1% / +5.3% | AVGO: +9.0%, Sharpe 0.51 |
| top8, in RS>=0.8, out RS<0.5 | 17 | 94% | 47 | +7.5% | 109 | +17.0% | -29% | 0.80 | 0.67 | +30.5% | 1.23 | 100% | +16.1% / +14.7% | DVN: +14.8%, Sharpe 0.73 |
| top8, in RS>=0.8, out RS<0.5, stop -20% | 18 | 93% | 47 | +6.3% | 104 | +15.8% | -29% | 0.76 | 0.64 | +28.1% | 1.16 | 100% | +14.9% / +13.5% | DVN: +13.4%, Sharpe 0.68 |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d | 31 | 80% | 45 | +2.7% | 52 | +9.9% | -28% | 0.59 | 0.55 | +13.0% | 0.71 | 90% | +8.3% / +5.9% | DVN: +9.0%, Sharpe 0.55 |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | 31 | 80% | 44 | +2.6% | 51 | +9.9% | -27% | 0.59 | 0.55 | +12.9% | 0.70 | 95% | +8.3% / +5.8% | DVN: +9.0%, Sharpe 0.55 |
| top8, in RS>=0.8, out RS<0.7 | 23 | 93% | 49 | +4.0% | 80 | +13.3% | -26% | 0.67 | 0.65 | +16.0% | 0.76 | 100% | +12.1% / +10.3% | META: +10.4%, Sharpe 0.56 |
| top8, in RS>=0.8, out RS<0.7, stop -20% | 23 | 93% | 48 | +4.0% | 78 | +13.0% | -29% | 0.66 | 0.64 | +15.4% | 0.74 | 100% | +11.8% / +9.9% | AVGO: +10.6%, Sharpe 0.57 |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d | 35 | 80% | 47 | +1.9% | 45 | +8.7% | -29% | 0.53 | 0.58 | +6.0% | 0.39 | 80% | +6.8% / +4.1% | AVGO: +8.1%, Sharpe 0.51 |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | 36 | 80% | 47 | +1.9% | 44 | +8.6% | -29% | 0.53 | 0.57 | +5.9% | 0.38 | 90% | +6.8% / +4.1% | AVGO: +8.1%, Sharpe 0.51 |
| top8, in RS>=0.8, out RS<0.5, 12-1 month momentum | 19 | 90% | 32 | +2.7% | 92 | +6.4% | -40% | 0.40 | 0.38 | +7.8% | 0.46 | 15% | +5.5% / +4.2% | GE: +4.8%, Sharpe 0.33 |
| top8, in RS>=0.8, out RS<0.5, monthly | 12 | 93% | 48 | +9.3% | 145 | +13.8% | -26% | 0.67 | 0.58 | +23.3% | 0.98 | 95% | +13.2% / +13.8% | DVN: +13.7%, Sharpe 0.66 |
| top8, in RS>=0.8, out RS<0.5, volatility-adjusted | 16 | 93% | 57 | +6.8% | 115 | +12.8% | -23% | 0.74 | 0.71 | +13.4% | 0.87 | 95% | +11.9% / +10.7% | GE: +9.7%, Sharpe 0.59 |

## Rotation: pre-registered selection (2015 large caps, train+validation only)

Gates: train+val Sharpe > SPY's, ranking beats >= 90% of random selections, CAGR without the single best stock >= SPY's, max drawdown at most 10 points worse than SPY's.

**Chosen: none — no rule set passed every gate**

| rule set | passes | train+val Sharpe | failed gates |
|---|---|---|---|
| top5, in RS>=0.8, out RS<0.5 | ❌ | 0.52 | train_val_sharpe_beats_spy |
| top5, in RS>=0.8, out RS<0.5, stop -20% | ❌ | 0.55 | train_val_sharpe_beats_spy |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d | ❌ | 0.56 | train_val_sharpe_beats_spy, ranking_beats_random, without_best_stock_beats_spy |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | ❌ | 0.56 | train_val_sharpe_beats_spy, ranking_beats_random, without_best_stock_beats_spy |
| top5, in RS>=0.8, out RS<0.7 | ❌ | 0.54 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top5, in RS>=0.8, out RS<0.7, stop -20% | ❌ | 0.63 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d | ❌ | 0.61 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | ❌ | 0.61 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5 | ❌ | 0.67 | train_val_sharpe_beats_spy |
| top8, in RS>=0.8, out RS<0.5, stop -20% | ❌ | 0.64 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d | ❌ | 0.55 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | ❌ | 0.55 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.7 | ❌ | 0.65 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.7, stop -20% | ❌ | 0.64 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d | ❌ | 0.58 | train_val_sharpe_beats_spy, ranking_beats_random, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | ❌ | 0.57 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5, 12-1 month momentum | ❌ | 0.38 | train_val_sharpe_beats_spy, ranking_beats_random, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5, monthly | ❌ | 0.58 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |
| top8, in RS>=0.8, out RS<0.5, volatility-adjusted | ❌ | 0.71 | train_val_sharpe_beats_spy, without_best_stock_beats_spy |

Calendar-year returns (2015 large caps, 20 bps per side):

| | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|---|---|---|---|
| SPY | -6% | +31% | +18% | +29% | -18% | +26% | +25% | +18% | +14% |
| equal-weight group | -7% | +29% | +14% | +31% | -4% | +16% | +16% | +17% | +13% |
| top5, in RS>=0.8, out RS<0.5 | -10% | +7% | +13% | +21% | +0% | +11% | +37% | +15% | +55% |
| top5, in RS>=0.8, out RS<0.5, stop -20% | -11% | +8% | +14% | +22% | -0% | +14% | +36% | +14% | +55% |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d | -5% | +3% | +16% | +21% | -1% | +21% | +19% | +9% | +18% |
| top5, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | -6% | +3% | +16% | +22% | -1% | +21% | +19% | +9% | +18% |
| top5, in RS>=0.8, out RS<0.7 | -7% | +8% | +7% | +21% | -4% | +19% | +30% | -2% | +53% |
| top5, in RS>=0.8, out RS<0.7, stop -20% | -7% | +7% | +9% | +22% | +10% | +21% | +30% | -2% | +52% |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d | -0% | -3% | +8% | +21% | -2% | +22% | +29% | -5% | +24% |
| top5, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | -0% | -3% | +8% | +21% | -2% | +22% | +29% | -5% | +24% |
| top8, in RS>=0.8, out RS<0.5 | -4% | +8% | +17% | +28% | +0% | +23% | +27% | +22% | +33% |
| top8, in RS>=0.8, out RS<0.5, stop -20% | -5% | +8% | +11% | +33% | +1% | +20% | +22% | +23% | +30% |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d | +4% | -5% | +11% | +30% | -2% | +14% | +13% | +14% | +10% |
| top8, in RS>=0.8, out RS<0.5, sell all when SPY<200d, stop -20% | +4% | -4% | +11% | +30% | -2% | +14% | +13% | +14% | +10% |
| top8, in RS>=0.8, out RS<0.7 | -6% | +9% | +17% | +18% | +2% | +20% | +25% | +6% | +29% |
| top8, in RS>=0.8, out RS<0.7, stop -20% | -6% | +6% | +13% | +18% | +6% | +21% | +25% | +5% | +29% |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d | +2% | +2% | +12% | +18% | -4% | +9% | +24% | +2% | +14% |
| top8, in RS>=0.8, out RS<0.7, sell all when SPY<200d, stop -20% | +2% | +2% | +12% | +18% | -4% | +9% | +24% | +1% | +14% |
| top8, in RS>=0.8, out RS<0.5, 12-1 month momentum | -12% | +10% | +2% | +24% | -12% | +2% | +41% | -1% | +12% |
| top8, in RS>=0.8, out RS<0.5, monthly | -3% | +12% | +16% | +19% | -5% | +26% | +23% | +5% | +34% |
| top8, in RS>=0.8, out RS<0.5, volatility-adjusted | -1% | +16% | +3% | +22% | -8% | +18% | +38% | +20% | +10% |

## Mean R by year (all universe, fixed exit)

| group | policy | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| combined | all | +0.80 | -0.43 | +0.30 | +1.07 | +0.03 | -0.44 | +0.53 | +0.42 | +0.23 | -0.01 |
| combined | SPY>200d & stock>200d | +0.86 | -0.42 | +0.03 | +0.94 | -0.03 | -0.79 | +0.38 | +0.42 | +0.19 | +0.03 |
| combined | SPY>200d & stock>200d & RS>=0.8 | +0.82 | -0.27 | +0.35 | +1.46 | -0.41 | -0.36 | +0.35 | +0.60 | +0.83 | +0.30 |
| combined | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | +0.89 | -0.13 | +0.45 | +1.36 | -0.52 | -0.07 | +0.30 | +0.46 | +0.81 | +0.50 |
| combined | score>=70 & SPY>200d & stock>200d | +1.02 | +0.65 | +0.42 | +1.14 | -0.54 | -0.96 | +0.43 | +0.69 | +0.52 | +0.12 |
| combined | score>=70 & SPY>200d & stock>200d & RS>=0.8 | +0.83 | +1.33 | +0.61 | +1.08 | -0.53 | -1.15 | +0.41 | +1.00 | +0.70 | +0.18 |
| baseline_random | all | +1.01 | +0.06 | +0.54 | +0.97 | +0.15 | -0.28 | +0.60 | +0.43 | +0.30 | +0.19 |
| baseline_random | SPY>200d & stock>200d | +1.04 | -0.24 | +0.51 | +0.84 | +0.17 | -0.78 | +0.27 | +0.42 | +0.21 | +0.17 |
| baseline_random | SPY>200d & stock>200d & RS>=0.8 | +1.19 | +0.12 | +0.61 | +1.18 | -0.24 | -0.74 | +0.48 | +0.52 | +0.39 | +0.18 |
| baseline_random | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | +1.09 | +0.28 | +0.68 | +1.01 | -0.30 | -0.63 | +0.53 | +0.61 | +0.64 | +0.08 |