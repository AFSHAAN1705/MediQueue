import heapq
from collections import deque

def fcfs(patients):
    """First Come First Serve"""
    sorted_patients = sorted(patients, key=lambda p: p.arrival_time)
    current_time = 0
    gantt = []
    
    for p in sorted_patients:
        if current_time < p.arrival_time:
            gantt.append({"id": "IDLE", "start": current_time, "end": p.arrival_time})
            current_time = p.arrival_time
            
        p.start_time = current_time
        p.completion_time = current_time + p.treatment_time
        p.turnaround_time = p.completion_time - p.arrival_time
        p.waiting_time = p.turnaround_time - p.treatment_time
        
        gantt.append({"id": p.id, "start": current_time, "end": p.completion_time})
        current_time = p.completion_time
        
    return sorted_patients, gantt

def sjf(patients):
    """Shortest Job First (Non-Preemptive)"""
    sorted_patients = sorted(patients, key=lambda p: p.arrival_time)
    current_time = 0
    gantt = []
    completed = []
    ready_queue = []
    idx = 0
    n = len(sorted_patients)
    
    while idx < n or ready_queue:
        while idx < n and sorted_patients[idx].arrival_time <= current_time:
            p = sorted_patients[idx]
            heapq.heappush(ready_queue, (p.treatment_time, p.arrival_time, p.id, p))
            idx += 1
            
        if not ready_queue:
            next_arr = sorted_patients[idx].arrival_time
            gantt.append({"id": "IDLE", "start": current_time, "end": next_arr})
            current_time = next_arr
            continue
            
        tt, at, pid, p = heapq.heappop(ready_queue)
        
        p.start_time = current_time
        p.completion_time = current_time + p.treatment_time
        p.turnaround_time = p.completion_time - p.arrival_time
        p.waiting_time = p.turnaround_time - p.treatment_time
        
        gantt.append({"id": p.id, "start": current_time, "end": p.completion_time})
        current_time = p.completion_time
        completed.append(p)
        
    return completed, gantt

def priority_scheduling(patients, aging_rate=0.1):
    """Priority Scheduling with Aging for Starvation Prevention"""
    sorted_patients = sorted(patients, key=lambda p: p.arrival_time)
    current_time = 0
    gantt = []
    completed = []
    ready_queue = []
    idx = 0
    n = len(sorted_patients)
    
    while idx < n or ready_queue:
        while idx < n and sorted_patients[idx].arrival_time <= current_time:
            p = sorted_patients[idx]
            heapq.heappush(ready_queue, (-p.emergency_level, p.arrival_time, p.id, p))
            idx += 1
            
        if not ready_queue:
            next_arr = sorted_patients[idx].arrival_time
            gantt.append({"id": "IDLE", "start": current_time, "end": next_arr})
            current_time = next_arr
            continue
            
        # Implementing AGING: recalculate priorities in the queue based on wait time
        new_ready = []
        for orig_neg_pr, at, pid, p in ready_queue:
            wait_time = current_time - p.arrival_time
            # Boost priority by aging_rate per minute of wait time
            boost = int(wait_time * aging_rate)
            eff_pr = p.emergency_level + boost
            heapq.heappush(new_ready, (-eff_pr, at, pid, p))
        ready_queue = new_ready
            
        neg_priority, at, pid, p = heapq.heappop(ready_queue)
        
        p.start_time = current_time
        p.completion_time = current_time + p.treatment_time
        p.turnaround_time = p.completion_time - p.arrival_time
        p.waiting_time = p.turnaround_time - p.treatment_time
        
        gantt.append({"id": p.id, "start": current_time, "end": p.completion_time})
        current_time = p.completion_time
        completed.append(p)
        
    return completed, gantt

def fcfs_multi_doctor(patients, num_doctors=2):
    """Multi-Doctor FCFS (Parallel Queues)"""
    sorted_patients = sorted(patients, key=lambda p: p.arrival_time)
    doctor_times = [0] * num_doctors
    gantt = []
    
    for p in sorted_patients:
        # Assign to doctor who is available earliest
        earliest_doc = min(range(num_doctors), key=lambda i: doctor_times[i])
        current_time = max(doctor_times[earliest_doc], p.arrival_time)
        
        if doctor_times[earliest_doc] < p.arrival_time:
             gantt.append({"id": "IDLE", "start": doctor_times[earliest_doc], "end": p.arrival_time, "doctor": earliest_doc})
             
        p.start_time = current_time
        p.completion_time = current_time + p.treatment_time
        p.turnaround_time = p.completion_time - p.arrival_time
        p.waiting_time = p.turnaround_time - p.treatment_time
        
        gantt.append({"id": p.id, "start": current_time, "end": p.completion_time, "doctor": earliest_doc})
        doctor_times[earliest_doc] = p.completion_time
        
    return sorted_patients, gantt

