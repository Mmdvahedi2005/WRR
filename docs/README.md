# Exercise 5 Documentation — WRR with Synchronization

> Branch: `Exercise-5-WRR` · Overview: [README_Exercise5_WRR.md](../README_Exercise5_WRR.md)
> Reports: [report_en.md](./reports/report_en.md) (EN) · [report_fa.md](./reports/report_fa.md) (FA)

This is the comprehensive guide for Exercise 5. It explains the algorithm,
the implementation, the experiment, and how to read every figure.

## 1. Algorithm in detail

Weighted Round Robin (WRR) is a preemptive CPU scheduling policy:

1. Each task has a positive integer **weight** and a CPU **burst**
   (total work units).
2. The scheduler visits tasks in input order.
3. On each visit, a task runs for up to `weight` quanta.
   Each quantum runs `min(quantum, remaining_burst)` units, so the last
   quantum may be shorter.
4. When `remaining_burst` reaches zero, the task's **completion time**
   is the current clock value and it is skipped in later rounds.
5. The loop ends when all tasks finish; **makespan** is the final clock.

Idealized share for continuously runnable tasks:

```text
share(i) = weight(i) / sum(weights) * 100%
```

Example (weights 3, 2, 1): 50.0%, 33.3%, 16.7%. With finite bursts the
actual shares differ — see Figure 6 in the overview README.

## 2. Implementation components

| Component | File / class | Role |
|-----------|--------------|------|
| `Task` | `exercise5_wrr.py` | Dataclass: name, weight, burst, remaining, first_start, completion, waiting. Validates weight > 0, burst >= 0. |
| `DispatchGuard` | `exercise5_wrr.py` | Mutual-exclusion abstraction. Modes: `semaphore` (BoundedSemaphore), `monitor` (Condition), `both` (semaphore then monitor, fixed order). |
| `schedule()` | `exercise5_wrr.py` | Deterministic dispatcher. Validates quantum > 0 and unique names. Returns events, gantt segments, metrics, makespan. |
| `gantt_svg()` | `exercise5_wrr.py` | Renders an SVG Gantt chart from gantt segments. |
| `main()` | `exercise5_wrr.py` | CLI (`--mode`, `--quantum`, `--gantt`). Default workload P1(3,5), P2(2,4), P3(1,3). |
| Tests | `test_exercise5_wrr.py` | 9 unit tests (see §5). |

### Synchronization design

- **Semaphore mode:** `BoundedSemaphore(1)` serializes each dispatch update.
- **Monitor mode:** `Condition` with a `_busy` flag serializes the same update.
- **Both mode:** acquires semaphore first, then monitor — fixed order
  prevents lock-order inversion. Releases in reverse order.

Because the dispatcher is single-threaded, all modes produce identical
schedules. The point is to demonstrate *correct ownership* of the critical
section, not to measure parallel speedup.

## 3. Worked example (step by step)

Workload: P1(w=3,b=5), P2(w=2,b=4), P3(w=1,b=3), quantum=1.

| Time | Task | Remaining after | Note |
|------|------|-----------------|------|
| 0–1 | P1 | 4 | Round 1, P1 quantum 1/3 |
| 1–2 | P1 | 3 | P1 quantum 2/3 |
| 2–3 | P1 | 2 | P1 quantum 3/3 |
| 3–4 | P2 | 3 | P2 quantum 1/2 |
| 4–5 | P2 | 2 | P2 quantum 2/2 |
| 5–6 | P3 | 2 | P3 quantum 1/1 |
| 6–7 | P1 | 1 | Round 2, P1 quantum 1/3 |
| 7–8 | P1 | 0 | P1 completes at 8 |
| 8–9 | P2 | 1 | P2 quantum 1/2 |
| 9–10 | P2 | 0 | P2 completes at 10 |
| 10–11 | P3 | 1 | P3 quantum 1/1 |
| 11–12 | P3 | 0 | P3 completes at 12 |

Makespan = 12. Waiting = completion − burst (arrival = 0):
P1: 8−5=3, P2: 10−4=6, P3: 12−3=9.

## 4. How to re-run the experiment

```bash
# 1. Install (only needed for WRR.py / figure regeneration)
python -m pip install -r requirements.txt

# 2. Run all three sync modes
python exercise5_wrr.py --mode all --quantum 1

# 3. Archive Gantt SVGs
python exercise5_wrr.py --mode all --quantum 1 --gantt outputs/wrr-gantt

# 4. Run tests
python -m unittest -v

# 5. Regenerate PNG figures from real output
python tools_generate_figures.py
python tools_generate_exercise5_figures.py
```

