# Exercise 5 — WRR Synchronization: DispatchGuard (Semaphore / Monitor / Both)

**Deterministic WRR Scheduling with Semaphore, Monitor, and Combined Guards — Equivalence Verified**

- **Course:** Operating Systems
- **Exercise:** 5 — WRR Synchronization
- **Branch:** Exercise-5-WRR
- **Source:** exercise5_wrr.py (preserved from main branch PR #1)
- **Modes:** semaphore, monitor, both
- **Workload:** P1(w=3,b=5), P2(w=2,b=4), P3(w=1,b=3), quantum=1
- **Result:** makespan=12; completions P1=8, P2=10, P3=12; identical across all modes
- **Tests:** 9 unit tests — all passing
- **Figures:** 2 SVG structural + 2 PNG data-driven

---

## Table of Contents

1. 1. Introduction
2. 2. Figures & Results
3. 3. Conclusion

---

## 1. 1. Introduction

WRR scheduling with three synchronization variants: Semaphore, Monitor, and Both. All modes produce identical results — equivalence verified by construction and by test.

## 2. 2. Figures & Results

![Figure 1: Figure 1 — DispatchGuard architecture](docs/figures/dispatch_guard_architecture.svg)

*Figure 1 — Figure 1 — DispatchGuard architecture*

![Figure 2: Figure 2 — Synchronization variant handover flow](docs/figures/sync_variant_handover.svg)

*Figure 2 — Figure 2 — Synchronization variant handover flow*

![Figure 3: Figure 3 — Gantt chart: identical across all modes](docs/figures/wrr_gantt_equivalence.png)

*Figure 3 — Figure 3 — Gantt chart: identical across all modes*

![Figure 4: Figure 4 — Throughput/equivalence chart across modes](docs/figures/sync_equivalence_chart.png)

*Figure 4 — Figure 4 — Throughput/equivalence chart across modes*

**Table 1 — Table 1 — Equivalence across all synchronization modes**

| Mode | Makespan | P1 Wait | P2 Wait | P3 Wait |
| --- | --- | --- | --- | --- |
| semaphore | 12 | 3 | 6 | 9 |
| monitor | 12 | 3 | 6 | 9 |
| both | 12 | 3 | 6 | 9 |

## 3. 3. Conclusion

Semaphore, Monitor, and Both modes produce identical WRR scheduling results.
