from algorithms.base import SchedulingAlgorithm

class FCFS(SchedulingAlgorithm):
    """
    First Come First Serve (FCFS) Scheduling Algorithm.
    Time Complexity: O(N log N) due to sorting by arrival time.
    Space Complexity: O(N) to store the Gantt chart and output processes.
    """
    def execute(self, processes):
        # Sort by arrival time
        sorted_processes = sorted(processes, key=lambda p: p.arrival_time)
        
        current_time = 0
        gantt_chart = []
        
        for p in sorted_processes:
            if current_time < p.arrival_time:
                # CPU is idle
                gantt_chart.append({"pid": "IDLE", "start": current_time, "end": p.arrival_time})
                current_time = p.arrival_time
                
            p.start_time = current_time
            p.response_time = p.start_time - p.arrival_time
            
            p.completion_time = current_time + p.burst_time
            p.turnaround_time = p.completion_time - p.arrival_time
            p.waiting_time = p.turnaround_time - p.burst_time
            
            gantt_chart.append({"pid": p.pid, "start": current_time, "end": p.completion_time})
            current_time = p.completion_time
            
        return sorted_processes, gantt_chart
