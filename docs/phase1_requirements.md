# Phase 1: Requirement Analysis

## 1. Project Goals
The primary goal of this project is to build a professional-grade simulation tool for Comparative Analysis of CPU Scheduling Algorithms. The system aims to provide an educational and analytical platform that mimics how an Operating System's CPU scheduler manages processes. By visualizing the queue dynamics, generating Gantt charts, and computing performance metrics, it will serve as an excellent demonstration of Operating System concepts and the Analysis and Design of Algorithms (ADA).

## 2. Problem Statement
Modern operating systems must manage multiple processes concurrently. CPU Scheduling determines the order in which processes access the CPU, aiming to maximize throughput and minimize waiting time. The problem is that different algorithms excel under different conditions. A clear, analytical simulation is required to evaluate Trade-offs, Time Complexity, and Performance of algorithms like First Come First Serve (FCFS), Shortest Job First (SJF), Round Robin (RR), Priority Scheduling, and Multi-Level Queue (MLQ).

## 3. Real-World Relevance
- **Operating Systems**: At the core of Windows, Linux, and macOS are sophisticated schedulers (e.g., Linux CFS) ensuring fair CPU time distribution.
- **Cloud Computing**: Datacenters use similar algorithms to schedule virtual machines and serverless functions.
- **Real-Time Systems**: Medical devices and autonomous vehicles rely on strict Priority and Preemptive scheduling (like SRTF) to guarantee task completion within strict deadlines.

## 4. CPU Scheduling in Operating Systems
CPU scheduling is a process which allows one process to use the CPU while the execution of another process is on hold (in waiting state) due to unavailability of any resource like I/O etc, thereby making full use of CPU. The aim of CPU scheduling is to make the system efficient, fast, and fair.

## 5. System Requirements

### Functional Requirements
- **Process Input Module**: The system must allow users to input dynamic processes with parameters: Process ID, Arrival Time, Burst Time, and Priority.
- **Scheduling Engine**: Must support execution of Preemptive and Non-Preemptive algorithms.
- **Metrics Calculation**: The system must calculate Completion Time (CT), Turnaround Time (TAT), Waiting Time (WT), and Response Time (RT) for each process.
- **Visualization**: Must dynamically generate a Gantt chart representing the CPU allocation over time.
- **Comparison Dashboard**: Must present an aggregated view of Average WT, Average TAT, CPU Utilization, and Throughput to compare algorithms side-by-side.

### Non-Functional Requirements
- **Performance**: The scheduling simulation should compute the results in under 1 second for queue sizes up to 10,000 processes.
- **Usability**: The Web UI must be aesthetically pleasing, responsive, and intuitive.
- **Modularity**: Code should be organized according to SOLID principles. Algorithms must be easily extensible.
- **Scalability**: The backend must handle high volumes of concurrent simulation requests.

## 6. Expected Outputs
- **Gantt Chart**: Visual timeline of execution.
- **Process Table**: A data grid showing the calculated metrics for each process.
- **Performance Graphs**: Bar and Line graphs illustrating comparative metrics across all executed algorithms.
- **Complexity Report**: O(N) notation breakdowns for Time and Space complexity for the chosen ADA data structures.
