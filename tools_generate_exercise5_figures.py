"""Generate Exercise 5 metrics figure from REAL schedule() output.

Reads metrics from exercise5_wrr.schedule() for the default workload and
writes docs/figures/wrr_metrics.png (grouped bars: completion / turnaround /
waiting per task). No numbers are hardcoded.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from exercise5_wrr import Task, schedule

SPECS = [("P1", 3, 5), ("P2", 2, 4), ("P3", 1, 3)]
result = schedule([Task(*s) for s in SPECS], 1, "semaphore")
metrics = result["metrics"]
print(metrics, "makespan=", result["makespan"])

names = [n for n, _, _ in SPECS]
completion = [metrics[n]["completion"] for n in names]
turnaround = [metrics[n]["turnaround"] for n in names]
waiting = [metrics[n]["waiting"] for n in names]

x = range(len(names))
w = 0.26
fig, ax = plt.subplots(figsize=(9, 4.8))
b1 = ax.bar([i - w for i in x], completion, width=w, label="Completion time", color="#4e79a7", edgecolor="white")
b2 = ax.bar(list(x), turnaround, width=w, label="Turnaround time", color="#f28e2b", edgecolor="white")
b3 = ax.bar([i + w for i in x], waiting, width=w, label="Waiting time", color="#59a14f", edgecolor="white")
for bars in (b1, b2, b3):
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, h + 0.25, f"{int(h)}",
                ha="center", va="bottom", fontsize=10, fontweight="bold")
ax.set_xticks(list(x))
ax.set_xticklabels([f"{n}\n(w={wt}, b={bu})" for n, wt, bu in SPECS])
ax.set_ylabel("Simulated time units")
ax.set_ylim(0, max(completion + turnaround + waiting) * 1.2)
ax.set_title("Exercise 5 Metrics — Completion / Turnaround / Waiting\n"
             "From exercise5_wrr.schedule() (makespan = 12, quantum = 1)",
             fontsize=10)
ax.legend(frameon=True, fontsize=9)
ax.grid(axis="y", linestyle="--", alpha=0.4)
ax.set_axisbelow(True)
for spine in ["top", "right"]:
    ax.spines[spine].set_visible(False)
plt.tight_layout()
plt.savefig("docs/figures/wrr_metrics.png", dpi=200, bbox_inches="tight")
plt.close()
print("saved docs/figures/wrr_metrics.png")