def round_robin(patients, time_quantum=2):
    """Round Robin"""
    sorted_patients = sorted(patients, key=lambda p: p.arrival_time)
    current_time = 0
    gantt = []
    completed = []
    ready_queue = deque()
    idx = 0
    n = len(sorted_patients)
    
    # Initialize remaining time
    for p in patients:
        p.remaining_time = p.treatment_time
        p.start_time = -1
        
    if n > 0:
        current_time = sorted_patients[0].arrival_time
        while idx < n and sorted_patients[idx].arrival_time <= current_time:
            ready_queue.append(sorted_patients[idx])
            idx += 1
            
    while ready_queue or idx < n:
        if not ready_queue:
            next_arr = sorted_patients[idx].arrival_time
            gantt.append({"id": "IDLE", "start": current_time, "end": next_arr})
            current_time = next_arr
            while idx < n and sorted_patients[idx].arrival_time <= current_time:
                ready_queue.append(sorted_patients[idx])
                idx += 1
            continue
            
        p = ready_queue.popleft()
        
        if p.start_time == -1:
            p.start_time = current_time
            
        exec_time = min(p.remaining_time, time_quantum)
        
        gantt.append({"id": p.id, "start": current_time, "end": current_time + exec_time})
            
        current_time += exec_time
        p.remaining_time -= exec_time
        
        while idx < n and sorted_patients[idx].arrival_time <= current_time:
            ready_queue.append(sorted_patients[idx])
            idx += 1
            
        if p.remaining_time > 0:
            ready_queue.append(p)
        else:
            p.completion_time = current_time
            p.turnaround_time = p.completion_time - p.arrival_time
            p.waiting_time = p.turnaround_time - p.treatment_time
            completed.append(p)
            
    return completed, gantt

def srtf(patients):
    """Shortest Remaining Time First (Preemptive)"""
    sorted_patients = sorted(patients, key=lambda p: p.arrival_time)
    current_time = 0
    gantt = []
    completed = []
    ready_queue = []
    idx = 0
    n = len(sorted_patients)
    
    for p in patients:
        p.remaining_time = p.treatment_time
        p.start_time = -1
        
    while idx < n or ready_queue:
        while idx < n and sorted_patients[idx].arrival_time <= current_time:
            p = sorted_patients[idx]
            heapq.heappush(ready_queue, (p.remaining_time, p.arrival_time, p.id, p))
            idx += 1
            
        if not ready_queue:
            next_arr = sorted_patients[idx].arrival_time
            gantt.append({"id": "IDLE", "start": current_time, "end": next_arr})
            current_time = next_arr
            continue
            
        rem_time, at, pid, p = heapq.heappop(ready_queue)
        
        if p.start_time == -1:
            p.start_time = current_time
            
        if idx < n:
            time_to_next = sorted_patients[idx].arrival_time - current_time
        else:
            time_to_next = float('inf')
            
        exec_time = min(p.remaining_time, time_to_next)
        
        if exec_time > 0:
            gantt.append({"id": p.id, "start": current_time, "end": current_time + exec_time})
                
            current_time += exec_time
            p.remaining_time -= exec_time
            
        if p.remaining_time == 0:
            p.completion_time = current_time
            p.turnaround_time = p.completion_time - p.arrival_time
            p.waiting_time = p.turnaround_time - p.treatment_time
            completed.append(p)
        else:
            # Re-check arrivals
            while idx < n and sorted_patients[idx].arrival_time <= current_time:
                new_p = sorted_patients[idx]
                heapq.heappush(ready_queue, (new_p.remaining_time, new_p.arrival_time, new_p.id, new_p))
                idx += 1
            heapq.heappush(ready_queue, (p.remaining_time, p.arrival_time, p.id, p))
            
    return completed, gantt
