# Your solver vs CP-SAT: plans and scores

"Your plan" is from `results/<puzzle>.solution.json` (`python -m src.main`, 10 s limit). "CP-SAT plan" is
from `cpsat/results/<puzzle>.json` (60 s limit; every one is proven OPTIMAL or INFEASIBLE). Both scores are
computed with the same penalty function, which matches the project's `total_penalty` to 9 decimal places.
Every CP-SAT plan below also passes the project's own `src.evaluation.validator.validate`.

The penalty is a sum of one value per dish, and days are interchangeable. So the score difference comes
entirely from which dishes are chosen, not from which day they are on. "Penalty" next to a dish is that
dish's contribution to the total; lower is better.

## Summary

| Puzzle | Your status | Your penalty | CP-SAT status | CP-SAT penalty | Difference | Change | Dishes differing | Verdict |
|---|---|---|---|---|---|---|---|---|
| easy_01 | SOLVABLE | 7.0576 | OPTIMAL | 6.7987 | -0.2589 | -3.67% | 3 of 21 | CP-SAT cheaper |
| easy_02 | SOLVABLE | 7.0576 | OPTIMAL | 6.7987 | -0.2589 | -3.67% | 3 of 21 | CP-SAT cheaper |
| easy_03 | SOLVABLE | 7.0671 | OPTIMAL | 6.8201 | -0.2470 | -3.49% | 4 of 21 | CP-SAT cheaper |
| easy_04 | SOLVABLE | 7.0576 | OPTIMAL | 6.7987 | -0.2589 | -3.67% | 3 of 21 | CP-SAT cheaper |
| easy_05 | SOLVABLE | 7.0576 | OPTIMAL | 6.7987 | -0.2589 | -3.67% | 3 of 21 | CP-SAT cheaper |
| easy_06 | SOLVABLE | 7.0576 | OPTIMAL | 6.7987 | -0.2589 | -3.67% | 3 of 21 | CP-SAT cheaper |
| easy_07 | SOLVABLE | 7.0576 | OPTIMAL | 6.7987 | -0.2589 | -3.67% | 3 of 21 | CP-SAT cheaper |
| easy_08 | SOLVABLE | 7.0576 | OPTIMAL | 6.7987 | -0.2589 | -3.67% | 3 of 21 | CP-SAT cheaper |
| easy_09 | SOLVABLE | 7.0576 | OPTIMAL | 6.7987 | -0.2589 | -3.67% | 3 of 21 | CP-SAT cheaper |
| easy_10 | SOLVABLE | 6.3084 | OPTIMAL | 6.2729 | -0.0355 | -0.56% | 2 of 21 | CP-SAT cheaper |
| hard_01 | SOLVABLE | 7.7574 | OPTIMAL | 7.7357 | -0.0216 | -0.28% | 3 of 21 | CP-SAT cheaper |
| hard_02 | SOLVABLE | 8.3333 | OPTIMAL | 8.2262 | -0.1071 | -1.29% | 2 of 21 | CP-SAT cheaper |
| hard_03 | SOLVABLE | 7.4762 | OPTIMAL | 7.4762 | +0.0000 | +0.00% | 0 of 21 | Same score |
| hard_04 | SOLVABLE | 8.4147 | OPTIMAL | 8.4147 | +0.0000 | +0.00% | 0 of 21 | Same score |
| hard_05 | SOLVABLE | 7.1203 | OPTIMAL | 6.8942 | -0.2262 | -3.18% | 4 of 21 | CP-SAT cheaper |
| impossible_01 | UNSOLVABLE | – | INFEASIBLE | – | – | – | Both: no solution |
| impossible_02 | UNSOLVABLE | – | INFEASIBLE | – | – | – | Both: no solution |
| impossible_03 | UNSOLVABLE | – | INFEASIBLE | – | – | – | Both: no solution |

## Plans

### easy_01

Your plan **7.0576** → CP-SAT **6.7987**: -0.2589 (-3.67%). 3 of 21 dishes differ (bold).

