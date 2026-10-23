# CS4263-Group-4

# Puzzle Set

**Fixed rules (all puzzles):**
- 7 days, 3 mains per day.
- All 21 dishes are distinct.
- Drinks, sides and snacks are never chosen.
- Limits apply to the sum over a day's 3 dishes unless marked weekly.
- "–" means no limit.
  
## Easy puzzles

Every easy puzzle has a daily budget and a daily energy range, plus at most one extra rule.

| Puzzle | Budget/day | Energy/day (kcal) | Extra rule |
|---|---|---|---|
| easy_01 | ≤ $20 | 1824–2736 | – |
| easy_02 | ≤ $20 | 1824–2736 | Protein ≥ 50.8 g/day |
| easy_03 | ≤ $20 | 1824–2736 | Sodium ≤ 4500 mg/day |
| easy_04 | ≤ $20 | 1824–2736 | Store rating ≥ 3.5 |
| easy_05 | ≤ $20 | 1824–2736 | Calcium ≥ 250 mg/day |
| easy_06 | ≤ $20 | 1824–2736 | Sugar ≤ 57 g/day; iron and vit C at least once per week |
| easy_07 | ≤ $20 | 1824–2736 | All 7 vitamin/iron flags at least once per week |
| easy_08 | ≤ $20 | 1824–2736 | Queue ≤ 45 min/day |
| easy_09 | ≤ $20 | 1824–2736 | Fat ≤ 88.7 g/day |
| easy_10 | ≤ $15 | 1571–1920 | Protein ≥ 43.2 g/day |

## Hard puzzles: daily limits

| Puzzle | Rating | Budget | Energy (kcal) | Protein (g) | Sodium (mg) | Sugar (g) | Fat (g) | Calcium (mg) | Fibre (g) | Queue (min) |
|---|---|---|---|---|---|---|---|---|---|---|
| hard_01 | ≥ 3.6 | ≤ $10 | 1824–2736 | ≥ 50.8 | ≤ 2500 | ≤ 57 | ≤ 100 | ≥ 250 | ≥ 12 | ≤ 24 |
| hard_02 | ≥ 3.5 | ≤ $12 | 1824–2736 | ≥ 125 | ≤ 3800 | ≤ 57 | – | ≥ 200 | – | ≤ 60 |
| hard_03 | ≥ 3.6 | ≤ $10 | 1824–2400 | ≥ 43.2 | ≤ 3500 | ≤ 51.8 | ≤ 90 | ≥ 600 | – | – |
| hard_04 | ≥ 3.6 | ≤ $20 | 1900–2736 | ≥ 85 | ≤ 4500 | ≤ 50 | ≤ 105 | ≥ 600 | ≥ 20 | ≤ 54 |
| hard_05 | ≥ 3.6 | ≤ $11 | 1824–2736 | ≥ 55 | ≤ 4500 | ≤ 57 | ≤ 100 | ≥ 200 | – | ≤ 18 |

## Hard puzzles: weekly sodium and vitamin/iron rules

| Puzzle | Weekly sodium (mg) | Required every day | Vitamin/iron flags per week |
|---|---|---|---|
| hard_01 | ≤ 17000 | – | All 7, at least 7 dishes each |
| hard_02 | ≤ 28000 | Vit B12 | All 7, at least 2 dishes each |
| hard_03 | ≤ 28000 | Vit C | All 7, at least 2 dishes each |
| hard_04 | ≤ 28000 | Vit C, folate, vit D | All 7, at least 3 dishes each |
| hard_05 | ≤ 28000 | – | All 7, at least 2 dishes each |

## Tightest constraint per hard puzzle

| Puzzle | Tightest constraint |
|---|---|
| hard_01 | $10 budget with 2500 mg sodium per day |
| hard_02 | 125 g protein on $12 a day |
| hard_03 | 600 mg calcium on $10 a day |
| hard_04 | High calcium, fibre and protein, plus three vitamins every day |
| hard_05 | 18-minute daily queue limit on $11 a day |
