# Exercise 6 — Video Presentation Package

## Problem / Goal
Create >2-minute video presentation on WRR vs EDF vs RM.

## Scientific Explanation
Video presentations need storyboard, timed scenes, visual demo, and narration script.

## Algorithm / Methodology
6-scene storyboard (150s), animated GIF from simulation traces, keyframe composite, narration text.

## Implementation
Python `video_storyboard_sim.py` + Pillow animated GIF.

## Custom Figures
- docs/figures/video_storyboard_timeline.svg — 6-scene timeline
- docs/figures/video_decision_guide.svg — decision guide
- docs/figures/video_keyframes_composite.png — keyframes
- outputs/wrr_vs_edf_rm_demo.gif — animated demo (150s)

## Usage Guide
Run `python3 src/video_storyboard_sim.py`. View `outputs/wrr_vs_edf_rm_demo.gif`.

## Sample I/O
6 scenes × 150s total. Scene 1: WRR intro, Scene 2: WRR in action, Scene 3: EDF, Scene 4: RM, Scene 5: Comparison, Scene 6: Conclusion.

## Test Commands
```
python3 -m unittest tests/test_video_storyboard.py -v
```

## Directory Tree
src/video_storyboard_sim.py
tests/test_video_storyboard.py
docs/figures/*.svg, *.png
outputs/wrr_vs_edf_rm_demo.gif
report_EX6_en.{md,docx,pdf}
report_EX6_fa.{md,docx,pdf}

## Conclusion
150-second video package exceeds 2-minute requirement. Narration script provided; voiceover recording needs external audio tooling.

---

**Reports:** `report_EX6_en.{md,docx,pdf}` and `report_EX6_fa.{md,docx,pdf}`
**Branch:** `Exercise-6-WRR` | **Preserves:** `WRR.py` and `exercise5_wrr.py` where applicable