| Day | Your plan | CP-SAT plan |
|---|---|---|
| 1 | **D012**, D022, D084 | D022, D023, D111 |
| 2 | D066, D080, D083 | D024, D066, D080 |
| 3 | D027, D081, D082 | **D065**, D070, D084 |
| 4 | D085, **D092**, **D106** | **D028**, D082, D085 |
| 5 | D023, D062, D110 | D027, D083, D110 |
| 6 | D024, D067, D109 | D081, **D107**, D109 |
| 7 | D025, D070, D111 | D025, D062, D067 |

| Only in your plan | Penalty | Only in CP-SAT plan | Penalty |
|---|---|---|---|
| D106 Economy Rice: Brown Rice + Stir-fried Kailan + Stir-fried Cabbage | 0.2812 | D107 Economy Rice: Brown Rice + Stir-fried Kailan + Mapo Tofu | 0.3288 |
| D092 Economy Rice: Brown Rice + Sweet & Sour Pork + Mapo Tofu | 0.4716 | D065 Economy Rice: White Rice + Sweet & Sour Pork + Stir-fried Cabbage | 0.3883 |
| D012 Fried Rice | 0.6355 | D028 Nasi Goreng | 0.4123 |
| **Total** | **1.3883** | **Total** | **1.1294** |

Swapping these dishes accounts for the whole difference: 1.1294 − 1.3883 = -0.2589.


### easy_02

Your plan **7.0576** → CP-SAT **6.7987**: -0.2589 (-3.67%). 3 of 21 dishes differ (bold).

| Day | Your plan | CP-SAT plan |
|---|---|---|
| 1 | **D012**, D022, D084 | D022, D023, D111 |
| 2 | D066, D080, D083 | D024, D066, D080 |
| 3 | D027, D081, D082 | D027, D081, D084 |
| 4 | D085, **D092**, **D106** | **D028**, D082, D085 |
| 5 | D023, D062, D110 | D083, **D107**, D109 |
| 6 | D024, D067, D109 | **D065**, D070, D110 |
| 7 | D025, D070, D111 | D025, D062, D067 |

| Only in your plan | Penalty | Only in CP-SAT plan | Penalty |
|---|---|---|---|
| D106 Economy Rice: Brown Rice + Stir-fried Kailan + Stir-fried Cabbage | 0.2812 | D107 Economy Rice: Brown Rice + Stir-fried Kailan + Mapo Tofu | 0.3288 |
| D092 Economy Rice: Brown Rice + Sweet & Sour Pork + Mapo Tofu | 0.4716 | D065 Economy Rice: White Rice + Sweet & Sour Pork + Stir-fried Cabbage | 0.3883 |
| D012 Fried Rice | 0.6355 | D028 Nasi Goreng | 0.4123 |
| **Total** | **1.3883** | **Total** | **1.1294** |

Swapping these dishes accounts for the whole difference: 1.1294 − 1.3883 = -0.2589.


### easy_03

Your plan **7.0671** → CP-SAT **6.8201**: -0.2470 (-3.49%). 4 of 21 dishes differ (bold).

| Day | Your plan | CP-SAT plan |
|---|---|---|
| 1 | **D012**, D022, D084 | D022, D023, D111 |
| 2 | D066, D080, D083 | D024, D066, D080 |
| 3 | D027, D081, D082 | **D028**, D084, D085 |
| 4 | D085, D092, **D106** | **D069**, D082, D092 |
| 5 | D023, **D062**, D110 | D083, **D107**, D109 |
| 6 | D024, **D067**, D109 | **D065**, D070, D110 |
| 7 | D034, D070, D111 | D027, D034, D081 |

