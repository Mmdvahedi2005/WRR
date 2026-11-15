import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from sync_verifier import explore_two_process_protocol, benchmark_mechanisms


class TestSyncVerifier(unittest.TestCase):
    def test_flawed_protocols_caught_with_counterexamples(self):
        naive = explore_two_process_protocol("naive_flag")
        self.assertFalse(naive.mutual_exclusion)
        self.assertIsNotNone(naive.counterexample_trace)

        alt = explore_two_process_protocol("strict_alternation")
        self.assertTrue(alt.mutual_exclusion)
        self.assertFalse(alt.progress_no_contention)

        dl = explore_two_process_protocol("flag_deadlock")
        self.assertTrue(dl.mutual_exclusion)
        self.assertFalse(dl.deadlock_free)

    def test_correct_protocols_verified(self):
        for proto in ("dekker", "peterson", "semaphore_fifo", "monitor_mesa"):
            v = explore_two_process_protocol(proto)
            self.assertTrue(v.mutual_exclusion, proto)
            self.assertTrue(v.deadlock_free, proto)
            self.assertTrue(v.progress_no_contention, proto)

    def test_threaded_harness_zero_safety_violations(self):
        bench = benchmark_mechanisms(iterations_per_thread=250)
        for row in bench:
            self.assertEqual(row["safety_violations"], 0)
            self.assertEqual(row["max_concurrent_in_cs"], 1)
            self.assertEqual(row["total_entries"], row["expected_entries"])


if __name__ == "__main__":
    unittest.main()
