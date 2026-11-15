"""
Exercise 2 — Quantitative & Formal Comparison of Weighted Round Robin (WRR),
Earliest Deadline First (EDF), and Rate Monotonic (RM) on Periodic Real-Time Workloads.

Implements:
  - Discrete-time preemptive job-level simulators for WRR, EDF, and RM
    over [0, H) where H = lcm(periods) or explicit horizon.
  - Liu & Layland sufficient bound for RM: n * (2^(1/n) - 1)
  - Exact Response-Time Analysis (RTA, Joseph & Pandya 1986) for RM
  - Processor Utilization Demand bound for EDF: sum(C_i / T_i) <= 1 (when D_i = T_i)
  - Deterministic seeded Monte Carlo experiment (UUniFast-style rational task sets)
    across utilization bands [0.55 .. 1.00] to measure empirical schedulability,
    deadline-miss ratio, starvation / inter-service gap, and context switches.
"""
from __future__ import annotations
from dataclasses import dataclass
from math import gcd, ceil
from typing import Iterable, Literal
import random
import json
import argparse
from pathlib import Path


def lcm(a: int, b: int) -> int:
    return abs(a * b) // gcd(a, b) if a and b else 0


def lcm_many(nums: Iterable[int]) -> int:
    res = 1
    for x in nums:
        res = lcm(res, x)
    return res


@dataclass(frozen=True)
class PeriodicTask:
    name: str
    cost: int          # C_i > 0
    period: int        # T_i > 0
    deadline: int      # D_i > 0 (relative deadline)
    weight: int = 1    # WRR weight w_i > 0
    phase: int = 0     # initial release offset >= 0

    def __post_init__(self):
        if self.cost <= 0 or self.period <= 0 or self.deadline <= 0 or self.weight <= 0:
            raise ValueError(f"Invalid parameters for {self.name}")
        if self.phase < 0:
            raise ValueError("phase must be non-negative")

    @property
    def utilization(self) -> float:
        return self.cost / self.period


def liu_layland_bound(n: int) -> float:
    if n <= 0:
        raise ValueError("n must be positive")
    return n * ((2.0 ** (1.0 / n)) - 1.0)


def exact_rm_rta(tasks: list[PeriodicTask]) -> dict[str, dict]:
    """
    Exact Response-Time Analysis (Joseph & Pandya 1986) for synchronous (phase=0)
    independent periodic tasks ordered by non-decreasing period (tie-break: input order).
    """
    ordered = sorted(enumerate(tasks), key=lambda x: (x[1].period, x[0]))
    rta_out = {}
    hp_list: list[PeriodicTask] = []
    for _, t in ordered:
        r_prev = t.cost
        converged = True
        while True:
            interference = sum(ceil(r_prev / hp.period) * hp.cost for hp in hp_list)
            r_next = t.cost + interference
            if r_next == r_prev:
                break
            if r_next > t.deadline:
                converged = False
                r_prev = r_next
                break
            r_prev = r_next
        rta_out[t.name] = {
            "worst_case_response": r_prev,
            "deadline": t.deadline,
            "schedulable": converged and (r_prev <= t.deadline),
        }
        hp_list.append(t)
    return rta_out


@dataclass
class JobInstance:
    task_idx: int
    task_name: str
    job_num: int
    release: int
    abs_deadline: int
    cost: int
    remaining: int
    weight: int
    period: int
    first_start: int | None = None
    completion: int | None = None
    missed_reported: bool = False


