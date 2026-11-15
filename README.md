# WRR Process Scheduler — Academic Repository (7 Exercises)

A Python-based **Weighted Round Robin (WRR)** process scheduler and complete
Operating Systems course project covering **7 exercises across 7 independent
GitHub branches**, all with real executable code, verified unit tests,
custom academic figures, and bilingual reports (English & Persian).

> **Repository:** https://github.com/Mmdvahedi2005/WRR
> **Main branch:** `main` | **Branches:** `Exercise-1-WRR` … `Exercise-7-WRR`
> **Do not merge exercise branches into `main` without explicit permission.**

---

## Course Assignment Coverage

| # | Course Item | Branch | Deliverables |
|---|-------------|--------|-------------|
| 1 | Complete WRR introduction (~40 pp, EN & FA) | `Exercise-1-WRR` | `wrr_scheduler.py`, 10 tests, 2 SVG + 3 PNG, bilingual MD/DOCX/PDF |
| 2 | WRR vs EDF vs RM comparison (~40+ pp) | `Exercise-2-WRR` | `compare_schedulers.py`, 6 tests, Monte Carlo (400 sets), 2 SVG + 3 PNG |
| 3 | Manual EDF & RM, 3 processes on paper | `Exercise-3-WRR` | `manual_edf_rm.py`, 3 tests, hand-worked worksheet, 2 SVG + 3 PNG |
| 4 | Dekker, Peterson, Semaphore, Monitor (~40+ pp) | `Exercise-4-WRR` | `sync_verifier.py` model checker, 3 tests, 2 SVG + 2 PNG |
| 5 | WRR Synchronization (Semaphore/Monitor/Both) | `Exercise-5-WRR` | `exercise5_wrr.py`, 9 tests, DispatchGuard, 2 SVG + 2 PNG |
| 6 | Video clip > 2 min (WRR vs EDF vs RM) | `Exercise-6-WRR` | `video_storyboard_sim.py`, 150s/6 scenes, animated GIF, storyboard |
| 7 | Research Paper & Seminar | `Exercise-7-WRR` | `seminar_synthesis.py`, PAPER EN/FA, SEMINAR EN/FA.pptx, REFERENCES.md |

---

## Base Project (`main` branch)

The script in [`WRR.py`](./WRR.py) is an interactive OS-process WRR scheduler
that launches external programs via `subprocess` and `psutil`, allocates
execution time by user-defined weights, and prints CPU time, elapsed runtime,
and return codes.

[`exercise5_wrr.py`](./exercise5_wrr.py) is a deterministic WRR simulation
with `DispatchGuard` synchronization (`semaphore`, `monitor`, `both`),
9 unit tests, and verified sample output.

---

## WRR vs. EDF vs. RM

These algorithms answer different scheduling questions. Results below come
from real simulation execution (Exercise 2 branch), not fabricated numbers.

| Property | WRR | EDF | RM |
|---|-----|-----|-----|
| Selection rule | Weighted turns / slices | Earliest absolute deadline | Fixed priority by period |
| Priority type | Weight-based service | Dynamic | Fixed |
| Periods required? | No | Usually yes | Yes |
| Deadlines required? | No | Yes | Evaluated (D=T typically) |
| Schedulability (U≤0.65) | 100% | 100% | 100% |
| Schedulability (U≈0.96) | 17.5% | 100% | 27.5% |
| Starvation under overload | No (proportional shares) | Domino cascade possible | Low-priority starved |

See **Exercise-2-WRR** branch for full Monte Carlo data (400 task sets,
seed=20261115).

---

## Project structure

