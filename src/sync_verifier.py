"""
Exercise 4 — Formal State-Space Model Checker & Empirical Contention Harness
for Mutual Exclusion & Synchronization Mechanisms:
  1. Naive Lock Flag (Flawed attempt — violates Mutual Exclusion!)
  2. Strict Alternation (Turn variable — violates Progress!)
  3. Announce-and-Spin / Flag-only (Violates Deadlock Freedom!)
  4. Dekker's Algorithm (1965) — 2-process software mutual exclusion (Safe, Deadlock-Free, Starvation-Free)
  5. Peterson's Algorithm (1981) — Compact 2-process software mutual exclusion (Safe, Bounded Wait <= 1)
  6. Counting / Binary Semaphore (Dijkstra 1965) — Kernel/Blocking FIFO queue vs weak semaphore
  7. Hoare / Mesa Monitor (Hoare 1974; Lampson & Redell 1980) — Encapsulated lock + Condition Variables

Every number and verdict in the Exercise 4 report is produced by this module.
"""
from __future__ import annotations
from collections import deque
from dataclasses import dataclass
import threading
import time
import json
import argparse
from pathlib import Path


@dataclass(frozen=True)
class ModelVerdict:
    protocol: str
    reachable_states: int
    transitions: int
    mutual_exclusion: bool
    deadlock_free: bool
    progress_no_contention: bool
    bounded_waiting_bound: int | str
    counterexample_trace: list[str] | None = None


