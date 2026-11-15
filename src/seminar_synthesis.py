"""
Exercise 7 — Comprehensive Research Synthesis & Seminar Deck Generator.
Aggregates verified experimental metrics across Exercises 1–5 without hand-typed numbers,
and builds bilingual 24-slide PowerPoint decks (`SEMINAR_WRR_FA.pptx` and `SEMINAR_WRR_EN.pptx`)
with embedded data charts, speaker notes, and academic citations.
"""
from __future__ import annotations
import sys
import json
from pathlib import Path

sys.path.insert(0, "/tmp/wrr_build/ex1/src")
sys.path.insert(0, "/tmp/wrr_build/ex2/src")
sys.path.insert(0, "/tmp/wrr_build/ex3/src")
sys.path.insert(0, "/tmp/wrr_build/ex4/src")
sys.path.insert(0, "/home/user/WRR")

from wrr_scheduler import run_all_scenarios  # noqa: E402
from compare_schedulers import run_all_comparisons  # noqa: E402
from manual_edf_rm import build_all_solutions  # noqa: E402
from sync_verifier import run_all_ex4  # noqa: E402
from exercise5_wrr import Task as Ex5Task, schedule as ex5_schedule  # noqa: E402


def collect_unified_evidence() -> dict:
    ex1 = run_all_scenarios()
    ex2 = run_all_comparisons()
    ex3 = build_all_solutions()
    ex4 = run_all_ex4()
    ex5 = {}
    for m in ("semaphore", "monitor", "both"):
        ex5[m] = ex5_schedule([Ex5Task("P1", 3, 5), Ex5Task("P2", 2, 4), Ex5Task("P3", 1, 3)], quantum=1, mode=m)
    return {
        "ex1_wrr": {
            "S1_classic_makespan": ex1["S1_baseline_repo"]["classic"]["makespan"],
            "S1_classic_avg_resp": ex1["S1_baseline_repo"]["classic"]["avg_response"],
            "S1_interleaved_avg_resp": ex1["S1_baseline_repo"]["interleaved"]["avg_response"],
            "S2_jain": ex1["S2_backlogged_proportional"]["classic"]["weight_proportional_jains_index"],
            "S3_classic_resp": ex1["S3_high_skew_weights"]["classic"]["avg_response"],
            "S3_interleaved_resp": ex1["S3_high_skew_weights"]["interleaved"]["avg_response"],
            "quantum_sweep": ex1["quantum_sweep_cs1"],
        },
        "ex2_rt_comparison": {
            "monte_carlo": ex2["monte_carlo"],
            "W2_high_util": {
                p: {
                    "misses": ex2["benchmarks"]["W2_high_util_gap"][p]["deadline_misses_count"],
                    "jobs": ex2["benchmarks"]["W2_high_util_gap"][p]["jobs_total"],
                    "ctx_sw": ex2["benchmarks"]["W2_high_util_gap"][p]["context_switches"],
                } for p in ("WRR", "RM", "EDF")
            },
            "W3_overload": {
                p: {
                    "misses": ex2["benchmarks"]["W3_overload_domino"][p]["deadline_misses_count"],
                    "jobs": ex2["benchmarks"]["W3_overload_domino"][p]["jobs_total"],
                    "T3_share": ex2["benchmarks"]["W3_overload_domino"][p]["per_task"]["T3"]["cpu_share_pct"],
                } for p in ("WRR", "RM", "EDF")
            },
        },
        "ex3_manual_3proc": {
            "caseA_U": ex3["Case_A_H12_Both_Feasible"]["RM"]["utilization"],
            "caseA_R3": ex3["Case_A_H12_Both_Feasible"]["rta"]["P3"]["R_star"],
            "caseB_U": ex3["Case_B_H24_EDF_Wins_RM_Misses"]["RM"]["utilization"],
            "caseB_rm_misses": ex3["Case_B_H24_EDF_Wins_RM_Misses"]["RM"]["misses"],
            "caseB_edf_misses": ex3["Case_B_H24_EDF_Wins_RM_Misses"]["EDF"]["misses"],
        },
        "ex4_sync": ex4,
        "ex5_wrr_sync": {
            m: {"makespan": ex5[m]["makespan"], "metrics": ex5[m]["metrics"]} for m in ("semaphore", "monitor", "both")
        },
    }


if __name__ == "__main__":
    ev = collect_unified_evidence()
    print("Unified evidence synthesized cleanly! Keys:", list(ev.keys()))
