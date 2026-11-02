# Scorer results

PASS = valid plan on a feasible puzzle, or 'no solution' on an impossible puzzle.

## Summary by method

| method | difficulty | runs | delivery_pct | final_pass_pct | false_feasible | false_infeasible | avg_violations | avg_penalty_valid | avg_tokens | avg_time_s |
|---|---|---|---|---|---|---|---|---|---|---|
| csp | easy | 10 | 100.00 | 100.00 | 0 | 0 | 0.00 | 6.98 |  | 10.24 |
| csp | hard | 5 | 100.00 | 100.00 | 0 | 0 | 0.00 | 7.82 |  | 10.16 |
| csp | impossible | 3 | 100.00 | 100.00 | 0 | 0 |  |  |  | 8.70 |
| llm | hard | 9 | 100.00 | 0.00 | 0 | 0 | 8.33 |  |  |  |
| llm | impossible | 3 | 100.00 | 0.00 | 3 | 0 | 10.33 |  |  |  |
| llm_medium | hard | 3 | 100.00 | 0.00 | 0 | 0 | 6.33 |  |  |  |

## Every run

| puzzle | difficulty | method | run | result | outcome | num_violations | penalty | what_went_wrong |
|---|---|---|---|---|---|---|---|---|
| easy_01 | easy | csp | 0 | PASS | valid | 0 | 7.06 |  |
| easy_02 | easy | csp | 0 | PASS | valid | 0 | 7.06 |  |
| easy_03 | easy | csp | 0 | PASS | valid | 0 | 7.07 |  |
| easy_04 | easy | csp | 0 | PASS | valid | 0 | 7.06 |  |
| easy_05 | easy | csp | 0 | PASS | valid | 0 | 7.06 |  |
| easy_06 | easy | csp | 0 | PASS | valid | 0 | 7.06 |  |
| easy_07 | easy | csp | 0 | PASS | valid | 0 | 7.06 |  |
| easy_08 | easy | csp | 0 | PASS | valid | 0 | 7.06 |  |
| easy_09 | easy | csp | 0 | PASS | valid | 0 | 7.06 |  |
| easy_10 | easy | csp | 0 | PASS | valid | 0 | 6.31 |  |
| hard_01 | hard | csp | 0 | PASS | valid | 0 | 7.76 |  |
| hard_01 | hard | llm | 1 | FAIL | invalid | 5 |  | D070 used 3 times (max 1); D084 used 2 times (max 1); D091 used 2 times (max 1); day 5: energy_kcal 1790 is under the min 1824; day 5: sodium_mg 2501 is over the max 2500 |
| hard_01 | hard | llm | 2 | FAIL | invalid | 13 |  | day 1: price_sgd 10.1 is over the max 10; day 1: sodium_mg 2806 is over the max 2500; day 4: energy_kcal 1635 is under the min 1824; day 4: protein_g 50.3 is under the min 50.8; day 5: price_sgd 11.5 is over the max 10; day 5: sodium_mg 3214 is over the max 2500; day 6: price_sgd 11.2 is over the max 10; day 6: energy_kcal 1808 is under the min 1824; day 6: sodium_mg 2885 is over the max 2500; day 7: price_sgd 11.3 is over the max 10; day 7: energy_kcal 1663 is under the min 1824; day 7: sodium_mg 2953 is over the max 2500; sodium_mg 18984 is over the max 17000 |
| hard_01 | hard | llm | 3 | FAIL | invalid | 9 |  | day 4: energy_kcal 1744 is under the min 1824; day 5: sodium_mg 3018 is over the max 2500; day 6: price_sgd 10.4 is over the max 10; day 6: energy_kcal 1807 is under the min 1824; day 6: sodium_mg 3019 is over the max 2500; day 7: price_sgd 10.3 is over the max 10; day 7: energy_kcal 1603 is under the min 1824; day 7: sodium_mg 2613 is over the max 2500; sodium_mg 18184 is over the max 17000 |
| hard_01 | hard | llm_medium | 1 | FAIL | invalid | 6 |  | D064 used 2 times (max 1); day 6: energy_kcal 1674 is under the min 1824; day 6: sodium_mg 2587 is over the max 2500; day 7: price_sgd 10.5 is over the max 10; day 7: sodium_mg 2943 is over the max 2500; sodium_mg 17519 is over the max 17000 |
| hard_01 | hard | llm_medium | 2 | FAIL | invalid | 5 |  | D065 used 2 times (max 1); D067 used 2 times (max 1); D080 used 2 times (max 1); day 5: price_sgd 10.3 is over the max 10; day 7: energy_kcal 1540 is under the min 1824 |
| hard_01 | hard | llm_medium | 3 | FAIL | invalid | 8 |  | D067 used 2 times (max 1); day 6: price_sgd 10.3 is over the max 10; day 6: energy_kcal 1599 is under the min 1824; day 6: sodium_mg 2625 is over the max 2500; day 7: price_sgd 10.3 is over the max 10; day 7: energy_kcal 1372 is under the min 1824; sodium_mg 17160 is over the max 17000; has_iron in 6 dishes (need 7) |
| hard_02 | hard | csp | 0 | PASS | valid | 0 | 8.33 |  |
| hard_03 | hard | csp | 0 | PASS | valid | 0 | 7.48 |  |
| hard_03 | hard | llm | 1 | FAIL | invalid | 5 |  | day 6: sodium_mg 3821 is over the max 3500; day 6: fat_g 97.6 is over the max 90; day 7: price_sgd 12.3 is over the max 10; day 7: sodium_mg 3549 is over the max 3500; day 7: has_vit_c in 0 dishes (need 1) |
| hard_03 | hard | llm | 2 | FAIL | invalid | 7 |  | day 5: price_sgd 10.1 is over the max 10; day 6: price_sgd 10.7 is over the max 10; day 6: energy_kcal 1597 is under the min 1824; day 6: calcium_mg 540 is under the min 600; day 7: price_sgd 10.5 is over the max 10; day 7: energy_kcal 1751 is under the min 1824; day 7: calcium_mg 475 is under the min 600 |
| hard_03 | hard | llm | 3 | FAIL | invalid | 5 |  | D083 used 2 times (max 1); D082 used 2 times (max 1); day 6: energy_kcal 1804 is under the min 1824; day 7: price_sgd 11.3 is over the max 10; day 7: energy_kcal 1760 is under the min 1824 |
| hard_04 | hard | csp | 0 | PASS | valid | 0 | 8.41 |  |
| hard_04 | hard | llm | 1 | FAIL | invalid | 11 |  | D081 used 2 times (max 1); D062 used 2 times (max 1); day 3: fibre_g 19.8 is under the min 20; day 4: fibre_g 17 is under the min 20; day 4: has_vit_d in 0 dishes (need 1); day 5: fibre_g 17.9 is under the min 20; day 6: energy_kcal 1533 is under the min 1900; day 6: calcium_mg 540 is under the min 600; day 6: fibre_g 16.8 is under the min 20; day 7: sodium_mg 4799 is over the max 4500; day 7: fibre_g 19.1 is under the min 20 |
| hard_04 | hard | llm | 2 | FAIL | invalid | 8 |  | day 5: energy_kcal 1888 is under the min 1900; day 5: calcium_mg 570 is under the min 600; day 6: sodium_mg 4733 is over the max 4500; day 6: calcium_mg 590 is under the min 600; day 6: fibre_g 18 is under the min 20; day 7: energy_kcal 1884 is under the min 1900; day 7: calcium_mg 560 is under the min 600; day 7: fibre_g 16.7 is under the min 20 |
| hard_04 | hard | llm | 3 | FAIL | invalid | 12 |  | D085 used 2 times (max 1); D109 used 2 times (max 1); D014 used 3 times (max 1); D104 used 3 times (max 1); D078 used 2 times (max 1); day 4: has_vit_d in 0 dishes (need 1); day 5: energy_kcal 1850 is under the min 1900; day 5: fibre_g 19.6 is under the min 20; day 6: energy_kcal 1881 is under the min 1900; day 6: fibre_g 17.2 is under the min 20; day 7: sodium_mg 4577 is over the max 4500; day 7: calcium_mg 560 is under the min 600 |
| hard_05 | hard | csp | 0 | PASS | valid | 0 | 7.12 |  |
| impossible_01 | impossible | csp | 0 | PASS | declared_infeasible | 0 |  | correctly said no solution |
| impossible_01 | impossible | llm | 1 | FAIL | invalid | 14 |  | gave a plan for an impossible puzzle |
| impossible_02 | impossible | csp | 0 | PASS | declared_infeasible | 0 |  | correctly said no solution |
| impossible_02 | impossible | llm | 1 | FAIL | invalid | 10 |  | gave a plan for an impossible puzzle |
| impossible_03 | impossible | csp | 0 | PASS | declared_infeasible | 0 |  | correctly said no solution |
| impossible_03 | impossible | llm | 1 | FAIL | invalid | 7 |  | gave a plan for an impossible puzzle |