Expected output matches `SAMPLE_RUN_Exercise5_WRR.txt` exactly.
Expected tests: 9/9 PASS (`TEST_RESULTS_Exercise5_WRR.txt`).

## 5. Test guide

| Test | What it checks |
|------|----------------|
| `test_weight_controls_quanta_per_round` | First 3 dispatches are A, A, B for weights 2, 1 |
| `test_all_sync_modes_same_schedule` | Gantt identical across semaphore/monitor/both |
| `test_completion_and_metrics` | Makespan 5; completions 5 and 4 |
| `test_partial_final_quantum` | Durations [2, 1] for burst 3, quantum 2 |
| `test_zero_burst` | Makespan 0, empty Gantt |
| `test_invalid_quantum` | ValueError for quantum 0 |
| `test_invalid_weight` | ValueError for weight 0 |
| `test_duplicate_names` | ValueError for duplicate names |
| `test_invalid_mode` | ValueError for unknown mode |

## 6. Figure reading guide

### `figures/wrr_gantt.png` (Figure 4)

- **What:** Gantt chart from real `schedule()` segments.
- **How to read:** Each block = 1 quantum. Rows = tasks. Read left to right.
  P1's three consecutive blocks show weight 3; P3's single block shows weight 1.
- **Interpretation:** Heavier tasks finish earlier (P1 at 8, P3 at 12).

### `figures/wrr_metrics.png` (Figure 5)

- **What:** Grouped bars for completion, turnaround, waiting per task.
- **How to read:** Blue = completion, orange = turnaround (equal here because
  arrival = 0), green = waiting. Values are labeled on top.
- **Interpretation:** Lower weight → later completion and longer waiting.

### `figures/wrr_cpu_share.png` (Figure 6)

- **What:** Idealized weight share (blue) vs actual burst share (orange).
- **How to read:** Compare each pair. P1: 50.0% ideal vs 41.7% actual.
- **Interpretation:** Finite bursts cause deviation from ideal proportions.

### `figures/architecture.svg` (Figure 1)

- **What:** Component diagram of `exercise5_wrr.py`.
- **How to read:** Follow arrows: CLI → Task → schedule() → DispatchGuard
  → gantt_svg() → outputs. Tests verify the pipeline.

### `figures/flowchart.svg` (Figure 2)

- **What:** Dispatch loop flowchart.
- **How to read:** Top to bottom; diamond = "any unfinished?"; loop back
  until all bursts consumed.

### `figures/wrr_sync_comparison.svg` (Figure 3)

- **What:** Side-by-side comparison of Semaphore / Monitor / Both guards.
- **How to read:** Each column shows acquire → dispatch → release for one mode.
  The dispatch step is identical; only the guard mechanism differs.

### `outputs/wrr-gantt-*.svg`

- **What:** Per-mode Gantt SVGs written by `gantt_svg()` during a run.
- **How to read:** Same as `wrr_gantt.png` but in SVG form, one file per mode.
  All three should look identical (deterministic simulation).

## 7. Advantages, limitations, assumptions

**Advantages**

- Simple, predictable proportional allocation.
- Deterministic and fully reproducible (same input → same output).
- Guard abstraction makes sync variants directly comparable.

**Limitations**

- No arrival times, I/O blocking, or context-switch overhead modeled.
- Single dispatcher: guards demonstrate ownership, not parallel speedup.
- Bursts are known integers; real systems must estimate them.

**Assumptions**

- All tasks arrive at time 0.
- Weights are positive integers; bursts are non-negative integers.
- Quantum is a positive integer (simulation) — `WRR.py` uses float seconds.

## 8. File list

| Path | Purpose |
|------|---------|
| `../README_Exercise5_WRR.md` | Exercise overview with figures |
| `../exercise5_wrr.py` | Simulation code |
| `../test_exercise5_wrr.py` | Unit tests |
| `../SAMPLE_RUN_Exercise5_WRR.txt` | Verified sample output |
| `../TEST_RESULTS_Exercise5_WRR.txt` | Verified test report |
| `../tools_generate_figures.py` | Gantt + share figure generator |
| `../tools_generate_exercise5_figures.py` | Metrics figure generator |
| `./figures/*` | All figures (PNG + SVG) |
| `./reports/report_en.md` | English academic report |
| `./reports/report_fa.md` | Persian academic report (گزارش فارسی) |
| `./references/README.md` | Bibliography |
| `../outputs/wrr-gantt-*.svg` | Generated per-mode Gantt charts |
| `../PROJECT_INDEX.md` | Index of all 7 exercises |
| `../PROJECT_PROGRESS.md` | Upgrade status |
