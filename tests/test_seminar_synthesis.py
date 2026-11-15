import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from seminar_synthesis import collect_unified_evidence


class TestSeminarSynthesis(unittest.TestCase):
    def test_evidence_cross_branch_consistency(self):
        ev = collect_unified_evidence()
        self.assertEqual(ev["ex1_wrr"]["S1_classic_makespan"], 12)
        self.assertEqual(ev["ex5_wrr_sync"]["semaphore"]["makespan"], 12)
        self.assertEqual(ev["ex3_manual_3proc"]["caseB_edf_misses"], [])
        self.assertEqual(len(ev["ex3_manual_3proc"]["caseB_rm_misses"]), 1)


if __name__ == "__main__":
    unittest.main()
