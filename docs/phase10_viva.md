# Phase 10: Final Presentation & Viva Preparation

## Viva Q&A

**Q1: Why did you choose React and Python for this OS simulation?**
*Answer:* Python provides excellent data structures (like `heapq` for Min-Heaps) which made implementing ADA-compliant scheduling algorithms highly efficient. React allowed me to build a dynamic, interactive dashboard to visualize the Gantt chart without full page reloads, which is critical for a "simulation" feel.

**Q2: What is the Time Complexity of your SJF algorithm?**
*Answer:* O(N log N). I used a Min-Heap (Priority Queue) to store the ready processes. Pushing and popping from the heap takes O(log N), and doing this for N processes yields O(N log N).

**Q3: How does Context Switching affect Round Robin?**
*Answer:* If the time quantum is too small, the context switch overhead dominates the CPU time, drastically reducing throughput and increasing turnaround time. This project simulates this by injecting "CS_OVERHEAD" blocks into the Gantt chart timeline.

**Q4: Did you implement starvation prevention?**
*Answer:* Yes, the theoretical concept is "Aging" where priority is gradually increased. Though the UI focuses on basic Priority scheduling, Aging can easily be plugged into the Preemptive Priority module by incrementing priority values when WT exceeds a threshold.

## PPT Script
- **Slide 1**: Title - Comparative Analysis of CPU Scheduling Algorithms.
- **Slide 2**: Problem Statement - Finding the balance between Throughput, TAT, and Response Time.
- **Slide 3**: Architecture - Show the Client-Server model.
- **Slide 4**: Demo - Run the React Dashboard and showcase the comparison graph.
