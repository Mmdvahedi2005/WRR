"""
Exercise 1 — Weighted Round Robin (WRR) CPU & Packet Scheduling Engine.
Implements both:
  1. Classical Round-Slice WRR (matching the base WRR.py / exercise5_wrr.py policy:
     each ready task receives up to `weight` consecutive quanta per round).
  2. Interleaved WRR (IWRR): spreads quanta across sub-rounds r = 1..max(w_i)
     so a heavy-weight task does not monopolize consecutive slices, reducing
     worst-case response latency for light-weight tasks while preserving exact
     proportional CPU shares.
Supports dynamic arrival times (arrival >= 0), context-switch cost accounting,
Jain's fairness index, starvation bound calculation, and scenario evaluation.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable, Literal
import json
import argparse
from pathlib import Path


@dataclass(frozen=True)
class WRRTaskSpec:
    name: str
    weight: int
    burst: int
    arrival: int = 0

    def __post_init__(self):
        if not self.name or not self.name.strip():
            raise ValueError("Task name must be non-empty")
        if self.weight <= 0:
            raise ValueError(f"Task {self.name}: weight must be positive (got {self.weight})")
        if self.burst < 0:
            raise ValueError(f"Task {self.name}: burst must be non-negative (got {self.burst})")
        if self.arrival < 0:
            raise ValueError(f"Task {self.name}: arrival must be non-negative (got {self.arrival})")


def jains_fairness_index(values: list[float]) -> float:
    """Compute Jain's Fairness Index J = (sum x_i)^2 / (n * sum x_i^2) in (0, 1]."""
    positive = [v for v in values if v > 0]
    if not positive:
        return 1.0
    n = len(positive)
    s1 = sum(positive)
    s2 = sum(v * v for v in positive)
    return (s1 * s1) / (n * s2) if s2 > 0 else 1.0


def theoretical_max_wait_bound(weights: list[int], target_index: int, quantum: int,
                               context_switch: int = 0) -> int:
    """
    Exact upper bound on waiting time between two consecutive services of task i
    when all N tasks are continuously backlogged under Classical WRR:
      W_max(i) = (sum_{j != i} w_j) * quantum + (N - 1) * context_switch_overhead
    """
    if quantum <= 0:
        raise ValueError("quantum must be positive")
    other_quanta = sum(w for idx, w in enumerate(weights) if idx != target_index)
    other_tasks = sum(1 for idx in range(len(weights)) if idx != target_index)
    return other_quanta * quantum + other_tasks * max(0, context_switch)


