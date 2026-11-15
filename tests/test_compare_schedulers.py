import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from compare_schedulers import PeriodicTask, liu_layland_bound, exact_rm_rta, simulate_periodic, BENCHMARK_SUITES, run_monte_carlo_schedulability


class TestCompareSchedulers(unittest.TestCase):
    def test_liu_layland_values(self):
        self.assertAlmostEqual(liu_layland_bound(1), 1.0, places=5)
        self.assertAlmostEqual(liu_layland_bound(2), 0.8284, places=3)
        self.assertAlmostEqual(liu_layland_bound(3), 0.7798, places=3)

    def test_underload_harmonic_zero_misses_all(self):
        tset = BENCHMARK_SUITES["W1_underload_harmonic"]
        for pol in ("WRR", "RM", "EDF"):
            r = simulate_periodic(tset, pol)
            self.assertTrue(r["feasible_on_horizon"], f"{pol} should be feasible")
            self.assertEqual(r["deadline_misses_count"], 0)

    def test_high_util_gap_edf_beats_rm_and_wrr(self):
        tset = BENCHMARK_SUITES["W2_high_util_gap"]
        edf = simulate_periodic(tset, "EDF")
        rm = simulate_periodic(tset, "RM")
        wrr = simulate_periodic(tset, "WRR")
        self.assertEqual(edf["deadline_misses_count"], 0)
        self.assertGreater(rm["deadline_misses_count"], 0)
        self.assertGreater(wrr["deadline_misses_count"], 0)
        rta = exact_rm_rta(tset)
        self.assertFalse(rta["T3"]["schedulable"])

    def test_overload_wrr_prevents_starvation_while_rm_starves_lowest(self):
        tset = BENCHMARK_SUITES["W3_overload_domino"]
        rm = simulate_periodic(tset, "RM", horizon=24)
        wrr = simulate_periodic(tset, "WRR", horizon=24)
        edf = simulate_periodic(tset, "EDF", horizon=24)
        self.assertEqual(rm["per_task"]["T3"]["cpu_share_pct"], 0.0)
        self.assertGreater(wrr["per_task"]["T3"]["cpu_share_pct"], 15.0)
        self.assertGreater(edf["deadline_misses_count"], rm["deadline_misses_count"])

    def test_rta_matches_simulation_feasibility(self):
        for wname in ("W1_underload_harmonic", "W2_high_util_gap", "W4_aperiodic_mixed_weights"):
            tset = BENCHMARK_SUITES[wname]
            rta = exact_rm_rta(tset)
            rta_ok = all(v["schedulable"] for v in rta.values())
            sim = simulate_periodic(tset, "RM")
            self.assertEqual(rta_ok, sim["feasible_on_horizon"])

    def test_monte_carlo_edf_100_percent_when_u_le_1(self):
        mc = run_monte_carlo_schedulability(seed=42, sets_per_band=15)
        for band in mc:
            self.assertEqual(band["EDF_feasible_pct"], 100.0)


if __name__ == "__main__":
    unittest.main()
