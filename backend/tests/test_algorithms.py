import pytest
from algorithms.hospital_algorithms import fcfs, sjf, round_robin, priority_scheduling, srtf

class MockPatient:
    def __init__(self, id, arrival_time, treatment_time, emergency_level=1):
        self.id = id
        self.arrival_time = arrival_time
        self.treatment_time = treatment_time
        self.emergency_level = emergency_level
        self.start_time = -1
        self.completion_time = 0
        self.turnaround_time = 0
        self.waiting_time = 0
        self.remaining_time = treatment_time

def test_fcfs():
    p1 = MockPatient(1, 0, 5)
    p2 = MockPatient(2, 1, 3)
    p3 = MockPatient(3, 2, 8)
    
    completed, gantt = fcfs([p1, p2, p3])
    
    assert gantt[0]["id"] == 1
    assert gantt[0]["end"] == 5
    assert gantt[1]["id"] == 2
    assert gantt[1]["end"] == 8
    assert gantt[2]["id"] == 3
    assert gantt[2]["end"] == 16
    assert completed[0].waiting_time == 0
    assert completed[1].waiting_time == 4 # 5 - 1
    assert completed[2].waiting_time == 6 # 8 - 2

def test_sjf():
    p1 = MockPatient(1, 0, 5)
    p2 = MockPatient(2, 1, 2)
    p3 = MockPatient(3, 2, 8)
    
    completed, gantt = sjf([p1, p2, p3])
    
    # p1 runs from 0 to 5. At 5, p2 and p3 are ready.
    # p2 (bt=2) is shorter than p3 (bt=8).
    # p2 runs 5 to 7. p3 runs 7 to 15.
    assert gantt[0]["id"] == 1
    assert gantt[1]["id"] == 2
    assert gantt[2]["id"] == 3
    assert gantt[1]["end"] == 7
    assert gantt[2]["end"] == 15

def test_priority():
    p1 = MockPatient(1, 0, 5, emergency_level=1)
    p2 = MockPatient(2, 1, 2, emergency_level=5) # High priority
    p3 = MockPatient(3, 2, 8, emergency_level=3)
    
    completed, gantt = priority_scheduling([p1, p2, p3])
    
    # p1 runs 0 to 5. At 5, p2(pr=5) and p3(pr=3) are ready.
    # p2 goes first.
    assert gantt[0]["id"] == 1
    assert gantt[1]["id"] == 2
    assert gantt[2]["id"] == 3

def test_srtf():
    p1 = MockPatient(1, 0, 5)
    p2 = MockPatient(2, 1, 2) # Arrives at 1, p1 has 4 left. p2 (2) < p1 (4). p2 preempts.
    
    completed, gantt = srtf([p1, p2])
    
    # p1 runs 0 to 1
    # p2 runs 1 to 3
    # p1 runs 3 to 7
    assert gantt[0]["id"] == 1
    assert gantt[0]["end"] == 1
    assert gantt[1]["id"] == 2
    assert gantt[1]["end"] == 3
    assert gantt[2]["id"] == 1
    assert gantt[2]["end"] == 7
