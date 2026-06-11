def calculate_average_metrics(processes):
    if not processes:
        return {}
        
    total_tat = sum(p.turnaround_time for p in processes)
    total_wt = sum(p.waiting_time for p in processes)
    total_rt = sum(p.response_time for p in processes)
    
    n = len(processes)
    return {
        "average_turnaround_time": round(total_tat / n, 2),
        "average_waiting_time": round(total_wt / n, 2),
        "average_response_time": round(total_rt / n, 2)
    }
