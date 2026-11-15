# Exercise 1 — WRR Algorithm Introduction

## 1. Overview
Complete introduction to the Weighted Round Robin (WRR) scheduling algorithm, including flowchart, pseudocode, figures, and full explanations in English and Persian. Covers both Classical WRR (block quanta per round) and Interleaved WRR (sub-rounds for lower response time).

## 2. Problem Statement
Provide a comprehensive, executable introduction to WRR scheduling for the Operating Systems course, with real simulation data, visual figures, and bilingual documentation.

## 3. Scientific Background
Round Robin is a time-sharing CPU scheduling algorithm. WRR extends it by assigning each process a weight; in each round, a process receives up to its weight number of quanta. Interleaved WRR divides each round into sub-rounds so low-weight processes are served earlier.

## 4. Methodology
Discrete-time deterministic simulator in Python (`wrr_scheduler.py`). Four scenarios: S1 baseline, S2 backlogged proportional, S3 high-skew weights, S4 dynamic arrivals. Metrics: makespan, average wait, average response, Jain's fairness index.

## 5. Implementation Details
Python class `WRRScheduler` with `classic` and `interleaved` modes. Quantum sweep analysis. 10 unit tests covering correctness, fairness, and edge cases.

## 6. Experimental Setup
Run `python3 src/wrr_scheduler.py` for scenario output. Run `python3 -m unittest tests/test_wrr_scheduler.py` for tests. No external dependencies beyond Python stdlib.

## 7. Results & Analysis
S1: Classic avg_resp=2.67 vs Interleaved avg_resp=1.00. S3: Classic avg_resp=7.25 vs Interleaved avg_resp=1.50. Both preserve identical throughput and weighted shares.

## 8. Figures & Visualizations
2 SVG structural diagrams (`wrr_flowchart.svg`, `wrr_architecture_overview.svg`) + 3 PNG data-driven charts (`wrr_gantt_variants.png`, `wrr_performance_tradeoff.png`, `wrr_architecture_overview.png`).

## 9. Testing
10 unit tests — all passing. Tests cover weight-controlled quanta, completion metrics, partial quantum, zero burst, invalid inputs, duplicate names, and mode equivalence.

## 10. Conclusion & References
WRR provides weighted CPU allocation proportional to assigned weights. The interleaved variant reduces response time for low-weight processes without affecting overall throughput. See `report_EX1_en.md` / `report_EX1_fa.md` for full bilingual reports.

---

**Source:** `src/` directory | **Tests:** `tests/` directory | **Figures:** `docs/figures/`
**Reports:** `report_EX1_en.md`, `.docx`, `.pdf` and `report_EX1_fa.md`, `.docx`, `.pdf`