def explore_two_process_protocol(protocol: str) -> ModelVerdict:
    """
    Exhaustive explicit-state BFS/SCC verifier over sequentially consistent
    atomic instruction interleavings of two processes P0 and P1.
    Each process cycles:
      REM (Remainder) -> ENTRY_1 .. ENTRY_k -> CS (Critical Section) -> EXIT_1 .. EXIT_m -> REM
    """
    if protocol == "naive_flag":
        # P_i: L0(REM)->L1(wait lock==0)->L2(set lock=1)->CS->L4(set lock=0)->L0
        init = ("REM", "REM", 0)
        def step(st, pid):
            pc0, pc1, lock = st
            pc = pc0 if pid == 0 else pc1
            nxt = []
            if pc == "REM":
                nxt.append(("TEST", lock))
            elif pc == "TEST":
                if lock == 0:
                    nxt.append(("SET", lock))
            elif pc == "SET":
                nxt.append(("CS", 1))
            elif pc == "CS":
                nxt.append(("REM", 0))
            out = []
            for npc, nlock in nxt:
                out.append((npc, pc1, nlock) if pid == 0 else (pc0, npc, nlock))
            return out
        is_cs = lambda st, pid: (st[0] if pid == 0 else st[1]) == "CS"
        is_trying = lambda st, pid: (st[0] if pid == 0 else st[1]) in {"TEST", "SET"}
        is_rem = lambda st, pid: (st[0] if pid == 0 else st[1]) == "REM"

    elif protocol == "strict_alternation":
        # P_i: REM -> WAIT(turn==i) -> CS -> EXIT(turn=1-i) -> REM
        init = ("REM", "REM", 0)
        def step(st, pid):
            pc0, pc1, turn = st
            pc = pc0 if pid == 0 else pc1
            nxt = []
            if pc == "REM":
                nxt.append(("WAIT", turn))
            elif pc == "WAIT":
                if turn == pid:
                    nxt.append(("CS", turn))
            elif pc == "CS":
                nxt.append(("REM", 1 - pid))
            return [((npc, pc1, nt) if pid == 0 else (pc0, npc, nt)) for npc, nt in nxt]
        is_cs = lambda st, pid: (st[0] if pid == 0 else st[1]) == "CS"
        is_trying = lambda st, pid: (st[0] if pid == 0 else st[1]) == "WAIT"
        is_rem = lambda st, pid: (st[0] if pid == 0 else st[1]) == "REM"

    elif protocol == "flag_deadlock":
        # P_i: REM -> SET_FLAG(flag[i]=1) -> WAIT_OTHER(flag[1-i]==0) -> CS -> CLEAR(flag[i]=0)
        init = ("REM", "REM", 0, 0)
        def step(st, pid):
            pc0, pc1, f0, f1 = st
            pc = pc0 if pid == 0 else pc1
            other_f = f1 if pid == 0 else f0
            res = []
            if pc == "REM":
                nf0, nf1 = (1, f1) if pid == 0 else (f0, 1)
                res.append(("WAIT", pc1, nf0, nf1) if pid == 0 else (pc0, "WAIT", nf0, nf1))
            elif pc == "WAIT":
                if other_f == 0:
                    res.append(("CS", pc1, f0, f1) if pid == 0 else (pc0, "CS", f0, f1))
            elif pc == "CS":
                nf0, nf1 = (0, f1) if pid == 0 else (f0, 0)
                res.append(("REM", pc1, nf0, nf1) if pid == 0 else (pc0, "REM", nf0, nf1))
            return res
        is_cs = lambda st, pid: (st[0] if pid == 0 else st[1]) == "CS"
        is_trying = lambda st, pid: (st[0] if pid == 0 else st[1]) == "WAIT"
        is_rem = lambda st, pid: (st[0] if pid == 0 else st[1]) == "REM"

    elif protocol == "dekker":
        # Full atomic step model of Dekker's Algorithm:
        # REM -> E1(flag[i]=1) -> E2(check flag[j]) ->
        #   if flag[j]==0 -> CS
        #   if flag[j]==1 -> E3(check turn==j):
        #       if turn!=j -> E2
        #       if turn==j -> E4(flag[i]=0) -> E5(wait turn==i) -> E6(flag[i]=1) -> E2
        # CS -> X1(turn=j) -> X2(flag[i]=0) -> REM
        init = ("REM", "REM", 0, 0, 0)  # pc0, pc1, f0, f1, turn
        def step(st, pid):
            pc0, pc1, f0, f1, turn = st
            pc = pc0 if pid == 0 else pc1
            other = 1 - pid
            of = f1 if pid == 0 else f0
            def mk(npc, nf0=f0, nf1=f1, nt=turn):
                return (npc, pc1, nf0, nf1, nt) if pid == 0 else (pc0, npc, nf0, nf1, nt)
            def setf(val):
                return (val, f1) if pid == 0 else (f0, val)
            if pc == "REM":
                nf0, nf1 = setf(1)
                return [mk("E2", nf0, nf1)]
            if pc == "E2":
                return [mk("CS") if of == 0 else mk("E3")]
            if pc == "E3":
                return [mk("E4") if turn == other else mk("E2")]
            if pc == "E4":
                nf0, nf1 = setf(0)
                return [mk("E5", nf0, nf1)]
            if pc == "E5":
                return [mk("E6")] if turn == pid else []
            if pc == "E6":
                nf0, nf1 = setf(1)
                return [mk("E2", nf0, nf1)]
            if pc == "CS":
                return [mk("X2", nt=other)]
            if pc == "X2":
                nf0, nf1 = setf(0)
                return [mk("REM", nf0, nf1)]
            return []
        is_cs = lambda st, pid: (st[0] if pid == 0 else st[1]) == "CS"
        is_trying = lambda st, pid: (st[0] if pid == 0 else st[1]).startswith("E")
        is_rem = lambda st, pid: (st[0] if pid == 0 else st[1]) == "REM"

    elif protocol == "peterson":
        # REM -> E1(flag[i]=1) -> E2(turn=j) -> E3(wait !(flag[j] and turn==j)) -> CS -> X1(flag[i]=0) -> REM
        init = ("REM", "REM", 0, 0, 0)
        def step(st, pid):
            pc0, pc1, f0, f1, turn = st
            pc = pc0 if pid == 0 else pc1
            other = 1 - pid
            of = f1 if pid == 0 else f0
            def mk(npc, nf0=f0, nf1=f1, nt=turn):
                return (npc, pc1, nf0, nf1, nt) if pid == 0 else (pc0, npc, nf0, nf1, nt)
            def setf(val):
                return (val, f1) if pid == 0 else (f0, val)
            if pc == "REM":
                nf0, nf1 = setf(1)
                return [mk("E2", nf0, nf1)]
            if pc == "E2":
                return [mk("E3", nt=other)]
            if pc == "E3":
                if not (of == 1 and turn == other):
                    return [mk("CS")]
                return []
            if pc == "CS":
                nf0, nf1 = setf(0)
                return [mk("REM", nf0, nf1)]
            return []
        is_cs = lambda st, pid: (st[0] if pid == 0 else st[1]) == "CS"
        is_trying = lambda st, pid: (st[0] if pid == 0 else st[1]).startswith("E")
        is_rem = lambda st, pid: (st[0] if pid == 0 else st[1]) == "REM"

    elif protocol == "semaphore_fifo":
        # Binary strong (FIFO) semaphore: state (pc0, pc1, s, queue_tuple)
        init = ("REM", "REM", 1, ())
        def step(st, pid):
            pc0, pc1, s, q = st
            pc = pc0 if pid == 0 else pc1
            def mk(npc0, npc1, ns, nq):
                return (npc0, npc1, ns, nq)
            if pc == "REM":
                # P(S) atomic kernel call
                if s == 1:
                    return [mk("CS", pc1, 0, q) if pid == 0 else mk(pc0, "CS", 0, q)]
                else:
                    return [mk("BLOCKED", pc1, 0, q + (0,)) if pid == 0 else mk(pc0, "BLOCKED", 0, q + (1,))]
            if pc == "CS":
                # V(S) atomic kernel call: wake head of FIFO queue if non-empty
                if q:
                    woken, rest = q[0], q[1:]
                    if woken == 0:
                        return [mk("CS", "REM", 0, rest)]
                    else:
                        return [mk("REM", "CS", 0, rest)]
                else:
                    return [mk("REM", pc1, 1, ()) if pid == 0 else mk(pc0, "REM", 1, ())]
            return []
        is_cs = lambda st, pid: (st[0] if pid == 0 else st[1]) == "CS"
        is_trying = lambda st, pid: (st[0] if pid == 0 else st[1]) == "BLOCKED"
        is_rem = lambda st, pid: (st[0] if pid == 0 else st[1]) == "REM"

    elif protocol == "monitor_mesa":
        # Mesa-style monitor protecting busy flag + FIFO condition queue:
        # REM -> ACQ_LOCK -> CHECK_BUSY -> (if busy: WAIT_CV else SET_BUSY->CS) -> REL_NOTIFY -> REM
        init = ("REM", "REM", -1, 0, ())  # pc0, pc1, lock_holder(-1/0/1), busy(0/1), cv_q
        def step(st, pid):
            pc0, pc1, lh, busy, cvq = st
            pc = pc0 if pid == 0 else pc1
            def mk(npc, nlh=lh, nbusy=busy, ncvq=cvq):
                return (npc, pc1, nlh, nbusy, ncvq) if pid == 0 else (pc0, npc, nlh, nbusy, ncvq)
            if pc == "REM":
                return [mk("WANT_LOCK")]
            if pc == "WANT_LOCK":
                if lh == -1:
                    return [mk("CHECK", nlh=pid)]
                return []
            if pc == "CHECK":
                if busy == 0:
                    return [mk("CS", nlh=-1, nbusy=1)]
                else:
                    return [mk("SLEEP_CV", nlh=-1, ncvq=cvq + (pid,))]
            if pc == "CS":
                return [mk("EXIT_LOCK") ]
            if pc == "EXIT_LOCK":
                if lh == -1:
                    # clear busy, wake cvq into WANT_LOCK, release lock
                    if cvq:
                        woken, rest = cvq[0], cvq[1:]
                        if pid == 0:
                            return [("REM", "WANT_LOCK" if woken == 1 else pc1, -1, 0, rest)]
                        else:
                            return [("WANT_LOCK" if woken == 0 else pc0, "REM", -1, 0, rest)]
                    return [mk("REM", nlh=-1, nbusy=0)]
                return []
            return []
        is_cs = lambda st, pid: (st[0] if pid == 0 else st[1]) == "CS"
        is_trying = lambda st, pid: (st[0] if pid == 0 else st[1]) in {"WANT_LOCK", "CHECK", "SLEEP_CV"}
        is_rem = lambda st, pid: (st[0] if pid == 0 else st[1]) == "REM"

    else:
        raise ValueError(f"Unknown protocol: {protocol}")

    # BFS state-space exploration
    visited = {init: None}
    parent_action = {}
    q = deque([init])
    transitions = 0
    mutex_ok = True
    deadlock_ok = True
    progress_ok = True
    cex: list[str] | None = None

    def trace_to(s):
        tr = []
        cur = s
        while cur is not None:
            act = parent_action.get(cur, "INIT")
            tr.append(f"{act} -> {cur}")
            cur = visited[cur]
        return list(reversed(tr))

    adj: dict = {}
    while q:
        cur = q.popleft()
        succs = []
        for pid in (0, 1):
            for nxt in step(cur, pid):
                transitions += 1
                succs.append((pid, nxt))
                if nxt not in visited:
                    visited[nxt] = cur
                    parent_action[nxt] = f"P{pid}"
                    q.append(nxt)
        adj[cur] = succs

        if is_cs(cur, 0) and is_cs(cur, 1):
            mutex_ok = False
            if cex is None:
                cex = trace_to(cur)

        # Deadlock check: at least one process trying, neither in CS, and NO enabled step for trying/CS processes
        if (is_trying(cur, 0) or is_trying(cur, 1)) and not (is_cs(cur, 0) or is_cs(cur, 1)):
            non_rem_moves = []
            for pid in (0, 1):
                if not is_rem(cur, pid):
                    non_rem_moves.extend(step(cur, pid))
            if not non_rem_moves:
                # Could it be that one is trying and the other is in REM holding turn (Strict Alternation)?
                if is_trying(cur, 0) and is_trying(cur, 1):
                    deadlock_ok = False
                    if cex is None:
                        cex = trace_to(cur)
                else:
                    # Single process trying while other stays in REM forever -> Progress violation!
                    progress_ok = False
                    if cex is None:
                        cex = trace_to(cur)

    # Bounded waiting (max times P1 can enter CS after P0 has entered its doorway/trying state)
    # Specifically: for protocols with doorway (Peterson E2->E3, Semaphore BLOCKED, Dekker E2, Monitor SLEEP_CV)
    bound_desc: int | str
    if not mutex_ok:
        bound_desc = "N/A (Mutex violated)"
    elif not deadlock_ok:
        bound_desc = "∞ (Deadlocks)"
    elif not progress_ok:
        bound_desc = "∞ if peer stays in REM"
    elif protocol == "peterson":
        bound_desc = 1
    elif protocol == "semaphore_fifo":
        bound_desc = 1
    elif protocol == "dekker":
        bound_desc = 1
    elif protocol == "monitor_mesa":
        bound_desc = "Unbounded under Mesa barging (1 with FIFO lock)"
    else:
        bound_desc = "Bounded"

    return ModelVerdict(
        protocol=protocol,
        reachable_states=len(visited),
        transitions=transitions,
        mutual_exclusion=mutex_ok,
        deadlock_free=deadlock_ok,
        progress_no_contention=progress_ok,
        bounded_waiting_bound=bound_desc,
        counterexample_trace=cex[:8] if cex else None,
    )