| Only in your plan | Penalty | Only in CP-SAT plan | Penalty |
|---|---|---|---|
| D106 Economy Rice: Brown Rice + Stir-fried Kailan + Stir-fried Cabbage | 0.2812 | D107 Economy Rice: Brown Rice + Stir-fried Kailan + Mapo Tofu | 0.3288 |
| D062 Economy Rice: White Rice + Steamed Chicken (Skinless) + Mapo Tofu | 0.4121 | D069 Economy Rice: White Rice + Fried Fish Fillet + Stir-fried Cabbage | 0.3645 |
| D067 Economy Rice: White Rice + Sweet & Sour Pork + Bitter Gourd with Egg | 0.4121 | D065 Economy Rice: White Rice + Sweet & Sour Pork + Stir-fried Cabbage | 0.3883 |
| D012 Fried Rice | 0.6355 | D028 Nasi Goreng | 0.4123 |
| **Total** | **1.7409** | **Total** | **1.4939** |

Swapping these dishes accounts for the whole difference: 1.4939 − 1.7409 = -0.2470.


### easy_04

Your plan **7.0576** → CP-SAT **6.7987**: -0.2589 (-3.67%). 3 of 21 dishes differ (bold).

| Day | Your plan | CP-SAT plan |
|---|---|---|
| 1 | **D012**, D022, D084 | D022, D023, **D065** |
| 2 | D066, D080, D083 | D024, D066, D080 |
| 3 | D027, D081, D082 | D027, D084, D109 |
| 4 | D085, **D092**, **D106** | **D028**, D082, D085 |
| 5 | D023, D062, D110 | D081, D083, **D107** |
| 6 | D024, D067, D109 | D070, D110, D111 |
| 7 | D025, D070, D111 | D025, D062, D067 |

| Only in your plan | Penalty | Only in CP-SAT plan | Penalty |
|---|---|---|---|
| D106 Economy Rice: Brown Rice + Stir-fried Kailan + Stir-fried Cabbage | 0.2812 | D107 Economy Rice: Brown Rice + Stir-fried Kailan + Mapo Tofu | 0.3288 |
| D092 Economy Rice: Brown Rice + Sweet & Sour Pork + Mapo Tofu | 0.4716 | D065 Economy Rice: White Rice + Sweet & Sour Pork + Stir-fried Cabbage | 0.3883 |
| D012 Fried Rice | 0.6355 | D028 Nasi Goreng | 0.4123 |
| **Total** | **1.3883** | **Total** | **1.1294** |

Swapping these dishes accounts for the whole difference: 1.1294 − 1.3883 = -0.2589.


### easy_05

Your plan **7.0576** → CP-SAT **6.7987**: -0.2589 (-3.67%). 3 of 21 dishes differ (bold).

| Day | Your plan | CP-SAT plan |
|---|---|---|
| 1 | **D012**, D022, D082 | D022, D023, D111 |
| 2 | D066, D080, D083 | D024, D066, D080 |
| 3 | D027, D081, D084 | D027, D083, D084 |
| 4 | D085, **D092**, **D106** | **D028**, D082, D085 |
| 5 | D023, D062, D110 | **D065**, D070, D110 |
| 6 | D024, D067, D109 | D081, **D107**, D109 |
| 7 | D025, D070, D111 | D025, D062, D067 |

| Only in your plan | Penalty | Only in CP-SAT plan | Penalty |
|---|---|---|---|
| D106 Economy Rice: Brown Rice + Stir-fried Kailan + Stir-fried Cabbage | 0.2812 | D107 Economy Rice: Brown Rice + Stir-fried Kailan + Mapo Tofu | 0.3288 |
| D092 Economy Rice: Brown Rice + Sweet & Sour Pork + Mapo Tofu | 0.4716 | D065 Economy Rice: White Rice + Sweet & Sour Pork + Stir-fried Cabbage | 0.3883 |
| D012 Fried Rice | 0.6355 | D028 Nasi Goreng | 0.4123 |
| **Total** | **1.3883** | **Total** | **1.1294** |

Swapping these dishes accounts for the whole difference: 1.1294 − 1.3883 = -0.2589.


### easy_06

Your plan **7.0576** → CP-SAT **6.7987**: -0.2589 (-3.67%). 3 of 21 dishes differ (bold).

