# Exercise 4 — Dekker, Peterson, Semaphore, Monitor: Formal Comparison

**Exhaustive Model Checking (7 protocols) + Threaded Contention Benchmarks**

- **Course:** Operating Systems
- **Exercise:** 4 — Synchronization Primitive Comparison
- **Branch:** Exercise-4-WRR
- **Method:** Exhaustive explicit-state BFS model checker
- **Protocols:** naive_flag, strict_alternation, flag_deadlock, dekker, peterson, semaphore_fifo, monitor_mesa
- **Finding:** Dekker & Peterson pass all properties (bound=1); Semaphore & Monitor pass all
- **Figures:** 2 SVG + 2 PNG
- **Tests:** 3 unit tests — all passing

---

## Table of Contents

1. 1. Introduction
2. 2. Protocols
3. 3. Figures & Results
4. 4. Conclusion

---

## 1. 1. Introduction

Comprehensive comparison of Dekker, Peterson, Semaphore, and Monitor synchronization primitives using exhaustive explicit-state BFS model checking (7 protocols) and threaded contention benchmarks.

## 2. 2. Protocols

- naive_flag, strict_alternation, flag_deadlock, dekker, peterson, semaphore_fifo, monitor_mesa
- Dekker & Peterson pass all properties (bound=1)
- Semaphore & Monitor pass all properties

## 3. 3. Figures & Results

![Figure 1: Figure 1 — Peterson vs Monitor state machine](docs/figures/peterson_vs_monitor_state.svg)

*Figure 1 — Figure 1 — Peterson vs Monitor state machine*

![Figure 2: Figure 2 — Synchronization architecture evolution](docs/figures/sync_evolution_architecture.svg)

*Figure 2 — Figure 2 — Synchronization architecture evolution*

![Figure 3: Figure 3 — Model checker verdicts](docs/figures/model_checker_verdicts.png)

*Figure 3 — Figure 3 — Model checker verdicts*

![Figure 4: Figure 4 — Contention benchmarks](docs/figures/contention_benchmarks.png)

*Figure 4 — Figure 4 — Contention benchmarks*

**Table 1 — Table 1 — Model checker results**

| Protocol | States | Mutex | Deadlock | Progress |
| --- | --- | --- | --- | --- |
| dekker | 86 | ✓ | ✓ | ✓ |
| peterson | 20 | ✓ | ✓ | ✓ |
| semaphore_fifo | 5 | ✓ | ✓ | ✓ |
| monitor_mesa | 24 | ✓ | ✓ | ✓ |

## 4. 4. Conclusion

Dekker and Peterson pass all formal properties. Semaphore and Monitor also pass all properties.
