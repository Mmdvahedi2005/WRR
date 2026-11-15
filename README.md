# Exercise 5 — WRR Synchronization

## Problem / Goal
WRR scheduling with semaphore, monitor, and combined guards; verify equivalence.

## Scientific Explanation
DispatchGuard wraps semaphore/monitor so WRR dispatch is serialized identically regardless of mechanism.

## Algorithm / Methodology
Deterministic WRR simulator with DispatchGuard. All 3 modes produce identical Gantt traces.

## Implementation
Python `exercise5_wrr.py` (preserved from main branch PR #1) with DispatchGuard class.

## Custom Figures
- docs/figures/dispatch_guard_architecture.svg — guard architecture
- docs/figures/sync_variant_handover.svg — handover flow
- docs/figures/wrr_gantt_equivalence.png — identical Gantt across modes
- docs/figures/sync_equivalence_chart.png — equivalence bar chart
- docs/figures/wrr_gantt.png — base Gantt (preserved)
- docs/figures/wrr_cpu_share.png — weight vs burst share (preserved)

## Usage Guide
Run `python3 exercise5_wrr.py --mode all`.

## Sample I/O
All modes: makespan=12, P1 completion=8, P2=10, P3=12, waits 3/6/9. Identical across semaphore, monitor, both.

## Test Commands
```
python3 -m unittest test_exercise5_wrr.py -v
```

## Directory Tree
exercise5_wrr.py
test_exercise5_wrr.py
README_Exercise5_WRR.md
docs/figures/*.svg, *.png
report_EX5_en.{md,docx,pdf}
report_EX5_fa.{md,docx,pdf}

## Conclusion
Semaphore, Monitor, and Combined modes produce identical WRR results. Equivalence verified.

---

**Reports:** `report_EX5_en.{md,docx,pdf}` and `report_EX5_fa.{md,docx,pdf}`
**Branch:** `Exercise-5-WRR` | **Preserves:** `WRR.py` and `exercise5_wrr.py` where applicable
