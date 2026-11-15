# Exercise 4 — Dekker, Peterson, Semaphore, Monitor Comparison

## 1. Overview
Complete comparison of Dekker, Peterson, Semaphore, and Monitor synchronization primitives. Uses exhaustive explicit-state BFS model checking across 7 protocols plus threaded contention benchmarks.

## 2. Problem Statement
Formally compare four mutual exclusion mechanisms with real model-checking data and threaded experiments, showing which properties each protocol satisfies or violates.

## 3. Scientific Background
Mutual exclusion ensures only one process enters a critical section at a time. Dekker and Peterson are software-only algorithms for 2 processes. Semaphores and Monitors are OS-provided synchronization primitives.

## 4. Methodology
Exhaustive explicit-state BFS model checker (`sync_verifier.py`) enumerating all reachable states for 7 protocol variants. Properties checked: mutual exclusion, deadlock freedom, progress (no contention), bounded waiting (FIFO/1). Threaded benchmark with 2,400 and 7,200 critical-section entries.

## 5. Implementation Details
State-based model checker with BFS exploration. Each protocol modeled as a finite-state machine. Threaded benchmark using Python threading with BoundedSemaphore and Condition.

## 6. Experimental Setup
Run `python3 src/sync_verifier.py` for model checking and benchmarks. Run `python3 -m unittest tests/test_sync_verifier.py` for tests.

## 7. Results & Analysis
Model checker: dekker (86 states, all pass), peterson (20 states, all pass), semaphore_fifo (5 states, all pass), monitor_mesa (24 states, all pass, Mesa barging noted). Naive flag, strict alternation, and flag deadlock fail various properties. Threaded: 0 safety violations across all runs.

## 8. Figures & Visualizations
2 SVG (`peterson_vs_monitor_state.svg`, `sync_evolution_architecture.svg`) + 2 PNG (`model_checker_verdicts.png`, `contention_benchmarks.png`).

## 9. Testing
3 unit tests — all passing. Cover model checker state counts, property verdicts, and benchmark safety.

## 10. Conclusion & References
Dekker and Peterson provide correct mutual exclusion for 2 processes with bounded waiting. Semaphore and Monitor are more general and also correct. All verified by exhaustive model checking and threaded experiments. See `report_EX4_en.md` / `report_EX4_fa.md`.

---

**Source:** `src/` directory | **Tests:** `tests/` directory | **Figures:** `docs/figures/`
**Reports:** `report_EX4_en.md`, `.docx`, `.pdf` and `report_EX4_fa.md`, `.docx`, `.pdf`