## Constraint pass rates

| method | difficulty | constraint | pass % | plans |
|---|---|---|---|---|
| csp | easy | daily:calcium_mg | 100.00 | 1 |
| csp | easy | daily:energy_kcal | 100.00 | 10 |
| csp | easy | daily:fat_g | 100.00 | 1 |
| csp | easy | daily:price_sgd | 100.00 | 10 |
| csp | easy | daily:protein_g | 100.00 | 2 |
| csp | easy | daily:queue_min | 100.00 | 1 |
| csp | easy | daily:sodium_mg | 100.00 | 1 |
| csp | easy | daily:sugar_g | 100.00 | 1 |
| csp | easy | known_ids | 100.00 | 10 |
| csp | easy | mains_only | 100.00 | 10 |
| csp | easy | no_repeat | 100.00 | 10 |
| csp | easy | store_rating | 100.00 | 1 |
| csp | easy | weekly_presence:has_folate | 100.00 | 1 |
| csp | easy | weekly_presence:has_iron | 100.00 | 2 |
| csp | easy | weekly_presence:has_vit_a | 100.00 | 1 |
| csp | easy | weekly_presence:has_vit_b12 | 100.00 | 1 |
| csp | easy | weekly_presence:has_vit_b6 | 100.00 | 1 |
| csp | easy | weekly_presence:has_vit_c | 100.00 | 2 |
| csp | easy | weekly_presence:has_vit_d | 100.00 | 1 |
| csp | hard | daily:calcium_mg | 100.00 | 5 |
| csp | hard | daily:energy_kcal | 100.00 | 5 |
| csp | hard | daily:fat_g | 100.00 | 4 |
| csp | hard | daily:fibre_g | 100.00 | 2 |
| csp | hard | daily:price_sgd | 100.00 | 5 |
| csp | hard | daily:protein_g | 100.00 | 5 |
| csp | hard | daily:queue_min | 100.00 | 4 |
| csp | hard | daily:sodium_mg | 100.00 | 5 |
| csp | hard | daily:sugar_g | 100.00 | 5 |
| csp | hard | daily_presence:has_folate | 100.00 | 1 |
| csp | hard | daily_presence:has_vit_b12 | 100.00 | 1 |
| csp | hard | daily_presence:has_vit_c | 100.00 | 2 |
| csp | hard | daily_presence:has_vit_d | 100.00 | 1 |
| csp | hard | known_ids | 100.00 | 5 |
| csp | hard | mains_only | 100.00 | 5 |
| csp | hard | no_repeat | 100.00 | 5 |
| csp | hard | store_rating | 100.00 | 5 |
| csp | hard | weekly:sodium_mg | 100.00 | 5 |
| csp | hard | weekly_presence:has_folate | 100.00 | 5 |
| csp | hard | weekly_presence:has_iron | 100.00 | 5 |
| csp | hard | weekly_presence:has_vit_a | 100.00 | 5 |
| csp | hard | weekly_presence:has_vit_b12 | 100.00 | 5 |
| csp | hard | weekly_presence:has_vit_b6 | 100.00 | 5 |
| csp | hard | weekly_presence:has_vit_c | 100.00 | 5 |
| csp | hard | weekly_presence:has_vit_d | 100.00 | 5 |
| llm | hard | daily:calcium_mg | 55.56 | 9 |
| llm | hard | daily:energy_kcal | 11.11 | 9 |
| llm | hard | daily:fat_g | 88.89 | 9 |
| llm | hard | daily:fibre_g | 50.00 | 6 |
| llm | hard | daily:price_sgd | 44.44 | 9 |
| llm | hard | daily:protein_g | 88.89 | 9 |
| llm | hard | daily:queue_min | 100.00 | 6 |
| llm | hard | daily:sodium_mg | 22.22 | 9 |
| llm | hard | daily:sugar_g | 100.00 | 9 |
| llm | hard | daily_presence:has_folate | 100.00 | 3 |
| llm | hard | daily_presence:has_vit_c | 83.33 | 6 |
| llm | hard | daily_presence:has_vit_d | 33.33 | 3 |
| llm | hard | known_ids | 100.00 | 9 |
| llm | hard | mains_only | 100.00 | 9 |
| llm | hard | no_repeat | 55.56 | 9 |
| llm | hard | store_rating | 100.00 | 9 |
| llm | hard | weekly:sodium_mg | 77.78 | 9 |
| llm | hard | weekly_presence:has_folate | 100.00 | 9 |
| llm | hard | weekly_presence:has_iron | 100.00 | 9 |
| llm | hard | weekly_presence:has_vit_a | 100.00 | 9 |
| llm | hard | weekly_presence:has_vit_b12 | 100.00 | 9 |
| llm | hard | weekly_presence:has_vit_b6 | 100.00 | 9 |
| llm | hard | weekly_presence:has_vit_c | 100.00 | 9 |
| llm | hard | weekly_presence:has_vit_d | 100.00 | 9 |
| llm | impossible | daily:calcium_mg | 33.33 | 3 |
| llm | impossible | daily:energy_kcal | 33.33 | 3 |
| llm | impossible | daily:fat_g | 100.00 | 3 |
| llm | impossible | daily:fibre_g | 0.00 | 2 |
| llm | impossible | daily:price_sgd | 33.33 | 3 |
| llm | impossible | daily:protein_g | 100.00 | 3 |
| llm | impossible | daily:queue_min | 100.00 | 2 |
| llm | impossible | daily:sodium_mg | 33.33 | 3 |
| llm | impossible | daily:sugar_g | 100.00 | 3 |
| llm | impossible | daily_presence:has_folate | 100.00 | 1 |
| llm | impossible | daily_presence:has_vit_c | 50.00 | 2 |
| llm | impossible | daily_presence:has_vit_d | 100.00 | 1 |
| llm | impossible | known_ids | 100.00 | 3 |
| llm | impossible | mains_only | 100.00 | 3 |
| llm | impossible | no_repeat | 100.00 | 3 |
| llm | impossible | store_rating | 100.00 | 3 |
| llm | impossible | weekly:sodium_mg | 66.67 | 3 |
| llm | impossible | weekly_presence:has_folate | 100.00 | 3 |
| llm | impossible | weekly_presence:has_iron | 66.67 | 3 |
| llm | impossible | weekly_presence:has_vit_a | 100.00 | 3 |
| llm | impossible | weekly_presence:has_vit_b12 | 100.00 | 3 |
| llm | impossible | weekly_presence:has_vit_b6 | 100.00 | 3 |
| llm | impossible | weekly_presence:has_vit_c | 100.00 | 3 |
| llm | impossible | weekly_presence:has_vit_d | 100.00 | 3 |
| llm_medium | hard | daily:calcium_mg | 100.00 | 3 |
| llm_medium | hard | daily:energy_kcal | 0.00 | 3 |
| llm_medium | hard | daily:fat_g | 100.00 | 3 |
| llm_medium | hard | daily:fibre_g | 100.00 | 3 |
| llm_medium | hard | daily:price_sgd | 0.00 | 3 |
| llm_medium | hard | daily:protein_g | 100.00 | 3 |
| llm_medium | hard | daily:queue_min | 100.00 | 3 |
| llm_medium | hard | daily:sodium_mg | 33.33 | 3 |
| llm_medium | hard | daily:sugar_g | 100.00 | 3 |
| llm_medium | hard | known_ids | 100.00 | 3 |
| llm_medium | hard | mains_only | 100.00 | 3 |
| llm_medium | hard | no_repeat | 0.00 | 3 |
| llm_medium | hard | store_rating | 100.00 | 3 |
| llm_medium | hard | weekly:sodium_mg | 33.33 | 3 |
| llm_medium | hard | weekly_presence:has_folate | 100.00 | 3 |
| llm_medium | hard | weekly_presence:has_iron | 66.67 | 3 |
| llm_medium | hard | weekly_presence:has_vit_a | 100.00 | 3 |
| llm_medium | hard | weekly_presence:has_vit_b12 | 100.00 | 3 |
| llm_medium | hard | weekly_presence:has_vit_b6 | 100.00 | 3 |
| llm_medium | hard | weekly_presence:has_vit_c | 100.00 | 3 |
| llm_medium | hard | weekly_presence:has_vit_d | 100.00 | 3 |
