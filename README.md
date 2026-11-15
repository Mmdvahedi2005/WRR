# Exercise 1 — WRR Algorithm Introduction

## Problem / Goal
Complete introduction to Weighted Round Robin scheduling with flowchart, pseudocode, figures, and bilingual explanations.

## Scientific Explanation
WRR extends Round Robin by assigning weights; each process receives up to its weight in quanta per round. Interleaved WRR reduces low-weight response time.

## Algorithm / Methodology
Discrete-time simulator, 4 scenarios (S1–S4), metrics: makespan, wait, response, Jain fairness.

## Implementation
Python `wrr_scheduler.py` with Classical and Interleaved WRR modes.

## Custom Figures
- docs/figures/wrr_flowchart.svg — scheduling logic
- docs/figures/wrr_architecture_overview.svg — system architecture
- docs/figures/wrr_gantt_variants.png — Gantt traces S1 & S3
- docs/figures/wrr_performance_tradeoff.png — throughput vs latency
- docs/figures/wrr_architecture_overview.png — component diagram

## Usage Guide
Run `python3 src/wrr_scheduler.py` to see scenario output.

## Sample I/O
S1 Baseline Classic: makespan=12, avg_wait=6.0, avg_resp=2.67, Jain=0.990
S1 Baseline Interleaved: makespan=12, avg_wait=7.0, avg_resp=1.00, Jain=0.968

## Test Commands
```
python3 -m unittest tests/test_wrr_scheduler.py -v
```

## Directory Tree
src/wrr_scheduler.py
tests/test_wrr_scheduler.py
docs/figures/*.svg, *.png
report_EX1_en.{md,docx,pdf}
report_EX1_fa.{md,docx,pdf}

## Conclusion
WRR provides weighted CPU allocation. Interleaved mode cuts response time for low-weight processes.

---

**Reports:** `report_EX1_en.{md,docx,pdf}` and `report_EX1_fa.{md,docx,pdf}`
**Branch:** `Exercise-1-WRR` | **Preserves:** `WRR.py` and `exercise5_wrr.py` where applicable
