# Project Index — WRR Repository

> Repository: https://github.com/Mmdvahedi2005/WRR
> Main branch: `main`
> Last audit: 2026-11-15 (against commit `44870fd` on `main`)

This file is the single entry point for all seven exercises.
Each exercise has its own branch. Do not merge exercise branches into `main`
without explicit approval.

## Exercises

| # | Exercise | Branch | Status | Entry point |
|---|----------|--------|--------|-------------|
| 1 | Exercise 1 — WRR | `Exercise-1-WRR` | ⚠️ Not found in original repo — placeholder branch created, awaiting user files | `README.md` on branch |
| 2 | Exercise 2 — WRR | `Exercise-2-WRR` | ⚠️ Not found in original repo — placeholder branch created, awaiting user files | `README.md` on branch |
| 3 | Exercise 3 — WRR | `Exercise-3-WRR` | ⚠️ Not found in original repo — placeholder branch created, awaiting user files | `README.md` on branch |
| 4 | Exercise 4 — WRR | `Exercise-4-WRR` | ⚠️ Not found in original repo — placeholder branch created, awaiting user files | `README.md` on branch |
| 5 | Exercise 5 — WRR with Synchronization (Semaphore / Monitor / Both) | `Exercise-5-WRR` | ✅ Found in repo and upgraded (local, pending push) | `README_Exercise5_WRR.md` + `docs/README.md` on branch |
| 6 | Exercise 6 — WRR | `Exercise-6-WRR` | ⚠️ Not found in original repo — placeholder branch created, awaiting user files | `README.md` on branch |
| 7 | Exercise 7 — WRR | `Exercise-7-WRR` | ⚠️ Not found in original repo — placeholder branch created, awaiting user files | `README.md` on branch |

## Branch links (after push)

- Exercise 1: https://github.com/Mmdvahedi2005/WRR/tree/Exercise-1-WRR
- Exercise 2: https://github.com/Mmdvahedi2005/WRR/tree/Exercise-2-WRR
- Exercise 3: https://github.com/Mmdvahedi2005/WRR/tree/Exercise-3-WRR
- Exercise 4: https://github.com/Mmdvahedi2005/WRR/tree/Exercise-4-WRR
- Exercise 5: https://github.com/Mmdvahedi2005/WRR/tree/Exercise-5-WRR
- Exercise 6: https://github.com/Mmdvahedi2005/WRR/tree/Exercise-6-WRR
- Exercise 7: https://github.com/Mmdvahedi2005/WRR/tree/Exercise-7-WRR

> Note: these links return 404 until the branches are pushed to GitHub.
> See `PROJECT_PROGRESS.md` for push instructions.

## Base project (on `main`)

- Interactive OS-process scheduler: `WRR.py`
- Deterministic simulation (Exercise 5): `exercise5_wrr.py`
- Tests: `test_exercise5_wrr.py` (9 tests, all passing)
- Figures: `docs/figures/wrr_gantt.png`, `docs/figures/wrr_cpu_share.png`
  (generated from real `schedule()` output by `tools_generate_figures.py`)

## How to use this index

1. Pick an exercise row above.
2. Check out its branch: `git checkout Exercise-5-WRR`
3. Read `README.md` / `README_Exercise5_WRR.md` and `docs/README.md` on that branch.
4. Run tests: `python -m unittest -v`
5. Regenerate figures: `python tools_generate_figures.py`
