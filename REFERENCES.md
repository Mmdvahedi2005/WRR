# References — WRR Academic Repository

## Primary Sources

1. **Liu, C. L., & Layland, J. W.** (1973). Scheduling algorithms for multiprogramming in a hard-real-time environment. *Journal of the ACM*, 20(1), 46–61. — Rate Monotonic optimality and utilization bound.

2. **Dertouzos, M. L.** (1974). Control robotics: The probabilistic scheduling of jobs with deadlines. *Proceedings of the IFAC*. — Earliest Deadline Foundations.

3. **Dekker, T. J.** (1960). A simple algorithm for mutual exclusion. *Communications of the ACM*.

4. **Peterson, G. L.** (1981). Myths about the mutual exclusion problem. *Information Processing Letters*, 12(3), 115–116.

5. **Lamport, L.** (1986). On interprocess communication. *Distributed Computing*, 1(2), 86–101. — Monitor semantics.

6. **Jain, R.** (1990). *The Art of Computer Systems Performance Analysis*. Wiley. — Jain's fairness index.

## Exercise-Specific References

### Exercise 1 — WRR Algorithm Introduction
- Classical Weighted Round Robin scheduling as implemented in network schedulers (e.g., Deficit Round Robin, WRR in Linux `sch_wrr`).
- Interleaved WRR variant for reduced response time of low-weight flows.

### Exercise 2 — WRR vs EDF vs RM
- Liu & Layland (1973) utilization bound: U_LL(n) = n(2^(1/n) − 1).
- Response-Time Analysis (RTA) for fixed-priority scheduling.
- Monte Carlo schedulability evaluation methodology.

### Exercise 3 — Manual EDF & RM Scheduling
- Hyperperiod computation: H = lcm(T₁, T₂, T₃).
- Fixed-priority response-time iteration: Rᵢ⁽ᵏ⁺¹⁾ = Cᵢ + Σⱼ₍ₚᵣᵢₒᵣ(j)₎ ceil(Rᵢ⁽ᵏ⁾ / Tⱼ) · Cⱼ.
- Earliest Deadline First: dynamic-priority optimal scheduler.

### Exercise 4 — Synchronization Primitives
- Exhaustive explicit-state model checking (BFS) for mutual exclusion protocols.
- Mesa-style monitors with condition variables and barging.
- Semaphore FIFO ordering guarantees.

### Exercise 5 — WRR Synchronization
- DispatchGuard pattern: unified guard wrapping semaphore and/or monitor.
- Deterministic WRR simulation with synchronization-equivalence verification.

### Exercise 6 — Video Presentation
- Storyboard-based video production for technical presentations.
- 6-scene narrative structure: Introduction → WRR → EDF → RM → Comparison → Conclusion.

### Exercise 7 — Research Paper & Seminar
- Cross-exercise evidence aggregation methodology.
- Readers-Writers problem: comparison across Semaphore, Monitor, Dekker, Peterson.
- Academic report formats: Markdown, DOCX (OOXML), PDF (ReportLab).

## Repository References

- **Source repository**: https://github.com/Mmdvahedi2005/WRR
- **Course structure reference**: kaspian021/Multilevel-Queue-Scheduling (same curriculum, PR #1 author)
- **7-branch curriculum**: Exercise-1-WRR through Exercise-7-WRR on independent branches
