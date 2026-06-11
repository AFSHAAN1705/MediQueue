# Phase 8: Testing & Debugging

## Unit Testing
We verified the algorithms using standard academic examples (e.g., Galvin's Operating System Concepts chapter on Scheduling).
- **FCFS**: Validated that processes execute in strictly increasing arrival time order.
- **SJF**: Validated that the convoy effect is reduced when a short process arrives just after a long one starts.
- **Round Robin**: Checked that context switching accurately interrupts processes at `Time Quantum = 2`.

## Edge-Case Testing
1. **Identical Arrival Times**: System relies on Process ID to break ties (FCFS behavior on tied parameters).
2. **Zero Burst Time**: A burst time of zero is immediately completed.
3. **High Context Switch Overhead**: Verified that setting Context Switch > Burst Time accurately penalizes preemptive algorithms like Round Robin, making FCFS perform better in some scenarios.
