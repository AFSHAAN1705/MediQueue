import heapq
from algorithms.base import SchedulingAlgorithm

class PriorityScheduling(SchedulingAlgorithm):
    """
    Priority Scheduling (Non-Preemptive).
    Uses a Min-Heap based on priority (lower value = higher priority).
    Time Complexity: O(N log N)
    Space Complexity: O(N)
    """
    def execute(self, processes):
        # Sort by arrival time initially
        sorted_processes = sorted(processes, key=lambda p: p.arrival_time)
        
        current_time = 0
        gantt_chart = []
        completed_processes = []
        
        ready_queue = [] # Min heap based on (priority, arrival_time, pid)
        idx = 0
        n = len(sorted_processes)
        
        while idx < n or ready_queue:
            # Enqueue all arrived processes
            while idx < n and sorted_processes[idx].arrival_time <= current_time:
                p = sorted_processes[idx]
                # lower priority value implies higher priority in min heap
                heapq.heappush(ready_queue, (p.priority, p.arrival_time, p.pid, p))
                idx += 1
                
            if not ready_queue:
                next_arrival = sorted_processes[idx].arrival_time
                gantt_chart.append({"pid": "IDLE", "start": current_time, "end": next_arrival})
                current_time = next_arrival
                continue
                
            # Pop the highest priority job
            priority, at, pid, p = heapq.heappop(ready_queue)
            
            p.start_time = current_time
            p.response_time = p.start_time - p.arrival_time
            
            p.completion_time = current_time + p.burst_time
            p.turnaround_time = p.completion_time - p.arrival_time
            p.waiting_time = p.turnaround_time - p.burst_time
            
            gantt_chart.append({"pid": p.pid, "start": current_time, "end": p.completion_time})
            current_time = p.completion_time
            
            completed_processes.append(p)
            
        return completed_processes, gantt_chart