def simulate_wrr(
    specs: Iterable[WRRTaskSpec],
    quantum: int = 1,
    variant: Literal["classic", "interleaved"] = "classic",
    context_switch: int = 0,
) -> dict:
    """
    Deterministic discrete-time simulator for Classical WRR and Interleaved WRR.
    """
    if quantum <= 0:
        raise ValueError("quantum must be positive")
    if context_switch < 0:
        raise ValueError("context_switch must be non-negative")
    if variant not in {"classic", "interleaved"}:
        raise ValueError("variant must be 'classic' or 'interleaved'")

    task_list = list(specs)
    if not task_list:
        raise ValueError("At least one task is required")
    if len({t.name for t in task_list}) != len(task_list):
        raise ValueError("Task names must be unique")

    remaining = {t.name: t.burst for t in task_list}
    first_start: dict[str, int | None] = {t.name: None for t in task_list}
    completion: dict[str, int | None] = {t.name: (t.arrival if t.burst == 0 else None) for t in task_list}
    slices_count = {t.name: 0 for t in task_list}

    clock = 0
    gantt: list[dict] = []
    events: list[dict] = []
    cs_count = 0
    cs_time = 0
    idle_time = 0
    last_running: str | None = None
    max_weight = max(t.weight for t in task_list)
    round_num = 0

    while any(remaining[t.name] > 0 for t in task_list):
        # Check if any unfinished task has arrived
        ready = [t for t in task_list if remaining[t.name] > 0 and t.arrival <= clock]
        if not ready:
            next_arr = min(t.arrival for t in task_list if remaining[t.name] > 0)
            gantt.append({"task": "IDLE", "start": clock, "end": next_arr})
            idle_time += (next_arr - clock)
            clock = next_arr
            last_running = None
            continue

        round_num += 1
        if variant == "classic":
            for t in task_list:
                if remaining[t.name] == 0 or t.arrival > clock:
                    continue
                if last_running is not None and last_running != t.name and context_switch > 0:
                    gantt.append({"task": "CS", "start": clock, "end": clock + context_switch})
                    clock += context_switch
                    cs_count += 1
                    cs_time += context_switch
                for q_idx in range(t.weight):
                    if remaining[t.name] == 0:
                        break
                    if first_start[t.name] is None:
                        first_start[t.name] = clock
                    run = min(quantum, remaining[t.name])
                    start = clock
                    remaining[t.name] -= run
                    clock += run
                    slices_count[t.name] += 1
                    last_running = t.name
                    if remaining[t.name] == 0:
                        completion[t.name] = clock
                    gantt.append({"task": t.name, "start": start, "end": clock})
                    events.append({
                        "round": round_num,
                        "task": t.name,
                        "start": start,
                        "end": clock,
                        "duration": run,
                        "remaining": remaining[t.name],
                        "slice_in_visit": q_idx + 1,
                    })
        else:
            # Interleaved WRR: sub-rounds s = 1 .. max_weight
            for sub in range(1, max_weight + 1):
                progressed = False
                for t in task_list:
                    if remaining[t.name] == 0 or t.arrival > clock or t.weight < sub:
                        continue
                    progressed = True
                    if last_running is not None and last_running != t.name and context_switch > 0:
                        gantt.append({"task": "CS", "start": clock, "end": clock + context_switch})
                        clock += context_switch
                        cs_count += 1
                        cs_time += context_switch
                    if first_start[t.name] is None:
                        first_start[t.name] = clock
                    run = min(quantum, remaining[t.name])
                    start = clock
                    remaining[t.name] -= run
                    clock += run
                    slices_count[t.name] += 1
                    last_running = t.name
                    if remaining[t.name] == 0:
                        completion[t.name] = clock
                    gantt.append({"task": t.name, "start": start, "end": clock})
                    events.append({
                        "round": round_num,
                        "sub_round": sub,
                        "task": t.name,
                        "start": start,
                        "end": clock,
                        "duration": run,
                        "remaining": remaining[t.name],
                    })
                if not any(remaining[t.name] > 0 for t in task_list):
                    break

    total_weight = sum(t.weight for t in task_list)
    total_burst = sum(t.burst for t in task_list)
    metrics = {}
    normalized_shares = []

    for idx, t in enumerate(task_list):
        comp = completion[t.name] if completion[t.name] is not None else t.arrival
        turnaround = comp - t.arrival
        waiting = turnaround - t.burst
        response = (first_start[t.name] - t.arrival) if first_start[t.name] is not None else 0
        ideal_share = (t.weight / total_weight) * 100.0
        actual_share = (t.burst / total_burst * 100.0) if total_burst > 0 else 0.0
        # Normalized rate ratio (service rate relative to weight while active)
        active_rate = (t.burst / max(1, turnaround)) / (t.weight / total_weight) if t.burst > 0 else 1.0
        normalized_shares.append(active_rate)
        metrics[t.name] = {
            "weight": t.weight,
            "burst": t.burst,
            "arrival": t.arrival,
            "first_start": first_start[t.name],
            "completion": comp,
            "turnaround": turnaround,
            "waiting": waiting,
            "response": response,
            "slices": slices_count[t.name],
            "ideal_weight_share_pct": round(ideal_share, 2),
            "actual_work_share_pct": round(actual_share, 2),
            "max_inter_service_wait_bound": theoretical_max_wait_bound(
                [x.weight for x in task_list], idx, quantum, context_switch
            ),
        }

    avg_turnaround = sum(m["turnaround"] for m in metrics.values()) / len(metrics)
    avg_waiting = sum(m["waiting"] for m in metrics.values()) / len(metrics)
    avg_response = sum(m["response"] for m in metrics.values()) / len(metrics)
    cpu_util = (total_burst / clock * 100.0) if clock > 0 else 100.0

    return {
        "variant": variant,
        "quantum": quantum,
        "context_switch": context_switch,
        "makespan": clock,
        "total_burst": total_burst,
        "idle_time": idle_time,
        "context_switches": cs_count,
        "context_switch_time": cs_time,
        "cpu_utilization_pct": round(cpu_util, 2),
        "avg_turnaround": round(avg_turnaround, 3),
        "avg_waiting": round(avg_waiting, 3),
        "avg_response": round(avg_response, 3),
        "weight_proportional_jains_index": round(jains_fairness_index(normalized_shares), 4),
        "metrics": metrics,
        "gantt": gantt,
        "events": events,
    }


