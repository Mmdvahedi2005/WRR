# Project Progress — WRR Upgrade

> Repository: https://github.com/Mmdvahedi2005/WRR
> Updated: 2026-11-15

## Audit findings (original `main` @ `44870fd`)

- Only **one branch** existed: `main`. No exercise branches.
- Only **one exercise** existed: **Exercise 5** (`exercise5_wrr.py`,
  `test_exercise5_wrr.py`, `README_Exercise5_WRR.md`,
  `SAMPLE_RUN_Exercise5_WRR.txt`, `TEST_RESULTS_Exercise5_WRR.txt`).
  Exercises 1–4 and 6–7 were **not found** in the repository.
- Base project: `WRR.py` (interactive `psutil` scheduler, no automated tests).
- `README.md` referenced two images (`wrr_readme_assets/wrr_gantt.png`,
  `wrr_readme_assets/wrr_cpu_share.png`) that **did not exist**
  (`wrr_readme_assets` was a 1-byte file, not a directory) — broken images.
- `assets/wrr_sync_comparison.svg` existed but was not referenced anywhere.
- No `docs/`, no PDF/Word reports, no `requirements.txt`.
- Verified by execution: `python -m unittest -v` → **9/9 PASS**;
  `python exercise5_wrr.py --mode all --quantum 1` output matches
  `SAMPLE_RUN_Exercise5_WRR.txt` exactly (makespan 12).

## What was done and pushed (all branches in sync with origin)

### `main`

- [x] Generated `docs/figures/wrr_gantt.png` and `docs/figures/wrr_cpu_share.png`
      from real `exercise5_wrr.schedule()` output via `tools_generate_figures.py`.
- [x] Fixed broken image paths in `README.md`; added figure captions,
      project structure, documentation links, and conclusion.
- [x] Removed blocking 1-byte file `wrr_readme_assets`.
- [x] Added `requirements.txt`, `.gitignore`, `PROJECT_INDEX.md`,
      `PROJECT_PROGRESS.md` (this file), `docs/README.md`.
- [x] Pushed `main` to GitHub on 2026-11-15 (commit `ef65502`).

### `Exercise-5-WRR` (from `main`)

- [x] Full upgrade: bilingual docs, `docs/README.md`, `docs/reports/`
      (`report_fa.md`, `report_en.md`), `docs/references/`,
      `docs/figures/` (architecture, flowchart, metrics, sync comparison),
      `outputs/` with generated Gantt SVGs.
- [x] Tests re-run: 9/9 PASS.
- [x] Pushed `Exercise-5-WRR` to GitHub on 2026-11-15 (commit `5fcc7c7`).

### `Exercise-1-WRR`, `Exercise-2-WRR`, `Exercise-3-WRR`,
### `Exercise-4-WRR`, `Exercise-6-WRR`, `Exercise-7-WRR`

- [x] Placeholder branches created with `README.md` stating the exercise
      was not found in the original repository and is awaiting user files.
      No code, numbers, or results were fabricated.
- [x] Pushed all six placeholder branches to GitHub on 2026-11-15.

## Remaining work

1. ~~Push all branches~~ — done 2026-11-15; verified `local == origin` for every branch.
2. When user provides files for Exercises 1–4 and 6–7, upgrade each branch
   the same way as Exercise 5 (README, docs, figures from real data, tests).
3. Optional: produce `.docx`/`.pdf` versions of reports from
   `docs/reports/*.md` once content is approved.

## Push status (completed 2026-11-15)

All branches were pushed by the repository owner's fine-grained PAT and
verified in sync (`git ls-remote` matched local tips one-to-one):

- `main` -> `ef65502`
- `Exercise-5-WRR` -> `5fcc7c7`
- `Exercise-1-WRR` -> `10575bd` · `Exercise-2-WRR` -> `feffe2c`
- `Exercise-3-WRR` -> `4fce0e3` · `Exercise-4-WRR` -> `39c3a88`
- `Exercise-6-WRR` -> `cb114a2` · `Exercise-7-WRR` -> `34b4e77`

A full mirror also exists in `WRR-upgrade.bundle` (kept in the workspace
of the working machine) as an offline backup of all branch tips.

Note: the fine-grained token used for the push was shared in a chat and
should be revoked and replaced by the owner (it was granted
`Contents: Read and write` on this repository only).

Do **not** merge exercise branches into `main` without review.

## Resume note

If work resumes later, read this file first, then `PROJECT_INDEX.md`,
and continue from the unchecked items above. Do not redo completed work.
