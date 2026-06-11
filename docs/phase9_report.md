# Phase 9: Academic Report

## Abstract
This project presents a comprehensive simulation and comparative analysis of CPU Scheduling algorithms. The system was developed using a modern React frontend and a Python backend, allowing for real-time visualization of queue dynamics.

## 1. Introduction
CPU Scheduling is the basis of multiprogrammed operating systems. By switching the CPU among processes, the OS can make the computer more productive.

## 2. Methodology
The backend was developed using object-oriented principles. We defined a generic `Algorithm` interface.
We implemented:
1. First Come First Serve (FCFS)
2. Shortest Job First (SJF)
3. Round Robin (RR)
4. Priority Scheduling

## 3. Complexity Analysis (ADA)
- **FCFS**: O(N log N) time due to initial sorting by arrival time. Space: O(N).
- **SJF**: O(N log N) using a Min-Heap (Priority Queue). It guarantees the shortest process is picked in O(log N) time. Space: O(N).
- **RR**: O(N * (Max_Burst / Time_Quantum)). Circular Queue implemented via Python `deque` gives O(1) pop and append. Space: O(N).

## 4. Results & Analysis
Based on the Comparison Dashboard:
- SJF consistently provided the minimum Average Waiting Time.
- FCFS suffered from the Convoy Effect.
- Round Robin provided the best Response Time, crucial for interactive systems.