| Day | Your plan | CP-SAT plan |
|---|---|---|
| 1 | **D012**, D022, D084 | D022, D023, D111 |
| 2 | D066, D080, D083 | D024, D066, D080 |
| 3 | D027, D081, D082 | **D028**, D084, D085 |
| 4 | D085, **D092**, **D106** | D027, D082, **D107** |
| 5 | D023, D062, D110 | D081, D083, D109 |
| 6 | D024, D067, D109 | **D065**, D070, D110 |
| 7 | D025, D070, D111 | D025, D062, D067 |

| Only in your plan | Penalty | Only in CP-SAT plan | Penalty |
|---|---|---|---|
| D106 Economy Rice: Brown Rice + Stir-fried Kailan + Stir-fried Cabbage | 0.2812 | D107 Economy Rice: Brown Rice + Stir-fried Kailan + Mapo Tofu | 0.3288 |
| D092 Economy Rice: Brown Rice + Sweet & Sour Pork + Mapo Tofu | 0.4716 | D065 Economy Rice: White Rice + Sweet & Sour Pork + Stir-fried Cabbage | 0.3883 |
| D012 Fried Rice | 0.6355 | D028 Nasi Goreng | 0.4123 |
| **Total** | **1.3883** | **Total** | **1.1294** |

Swapping these dishes accounts for the whole difference: 1.1294 − 1.3883 = -0.2589.


### easy_07

Your plan **7.0576** → CP-SAT **6.7987**: -0.2589 (-3.67%). 3 of 21 dishes differ (bold).

| Day | Your plan | CP-SAT plan |
|---|---|---|
| 1 | **D012**, D022, D084 | D022, D023, D111 |
| 2 | D066, D080, D083 | D024, D066, D080 |
| 3 | D027, D081, D082 | **D028**, D084, D085 |
| 4 | D085, **D092**, **D106** | D027, D081, D082 |
| 5 | D023, D062, D110 | D083, **D107**, D109 |
| 6 | D024, D067, D109 | **D065**, D070, D110 |
| 7 | D025, D070, D111 | D025, D062, D067 |

| Only in your plan | Penalty | Only in CP-SAT plan | Penalty |
|---|---|---|---|
| D106 Economy Rice: Brown Rice + Stir-fried Kailan + Stir-fried Cabbage | 0.2812 | D107 Economy Rice: Brown Rice + Stir-fried Kailan + Mapo Tofu | 0.3288 |
| D092 Economy Rice: Brown Rice + Sweet & Sour Pork + Mapo Tofu | 0.4716 | D065 Economy Rice: White Rice + Sweet & Sour Pork + Stir-fried Cabbage | 0.3883 |
| D012 Fried Rice | 0.6355 | D028 Nasi Goreng | 0.4123 |
| **Total** | **1.3883** | **Total** | **1.1294** |

Swapping these dishes accounts for the whole difference: 1.1294 − 1.3883 = -0.2589.


### easy_08

Your plan **7.0576** → CP-SAT **6.7987**: -0.2589 (-3.67%). 3 of 21 dishes differ (bold).

| Day | Your plan | CP-SAT plan |
|---|---|---|
| 1 | **D012**, D022, D084 | D022, D023, D111 |
| 2 | D066, D080, D083 | D024, D066, D080 |
| 3 | D027, D081, D082 | **D028**, D084, D085 |
| 4 | D085, **D092**, **D106** | D027, D082, D109 |
| 5 | D023, D062, D110 | D081, D083, **D107** |
| 6 | D024, D067, D109 | **D065**, D070, D110 |
| 7 | D025, D070, D111 | D025, D062, D067 |

| Only in your plan | Penalty | Only in CP-SAT plan | Penalty |
|---|---|---|---|
| D106 Economy Rice: Brown Rice + Stir-fried Kailan + Stir-fried Cabbage | 0.2812 | D107 Economy Rice: Brown Rice + Stir-fried Kailan + Mapo Tofu | 0.3288 |
| D092 Economy Rice: Brown Rice + Sweet & Sour Pork + Mapo Tofu | 0.4716 | D065 Economy Rice: White Rice + Sweet & Sour Pork + Stir-fried Cabbage | 0.3883 |
| D012 Fried Rice | 0.6355 | D028 Nasi Goreng | 0.4123 |
| **Total** | **1.3883** | **Total** | **1.1294** |