```text
WRR/
├── README.md                      # This file (base WRR project)
├── PROJECT_INDEX.md               # Index of all 7 exercises and branches
├── PROJECT_PROGRESS.md            # Upgrade status and completion log
├── WRR.py                         # Interactive OS-process WRR scheduler (psutil)
├── exercise5_wrr.py               # Exercise 5: deterministic WRR + sync variants
├── test_exercise5_wrr.py          # Unit tests for Exercise 5 (9 tests)
├── README_Exercise5_WRR.md        # Exercise 5 overview
├── SAMPLE_RUN_Exercise5_WRR.txt   # Verified sample output
├── TEST_RESULTS_Exercise5_WRR.txt # Verified test report
├── tools_generate_figures.py      # Regenerates figures from real schedule() output
├── requirements.txt               # Python dependencies
├── assets/
│   └── wrr_sync_comparison.svg    # Sync-variant comparison diagram
├── docs/
│   ├── README.md                  # Documentation guide
│   ├── figures/                   # Generated figures (PNG/SVG)
│   ├── reports/                   # Academic reports (FA/EN)
│   └── references/                # References
└── outputs/                       # Generated Gantt SVGs from exercise5 runs
```

### Per-exercise branch structure

Each `Exercise-N-WRR` branch contains:

```text
src/           # Executable Python source (real simulation, no fake data)
tests/         # Unit tests (all verified passing)
docs/figures/  # 2–4+ custom SVG + PNG figures (unified academic style)
docs/README.md # 10-section documentation guide
README.md      # Branch root: problem, explanation, figures, usage, tests
report_EXN_en.{md,docx,pdf}   # Bilingual academic report (English)
report_EXN_fa.{md,docx,pdf}   # Bilingual academic report (Persian)
```

---

## Documentation

- **Project index (all exercises):** [PROJECT_INDEX.md](./PROJECT_INDEX.md)
- **Project progress:** [PROJECT_PROGRESS.md](./PROJECT_PROGRESS.md)
- **Documentation guide:** [docs/README.md](./docs/README.md)
- **Exercise 5 overview:** [README_Exercise5_WRR.md](./README_Exercise5_WRR.md)
- **Per-exercise docs:** `docs/README.md` on each `Exercise-N-WRR` branch

---

## Verification

All results, tables, and charts are backed by real code execution:

- **Exercise 1:** `python3 src/wrr_scheduler.py` → 4 scenarios, 10 tests pass
- **Exercise 2:** `python3 src/compare_schedulers.py` → 4 workloads + Monte Carlo, 6 tests pass
- **Exercise 3:** `python3 src/manual_edf_rm.py` → Case A & B RTA, 3 tests pass
- **Exercise 4:** `python3 src/sync_verifier.py` → 7 protocols model-checked, 3 tests pass
- **Exercise 5:** `python3 exercise5_wrr.py --mode all` → 3 modes identical, 9 tests pass
- **Exercise 6:** `python3 src/video_storyboard_sim.py` → 150s storyboard, 1 test pass
- **Exercise 7:** `python3 src/seminar_synthesis.py` → cross-exercise synthesis, 1 test pass

Run all Exercise 5 tests: `python3 -m unittest test_exercise5_wrr.py -v`

---

## Requirements

- Python 3.8+ (recommended)
- `psutil` (for WRR.py)
- `reportlab`, `python-pptx`, `arabic-reshaper`, `python-bidi`, `pypdf` (for report generation)

```bash
python -m pip install psutil reportlab python-pptx arabic-reshaper python-bidi pypdf
```

---

## Run

```bash
git clone https://github.com/Mmdvahedi2005/WRR.git
cd WRR
python -m pip install -r requirements.txt
python WRR.py
```

Then follow the prompts. See each exercise branch README for experiment commands.

---

## Conclusion

This repository provides a complete, executable, scientifically accurate
OS course project with 7 exercises on independent branches. All numerical
claims are backed by real simulation/test execution. Bilingual reports
(Markdown, DOCX, PDF) are provided in English and Persian. No exercise
branches are merged into `main`.

---

**Author:** Mmdvahedi2005  
**Repository:** https://github.com/Mmdvahedi2005/WRR  
**Last updated:** 2026-11-15
