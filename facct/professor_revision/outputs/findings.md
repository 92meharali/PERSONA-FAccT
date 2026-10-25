# Professor-requested checks

Exploratory amendment; 2,000 paired prompt-cluster draws. Original source ratings and scores are unchanged.

## Counts at 20%

| Domain | Criterion | Cases / prompts | H | Full markers | 300-character markers | Full length | 300-character length | Random expectation |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| mental_health | D_ge3 | 165 / 99 | 42 | 63 | 68 | 54 | 58 | 33 |
| mental_health | D_gt3 | 57 / 42 | 13 | 26 | 22 | 21 | 22 | 11.4 |
| mental_health | D_ge4 | 5 / 4 | 0 | 3 | 2 | 1 | 1 | 1 |
| mental_health | F_lt4 | 95 / 77 | 18 | 22 | 19 | 19 | 23 | 19 |
| mental_health | OA_lt4 | 133 / 111 | 31 | 33 | 31 | 26 | 35 | 26.6 |
| mental_health | followup | 19 / 13 | 6 | 12 | 10 | 4 | 6 | 3.8 |
| education | D_ge3 | 12 / 7 | 7 | 9 | 10 | 3 | 6 | 2.4 |
| education | D_gt3 | 8 / 5 | 3 | 5 | 6 | 1 | 3 | 1.6 |
| education | D_ge4 | 8 / 5 | 3 | 5 | 6 | 1 | 3 | 1.6 |
| education | F_lt4 | 25 / 17 | 10 | 1 | 2 | 3 | 2 | 5 |
| education | OA_lt4 | 18 / 10 | 9 | 3 | 4 | 1 | 3 | 3.6 |
| health | D_ge3 | 23 / 15 | 10 | 21 | 19 | 5 | 14 | 4.6 |
| health | D_gt3 | 20 / 13 | 8 | 18 | 17 | 4 | 13 | 4 |
| health | D_ge4 | 8 / 6 | 2 | 7 | 7 | 0 | 6 | 1.6 |
| health | F_lt4 | 120 / 69 | 25 | 32 | 36 | 26 | 29 | 24 |
| health | OA_lt4 | 9 / 7 | 3 | 9 | 9 | 0 | 7 | 1.8 |

## Paired recall differences at 20%

