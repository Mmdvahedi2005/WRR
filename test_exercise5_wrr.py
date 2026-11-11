import unittest
from exercise5_wrr import Task, schedule

class WRRSchedulingTests(unittest.TestCase):
    def test_weight_controls_quanta_per_round(self):
        r=schedule([Task("A",2,5),Task("B",1,4)])
        self.assertEqual([e["task"] for e in r["events"][:3]],["A","A","B"])
    def test_all_sync_modes_same_schedule(self):
        outputs=[]
        for mode in ("semaphore","monitor","both"):
            outputs.append(schedule([Task("A",3,5),Task("B",1,4)],mode=mode))
        self.assertEqual(outputs[0]["gantt"],outputs[1]["gantt"])
        self.assertEqual(outputs[1]["gantt"],outputs[2]["gantt"])
    def test_completion_and_metrics(self):
        r=schedule([Task("A",1,3),Task("B",1,2)])
        self.assertEqual(r["makespan"],5)
        self.assertEqual(r["metrics"]["A"]["completion"],4)
        self.assertEqual(r["metrics"]["B"]["completion"],5)
    def test_partial_final_quantum(self):
        r=schedule([Task("A",4,3)],quantum=2)
        self.assertEqual([e["duration"] for e in r["events"]],[2,1])
    def test_zero_burst(self):
        r=schedule([Task("A",1,0)])
        self.assertEqual(r["makespan"],0)
        self.assertEqual(r["gantt"],[])
    def test_invalid_quantum(self):
        with self.assertRaises(ValueError): schedule([Task("A",1,2)],quantum=0)
    def test_invalid_weight(self):
        with self.assertRaises(ValueError): Task("A",0,2)
    def test_duplicate_names(self):
        with self.assertRaises(ValueError): schedule([Task("A",1,1),Task("A",2,1)])
    def test_invalid_mode(self):
        with self.assertRaises(ValueError): schedule([Task("A",1,1)],mode="unknown")

if __name__=="__main__": unittest.main()
