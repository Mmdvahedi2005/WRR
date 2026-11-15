# Exercise 3 — Manual EDF & RM Scheduling

## 1. Overview
Manual scheduling of EDF and RM with 3 processes on paper. Case A (H=12, U=11/12 > Liu-Layland bound) and Case B (H=24, U=23/24). Includes hand-worked 24-tick timeline grids, RTA traces, and deadline audit tables.

## 2. Problem Statement
Demonstrate manual EDF and RM scheduling with 3 processes, showing where RM fails and EDF succeeds, with complete hand-worked documentation suitable for course submission.

## 3. Scientific Background
RM uses static priorities by period (shorter period = higher priority). EDF uses dynamic priorities by absolute deadline (earliest = higher priority). The Liu-Layland bound for n=3 is approximately 0.7798; utilization above this requires exact Response-Time Analysis.

## 4. Methodology
Fixed-priority RTA with fixed-point iteration. Manual timeline construction tick-by-tick over the hyperperiod. Deadline audit table for all jobs over [0, H).

## 5. Implementation Details
Python solver (`manual_edf_rm.py`) computing RTA traces and simulating both RM and EDF schedules. Verified against hand-worked results.

## 6. Experimental Setup
Run `python3 src/manual_edf_rm.py` for Case A and Case B analysis. Run `python3 -m unittest tests/test_manual_edf_rm.py` for tests.

## 7. Results & Analysis
Case A: Both RM and EDF feasible (0 misses, U=0.9167 > LL=0.7798). Case B: RM misses P3,1 at t=12 (RTA diverges [4,8,9,13] > 12); EDF meets all 11/11 deadlines because at t=9, d(P3,1)=12 < d(P2,2)=16.

## 8. Figures & Visualizations
2 SVG (`manual_method_flowchart.svg`, `hyperperiod_lattice.svg`) + 3 PNG (`case_a_h12_rm_edf_gantt.png`, `case_b_h24_rm_edf_gantt.png`, `handworked_paper_worksheet.png`).

## 9. Testing
3 unit tests — all passing. Cover RTA convergence, deadline miss detection, and EDF vs RM divergence.

## 10. Conclusion & References
RM can miss deadlines even when utilization < 1 due to static priority inversion. EDF meets all deadlines in Case B. Hand-worked worksheet provided for paper submission. See `report_EX3_en.md` / `report_EX3_fa.md`.

---

**Source:** `src/` directory | **Tests:** `tests/` directory | **Figures:** `docs/figures/`
**Reports:** `report_EX3_en.md`, `.docx`, `.pdf` and `report_EX3_fa.md`, `.docx`, `.pdf`
