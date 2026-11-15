import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from wrr_scheduler import WRRTaskSpec, simulate_wrr, jains_fairness_index, theoretical_max_wait_bound, run_all_scenarios


class TestWRRScheduler(unittest.TestCase):
    def test_baseline_matches_exercise5_exact(self):
        specs = [WRRTaskSpec("P1", 3, 5), WRRTaskSpec("P2", 2, 4), WRRTaskSpec("P3", 1, 3)]
        res = simulate_wrr(specs, quantum=1, variant="classic")
        self.assertEqual(res["makespan"], 12)
        self.assertEqual(res["metrics"]["P1"]["completion"], 8)
        self.assertEqual(res["metrics"]["P2"]["completion"], 10)
        self.assertEqual(res["metrics"]["P3"]["completion"], 12)
        self.assertEqual(res["metrics"]["P1"]["waiting"], 3)
        self.assertEqual(res["metrics"]["P2"]["waiting"], 6)
        self.assertEqual(res["metrics"]["P3"]["waiting"], 9)

    def test_interleaved_reduces_first_response(self):
        specs = [WRRTaskSpec("Heavy", 8, 16), WRRTaskSpec("Light1", 1, 2), WRRTaskSpec("Light2", 1, 2)]
        c = simulate_wrr(specs, quantum=1, variant="classic")
        i = simulate_wrr(specs, quantum=1, variant="interleaved")
        self.assertEqual(c["makespan"], i["makespan"])
        self.assertEqual(c["metrics"]["Light1"]["response"], 8)
        self.assertEqual(i["metrics"]["Light1"]["response"], 1)
        self.assertLess(i["avg_response"], c["avg_response"])

    def test_backlogged_proportional_shares(self):
        specs = [WRRTaskSpec("P1", 3, 18), WRRTaskSpec("P2", 2, 12), WRRTaskSpec("P3", 1, 6)]
        res = simulate_wrr(specs, quantum=1, variant="classic")
        self.assertEqual(res["makespan"], 36)
        self.assertAlmostEqual(res["metrics"]["P1"]["actual_work_share_pct"], 50.0, places=1)
        self.assertAlmostEqual(res["metrics"]["P2"]["actual_work_share_pct"], 33.33, places=1)
        self.assertAlmostEqual(res["metrics"]["P3"]["actual_work_share_pct"], 16.67, places=1)
        self.assertGreater(res["weight_proportional_jains_index"], 0.99)

    def test_dynamic_arrivals_with_idle_gap(self):
        specs = [WRRTaskSpec("Early", 2, 2, arrival=0), WRRTaskSpec("Late", 1, 3, arrival=5)]
        res = simulate_wrr(specs, quantum=1, variant="classic")
        self.assertEqual(res["idle_time"], 3)
        self.assertEqual(res["makespan"], 8)
        self.assertEqual(res["metrics"]["Late"]["waiting"], 0)

    def test_context_switch_accounting(self):
        specs = [WRRTaskSpec("A", 1, 2), WRRTaskSpec("B", 1, 2)]
        res = simulate_wrr(specs, quantum=1, variant="classic", context_switch=1)
        # Order: A(0-1), CS(1-2), B(2-3), CS(3-4), A(4-5), CS(5-6), B(6-7) -> 3 CS, makespan 7
        self.assertEqual(res["context_switches"], 3)
        self.assertEqual(res["makespan"], 7)

    def test_partial_final_quantum(self):
        res = simulate_wrr([WRRTaskSpec("A", 3, 5)], quantum=2)
        self.assertEqual([e["duration"] for e in res["events"]], [2, 2, 1])

    def test_zero_burst_edge_case(self):
        res = simulate_wrr([WRRTaskSpec("Zero", 2, 0), WRRTaskSpec("Work", 1, 3)], quantum=1)
        self.assertEqual(res["makespan"], 3)
        self.assertEqual(res["metrics"]["Zero"]["completion"], 0)

    def test_max_wait_bound_formula(self):
        self.assertEqual(theoretical_max_wait_bound([3, 2, 1], target_index=2, quantum=2, context_switch=1), (3 + 2) * 2 + 2 * 1)

    def test_validation_errors(self):
        with self.assertRaises(ValueError):
            WRRTaskSpec("", 1, 1)
        with self.assertRaises(ValueError):
            WRRTaskSpec("P", 0, 1)
        with self.assertRaises(ValueError):
            WRRTaskSpec("P", 1, -1)
        with self.assertRaises(ValueError):
            simulate_wrr([WRRTaskSpec("A", 1, 1), WRRTaskSpec("A", 2, 1)])
        with self.assertRaises(ValueError):
            simulate_wrr([WRRTaskSpec("A", 1, 1)], quantum=0)

    def test_all_standard_scenarios_reproducible(self):
        all_s = run_all_scenarios()
        self.assertIn("S1_baseline_repo", all_s)
        self.assertEqual(len(all_s["quantum_sweep_cs1"]), 6)


if __name__ == "__main__":
    unittest.main()