def simulate_periodic(
    tasks: list[PeriodicTask],
    policy: Literal["WRR", "EDF", "RM"],
    horizon: int | None = None,
    wrr_quantum: int = 1,
) -> dict:
    """
    Simulate periodic task set over [0, horizon) on a single preemptive CPU.
    Conventions:
      - Discrete tick clock t = 0, 1, ..., horizon - 1.
      - Overrun jobs (remaining > 0 at abs_deadline) are recorded as deadline misses
        at t = abs_deadline and continue until finished (non-aborting overrun model,
        standard for overload / Domino-effect analysis).
      - RM priority: shorter period first; tie-broken by smaller task index.
      - EDF priority: earlier absolute deadline first; tie-broken by smaller task index, then earlier release.
      - WRR policy: cyclic round over task indices 0..N-1; each task with ready job(s)
        executes its oldest unfinished job for up to `weight * wrr_quantum` ticks per visit.
    """
    if not tasks:
        raise ValueError("Task list must be non-empty")
    if policy not in {"WRR", "EDF", "RM"}:
        raise ValueError("policy must be WRR, EDF, or RM")
    if wrr_quantum <= 0:
        raise ValueError("wrr_quantum must be positive")

    H = horizon if horizon is not None else lcm_many([t.period for t in tasks])
    if H <= 0:
        raise ValueError("horizon must be positive")

    # Pre-generate all jobs released in [0, H)
    all_jobs: list[JobInstance] = []
    for idx, t in enumerate(tasks):
        jnum = 1
        rel = t.phase
        while rel < H:
            all_jobs.append(JobInstance(
                task_idx=idx,
                task_name=t.name,
                job_num=jnum,
                release=rel,
                abs_deadline=rel + t.deadline,
                cost=t.cost,
                remaining=t.cost,
                weight=t.weight,
                period=t.period,
            ))
            rel += t.period
            jnum += 1

    timeline: list[str] = []
    misses: list[dict] = []

    # WRR cursor state
    wrr_idx = 0
    wrr_budget_used = 0

    for tick in range(H):
        # Check deadline misses for jobs whose deadline is <= tick and still remaining > 0
        for j in all_jobs:
            if not j.missed_reported and j.abs_deadline <= tick and j.remaining > 0:
                j.missed_reported = True
                misses.append({
                    "tick": tick,
                    "task": j.task_name,
                    "job": f"{j.task_name},{j.job_num}",
                    "release": j.release,
                    "abs_deadline": j.abs_deadline,
                    "remaining_at_deadline": j.remaining,
                })

        ready_jobs = [j for j in all_jobs if j.release <= tick and j.remaining > 0]
        if not ready_jobs:
            timeline.append("IDLE")
            wrr_budget_used = 0
            continue

        chosen: JobInstance | None = None
        if policy == "RM":
            # Oldest job of highest-priority (smallest period, smallest task_idx) task
            ready_jobs.sort(key=lambda j: (j.period, j.task_idx, j.release, j.job_num))
            chosen = ready_jobs[0]
        elif policy == "EDF":
            ready_jobs.sort(key=lambda j: (j.abs_deadline, j.task_idx, j.release, j.job_num))
            chosen = ready_jobs[0]
        else:  # WRR
            n = len(tasks)
            for _ in range(n + 1):
                t_cand = tasks[wrr_idx]
                cand_jobs = [j for j in ready_jobs if j.task_idx == wrr_idx]
                max_slice_ticks = t_cand.weight * wrr_quantum
                if cand_jobs and wrr_budget_used < max_slice_ticks:
                    cand_jobs.sort(key=lambda j: (j.release, j.job_num))
                    chosen = cand_jobs[0]
                    break
                wrr_idx = (wrr_idx + 1) % n
                wrr_budget_used = 0

        assert chosen is not None
        if chosen.first_start is None:
            chosen.first_start = tick
        chosen.remaining -= 1
        timeline.append(chosen.task_name)
        if chosen.remaining == 0:
            chosen.completion = tick + 1

        if policy == "WRR":
            wrr_budget_used += 1
            # If no more ready jobs for this task or budget exhausted, advance cursor
            rem_for_task = [j for j in all_jobs if j.task_idx == wrr_idx and j.release <= tick and j.remaining > 0]
            if not rem_for_task or wrr_budget_used >= tasks[wrr_idx].weight * wrr_quantum:
                wrr_idx = (wrr_idx + 1) % len(tasks)
                wrr_budget_used = 0

    # End-of-horizon deadline check at tick = H
    for j in all_jobs:
        if not j.missed_reported and j.abs_deadline <= H and j.remaining > 0:
            j.missed_reported = True
            misses.append({
                "tick": H,
                "task": j.task_name,
                "job": f"{j.task_name},{j.job_num}",
                "release": j.release,
                "abs_deadline": j.abs_deadline,
                "remaining_at_deadline": j.remaining,
            })

    # Merge contiguous timeline segments into Gantt blocks
    gantt: list[dict] = []
    for tick, label in enumerate(timeline):
        if gantt and gantt[-1]["task"] == label:
            gantt[-1]["end"] = tick + 1
        else:
            gantt.append({"task": label, "start": tick, "end": tick + 1})

    # Context switches (transitions between non-IDLE distinct tasks)
    preemptions = 0
    prev_task = None
    for label in timeline:
        if label == "IDLE":
            prev_task = None
            continue
        if prev_task is not None and prev_task != label:
            preemptions += 1
        prev_task = label

    # Per-task summary
    per_task = {}
    for idx, t in enumerate(tasks):
        tjobs = [j for j in all_jobs if j.task_idx == idx]
        completed = [j for j in tjobs if j.completion is not None]
        t_misses = [m for m in misses if m["task"] == t.name]
        resp_times = [j.completion - j.release for j in completed if j.completion is not None]
        ticks_served = sum(1 for lbl in timeline if lbl == t.name)
        per_task[t.name] = {
            "jobs_released": len(tjobs),
            "jobs_completed": len(completed),
            "deadline_misses": len(t_misses),
            "ticks_served": ticks_served,
            "cpu_share_pct": round(ticks_served / H * 100.0, 2),
            "max_response_time": max(resp_times) if resp_times else None,
            "avg_response_time": round(sum(resp_times) / len(resp_times), 3) if resp_times else None,
        }

    idle_ticks = sum(1 for lbl in timeline if lbl == "IDLE")
    return {
        "policy": policy,
        "horizon": H,
        "total_utilization": round(sum(t.utilization for t in tasks), 4),
        "jobs_total": len(all_jobs),
        "deadline_misses_count": len(misses),
        "deadline_miss_ratio": round(len(misses) / max(1, len(all_jobs)), 4),
        "feasible_on_horizon": len(misses) == 0,
        "context_switches": preemptions,
        "idle_ticks": idle_ticks,
        "cpu_busy_pct": round((H - idle_ticks) / H * 100.0, 2),
        "misses": misses,
        "per_task": per_task,
        "gantt": gantt,
        "timeline": timeline,
    }


