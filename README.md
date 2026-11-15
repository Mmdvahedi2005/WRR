# Exercise 3 — Manual EDF & RM Scheduling

## Problem / Goal
Manual EDF and RM scheduling with 3 processes on paper, showing RM failure and EDF success.

## Scientific Explanation
RM static priority by period, EDF dynamic by deadline. Liu-Layland bound for n=3 ≈ 0.7798; above this need exact RTA.

## Algorithm / Methodology
Fixed-point RTA, manual tick-by-tick timeline over hyperperiod, deadline audit table.

## Implementation
Python `manual_edf_rm.py` solver for Case A (H=12) and Case B (H=24).

## Custom Figures
- docs/figures/manual_method_flowchart.svg — manual method
- docs/figures/hyperperiod_lattice.svg — hyperperiod lattice
- docs/figures/case_a_h12_rm_edf_gantt.png — Case A Gantt
- docs/figures/case_b_h24_rm_edf_gantt.png — Case B Gantt
- docs/figures/handworked_paper_worksheet.png — 24-tick worksheet

## Usage Guide
Run `python3 src/manual_edf_rm.py`.

## Sample I/O
Case B: RM misses P3,1 at t=12 (RTA diverges [4,8,9,13] > 12). EDF meets all 11/11 deadlines.

## Test Commands
```
python3 -m unittest tests/test_manual_edf_rm.py -v
```

## Directory Tree
src/manual_edf_rm.py
tests/test_manual_edf_rm.py
docs/figures/*.svg, *.png
report_EX3_en.{md,docx,pdf}
report_EX3_fa.{md,docx,pdf}

## Conclusion
RM can miss deadlines below U=1; EDF meets all deadlines. Hand-worked worksheet included for submission.

---

**Reports:** `report_EX3_en.{md,docx,pdf}` and `report_EX3_fa.{md,docx,pdf}`
**Branch:** `Exercise-3-WRR` | **Preserves:** `WRR.py` and `exercise5_wrr.py` where applicable
