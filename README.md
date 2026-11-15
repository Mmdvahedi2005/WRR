# Exercise 4 — Synchronization Primitives Comparison

## Problem / Goal
Complete comparison of Dekker, Peterson, Semaphore, and Monitor with formal model checking.

## Scientific Explanation
Mutual exclusion primitives compared via exhaustive explicit-state BFS and threaded contention benchmarks.

## Algorithm / Methodology
7 protocols model-checked (BFS). Properties: mutex, deadlock-free, progress, bounded waiting. Threaded benchmark 2,400/7,200 entries.

## Implementation
Python `sync_verifier.py` model checker + threaded benchmark.

## Custom Figures
- docs/figures/peterson_vs_monitor_state.svg — state machines
- docs/figures/sync_evolution_architecture.svg — architecture evolution
- docs/figures/model_checker_verdicts.png — pass/fail matrix
- docs/figures/contention_benchmarks.png — threaded results

## Usage Guide
Run `python3 src/sync_verifier.py`.

## Sample I/O
dekker: 86 states, all properties pass. peterson: 20 states, all pass. semaphore_fifo: 5 states, all pass. monitor_mesa: 24 states, all pass.

## Test Commands
```
python3 -m unittest tests/test_sync_verifier.py -v
```

## Directory Tree
src/sync_verifier.py
tests/test_sync_verifier.py
docs/figures/*.svg, *.png
report_EX4_en.{md,docx,pdf}
report_EX4_fa.{md,docx,pdf}

## Conclusion
Dekker & Peterson pass all properties for 2 processes. Semaphore & Monitor also pass all properties.

---

**Reports:** `report_EX4_en.{md,docx,pdf}` and `report_EX4_fa.{md,docx,pdf}`
**Branch:** `Exercise-4-WRR` | **Preserves:** `WRR.py` and `exercise5_wrr.py` where applicable