BENCHMARK_SUITES: dict[str, list[PeriodicTask]] = {
    "W1_underload_harmonic": [
        PeriodicTask("T1", cost=1, period=4, deadline=4, weight=3),
        PeriodicTask("T2", cost=2, period=8, deadline=8, weight=2),
        PeriodicTask("T3", cost=2, period=16, deadline=16, weight=1),
    ],  # U = 0.25 + 0.25 + 0.125 = 0.625 <= LL(3)=0.7798
    "W2_high_util_gap": [
        PeriodicTask("T1", cost=2, period=5, deadline=5, weight=3),
        PeriodicTask("T2", cost=3, period=8, deadline=8, weight=2),
        PeriodicTask("T3", cost=4, period=20, deadline=20, weight=1),
    ],  # U = 0.40 + 0.375 + 0.20 = 0.975 (EDF=0 misses, RM misses, WRR misses)
    "W3_overload_domino": [
        PeriodicTask("T1", cost=2, period=4, deadline=4, weight=4),
        PeriodicTask("T2", cost=3, period=6, deadline=6, weight=2),
        PeriodicTask("T3", cost=3, period=8, deadline=8, weight=1),
    ],  # U = 0.50 + 0.50 + 0.375 = 1.375 (Overload: EDF Domino vs RM low-prio isolation vs WRR guaranteed share!)
    "W4_aperiodic_mixed_weights": [
        PeriodicTask("Sensor", cost=1, period=6, deadline=6, weight=4),
        PeriodicTask("Control", cost=2, period=9, deadline=9, weight=3),
        PeriodicTask("Logger", cost=4, period=18, deadline=18, weight=2),
    ],  # U = 1/6 + 2/9 + 4/18 = 11/18 = 0.6111
}