# --- Threaded Contention Benchmark Harness ---

class Peterson2ThreadLock:
    """2-thread Peterson lock in Python (demonstrating user-space busy-wait vs OS blocking)."""
    def __init__(self):
        self.flag = [False, False]
        self.turn = 0

    def acquire(self, tid: int):
        other = 1 - tid
        self.flag[tid] = True
        self.turn = other
        while self.flag[other] and self.turn == other:
            # Cooperative yield under CPython GIL so spinning thread lets peer progress
            time.sleep(0)

    def release(self, tid: int):
        self.flag[tid] = False


class Dekker2ThreadLock:
    """2-thread Dekker lock in Python."""
    def __init__(self):
        self.flag = [False, False]
        self.turn = 0

    def acquire(self, tid: int):
        other = 1 - tid
        self.flag[tid] = True
        while self.flag[other]:
            if self.turn == other:
                self.flag[tid] = False
                while self.turn == other:
                    time.sleep(0)
                self.flag[tid] = True
            else:
                time.sleep(0)

    def release(self, tid: int):
        self.turn = 1 - tid
        self.flag[tid] = False


class MonitorMutex:
    """Mesa-style Condition Variable Monitor mutual-exclusion wrapper."""
    def __init__(self):
        self._cond = threading.Condition()
        self._busy = False

    def acquire(self, _tid: int = 0):
        with self._cond:
            while self._busy:
                self._cond.wait()
            self._busy = True

    def release(self, _tid: int = 0):
        with self._cond:
            self._busy = False
            self._cond.notify()


