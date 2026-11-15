# Exercise 2 — WRR vs EDF vs RM Comparison

## Problem / Goal
Comprehensive comparison of WRR, EDF, and RM schedulers across all aspects.

## Scientific Explanation
EDF (dynamic, optimal), RM (static, Liu-Layland bound), WRR (weighted fair-share). Compared via discrete-time simulation and Monte Carlo.

## Algorithm / Methodology
4 workload scenarios + 400-set Monte Carlo (seed=20261115). RTA, Liu-Layland, context-switch counting.

## Implementation
Python `compare_schedulers.py` job-level periodic simulator.

## Custom Figures
- docs/figures/taxonomy_wrr_rm_edf.svg — algorithm taxonomy
- docs/figures/overload_starvation_mechanism.svg — starvation mechanism
- docs/figures/schedulability_monte_carlo.png — feasibility ratios
- docs/figures/w2_high_util_gantt_comparison.png — W2 Gantt
- docs/figures/w3_overload_starvation_domino.png — domino cascade

## Usage Guide
Run `python3 src/compare_schedulers.py`.

## Sample I/O
W2: EDF=0/15 misses, RM=1/15, WRR=1/15 misses. W3: WRR shares 50/33/17%, RM starves T3, EDF domino 9/13 misses.

## Test Commands
```
python3 -m unittest tests/test_compare_schedulers.py -v
```

## Directory Tree
src/compare_schedulers.py
tests/test_compare_schedulers.py
docs/figures/*.svg, *.png
report_EX2_en.{md,docx,pdf}
report_EX2_fa.{md,docx,pdf}

## Conclusion
EDF best schedulability, RM good at low U, WRR weighted fairness with lower deadline guarantees at high U.

---

**Reports:** `report_EX2_en.{md,docx,pdf}` and `report_EX2_fa.{md,docx,pdf}`
**Branch:** `Exercise-2-WRR` | **Preserves:** `WRR.py` and `exercise5_wrr.py` where applicable
