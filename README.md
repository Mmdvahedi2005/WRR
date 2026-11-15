# Exercise 7 — Research Paper & Seminar

## Problem / Goal
Synthesize Exercises 1–5 into research paper and seminar with bilingual support.

## Scientific Explanation
Cross-exercise evidence aggregation integrating WRR, EDF/RM, manual scheduling, synchronization, and WRR sync.

## Algorithm / Methodology
Evidence collector importing Ex 1–5 modules. Bilingual report generation (MD, DOCX, PDF).

## Implementation
Python `seminar_synthesis.py` + doc engine + python-pptx decks.

## Custom Figures
- docs/figures/research_synthesis_pipeline.svg — synthesis pipeline
- docs/figures/scheduling_sync_taxonomy.svg — scheduling/sync taxonomy
- docs/figures/synthesis_headline_findings.png — headline results

## Usage Guide
View PAPER_EN.md / PAPER_FA.md. Open SEMINAR_WRR_EN.pptx / SEMINAR_WRR_FA.pptx. Read REFERENCES.md.

## Sample I/O
PAPER_EN: ~40 pages equivalent. SEMINAR_EN: 8 slides. REFERENCES.md with Liu-Layland, Dekker, Peterson, Lamport, Jain.

## Test Commands
```
python3 -m unittest tests/test_seminar_synthesis.py -v
```

## Directory Tree
src/seminar_synthesis.py
tests/test_seminar_synthesis.py
docs/figures/*.svg, *.png
PAPER_EN.{md,docx,pdf}
PAPER_FA.{md,docx,pdf}
SEMINAR_WRR_EN.pptx
SEMINAR_WRR_FA.pptx
REFERENCES.md
report_EX7_en.{md,docx,pdf}
report_EX7_fa.{md,docx,pdf}

## Conclusion
Complete academic synthesis with bilingual paper, seminar decks, and references. All claims backed by real code.

---

**Reports:** `report_EX7_en.{md,docx,pdf}` and `report_EX7_fa.{md,docx,pdf}`
**Branch:** `Exercise-7-WRR` | **Preserves:** `WRR.py` and `exercise5_wrr.py` where applicable
