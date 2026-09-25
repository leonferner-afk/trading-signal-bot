# Strategy research

Universe: 199 symbols with data (3 failed), 10 years of daily bars, costs 10+5 bps per side. Gap-invalidated setups skipped: 702. Validation from 2023-01-21, out-of-sample (OOS) from 2024-11-22.

## Portfolio simulation (max 8 open, max 3 new/day, 1% risk per trade, no leverage)

SPY buy-and-hold: +15.0%/yr, max drawdown -34% · OOS: +16.5%/yr, max DD -19%

| rule set | exit | trades/yr | win% | avgR | CAGR | max DD* | OOS CAGR | OOS max DD* |
|---|---|---|---|---|---|---|---|---|
| random entries (reference) | fixed | 74.5 | 23 | -1.29 | +17.2% | -58% | +16.1% | -19% |
| random entries (reference) | trail | 75.7 | 25 | -1.35 | +13.0% | -53% | -2.8% | -33% |
| random entries, trend filter | fixed | 66.1 | 24 | +0.49 | +21.2% | -43% | +19.6% | -27% |
| random entries, trend filter | trail | 74.7 | 32 | +0.39 | +20.9% | -30% | +18.8% | -27% |
| RS leaders (top 20%), trend filter | fixed | 69.6 | 22 | +0.40 | +19.6% | -38% | -0.2% | -35% |
| RS leaders (top 20%), trend filter | trail | 73.4 | 30 | +0.42 | +23.9% | -35% | +8.3% | -30% |
| RS leaders near 52w high | fixed | 64.4 | 25 | +0.62 | +27.5% | -27% | +51.9% | -20% |
| RS leaders near 52w high | trail | 81.5 | 34 | +0.27 | +17.2% | -25% | -3.0% | -22% |
| signals score>=70 + trend (current live) | fixed | 44.4 | 21 | +0.43 | +14.0% | -29% | +4.0% | -24% |
| signals score>=70 + trend (current live) | trail | 48.3 | 32 | +0.23 | +7.0% | -18% | -2.1% | -20% |
| signals score>=70 + trend + RS top 20% | fixed | 37.7 | 24 | +0.67 | +22.3% | -23% | +13.9% | -14% |
| signals score>=70 + trend + RS top 20% | trail | 38.7 | 30 | +0.40 | +13.8% | -22% | +11.1% | -16% |
| signals any score + trend + RS top 20% | fixed | 78.5 | 23 | +0.76 | +43.8% | -39% | +82.7% | -16% |
| signals any score + trend + RS top 20% | trail | 89.4 | 30 | +0.55 | +33.8% | -38% | +61.3% | -19% |

*Drawdown measured on realized equity (at exits), so it understates intra-trade drawdown.

## Per-trade results (one position per symbol)

