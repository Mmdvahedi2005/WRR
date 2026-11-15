# WRR Scheduler — Academic Report (EN)

## 1. Introduction

Weighted Round Robin (WRR) is a CPU scheduling policy that gives each
runnable process a number of consecutive time quanta proportional to its
assigned weight. Unlike plain Round Robin, WRR allows different processes
to receive different shares of CPU service while preserving a simple,
predictable dispatch order.

This repository contains two implementations:

1. **`WRR.py`** — an interactive user-space scheduler that launches external
   programs and suspends/resumes them with `psutil` to approximate weighted
   time slicing on a real operating system.
2. **`exercise5_wrr.py`** — a deterministic simulation used for Exercise 5.
   It models CPU bursts as integer work units and compares three
   synchronization designs (Semaphore, Monitor, Both) on identical workloads.

## 2. Algorithm

For each unfinished task, the scheduler grants up to `weight` quanta per
round, in input order. The final quantum of a task is shortened to its
remaining burst. Finished tasks are skipped.

For continuously runnable tasks, the idealized service share is:

```text
share(i) = weight(i) / sum(weights) * 100%
```

For weights 3, 2, 1 this gives 50.0%, 33.3%, and 16.7%. These are
expectations, not guarantees: finite bursts, completion order, and (for
`WRR.py`) OS scheduling and timing overhead change measured results.

## 3. Implementation

### 3.1 `WRR.py` (OS processes)

- Reads process count, quantum, executable paths, and weights.
- Launches each program with `subprocess.Popen`, then suspends it.
- Cycles through the list, resuming each unfinished process for up to
  `weight` slices bounded by `quantum` (`wait(timeout=quantum)`).
- Records CPU time via `psutil.Process.cpu_times()` and prints a final table
  (weight, CPU time, runtime, return code).
- Cleanup in `finally` resumes and terminates any still-running processes.

### 3.2 `exercise5_wrr.py` (simulation)

- `Task` dataclass: name, weight, burst, remaining, completion, waiting.
- `DispatchGuard`: mutual-exclusion abstraction with three modes
  (`semaphore`, `monitor`, `both`). The `both` mode always acquires in fixed
  order (semaphore, then monitor) to avoid lock-order inversion.
- `schedule()`: deterministic single-dispatcher loop; returns events,
  Gantt segments, per-task metrics, and makespan.
- `gantt_svg()`: writes an SVG Gantt chart per mode.

## 4. Experiment (Exercise 5, verified)

Workload: `P1(weight=3, burst=5)`, `P2(weight=2, burst=4)`,
`P3(weight=1, burst=3)`, `quantum=1`.

Command:

```bash
python exercise5_wrr.py --mode all --quantum 1
python -m unittest -v
```

Results (identical for Semaphore, Monitor, and Both — verified by tests):

| Task | Weight | Burst | Completion | Turnaround | Waiting |
|------|--------|-------|------------|------------|---------|
| P1 | 3 | 5 | 8 | 8 | 3 |
| P2 | 2 | 4 | 10 | 10 | 6 |
| P3 | 1 | 3 | 12 | 12 | 9 |

Makespan: **12**. Tests: **9/9 PASS** (dispatch order, mode equivalence,
metrics, partial final quantum, zero burst, invalid inputs).

Figures `docs/figures/wrr_gantt.png` and `docs/figures/wrr_cpu_share.png`
are generated from this exact output by `tools_generate_figures.py`.

## 5. Analysis

- **Dispatch order** follows weights: P1 (3 quanta), P2 (2), P3 (1) in
  round 1; P1 completes first (time 8), then P2 (10), then P3 (12).
- **Synchronization variants produce identical schedules.** This is by
  design: the dispatcher is single-threaded and deterministic, so the
  guards demonstrate correct critical-section ownership, not parallel
  speedup. No performance ranking between Semaphore and Monitor is claimed.
- **Weight share vs burst share:** idealized shares (50.0/33.3/16.7%)
  differ from actual burst shares (41.7/33.3/25.0%) because bursts are
  finite and tasks finish at different times.

## 6. Limitations and assumptions

- The simulation assumes all tasks arrive at time 0, bursts are known
  integers, and there is no I/O blocking or context-switch overhead.
- `WRR.py` is an educational user-space scheduler, not a kernel scheduler
  and not a hard real-time scheduler. `wait(timeout=quantum)` is a slice
  limit, not a real-time guarantee.
- EDF and RM are discussed only at algorithm level in `README.md`; they are
  not implemented or benchmarked in this repository.

## 7. Conclusion

WRR provides a simple way to allocate CPU service proportionally to weights.
The deterministic simulation in this repository makes the policy fully
reproducible: same workload, same schedule, same metrics, every run.
The OS-process variant shows how the same idea maps to real process
control with `psutil`, with the caveat that real measurements include OS
and timing noise.

## References

See `docs/references/README.md`.