| Domain | Criterion | Contrast | Difference, pp [95%] | Finite draws |
|---|---|---|---:|---:|
| mental_health | D_ge3 | HumT minus markers_full | -12.7 [-21.9, -4.1] | 2000/2000 |
| mental_health | D_ge3 | HumT minus markers_300 | -15.8 [-23.4, -7.7] | 2000/2000 |
| mental_health | D_ge3 | markers_300 minus markers_full | +3.0 [-3.2, +8.0] | 2000/2000 |
| mental_health | D_ge3 | HumT minus random_expected | +5.5 [-0.8, +11.8] | 2000/2000 |
| mental_health | D_gt3 | HumT minus markers_full | -22.8 [-38.9, -6.7] | 2000/2000 |
| mental_health | D_gt3 | HumT minus markers_300 | -15.8 [-31.4, +0.0] | 2000/2000 |
| mental_health | D_gt3 | markers_300 minus markers_full | -7.0 [-18.2, +3.2] | 2000/2000 |
| mental_health | D_gt3 | HumT minus random_expected | +2.8 [-7.0, +12.8] | 2000/2000 |
| mental_health | D_ge4 | HumT minus markers_full | -60.0 [-100.0, +0.0] | 1967/2000 |
| mental_health | D_ge4 | HumT minus markers_300 | -40.0 [-100.0, +0.0] | 1967/2000 |
| mental_health | D_ge4 | markers_300 minus markers_full | -20.0 [-100.0, +0.0] | 1967/2000 |
| mental_health | D_ge4 | HumT minus random_expected | -20.0 [-20.0, -20.0] | 1967/2000 |
| mental_health | F_lt4 | HumT minus markers_full | -4.2 [-15.1, +7.6] | 2000/2000 |
| mental_health | F_lt4 | HumT minus markers_300 | -1.1 [-11.0, +10.4] | 2000/2000 |
| mental_health | F_lt4 | markers_300 minus markers_full | -3.2 [-13.2, +5.8] | 2000/2000 |
| mental_health | F_lt4 | HumT minus random_expected | -1.1 [-7.6, +8.2] | 2000/2000 |
| mental_health | OA_lt4 | HumT minus markers_full | -1.5 [-9.1, +8.2] | 2000/2000 |
| mental_health | OA_lt4 | HumT minus markers_300 | +0.0 [-9.0, +8.1] | 2000/2000 |
| mental_health | OA_lt4 | markers_300 minus markers_full | -1.5 [-6.7, +6.2] | 2000/2000 |
| mental_health | OA_lt4 | HumT minus random_expected | +3.3 [-2.3, +10.5] | 2000/2000 |
| mental_health | followup | HumT minus markers_full | -31.6 [-66.7, +3.8] | 2000/2000 |
| mental_health | followup | HumT minus markers_300 | -21.1 [-55.6, +3.6] | 2000/2000 |
| mental_health | followup | markers_300 minus markers_full | -10.5 [-28.6, +15.4] | 2000/2000 |
| mental_health | followup | HumT minus random_expected | +11.6 [-7.5, +30.0] | 2000/2000 |
| education | D_ge3 | HumT minus markers_full | -16.7 [-50.0, +15.1] | 1995/2000 |
| education | D_ge3 | HumT minus markers_300 | -25.0 [-75.0, +20.0] | 1995/2000 |
| education | D_ge3 | markers_300 minus markers_full | +8.3 [-20.0, +41.7] | 1995/2000 |
| education | D_ge3 | HumT minus random_expected | +38.3 [-1.2, +70.1] | 1995/2000 |
| education | D_gt3 | HumT minus markers_full | -25.0 [-75.0, +26.2] | 1979/2000 |
| education | D_gt3 | HumT minus markers_300 | -37.5 [-100.0, +36.1] | 1979/2000 |
| education | D_gt3 | markers_300 minus markers_full | +12.5 [-37.5, +60.0] | 1979/2000 |
| education | D_gt3 | HumT minus random_expected | +17.5 [-20.0, +46.8] | 1979/2000 |
| education | D_ge4 | HumT minus markers_full | -25.0 [-75.0, +26.2] | 1979/2000 |
| education | D_ge4 | HumT minus markers_300 | -37.5 [-100.0, +36.1] | 1979/2000 |
| education | D_ge4 | markers_300 minus markers_full | +12.5 [-37.5, +60.0] | 1979/2000 |
| education | D_ge4 | HumT minus random_expected | +17.5 [-20.0, +46.8] | 1979/2000 |
| education | F_lt4 | HumT minus markers_full | +36.0 [+14.8, +57.9] | 2000/2000 |
| education | F_lt4 | HumT minus markers_300 | +32.0 [+4.0, +54.8] | 2000/2000 |
| education | F_lt4 | markers_300 minus markers_full | +4.0 [-3.7, +20.0] | 2000/2000 |
| education | F_lt4 | HumT minus random_expected | +20.0 [-2.4, +39.2] | 2000/2000 |
| education | OA_lt4 | HumT minus markers_full | +33.3 [-11.1, +70.8] | 2000/2000 |
| education | OA_lt4 | HumT minus markers_300 | +27.8 [-23.1, +66.7] | 2000/2000 |
| education | OA_lt4 | markers_300 minus markers_full | +5.6 [-7.4, +30.8] | 2000/2000 |
| education | OA_lt4 | HumT minus random_expected | +30.0 [+3.6, +52.8] | 2000/2000 |
| health | D_ge3 | HumT minus markers_full | -47.8 [-63.2, -26.7] | 2000/2000 |
| health | D_ge3 | HumT minus markers_300 | -39.1 [-62.5, -10.7] | 2000/2000 |
| health | D_ge3 | markers_300 minus markers_full | -8.7 [-25.0, +4.8] | 2000/2000 |
| health | D_ge3 | HumT minus random_expected | +23.5 [+5.1, +45.2] | 2000/2000 |
| health | D_gt3 | HumT minus markers_full | -50.0 [-66.7, -26.3] | 2000/2000 |
| health | D_gt3 | HumT minus markers_300 | -45.0 [-66.7, -13.6] | 2000/2000 |
| health | D_gt3 | markers_300 minus markers_full | -5.0 [-21.1, +5.9] | 2000/2000 |
| health | D_gt3 | HumT minus random_expected | +20.0 [-1.2, +43.3] | 2000/2000 |
| health | D_ge4 | HumT minus markers_full | -62.5 [-100.0, -27.2] | 1995/2000 |
| health | D_ge4 | HumT minus markers_300 | -62.5 [-100.0, -27.3] | 1995/2000 |
| health | D_ge4 | markers_300 minus markers_full | +0.0 [+0.0, +12.5] | 1995/2000 |
| health | D_ge4 | HumT minus random_expected | +5.0 [-20.0, +46.8] | 1995/2000 |
| health | F_lt4 | HumT minus markers_full | -5.8 [-13.3, +3.0] | 2000/2000 |
| health | F_lt4 | HumT minus markers_300 | -9.2 [-17.4, +0.0] | 2000/2000 |
| health | F_lt4 | markers_300 minus markers_full | +3.3 [-1.8, +9.3] | 2000/2000 |
| health | F_lt4 | HumT minus random_expected | +0.8 [-6.2, +7.4] | 2000/2000 |
| health | OA_lt4 | HumT minus markers_full | -66.7 [-100.0, -33.3] | 1999/2000 |
| health | OA_lt4 | HumT minus markers_300 | -66.7 [-100.0, -25.0] | 1999/2000 |
| health | OA_lt4 | markers_300 minus markers_full | +0.0 [-27.3, +0.0] | 1999/2000 |
| health | OA_lt4 | HumT minus random_expected | +13.3 [-19.9, +46.8] | 1999/2000 |

## Exclusive original-queue cases

 policy_only  n  clusters  D_eq3  D_gt3  D_ge4  F_lt4  OA_lt4  followup  natural  median_words  median_marker_fraction
        HumT 20        19     14      6      0      3       6         1       11         172.0                0.078894
markers_full 41        33     22     19      3      6       8         7       20         165.0                0.109756

Case profiles reuse original ratings and resolved follow-up labels. They are not newly adjudicated meanings or independent semantic codes.

The 300-character policies slice annotated text using the source scorer's documented Python operation. Historical scorer invocation is unauthenticated, especially where transfer export text differs. These checks test the available length restriction without proving full input equivalence.
