# Documentation Guide — WRR

This folder collects all documentation for the WRR repository.
Start here, then follow the links below.

## Contents

- [Figures](./figures/) — generated diagrams and charts
  - `wrr_gantt.png` — Gantt chart from real `schedule()` output
    (P1 w=3/b=5, P2 w=2/b=4, P3 w=1/b=3, quantum=1, makespan=12).
    Read it left-to-right: each block is one quantum; taller weight means
    more consecutive blocks per round.
  - `wrr_cpu_share.png` — idealized weight share vs actual burst share.
    Blue = `w_i / Σw`, orange = `burst_i / Σburst`. Use it to see why
    weight proportions are expectations, not guarantees, with finite bursts.
- [Reports](./reports/) — academic reports
  - `report_en.md` — English report (Exercise 5 + base project).
  - `report_fa.md` — Persian report (گزارش فارسی).
- [References](./references/) — bibliography and further reading.

## How figures are produced

All PNG figures are generated from the real scheduler code, not drawn by hand:

```bash
python tools_generate_figures.py
```

The script imports `exercise5_wrr.schedule()`, runs the default workload,
and writes the PNGs above. If you change the workload in the script,
re-run it so figures and code stay consistent.

## How to run and test

```bash
python -m pip install -r requirements.txt
python exercise5_wrr.py --mode all --quantum 1   # simulation + Gantt SVGs
python -m unittest -v                            # 9 tests
python WRR.py                                    # interactive OS scheduler
```

Generated Gantt SVGs are written to the current directory by default
(`wrr-gantt-<mode>.svg`); copy them to `outputs/` for archiving.

## File map

| Path | Purpose |
|------|---------|
| `../README.md` | Base project overview (WRR.py) |
| `../PROJECT_INDEX.md` | Index of all 7 exercises and branches |
| `../PROJECT_PROGRESS.md` | Upgrade status and remaining work |
| `../README_Exercise5_WRR.md` | Exercise 5 overview |
| `../exercise5_wrr.py` | Deterministic WRR simulation |
| `../test_exercise5_wrr.py` | Unit tests (9 tests) |
| `../WRR.py` | Interactive OS-process scheduler |
| `../tools_generate_figures.py` | Figure generation from real output |
| `../assets/wrr_sync_comparison.svg` | Sync-variant comparison diagram |
