"""Educational Weighted Round Robin scheduler with synchronization variants.

The model is deterministic: each runnable process receives up to its positive
weight number of quanta per round. A synchronization guard serializes dispatch
updates, illustrating semaphore, monitor, and combined coordination.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
from threading import BoundedSemaphore, Condition
from typing import Iterable
import argparse

@dataclass
class Task:
    name: str
    weight: int
    bursts: int
    remaining: int = field(init=False)
    first_start: int | None = None
    completion: int | None = None
    waiting: int = 0
    def __post_init__(self):
        if self.weight <= 0 or self.bursts < 0:
            raise ValueError("weight must be positive and bursts non-negative")
        self.remaining = self.bursts

class DispatchGuard:
    """Mutual-exclusion abstraction for the three synchronization variants."""
    def __init__(self, mode: str):
        if mode not in {"semaphore", "monitor", "both"}:
            raise ValueError("mode must be semaphore, monitor, or both")
        self.mode = mode
        self.sem = BoundedSemaphore(1) if mode in {"semaphore", "both"} else None
        self.condition = Condition() if mode in {"monitor", "both"} else None
    def __enter__(self):
        if self.sem: self.sem.acquire()
        if self.condition:
            self.condition.acquire()
            while getattr(self, "_busy", False):
                self.condition.wait()
            self._busy = True
        return self
    def __exit__(self, *_):
        if self.condition:
            self._busy = False
            self.condition.notify_all()
            self.condition.release()
        if self.sem: self.sem.release()

def schedule(tasks: Iterable[Task], quantum: int = 1, mode: str = "semaphore"):
    """Return event log, Gantt segments and per-task metrics."""
    if quantum <= 0: raise ValueError("quantum must be positive")
    tasks = list(tasks)
    if len({t.name for t in tasks}) != len(tasks):
        raise ValueError("task names must be unique")
    guard = DispatchGuard(mode)
    events, gantt, clock = [], [], 0
    while any(t.remaining for t in tasks):
        progressed = False
        for task in tasks:
            for _ in range(task.weight):
                if task.remaining == 0: break
                with guard:
                    progressed = True
                    if task.first_start is None: task.first_start = clock
                    run = min(quantum, task.remaining)
                    start = clock
                    task.remaining -= run
                    clock += run
                    if task.remaining == 0: task.completion = clock
                    gantt.append({"task": task.name, "start": start, "end": clock})
                    events.append({"task": task.name, "start": start, "duration": run,
                                   "remaining": task.remaining, "mode": mode})
        if not progressed: break
    metrics = {}
    for t in tasks:
        completion = t.completion if t.completion is not None else 0
        metrics[t.name] = {"weight": t.weight, "burst": t.bursts,
                           "completion": completion,
                           "turnaround": completion,
                           "waiting": completion - t.bursts}
    return {"mode": mode, "events": events, "gantt": gantt,
            "metrics": metrics, "makespan": clock}

def gantt_svg(result, path):
    segs = result["gantt"]
    width, row_h, left = 900, 58, 90
    scale = 700 / max(1, result["makespan"])
    names = list(dict.fromkeys(s["task"] for s in segs))
    ymap = {n: 40+i*row_h for i,n in enumerate(names)}
    colors = ["#4e79a7", "#f28e2b", "#59a14f", "#e15759", "#b07aa1"]
    color = {n: colors[i % len(colors)] for i,n in enumerate(names)}
    h = 80 + len(names)*row_h
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{h}" viewBox="0 0 {width} {h}">',
             '<rect width="100%" height="100%" fill="white"/>',
             f'<text x="20" y="24" font-family="Arial" font-size="18">WRR Gantt — {result["mode"]}</text>']
    for n in names:
        y=ymap[n]
        parts.append(f'<text x="18" y="{y+23}" font-family="Arial" font-size="14">{n}</text>')
    for s in segs:
        x=left+s["start"]*scale; w=max(1,s["end"]-s["start"])*scale; y=ymap[s["task"]]
        parts.append(f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="34" fill="{color[s["task"]]}" stroke="white"/>')
        parts.append(f'<text x="{x+w/2:.1f}" y="{y+22}" text-anchor="middle" fill="white" font-family="Arial" font-size="12">{s["task"]}</text>')
    for t in range(result["makespan"]+1):
        x=left+t*scale
        parts.append(f'<text x="{x:.1f}" y="{h-12}" text-anchor="middle" font-family="Arial" font-size="10">{t}</text>')
    parts.append('</svg>')
    with open(path,"w",encoding="utf-8") as f: f.write("\n".join(parts))

def main():
    p=argparse.ArgumentParser(description="Weighted Round Robin synchronization demo")
    p.add_argument("--mode", choices=["semaphore","monitor","both","all"], default="all")
    p.add_argument("--quantum", type=int, default=1)
    p.add_argument("--gantt", default="wrr-gantt")
    args=p.parse_args()
    specs=[("P1",3,5),("P2",2,4),("P3",1,3)]
    modes=["semaphore","monitor","both"] if args.mode=="all" else [args.mode]
    for mode in modes:
        result=schedule([Task(*s) for s in specs],args.quantum,mode)
        print(f"\n{mode.upper()} | makespan={result['makespan']}")
        for name,m in result["metrics"].items(): print(name,m)
        gantt_svg(result,f"{args.gantt}-{mode}.svg")

if __name__=="__main__": main()