def run_monte_carlo_schedulability(seed: int = 20261115, sets_per_band: int = 80) -> list[dict]:
    """
    Generate synthetic 3-task periodic sets with periods chosen from {4,5,6,8,10,12,15,20,24}
    (bounded hyperperiod <= 120) across utilization bands and compare WRR (rate-proportional weights),
    RM, and EDF.
    """
    rng = random.Random(seed)
    period_pool = [4, 6, 8, 10, 12, 15, 20, 24]
    bands = [(0.50, 0.65), (0.65, 0.78), (0.78, 0.88), (0.88, 0.96), (0.96, 1.00)]
    band_stats = []

    for lo, hi in bands:
        generated = 0
        attempts = 0
        ok = {"WRR": 0, "RM": 0, "EDF": 0}
        miss_sum = {"WRR": 0.0, "RM": 0.0, "EDF": 0.0}
        while generated < sets_per_band and attempts < 15000:
            attempts += 1
            ps = sorted(rng.sample(period_pool, 3))
            H = lcm_many(ps)
            if H > 240:
                continue
            cs = [rng.randint(1, p - 1) for p in ps]
            u = sum(c / p for c, p in zip(cs, ps))
            if not (lo <= u <= hi):
                continue
            # Assign WRR weights proportional to ceil(u_i * 10)
            ws = [max(1, round((c / p) * 10)) for c, p in zip(cs, ps)]
            tset = [PeriodicTask(f"T{i+1}", cost=cs[i], period=ps[i], deadline=ps[i], weight=ws[i]) for i in range(3)]
            generated += 1
            for pol in ("WRR", "RM", "EDF"):
                sim = simulate_periodic(tset, policy=pol, horizon=H)
                if sim["feasible_on_horizon"]:
                    ok[pol] += 1
                miss_sum[pol] += sim["deadline_miss_ratio"]

        n = max(1, generated)
        band_stats.append({
            "band": f"[{lo:.2f}, {hi:.2f}]",
            "count": generated,
            "EDF_feasible_pct": round(ok["EDF"] / n * 100.0, 1),
            "RM_feasible_pct": round(ok["RM"] / n * 100.0, 1),
            "WRR_feasible_pct": round(ok["WRR"] / n * 100.0, 1),
            "EDF_avg_miss_pct": round(miss_sum["EDF"] / n * 100.0, 2),
            "RM_avg_miss_pct": round(miss_sum["RM"] / n * 100.0, 2),
            "WRR_avg_miss_pct": round(miss_sum["WRR"] / n * 100.0, 2),
        })
    return band_stats


def run_all_comparisons() -> dict:
    suites_out = {}
    for wname, tset in BENCHMARK_SUITES.items():
        H = 24 if wname == "W3_overload_domino" else lcm_many([t.period for t in tset])
        suites_out[wname] = {
            "utilization": round(sum(t.utilization for t in tset), 4),
            "liu_layland_bound": round(liu_layland_bound(len(tset)), 4),
            "rm_rta": exact_rm_rta(tset),
            "horizon": H,
            "WRR": simulate_periodic(tset, "WRR", horizon=H),
            "RM": simulate_periodic(tset, "RM", horizon=H),
            "EDF": simulate_periodic(tset, "EDF", horizon=H),
        }
    mc = run_monte_carlo_schedulability()
    return {"benchmarks": suites_out, "monte_carlo": mc}


def main():
    p = argparse.ArgumentParser(description="Exercise 2 — WRR vs EDF vs RM Comparison Engine")
    p.add_argument("--out", type=Path, default=None)
    args = p.parse_args()
    res = run_all_comparisons()
    for wname, data in res["benchmarks"].items():
        print(f"=== {wname} (U={data['utilization']}, H={data['horizon']}) ===")
        for pol in ("WRR", "RM", "EDF"):
            s = data[pol]
            print(f"  {pol:3s}: misses={s['deadline_misses_count']:2d}/{s['jobs_total']:2d} "
                  f"ctx_sw={s['context_switches']:2d} shares={[v['cpu_share_pct'] for v in s['per_task'].values()]}")
    print("=== Monte Carlo Schedulability (seed=20261115) ===")
    for b in res["monte_carlo"]:
        print(" ", b)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        # Exclude bulky tick-by-tick arrays only if needed, keep gantt
        args.out.write_text(json.dumps(res, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
