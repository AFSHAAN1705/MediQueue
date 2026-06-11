from collections import deque
from algorithms.base import SchedulingAlgorithm

class RoundRobin(SchedulingAlgorithm):
    """
    Round Robin Scheduling Algorithm.
    Uses a Circular Queue (implemented via Python's deque).
    Time Complexity: O(N * (max_burst / time_quantum))
    Space Complexity: O(N) for the ready queue.
    """
    def __init__(self, time_quantum=2, context_switch=0):
        self.time_quantum = time_quantum
        self.context_switch = context_switch

    def execute(self, processes):
        # Sort by arrival time initially
        sorted_processes = sorted(processes, key=lambda p: p.arrival_time)
        
        current_time = 0
        gantt_chart = []
        completed_processes = []
        ready_queue = deque()
        
        idx = 0
        n = len(sorted_processes)
        
        # Enqueue first process(es)
        if n > 0:
            current_time = sorted_processes[0].arrival_time
            while idx < n and sorted_processes[idx].arrival_time <= current_time:
                ready_queue.append(sorted_processes[idx])
                idx += 1
                
        while ready_queue or idx < n:
            if not ready_queue:
                # CPU is idle
                next_arrival = sorted_processes[idx].arrival_time
                gantt_chart.append({"pid": "IDLE", "start": current_time, "end": next_arrival})
                current_time = next_arrival
                while idx < n and sorted_processes[idx].arrival_time <= current_time:
                    ready_queue.append(sorted_processes[idx])
                    idx += 1
                continue
                
            p = ready_queue.popleft()
            
            if p.start_time == -1:
                p.start_time = current_time
                p.response_time = current_time - p.arrival_time
                
            execute_time = min(p.remaining_time, self.time_quantum)
            
            gantt_chart.append({"pid": p.pid, "start": current_time, "end": current_time + execute_time})
            current_time += execute_time
            p.remaining_time -= execute_time
            
            # Context switch overhead simulation (added to Gantt as overhead)
            if self.context_switch > 0 and (p.remaining_time > 0 or ready_queue or idx < n):
                gantt_chart.append({"pid": "CS_OVERHEAD", "start": current_time, "end": current_time + self.context_switch})
                current_time += self.context_switch
            
            # Check for new arrivals while process was executing
            while idx < n and sorted_processes[idx].arrival_time <= current_time:
                ready_queue.append(sorted_processes[idx])
                idx += 1
                
            if p.remaining_time > 0:
                ready_queue.append(p) # Put back in circular queue
            else:
                p.completion_time = current_time
                if self.context_switch > 0 and gantt_chart[-1]["pid"] == "CS_OVERHEAD":
                    # completion time is actually before the context switch that happens after it
                    p.completion_time -= self.context_switch
                p.turnaround_time = p.completion_time - p.arrival_time
                p.waiting_time = p.turnaround_time - p.burst_time
                completed_processes.append(p)
                
        return completed_processes, gantt_chart