| group | exit | policy | n | win% | avgR | t | PF | ≥+50% | OOS n | OOS avgR | OOS PF |
|---|---|---|---|---|---|---|---|---|---|---|---|
| breakout | fixed | all | 4902 | 17 | +0.434 | 6.13 | 1.536 | 3.8% | 1123 | +0.090 | 1.33 |
| breakout | fixed | score>=70 | 739 | 22 | +0.556 | 4.47 | 1.611 | 6.6% | 153 | +0.198 | 1.35 |
| breakout | fixed | score>=80 | 108 | 17 | -0.053 | -0.19 | 0.742 | 0.9% | 17 | -0.673 | 0.32 |
| breakout | fixed | SPY>200d & stock>200d | 3900 | 17 | +0.397 | 5.14 | 1.553 | 3.6% | 911 | +0.143 | 1.30 |
| breakout | fixed | score>=70 & SPY>200d & stock>200d | 632 | 22 | +0.547 | 4.07 | 1.574 | 6.3% | 138 | +0.294 | 1.46 |
| breakout | fixed | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 369 | 23 | +0.676 | 3.66 | 1.68 | 8.4% | 87 | +0.545 | 1.67 |
| breakout | fixed | SPY>200d & stock>200d & RS>=0.8 | 1596 | 18 | +0.563 | 4.41 | 1.656 | 6.5% | 389 | +0.694 | 1.56 |
| breakout | fixed | SPY>200d & stock>200d & RS>=0.9 | 897 | 18 | +0.536 | 3.24 | 1.558 | 8.1% | 205 | +0.664 | 1.61 |
| breakout | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1303 | 18 | +0.599 | 4.45 | 1.619 | 5.3% | 297 | +1.014 | 1.71 |
| breakout | fixed | score>=70 & SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 320 | 23 | +0.683 | 3.43 | 1.681 | 6.9% | 69 | +0.591 | 1.64 |
| momentum | fixed | all | 3859 | 23 | +0.382 | 7.97 | 1.451 | 4.6% | 897 | +0.119 | 1.21 |
| momentum | fixed | score>=70 | 154 | 24 | +0.619 | 2.54 | 2.102 | 13.6% | 37 | +0.911 | 2.54 |
| momentum | fixed | score>=80 | 3 | 0 | -0.720 | -4.68 | 0.0 | 0.0% | 1 | -0.772 | 0.00 |
| momentum | fixed | SPY>200d & stock>200d | 3412 | 23 | +0.418 | 8.11 | 1.512 | 4.5% | 819 | +0.115 | 1.22 |
| momentum | fixed | score>=70 & SPY>200d & stock>200d | 138 | 25 | +0.643 | 2.5 | 2.141 | 13.8% | 35 | +1.015 | 2.71 |
| momentum | fixed | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 76 | 26 | +0.815 | 2.28 | 2.377 | 17.1% | 22 | +1.296 | 3.25 |
| momentum | fixed | SPY>200d & stock>200d & RS>=0.8 | 1368 | 23 | +0.475 | 5.69 | 1.59 | 7.7% | 332 | +0.354 | 1.50 |
| momentum | fixed | SPY>200d & stock>200d & RS>=0.9 | 743 | 24 | +0.557 | 4.81 | 1.673 | 10.4% | 169 | +0.679 | 2.04 |
| momentum | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1118 | 23 | +0.508 | 5.36 | 1.643 | 6.1% | 267 | +0.429 | 1.59 |
| momentum | fixed | score>=70 & SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 50 | 26 | +0.806 | 1.75 | 2.518 | 20.0% | 14 | +2.174 | 5.83 |
| reversal | fixed | all | 1088 | 21 | +0.316 | 2.63 | 1.7 | 6.9% | 310 | +0.260 | 1.56 |
| reversal | fixed | score>=70 | 6 | 0 | -0.996 | -7.43 | 0.0 | 0.0% | 3 | -0.937 | 0.00 |
| reversal | fixed | SPY>200d & stock>200d | 127 | 14 | -0.325 | -1.32 | 0.682 | 1.6% | 19 | -0.661 | 0.82 |
| reversal | fixed | score>=70 & SPY>200d & stock>200d | 2 | 0 | -0.939 | -4.73 | 0.0 | 0.0% | 0 | — | — |
| reversal | fixed | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 1 | 0 | -1.137 | None | 0.0 | 0.0% | 0 | — | — |
| reversal | fixed | SPY>200d & stock>200d & RS>=0.8 | 31 | 16 | -0.029 | -0.05 | 1.233 | 6.5% | 5 | -0.085 | 1.72 |
| reversal | fixed | SPY>200d & stock>200d & RS>=0.9 | 11 | 9 | -0.642 | -0.79 | 0.679 | 9.1% | 2 | -2.393 | 0.00 |
| reversal | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 3 | 0 | -1.431 | -3.26 | 0.0 | 0.0% | 0 | — | — |
| combined | fixed | all | 5974 | 20 | +0.403 | 7.48 | 1.482 | 4.0% | 1370 | +0.240 | 1.40 |
| combined | fixed | score>=70 | 809 | 23 | +0.578 | 4.92 | 1.69 | 7.3% | 174 | +0.251 | 1.43 |
| combined | fixed | score>=80 | 111 | 16 | -0.071 | -0.27 | 0.72 | 0.9% | 18 | -0.678 | 0.30 |
| combined | fixed | SPY>200d & stock>200d | 4922 | 20 | +0.367 | 6.63 | 1.496 | 3.8% | 1151 | +0.256 | 1.36 |
| combined | fixed | score>=70 & SPY>200d & stock>200d | 696 | 23 | +0.579 | 4.57 | 1.664 | 7.0% | 157 | +0.355 | 1.56 |
| combined | fixed | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 400 | 24 | +0.701 | 4.0 | 1.774 | 9.5% | 98 | +0.672 | 1.89 |
| combined | fixed | SPY>200d & stock>200d & RS>=0.8 | 2048 | 21 | +0.533 | 5.91 | 1.587 | 6.6% | 499 | +0.707 | 1.63 |
| combined | fixed | SPY>200d & stock>200d & RS>=0.9 | 1161 | 20 | +0.498 | 4.56 | 1.522 | 8.7% | 269 | +0.617 | 1.78 |
| combined | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1674 | 21 | +0.558 | 5.65 | 1.622 | 5.5% | 387 | +0.820 | 1.67 |
| combined | fixed | score>=70 & SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 338 | 24 | +0.705 | 3.66 | 1.763 | 8.0% | 77 | +0.824 | 2.09 |
| baseline_random | fixed | all | 12319 | 25 | +0.371 | 5.38 | 1.657 | 6.6% | 2927 | +0.273 | 1.53 |
| baseline_random | fixed | SPY>200d & stock>200d | 7999 | 24 | +0.414 | 12.38 | 1.522 | 4.7% | 1906 | +0.239 | 1.32 |
| baseline_random | fixed | SPY>200d & stock>200d & RS>=0.8 | 3155 | 24 | +0.495 | 9.02 | 1.598 | 7.9% | 776 | +0.460 | 1.55 |
| baseline_random | fixed | SPY>200d & stock>200d & RS>=0.9 | 1747 | 25 | +0.615 | 8.1 | 1.742 | 10.9% | 424 | +0.662 | 1.84 |
| baseline_random | fixed | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 2072 | 25 | +0.599 | 8.52 | 1.736 | 5.5% | 464 | +0.534 | 1.51 |
| breakout | trail | all | 5043 | 25 | +0.313 | 4.51 | 1.48 | 2.1% | 1153 | +0.060 | 1.25 |
| breakout | trail | score>=70 | 752 | 29 | +0.281 | 2.36 | 1.424 | 2.5% | 155 | -0.041 | 1.03 |
| breakout | trail | score>=80 | 108 | 21 | -0.299 | -1.63 | 0.549 | 0.9% | 17 | -0.738 | 0.19 |
| breakout | trail | SPY>200d & stock>200d | 4035 | 25 | +0.265 | 3.69 | 1.452 | 2.0% | 932 | +0.205 | 1.25 |
| breakout | trail | score>=70 & SPY>200d & stock>200d | 646 | 30 | +0.239 | 2.04 | 1.392 | 2.6% | 140 | +0.015 | 1.13 |
| breakout | trail | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 380 | 30 | +0.312 | 2.1 | 1.464 | 3.4% | 88 | +0.169 | 1.38 |
| breakout | trail | SPY>200d & stock>200d & RS>=0.8 | 1634 | 26 | +0.370 | 2.94 | 1.535 | 3.2% | 392 | +0.597 | 1.50 |
| breakout | trail | SPY>200d & stock>200d & RS>=0.9 | 900 | 28 | +0.419 | 2.81 | 1.592 | 3.7% | 204 | +0.466 | 1.53 |
| breakout | trail | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1343 | 27 | +0.365 | 2.89 | 1.528 | 2.6% | 303 | +0.817 | 1.61 |
| breakout | trail | score>=70 & SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 327 | 31 | +0.343 | 2.14 | 1.567 | 3.1% | 70 | +0.083 | 1.17 |
| momentum | trail | all | 4147 | 30 | +0.244 | 5.83 | 1.409 | 2.4% | 983 | +0.013 | 1.10 |
| momentum | trail | score>=70 | 158 | 32 | +0.204 | 1.18 | 1.424 | 4.4% | 38 | +0.508 | 2.04 |
| momentum | trail | score>=80 | 3 | 0 | -0.665 | -5.69 | 0.0 | 0.0% | 1 | -0.772 | 0.00 |
| momentum | trail | SPY>200d & stock>200d | 3691 | 31 | +0.251 | 5.74 | 1.437 | 2.2% | 900 | +0.031 | 1.12 |
| momentum | trail | score>=70 & SPY>200d & stock>200d | 140 | 32 | +0.284 | 1.48 | 1.59 | 5.0% | 36 | +0.574 | 2.13 |
| momentum | trail | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 78 | 31 | +0.402 | 1.39 | 1.83 | 7.7% | 23 | +1.037 | 2.96 |
| momentum | trail | SPY>200d & stock>200d & RS>=0.8 | 1461 | 31 | +0.247 | 3.43 | 1.469 | 3.5% | 365 | +0.114 | 1.30 |
| momentum | trail | SPY>200d & stock>200d & RS>=0.9 | 791 | 33 | +0.351 | 3.28 | 1.593 | 4.3% | 188 | +0.162 | 1.39 |
| momentum | trail | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1196 | 31 | +0.268 | 3.4 | 1.543 | 3.3% | 291 | +0.204 | 1.46 |
| momentum | trail | score>=70 & SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 51 | 33 | +0.635 | 1.56 | 2.676 | 9.8% | 14 | +1.847 | 5.61 |
| reversal | trail | all | 1084 | 25 | +0.610 | 3.23 | 2.799 | 6.1% | 310 | +0.534 | 2.46 |
| reversal | trail | score>=70 | 6 | 17 | -0.750 | -2.44 | 0.134 | 0.0% | 3 | -0.446 | 0.48 |
| reversal | trail | SPY>200d & stock>200d | 127 | 21 | -0.396 | -1.74 | 0.697 | 0.8% | 19 | -0.385 | 0.89 |
| reversal | trail | score>=70 & SPY>200d & stock>200d | 2 | 0 | -0.939 | -4.73 | 0.0 | 0.0% | 0 | — | — |
| reversal | trail | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 1 | 0 | -1.137 | None | 0.0 | 0.0% | 0 | — | — |
| reversal | trail | SPY>200d & stock>200d & RS>=0.8 | 31 | 23 | +0.124 | 0.19 | 1.527 | 3.2% | 5 | -0.086 | 1.64 |
| reversal | trail | SPY>200d & stock>200d & RS>=0.9 | 11 | 9 | +0.147 | 0.09 | 1.482 | 9.1% | 2 | -2.393 | 0.00 |
| reversal | trail | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 3 | 0 | -1.431 | -3.26 | 0.0 | 0.0% | 0 | — | — |
| combined | trail | all | 6287 | 27 | +0.297 | 5.46 | 1.442 | 2.3% | 1465 | +0.125 | 1.30 |
| combined | trail | score>=70 | 826 | 30 | +0.301 | 2.71 | 1.471 | 2.9% | 177 | +0.033 | 1.21 |
| combined | trail | score>=80 | 111 | 21 | -0.309 | -1.72 | 0.53 | 0.9% | 18 | -0.740 | 0.18 |
| combined | trail | SPY>200d & stock>200d | 5197 | 28 | +0.266 | 4.89 | 1.436 | 2.2% | 1228 | +0.236 | 1.30 |
| combined | trail | score>=70 & SPY>200d & stock>200d | 714 | 31 | +0.282 | 2.56 | 1.473 | 3.1% | 160 | +0.097 | 1.32 |
| combined | trail | score>=70 & SPY>200d & stock>200d & RS>=0.8 | 416 | 30 | +0.333 | 2.36 | 1.52 | 4.1% | 100 | +0.315 | 1.70 |
| combined | trail | SPY>200d & stock>200d & RS>=0.8 | 2145 | 27 | +0.366 | 3.82 | 1.485 | 3.5% | 527 | +0.484 | 1.47 |
| combined | trail | SPY>200d & stock>200d & RS>=0.9 | 1194 | 29 | +0.443 | 3.7 | 1.546 | 4.0% | 284 | +0.400 | 1.50 |
| combined | trail | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 1759 | 29 | +0.349 | 3.7 | 1.579 | 3.1% | 411 | +0.592 | 1.61 |
| combined | trail | score>=70 & SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 349 | 31 | +0.403 | 2.54 | 1.746 | 4.0% | 79 | +0.439 | 1.99 |
| baseline_random | trail | all | 12793 | 32 | +0.418 | 5.62 | 2.335 | 4.4% | 2908 | +0.362 | 1.92 |
| baseline_random | trail | SPY>200d & stock>200d | 9341 | 32 | +0.338 | 11.3 | 1.591 | 2.9% | 2293 | +0.171 | 1.31 |
| baseline_random | trail | SPY>200d & stock>200d & RS>=0.8 | 3392 | 32 | +0.386 | 7.09 | 1.709 | 4.2% | 837 | +0.287 | 1.49 |
| baseline_random | trail | SPY>200d & stock>200d & RS>=0.9 | 1790 | 34 | +0.566 | 6.57 | 2.024 | 5.9% | 424 | +0.504 | 1.96 |
| baseline_random | trail | SPY>200d & stock>200d & RS>=0.8 & high52>=0.9 | 2264 | 35 | +0.401 | 6.84 | 1.683 | 2.6% | 529 | +0.310 | 1.35 |

## Score buckets (fixed exit, every candidate, no position lock)

| strategy | score | n | avgR |
|---|---|---|---|
| breakout | [0, 50) | 2919 | +0.292 |
| breakout | [50, 60) | 2654 | +0.272 |
| breakout | [60, 70) | 2143 | +0.566 |
| breakout | [70, 80) | 801 | +0.509 |
| breakout | [80, 90) | 113 | -0.141 |
| momentum | [0, 50) | 6320 | +0.441 |
| momentum | [50, 60) | 4124 | +0.292 |
| momentum | [60, 70) | 1414 | +0.275 |
| momentum | [70, 80) | 182 | +0.647 |
| momentum | [80, 90) | 3 | -0.720 |
| reversal | [0, 50) | 853 | +0.353 |
| reversal | [50, 60) | 234 | +0.177 |
| reversal | [60, 70) | 75 | +0.152 |
| reversal | [70, 80) | 6 | -0.996 |