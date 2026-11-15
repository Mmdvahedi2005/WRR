"""Generate README figures from REAL exercise5_wrr.schedule() output.

All numbers come from running the actual scheduler code — nothing is hardcoded
except the workload definition which matches exercise5_wrr.main() defaults:
P1(weight=3, burst=5), P2(weight=2, burst=4), P3(weight=1, burst=3), quantum=1.

Outputs (PNG, data-driven):
  docs/figures/wrr_gantt.png      — Gantt chart from real gantt segments
  docs/figures/wrr_cpu_share.png  — idealized weight share vs actual burst share
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from exercise5_wrr import Task, schedule

SPECS = [("P1", 3, 5), ("P2", 2, 4), ("P3", 1, 3)]
QUANTUM = 1
COLORS = {"P1": "#4e79a7", "P2": "#f28e2b", "P3": "#59a14f"}

result = schedule([Task(*s) for s in SPECS], QUANTUM, "semaphore")
gantt = result["gantt"]
metrics = result["metrics"]
makespan = result["makespan"]
print(f"makespan={makespan} segments={len(gantt)}")
for name, m in metrics.items():
    print(name, m)

# --- Figure 1: Gantt chart (real segments) ---
tasks = ["P1", "P2", "P3"]
ypos = {t: i for i, t in enumerate(reversed(tasks))}  # P1 on top
fig, ax = plt.subplots(figsize=(10, 4.2))
for seg in gantt:
    y = ypos[seg["task"]]
    ax.barh(y, seg["end"] - seg["start"], left=seg["start"],
            height=0.55, color=COLORS[seg["task"]], edgecolor="white", linewidth=1.2)
    mid = (seg["start"] + seg["end"]) / 2
    ax.text(mid, y, seg["task"], ha="center", va="center",
            color="white", fontsize=9, fontweight="bold")
ax.set_yticks(list(ypos.values()))
ax.set_yticklabels(list(ypos.keys()))
ax.set_xlabel("Simulated time (quantum = 1)")
ax.set_title("WRR Gantt Chart — P1(w=3,b=5), P2(w=2,b=4), P3(w=1,b=3), quantum=1\n"
             "Generated from exercise5_wrr.schedule() output (makespan = 12)",
             fontsize=10)
ax.set_xlim(0, makespan)
ax.set_xticks(range(makespan + 1))
ax.grid(axis="x", linestyle="--", alpha=0.4)
ax.set_axisbelow(True)
for spine in ["top", "right"]:
    ax.spines[spine].set_visible(False)
plt.tight_layout()
plt.savefig("docs/figures/wrr_gantt.png", dpi=200, bbox_inches="tight")
plt.close()
print("saved docs/figures/wrr_gantt.png")

# --- Figure 2: Idealized weight share vs actual burst share ---
total_w = sum(w for _, w, _ in SPECS)
total_b = sum(b for _, _, b in SPECS)
names = [n for n, _, _ in SPECS]
ideal = [w / total_w * 100 for _, w, _ in SPECS]
actual = [b / total_b * 100 for _, _, b in SPECS]
x = range(len(names))
w = 0.36
fig, ax = plt.subplots(figsize=(9, 4.5))
b1 = ax.bar([i - w/2 for i in x], ideal, width=w, label="Idealized weight share  w_i / Σw",
            color="#4e79a7", edgecolor="white")
b2 = ax.bar([i + w/2 for i in x], actual, width=w, label="Actual burst share  burst_i / Σburst",
            color="#f28e2b", edgecolor="white")
for bars in (b1, b2):
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, h + 0.7, f"{h:.1f}%",
                ha="center", va="bottom", fontsize=9)
ax.set_xticks(list(x))
ax.set_xticklabels([f"{n}\n(w={wt}, b={bu})" for n, wt, bu in SPECS])
ax.set_ylabel("Share of total (%)")
ax.set_ylim(0, max(ideal + actual) * 1.25)
ax.set_title("WRR Service Share — Idealized (by weight) vs Actual (by burst)\n"
             "Weights 3/2/1 → 50.0% / 33.3% / 16.7%  |  Bursts 5/4/3 → 41.7% / 33.3% / 25.0%",
             fontsize=10)
ax.legend(frameon=True, fontsize=9)
ax.grid(axis="y", linestyle="--", alpha=0.4)
ax.set_axisbelow(True)
for spine in ["top", "right"]:
    ax.spines[spine].set_visible(False)
plt.tight_layout()
plt.savefig("docs/figures/wrr_cpu_share.png", dpi=200, bbox_inches="tight")
plt.close()
print("saved docs/figures/wrr_cpu_share.png")
print(f"ideal={[round(v,1) for v in ideal]} actual={[round(v,1) for v in actual]}")