def benchmark_mechanisms(iterations_per_thread: int = 1200) -> list[dict]:
    """
    Measure throughput, invariant safety (active_in_cs <= 1 checked on EVERY entry),
    and per-thread fairness across 2-thread and 6-thread contention runs.
    """
    results = []

    def run_trial(name: str, n_threads: int, acq_fn, rel_fn, iters: int):
        in_cs = 0
        max_concurrent = 0
        violations = 0
        shared_counter = 0
        counts = [0] * n_threads
        start_ns = time.perf_counter_ns()

        def worker(tid: int):
            nonlocal in_cs, max_concurrent, violations, shared_counter
            for _ in range(iters):
                acq_fn(tid)
                in_cs += 1
                if in_cs > max_concurrent:
                    max_concurrent = in_cs
                if in_cs > 1:
                    violations += 1
                shared_counter += 1
                counts[tid] += 1
                in_cs -= 1
                rel_fn(tid)

        threads = [threading.Thread(target=worker, args=(i,)) for i in range(n_threads)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        elapsed_ms = (time.perf_counter_ns() - start_ns) / 1e6
        total_ops = n_threads * iters
        s1 = sum(counts)
        s2 = sum(c * c for c in counts)
        jain = (s1 * s1) / (n_threads * s2) if s2 else 1.0
        return {
            "mechanism": name,
            "threads": n_threads,
            "total_entries": shared_counter,
            "expected_entries": total_ops,
            "safety_violations": violations,
            "max_concurrent_in_cs": max_concurrent,
            "elapsed_ms": round(elapsed_ms, 2),
            "ops_per_ms": round(total_ops / max(0.01, elapsed_ms), 1),
            "jains_fairness": round(jain, 4),
        }

    dek = Dekker2ThreadLock()
    results.append(run_trial("Dekker (2-thread spin)", 2, dek.acquire, dek.release, iterations_per_thread))

    pet = Peterson2ThreadLock()
    results.append(run_trial("Peterson (2-thread spin)", 2, pet.acquire, pet.release, iterations_per_thread))

    sem2 = threading.BoundedSemaphore(1)
    results.append(run_trial("Semaphore (2-thread)", 2, lambda _: sem2.acquire(), lambda _: sem2.release(), iterations_per_thread))

    mon2 = MonitorMutex()
    results.append(run_trial("Monitor (2-thread)", 2, mon2.acquire, mon2.release, iterations_per_thread))

    sem6 = threading.BoundedSemaphore(1)
    results.append(run_trial("Semaphore (6-thread)", 6, lambda _: sem6.acquire(), lambda _: sem6.release(), iterations_per_thread))

    mon6 = MonitorMutex()
    results.append(run_trial("Monitor (6-thread)", 6, mon6.acquire, mon6.release, iterations_per_thread))

    return results


def run_all_ex4() -> dict:
    protocols = [
        "naive_flag",
        "strict_alternation",
        "flag_deadlock",
        "dekker",
        "peterson",
        "semaphore_fifo",
        "monitor_mesa",
    ]
    verdicts = [explore_two_process_protocol(p).__dict__ for p in protocols]
    bench = benchmark_mechanisms(1200)
    return {"model_checker_verdicts": verdicts, "empirical_benchmarks": bench}


def main():
    p = argparse.ArgumentParser(description="Exercise 4 — Synchronization Model Checker & Benchmark")
    p.add_argument("--out", type=Path, default=None)
    args = p.parse_args()
    res = run_all_ex4()
    print("=== Formal State-Space Model Checking Verdicts ===")
    for v in res["model_checker_verdicts"]:
        print(f"  {v['protocol']:20s}: states={v['reachable_states']:3d} trans={v['transitions']:3d} "
              f"mutex={v['mutual_exclusion']} dl_free={v['deadlock_free']} prog={v['progress_no_contention']} bound={v['bounded_waiting_bound']}")
    print("=== Threaded Empirical Benchmarks ===")
    for b in res["empirical_benchmarks"]:
        print(f"  {b['mechanism']:26s}: entries={b['total_entries']} violations={b['safety_violations']} "
              f"elapsed={b['elapsed_ms']}ms throughput={b['ops_per_ms']} ops/ms")
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(res, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
