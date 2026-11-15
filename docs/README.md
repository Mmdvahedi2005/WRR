# Exercise 6 — Video Presentation Package

## 1. Overview
Video presentation package comparing WRR vs EDF vs RM. 6 scenes totaling 150 seconds (02:30) — exceeds the 2-minute course requirement. Includes animated GIF demo, storyboard SVG, keyframe composite, and narration script.

## 2. Problem Statement
Create a >2-minute video presentation on WRR specifications and comparison with EDF and RM, suitable for course submission.

## 3. Scientific Background
Video presentations require a storyboard with timed scenes, visual demonstrations, and a clear narrative arc. This package provides all pre-production assets plus a rendered animated GIF demo.

## 4. Methodology
6-scene storyboard (`video_storyboard_sim.py`) with timed scenes: Intro → WRR → EDF → RM → Comparison → Conclusion. Animated GIF generated from simulation traces. Keyframe composite for slide extraction.

## 5. Implementation Details
Python script generating storyboard timing, simulation traces for high-util and overload cases, and Pillow multi-frame animated GIF (`wrr_vs_edf_rm_demo.gif`).

## 6. Experimental Setup
Run `python3 src/video_storyboard_sim.py` for storyboard and simulation output. View `outputs/wrr_vs_edf_rm_demo.gif` for the animated demo.

## 7. Results & Analysis
150 seconds / 6 scenes. GIF demo shows WRR vs EDF vs RM execution traces under different utilization conditions. Keyframe composite PNG for slide extraction.

## 8. Figures & Visualizations
2 SVG (`video_storyboard_timeline.svg`, `video_decision_guide.svg`) + 1 PNG (`video_keyframes_composite.png`) + 1 GIF (`wrr_vs_edf_rm_demo.gif`).

## 9. Testing
1 unit test — passing. Verifies storyboard scene count and total duration ≥ 120 seconds.

## 10. Conclusion & References
The video package exceeds the 2-minute requirement with 150 seconds of content across 6 scenes. Narration script provided as text; recorded voiceover requires external audio tooling. See `report_EX6_en.md` / `report_EX6_fa.md`.

---

**Source:** `src/` directory | **Tests:** `tests/` directory | **Figures:** `docs/figures/`
**Reports:** `report_EX6_en.md`, `.docx`, `.pdf` and `report_EX6_fa.md`, `.docx`, `.pdf`
