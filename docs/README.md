# Exercise 5 — WRR Synchronization

## 1. Overview
WRR scheduling with synchronization guards. DispatchGuard provides a unified interface wrapping semaphore, monitor, or both. All three modes produce identical WRR scheduling results — equivalence verified by construction and by 9 unit tests.

## 2. Problem Statement
Demonstrate that WRR scheduling is correct and equivalent across different synchronization mechanisms (semaphore, monitor, combined), with deterministic simulation output.

## 3. Scientific Background
The DispatchGuard pattern wraps synchronization primitives so that the WRR dispatch loop is serialized regardless of the underlying mechanism. This proves synchronization choice does not affect scheduling semantics.

## 4. Methodology
Deterministic WRR simulator (`exercise5_wrr.py`) with `DispatchGuard` class supporting `semaphore`, `monitor`, and `both` modes. Each mode produces the same Gantt trace and metrics.

## 5. Implementation Details
Python `schedule()` function with `DispatchGuard` context manager. Uses `threading.BoundedSemaphore` and `threading.Condition`. Gantt SVG export via `gantt_svg()`.

## 6. Experimental Setup
Preserved from main branch (PR #1). Run `python3 exercise5_wrr.py --mode all`. Run `python3 -m unittest test_exercise5_wrr.py`.

## 7. Results & Analysis
All modes: makespan=12, completions P1=8, P2=10, P3=12, waits 3/6/9. Identical Gantt segments across semaphore, monitor, and both.

## 8. Figures & Visualizations
2 SVG (`dispatch_guard_architecture.svg`, `sync_variant_handover.svg`) + 2 PNG (`wrr_gantt_equivalence.png`, `sync_equivalence_chart.png`). Plus preserved `wrr_gantt.png` and `wrr_cpu_share.png`.

## 9. Testing
9 unit tests — all passing. Cover weight-controlled quanta, mode equivalence, completion metrics, partial quantum, zero burst, invalid inputs, duplicate names, and invalid mode.

## 10. Conclusion & References
Semaphore, Monitor, and Combined synchronization produce identical WRR scheduling results. Equivalence is guaranteed by the deterministic serial dispatch guard. See `report_EX5_en.md` / `report_EX5_fa.md`.

---

**Source:** `src/` directory | **Tests:** `tests/` directory | **Figures:** `docs/figures/`
**Reports:** `report_EX5_en.md`, `.docx`, `.pdf` and `report_EX5_fa.md`, `.docx`, `.pdf`
