# Project Index — WRR Repository

> Repository: https://github.com/Mmdvahedi2005/WRR
> Main branch: `main`
> Last audit: 2026-11-15 — all 7 exercises complete and pushed

This file is the single entry point for all seven exercises.
Each exercise has its own branch. Do not merge exercise branches into `main`
without explicit approval.

## Exercises

| # | Exercise | Branch | Status | Entry point |
|---|----------|--------|--------|-------------|
| 1 | Exercise 1 — WRR Algorithm Introduction | `Exercise-1-WRR` | ✅ Complete — code, tests, figures, docs, bilingual reports | `README.md` on branch |
| 2 | Exercise 2 — WRR vs EDF vs RM Comparison | `Exercise-2-WRR` | ✅ Complete — simulator, Monte Carlo, figures, bilingual reports | `README.md` on branch |
| 3 | Exercise 3 — Manual EDF & RM Scheduling | `Exercise-3-WRR` | ✅ Complete — RTA solver, hand-worked worksheet, bilingual reports | `README.md` on branch |
| 4 | Exercise 4 — Dekker, Peterson, Semaphore, Monitor | `Exercise-4-WRR` | ✅ Complete — model checker, threaded benchmarks, bilingual reports | `README.md` on branch |
| 5 | Exercise 5 — WRR Synchronization (Semaphore / Monitor / Both) | `Exercise-5-WRR` | ✅ Complete — exercise5_wrr.py, 9 tests, DispatchGuard, bilingual reports | `README_Exercise5_WRR.md` + `docs/README.md` on branch |
| 6 | Exercise 6 — Video Presentation (>2 min) | `Exercise-6-WRR` | ✅ Complete — 150s storyboard, animated GIF, keyframes, narration | `README.md` on branch |
| 7 | Exercise 7 — Research Paper & Seminar | `Exercise-7-WRR` | ✅ Complete — PAPER EN/FA, SEMINAR EN/FA.pptx, REFERENCES.md | `README.md` on branch |

## Branch links

- Exercise 1: https://github.com/Mmdvahedi2005/WRR/tree/Exercise-1-WRR
- Exercise 2: https://github.com/Mmdvahedi2005/WRR/tree/Exercise-2-WRR
- Exercise 3: https://github.com/Mmdvahedi2005/WRR/tree/Exercise-3-WRR
- Exercise 4: https://github.com/Mmdvahedi2005/WRR/tree/Exercise-4-WRR
- Exercise 5: https://github.com/Mmdvahedi2005/WRR/tree/Exercise-5-WRR
- Exercise 6: https://github.com/Mmdvahedi2005/WRR/tree/Exercise-6-WRR
- Exercise 7: https://github.com/Mmdvahedi2005/WRR/tree/Exercise-7-WRR

> All branches are live on GitHub (pushed and verified 2026-11-15).

## Base project (on `main`)

- Interactive OS-process scheduler: `WRR.py`
- Deterministic simulation (Exercise 5): `exercise5_wrr.py`
- Tests: `test_exercise5_wrr.py` (9 tests, all passing)
- Figures: generated from real `schedule()` output

## How to use this index

1. Pick an exercise row above.
2. Check out its branch: `git checkout Exercise-5-WRR`
3. Read `README.md` / `README_Exercise5_WRR.md` and `docs/README.md` on that branch.
4. Run tests: `python -m unittest -v`
5. View bilingual reports: `report_EXN_en.{md,docx,pdf}` / `report_EXN_fa.{md,docx,pdf}`