Swapping these dishes accounts for the whole difference: 1.1294 − 1.3883 = -0.2589.


### easy_09

Your plan **7.0576** → CP-SAT **6.7987**: -0.2589 (-3.67%). 3 of 21 dishes differ (bold).

| Day | Your plan | CP-SAT plan |
|---|---|---|
| 1 | **D012**, D022, D084 | D022, D023, **D065** |
| 2 | D066, D080, D083 | D024, D066, D080 |
| 3 | D027, D081, D082 | **D028**, D084, D085 |
| 4 | D085, **D092**, **D106** | D027, D082, D109 |
| 5 | D023, D062, D110 | D081, D083, **D107** |
| 6 | D024, D067, D109 | D070, D110, D111 |
| 7 | D025, D070, D111 | D025, D062, D067 |

| Only in your plan | Penalty | Only in CP-SAT plan | Penalty |
|---|---|---|---|
| D106 Economy Rice: Brown Rice + Stir-fried Kailan + Stir-fried Cabbage | 0.2812 | D107 Economy Rice: Brown Rice + Stir-fried Kailan + Mapo Tofu | 0.3288 |
| D092 Economy Rice: Brown Rice + Sweet & Sour Pork + Mapo Tofu | 0.4716 | D065 Economy Rice: White Rice + Sweet & Sour Pork + Stir-fried Cabbage | 0.3883 |
| D012 Fried Rice | 0.6355 | D028 Nasi Goreng | 0.4123 |
| **Total** | **1.3883** | **Total** | **1.1294** |

Swapping these dishes accounts for the whole difference: 1.1294 − 1.3883 = -0.2589.


### easy_10

Your plan **6.3084** → CP-SAT **6.2729**: -0.0355 (-0.56%). 2 of 21 dishes differ (bold).

| Day | Your plan | CP-SAT plan |
|---|---|---|
| 1 | D022, D023, D080 | D022, D084, D085 |
| 2 | D027, D082, D084 | D080, D107, D111 |
| 3 | D081, D083, D106 | D024, D082, D109 |
| 4 | D024, D085, D110 | D081, D083, D106 |
| 5 | D025, D026, **D066** | D026, D027, D110 |
| 6 | D034, D107, D109 | D023, **D029**, D108 |
| 7 | **D069**, D108, D111 | D025, D034, **D070** |

| Only in your plan | Penalty | Only in CP-SAT plan | Penalty |
|---|---|---|---|
| D069 Economy Rice: White Rice + Fried Fish Fillet + Stir-fried Cabbage | 0.3645 | D029 Mee Goreng | 0.3528 |
| D066 Economy Rice: White Rice + Sweet & Sour Pork + Mapo Tofu | 0.4359 | D070 Economy Rice: White Rice + Fried Fish Fillet + Mapo Tofu | 0.4121 |
| **Total** | **0.8004** | **Total** | **0.7649** |

Swapping these dishes accounts for the whole difference: 0.7649 − 0.8004 = -0.0355.


### hard_01

Your plan **7.7574** → CP-SAT **7.7357**: -0.0216 (-0.28%). 3 of 21 dishes differ (bold).

| Day | Your plan | CP-SAT plan |
|---|---|---|
| 1 | D035, D092, **D107** | D071, D080, D092 |
| 2 | D070, D080, D093 | D067, D084, D096 |
| 3 | D064, D084, D096 | D070, **D082**, D091 |
| 4 | D069, D085, D090 | **D068**, D083, D093 |
| 5 | D071, D081, D091 | D064, D065, D081 |
| 6 | **D036**, D066, **D109** | D069, D085, D090 |
| 7 | D065, D067, D083 | D035, D066, **D111** |

