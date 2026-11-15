import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from video_storyboard_sim import generate_storyboard_data


class TestVideoStoryboard(unittest.TestCase):
    def test_duration_exceeds_two_minutes(self):
        d = generate_storyboard_data()
        self.assertGreater(d["total_duration_seconds"], 120)
        self.assertEqual(d["total_scenes"], 6)
        self.assertEqual(d["high_util_race"]["EDF"]["deadline_misses_count"], 0)
        self.assertGreater(d["overload_race"]["WRR"]["per_task"]["P3"]["cpu_share_pct"], 0.0)


if __name__ == "__main__":
    unittest.main()
