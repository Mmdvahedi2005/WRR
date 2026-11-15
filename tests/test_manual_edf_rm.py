import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from manual_edf_rm import CASE_A_TASKS, CASE_B_TASKS, rta_steps, solve_tick_by_tick, build_all_solutions


class TestManualEDFRM(unittest.TestCase):
    def test_case_a_both_feasible_above_ll_bound(self):
        rta = rta_steps(CASE_A_TASKS)
        self.assertEqual(rta["P3"]["R_star"], 11)
        self.assertTrue(rta["P3"]["feasible"])
        rm = solve_tick_by_tick(CASE_A_TASKS, "RM")
        edf = solve_tick_by_tick(CASE_A_TASKS, "EDF")
        self.assertEqual(rm["hyperperiod"], 12)
        self.assertTrue(rm["feasible"])
        self.assertTrue(edf["feasible"])
        # Total idle ticks in H=12 with demand 3+4+4=11 must be 1
        self.assertEqual(sum(1 for r in rm["step_table"] if r["task"] == "IDLE"), 1)
        self.assertEqual(sum(1 for r in edf["step_table"] if r["task"] == "IDLE"), 1)

    def test_case_b_edf_succeeds_rm_misses_p3_at_t12(self):
        rta = rta_steps(CASE_B_TASKS)
        self.assertFalse(rta["P3"]["feasible"])
        rm = solve_tick_by_tick(CASE_B_TASKS, "RM")
        edf = solve_tick_by_tick(CASE_B_TASKS, "EDF")
        self.assertEqual(edf["hyperperiod"], 24)
        self.assertTrue(edf["feasible"])
        self.assertFalse(rm["feasible"])
        self.assertEqual(len(rm["misses"]), 1)
        self.assertEqual(rm["misses"][0]["tick"], 12)
        self.assertEqual(rm["misses"][0]["job"], "P3,1")

    def test_build_all_solutions_structure(self):
        sol = build_all_solutions()
        self.assertEqual(len(sol["Case_B_H24_EDF_Wins_RM_Misses"]["EDF"]["step_table"]), 24)


if __name__ == "__main__":
    unittest.main()