| Only in your plan | Penalty | Only in CP-SAT plan | Penalty |
|---|---|---|---|
| D109 Economy Rice: Brown Rice + Stir-fried Cabbage + Mapo Tofu | 0.3050 | D082 Economy Rice: White Rice + Stir-fried Kailan + Bitter Gourd with Egg | 0.2693 |
| D107 Economy Rice: Brown Rice + Stir-fried Kailan + Mapo Tofu | 0.3288 | D111 Economy Rice: Brown Rice + Mapo Tofu + Bitter Gourd with Egg | 0.3288 |
| D036 Naan | 0.3742 | D068 Economy Rice: White Rice + Fried Fish Fillet + Stir-fried Kailan | 0.3883 |
| **Total** | **1.0080** | **Total** | **0.9864** |

Swapping these dishes accounts for the whole difference: 0.9864 − 1.0080 = -0.0216.


### hard_02

Your plan **8.3333** → CP-SAT **8.2262**: -0.1071 (-1.29%). 2 of 21 dishes differ (bold).

| Day | Your plan | CP-SAT plan |
|---|---|---|
| 1 | D027, D063, D066 | D074, D083, D107 |
| 2 | D073, D092, D096 | **D060**, D062, D081 |
| 3 | D070, D075, **D104** | **D061**, D085, D100 |
| 4 | **D071**, D078, D100 | D088, D109, D111 |
| 5 | D074, D107, D109 | D027, D063, D066 |
| 6 | D081, D083, D088 | D070, D073, D092 |
| 7 | D062, D085, D111 | D075, D078, D096 |

| Only in your plan | Penalty | Only in CP-SAT plan | Penalty |
|---|---|---|---|
| D071 Economy Rice: White Rice + Fried Fish Fillet + Bitter Gourd with Egg | 0.3883 | D061 Economy Rice: White Rice + Steamed Chicken (Skinless) + Stir-fried Cabbage | 0.3645 |
| D104 Economy Rice: Brown Rice + Curry Chicken + Mapo Tofu | 0.4716 | D060 Economy Rice: White Rice + Steamed Chicken (Skinless) + Stir-fried Kailan | 0.3883 |
| **Total** | **0.8600** | **Total** | **0.7528** |

Swapping these dishes accounts for the whole difference: 0.7528 − 0.8600 = -0.1071.


### hard_03

Same score (7.4762). The two plans use the same 21 dishes, grouped into days differently.


### hard_04

Same score (8.4147). The two plans use the same 21 dishes, in the same days.


### hard_05

Your plan **7.1203** → CP-SAT **6.8942**: -0.2262 (-3.18%). 4 of 21 dishes differ (bold).

| Day | Your plan | CP-SAT plan |
|---|---|---|
| 1 | D028, D062, D080 | D022, D062, D083 |
| 2 | D026, D066, D107 | D027, D080, **D111** |
| 3 | D029, D070, D109 | D023, **D078**, D084 |
| 4 | D022, **D071**, **D096** | D028, D082, **D085** |
| 5 | D024, D082, **D092** | D024, **D065**, D081 |
| 6 | D023, **D069**, D081 | D026, D066, D107 |
| 7 | D027, D083, D084 | D029, D070, D109 |

| Only in your plan | Penalty | Only in CP-SAT plan | Penalty |
|---|---|---|---|
| D069 Economy Rice: White Rice + Fried Fish Fillet + Stir-fried Cabbage | 0.3645 | D085 Economy Rice: White Rice + Mapo Tofu + Bitter Gourd with Egg | 0.2931 |
| D071 Economy Rice: White Rice + Fried Fish Fillet + Bitter Gourd with Egg | 0.3883 | D111 Economy Rice: Brown Rice + Mapo Tofu + Bitter Gourd with Egg | 0.3288 |
| D096 Economy Rice: Brown Rice + Fried Fish Fillet + Mapo Tofu | 0.4478 | D065 Economy Rice: White Rice + Sweet & Sour Pork + Stir-fried Cabbage | 0.3883 |
| D092 Economy Rice: Brown Rice + Sweet & Sour Pork + Mapo Tofu | 0.4716 | D078 Economy Rice: White Rice + Curry Chicken + Mapo Tofu | 0.4359 |
| **Total** | **1.6723** | **Total** | **1.4461** |

Swapping these dishes accounts for the whole difference: 1.4461 − 1.6723 = -0.2262.

