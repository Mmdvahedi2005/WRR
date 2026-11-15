# Exercise 2 — WRR vs EDF vs RM Comparison

## 1. Overview
Comprehensive comparison of WRR with Earliest Deadline First (EDF) and Rate Monotonic (RM) across starvation, deadlines, overhead, fairness, and schedulability. Includes real simulation data from a discrete-time job simulator with RTA and Monte Carlo experiments.

## 2. Problem Statement
Compare three CPU scheduling algorithms (WRR, EDF, RM) in all aspects, with scientifically accurate results backed by code execution.

## 3. Scientific Background
EDF is a dynamic-priority optimal scheduler. RM is a static-priority optimal scheduler for periodic tasks with utilization bound U_LL(n) = n(2^(1/n) − 1). WRR is a weight-based fair-share scheduler without deadline awareness.

## 4. Methodology
Discrete-time periodic job simulator (`compare_schedulers.py`) with Response-Time Analysis, Liu-Layland bound, and 400-set Monte Carlo experiments (seed=20261115). Four workload scenarios: W1 underload, W2 high-util gap, W3 overload domino, plus utilization-band feasibility.

## 5. Implementation Details
Job-level simulator with periodic task release, deadline tracking, context-switch counting, and schedulability reporting. RTA for RM, EDF simulation, WRR weighted-slice simulation.

## 6. Experimental Setup
Run `python3 src/compare_schedulers.py` for all benchmarks. Run `python3 -m unittest tests/test_compare_schedulers.py` for tests.

## 7. Results & Analysis
W1: All 0/7 misses. W2: EDF=0/15, RM=1/15, WRR=1/15 misses. W3: WRR proportional shares (50/33/17), RM starves T3 completely, EDF domino cascade (9/13 misses). Monte Carlo: EDF 100% up to U≈0.96, RM degrades after 0.78, WRR degrades after 0.65.

## 8. Figures & Visualizations
2 SVG (`taxonomy_wrr_rm_edf.svg`, `overload_starvation_mechanism.svg`) + 3 PNG (`schedulability_monte_carlo.png`, `w2_high_util_gantt_comparison.png`, `w3_overload_starvation_domino.png`).

## 9. Testing
6 unit tests — all passing. Cover feasibility, miss counts, context switches, and Monte Carlo determinism.

## 10. Conclusion & References
EDF achieves the best schedulability, RM performs well at low utilization, and WRR provides weighted fairness with predictable proportional shares but lower deadline guarantees at high utilization. See `report_EX2_en.md` / `report_EX2_fa.md`.

---

**Source:** `src/` directory | **Tests:** `tests/` directory | **Figures:** `docs/figures/`
**Reports:** `report_EX2_en.md`, `.docx`, `.pdf` and `report_EX2_fa.md`, `.docx`, `.pdf`
