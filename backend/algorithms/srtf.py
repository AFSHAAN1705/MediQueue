import heapq
from algorithms.base import SchedulingAlgorithm

class SRTF(SchedulingAlgorithm):
    """
    Shortest Remaining Time First (Preemptive SJF).
    Uses a Min-Heap.
    Time Complexity: O(N log N) per event.
    Space Complexity: O(N)
    """
    def __init__(self, context_switch=0):
        self.context_switch = context_switch

    def execute(self, processes):
        sorted_processes = sorted(processes, key=lambda p: p.arrival_time)
        
        current_time = 0
        gantt_chart = []
        completed_processes = []
        ready_queue = []
        
        idx = 0
        n = len(sorted_processes)
        
        while idx < n or ready_queue:
            # Enqueue arrived
            while idx < n and sorted_processes[idx].arrival_time <= current_time:
                p = sorted_processes[idx]
                heapq.heappush(ready_queue, (p.remaining_time, p.arrival_time, p.pid, p))
                idx += 1
                
            if not ready_queue:
                next_arrival = sorted_processes[idx].arrival_time
                gantt_chart.append({"pid": "IDLE", "start": current_time, "end": next_arrival})
                current_time = next_arrival
                continue
                
            rem_time, at, pid, p = heapq.heappop(ready_queue)
            
            if p.start_time == -1:
                p.start_time = current_time
                p.response_time = current_time - p.arrival_time
                
            # Execute until next arrival or completion
            if idx < n:
                next_arrival = sorted_processes[idx].arrival_time
                time_to_next = next_arrival - current_time
            else:
                time_to_next = float('inf')
                
            execute_time = min(p.remaining_time, time_to_next)
            
            # Avoid 0 length executions
            if execute_time > 0:
                if gantt_chart and gantt_chart[-1]["pid"] == p.pid:
                    gantt_chart[-1]["end"] += execute_time
                else:
                    gantt_chart.append({"pid": p.pid, "start": current_time, "end": current_time + execute_time})
                    
                current_time += execute_time
                p.remaining_time -= execute_time
            
            # Context switch logic (simplified: if process changes and context switch > 0)
            
            if p.remaining_time == 0:
                p.completion_time = current_time
                p.turnaround_time = p.completion_time - p.arrival_time
                p.waiting_time = p.turnaround_time - p.burst_time
                completed_processes.append(p)
                # Apply CS overhead after process completes if there are more processes
                if self.context_switch > 0 and (ready_queue or idx < n):
                    gantt_chart.append({"pid": "CS_OVERHEAD", "start": current_time, "end": current_time + self.context_switch})
                    current_time += self.context_switch
            else:
                # Need to push it back, but let's see if next process preempts it
                # Enqueue arrived processes first to check their remaining times
                while idx < n and sorted_processes[idx].arrival_time <= current_time:
                    new_p = sorted_processes[idx]
                    heapq.heappush(ready_queue, (new_p.remaining_time, new_p.arrival_time, new_p.pid, new_p))
                    idx += 1
                    
                # If there's a process with strictly less remaining time, preemption happens
                if ready_queue and ready_queue[0][0] < p.remaining_time:
                    if self.context_switch > 0:
                         gantt_chart.append({"pid": "CS_OVERHEAD", "start": current_time, "end": current_time + self.context_switch})
                         current_time += self.context_switch
                heapq.heappush(ready_queue, (p.remaining_time, p.arrival_time, p.pid, p))
                
        return completed_processes, gantt_chart