STANDARD_SCENARIOS: dict[str, dict] = {
    "S1_baseline_repo": {
        "description": "Repository baseline workload matching exercise5_wrr.py: P1(w=3,b=5), P2(w=2,b=4), P3(w=1,b=3)",
        "quantum": 1,
        "tasks": [
            {"name": "P1", "weight": 3, "burst": 5, "arrival": 0},
            {"name": "P2", "weight": 2, "burst": 4, "arrival": 0},
            {"name": "P3", "weight": 1, "burst": 3, "arrival": 0},
        ],
    },
    "S2_backlogged_proportional": {
        "description": "Sustained backlogged workload where bursts are large multiples of weights (exact 50% / 33.3% / 16.7% share)",
        "quantum": 1,
        "tasks": [
            {"name": "P1", "weight": 3, "burst": 18, "arrival": 0},
            {"name": "P2", "weight": 2, "burst": 12, "arrival": 0},
            {"name": "P3", "weight": 1, "burst": 6, "arrival": 0},
        ],
    },
    "S3_high_skew_weights": {
        "description": "High weight skew (w=8, 2, 1, 1) comparing Classical WRR burstiness vs Interleaved WRR response latency",
        "quantum": 1,
        "tasks": [
            {"name": "VideoEnc", "weight": 8, "burst": 16, "arrival": 0},
            {"name": "APIWorker", "weight": 2, "burst": 6, "arrival": 0},
            {"name": "Telemetry", "weight": 1, "burst": 4, "arrival": 0},
            {"name": "AuditLog", "weight": 1, "burst": 4, "arrival": 0},
        ],
    },
    "S4_dynamic_arrivals": {
        "description": "Staggered arrivals with an idle gap and late high-weight entrant",
        "quantum": 2,
        "tasks": [
            {"name": "J1", "weight": 1, "burst": 6, "arrival": 0},
            {"name": "J2", "weight": 3, "burst": 9, "arrival": 2},
            {"name": "J3", "weight": 2, "burst": 5, "arrival": 4},
            {"name": "J4", "weight": 4, "burst": 8, "arrival": 16},
        ],
    },
}


def run_all_scenarios() -> dict:
    results = {}
    for sname, cfg in STANDARD_SCENARIOS.items():
        specs = [WRRTaskSpec(**t) for t in cfg["tasks"]]
        q = cfg["quantum"]
        results[sname] = {
            "description": cfg["description"],
            "classic": simulate_wrr(specs, quantum=q, variant="classic"),
            "interleaved": simulate_wrr(specs, quantum=q, variant="interleaved"),
        }
    # Quantum sweep on S2_backlogged_proportional with context_switch=1
    s2_specs = [WRRTaskSpec(**t) for t in STANDARD_SCENARIOS["S2_backlogged_proportional"]["tasks"]]
    q_sweep = []
    for q in [1, 2, 3, 4, 6, 8]:
        r = simulate_wrr(s2_specs, quantum=q, variant="classic", context_switch=1)
        q_sweep.append({
            "quantum": q,
            "makespan": r["makespan"],
            "cpu_utilization_pct": r["cpu_utilization_pct"],
            "context_switches": r["context_switches"],
            "avg_waiting": r["avg_waiting"],
            "avg_response": r["avg_response"],
        })
    results["quantum_sweep_cs1"] = q_sweep
    return results


def main():
    parser = argparse.ArgumentParser(description="Exercise 1 — WRR Simulator (Classic & Interleaved)")
    parser.add_argument("--scenario", choices=list(STANDARD_SCENARIOS.keys()) + ["all"], default="all")
    parser.add_argument("--out", type=Path, default=None, help="Optional JSON output path")
    args = parser.parse_args()

    all_res = run_all_scenarios()
    if args.scenario != "all":
        subset = {args.scenario: all_res[args.scenario]}
    else:
        subset = all_res

    for k, v in subset.items():
        if k == "quantum_sweep_cs1":
            continue
        print(f"=== {k}: {v['description']} ===")
        for var in ("classic", "interleaved"):
            rv = v[var]
            print(f"  [{var.upper()}] makespan={rv['makespan']} avg_wait={rv['avg_waiting']} "
                  f"avg_resp={rv['avg_response']} Jain={rv['weight_proportional_jains_index']}")

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(all_res, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
