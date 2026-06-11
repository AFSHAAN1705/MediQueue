import heapq
from algorithms.base import SchedulingAlgorithm

class SJF(SchedulingAlgorithm):
    """
    Shortest Job First (Non-Preemptive) Scheduling Algorithm.
    Uses a Min-Heap to efficiently extract the process with the shortest burst time.
    Time Complexity: O(N log N) since each process is pushed and popped from heap once.
    Space Complexity: O(N) for the priority queue (heap).
    """
    def execute(self, processes):
        # Sort processes by arrival time initially
        sorted_processes = sorted(processes, key=lambda p: p.arrival_time)
        
        current_time = 0
        gantt_chart = []
        completed_processes = []
        
        ready_queue = [] # Min heap based on (burst_time, arrival_time, pid)
        idx = 0
        n = len(sorted_processes)
        
        while idx < n or ready_queue:
            # Enqueue all processes that have arrived up to current_time
            while idx < n and sorted_processes[idx].arrival_time <= current_time:
                p = sorted_processes[idx]
                # push tuple: (burst_time, arrival_time, pid, process_obj)
                heapq.heappush(ready_queue, (p.burst_time, p.arrival_time, p.pid, p))
                idx += 1
                
            if not ready_queue:
                # CPU is idle
                next_arrival = sorted_processes[idx].arrival_time
                gantt_chart.append({"pid": "IDLE", "start": current_time, "end": next_arrival})
                current_time = next_arrival
                continue
                
            # Pop the shortest job
            bt, at, pid, p = heapq.heappop(ready_queue)
            
            p.start_time = current_time
            p.response_time = p.start_time - p.arrival_time
            
            p.completion_time = current_time + p.burst_time
            p.turnaround_time = p.completion_time - p.arrival_time
            p.waiting_time = p.turnaround_time - p.burst_time
            
            gantt_chart.append({"pid": p.pid, "start": current_time, "end": p.completion_time})
            current_time = p.completion_time
            
            completed_processes.append(p)
            
        return completed_processes, gantt_chart
