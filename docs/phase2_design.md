# Phase 2: System Design

This section covers the comprehensive architecture and design of the CPU Scheduling Simulation System.

## 1. System Architecture

The application is built using a modern **Client-Server Architecture**.
- **Frontend (Client)**: React.js application responsible for input collection and visual output rendering.
- **Backend (Server)**: Flask API (Python) responsible for algorithmic computation and result aggregation.

```mermaid
graph TD
    Client[React Web Application] -->|HTTP POST Process Data| API[Flask REST API]
    API --> Controller[Scheduling Controller]
    Controller --> Engine[Algorithm Engine]
    
    Engine --> FCFS[FCFS Module]
    Engine --> SJF[SJF Module]
    Engine --> RR[Round Robin Module]
    Engine --> Priority[Priority Module]
    Engine --> MLQ[MLQ Module]
    
    FCFS --> Metrics[Metrics Calculator]
    SJF --> Metrics
    RR --> Metrics
    Priority --> Metrics
    MLQ --> Metrics
    
    Metrics --> Response[JSON Response]
    Response --> API
    API -->|HTTP 200 OK Response Data| Client
    Client --> Chart[Gantt Chart UI]
    Client --> Tables[Metrics Table UI]
```

## 2. Data Flow Diagram

```mermaid
sequenceDiagram
    participant User
    participant React UI
    participant Flask API
    participant CPU Scheduler

    User->>React UI: Input Process (ID, AT, BT, Priority)
    User->>React UI: Select Algorithms
    User->>React UI: Click 'Simulate'
    
    React UI->>Flask API: POST /api/simulate (JSON Data)
    Flask API->>CPU Scheduler: Parse JSON to Process Objects
    
    loop For each selected Algorithm
        CPU Scheduler->>CPU Scheduler: Execute Algorithm
        CPU Scheduler->>CPU Scheduler: Generate Execution Timeline (Gantt)
        CPU Scheduler->>CPU Scheduler: Calculate WT, TAT, RT, CT
    end
    
    CPU Scheduler-->>Flask API: Return Results & Metrics
    Flask API-->>React UI: Return JSON Response
    
    React UI->>User: Render Interactive Dashboard & Charts
```

## 3. UML Class Diagram for Scheduler Engine

The backend core logic is object-oriented. The classes decouple the state of a process from the logic of an algorithm.

```mermaid
classDiagram
    class Process {
        +int pid
        +int arrival_time
        +int burst_time
        +int remaining_time
        +int priority
        +int start_time
        +int completion_time
        +int turnaround_time
        +int waiting_time
        +int response_time
        +calculate_metrics()
    }

    class Algorithm {
        <<interface>>
        +execute(processes: List~Process~) Result
    }

    class FCFS {
        +execute(processes: List~Process~) Result
    }

    class SJF {
        +boolean preemptive
        +execute(processes: List~Process~) Result
    }

    class RoundRobin {
        +int time_quantum
        +execute(processes: List~Process~) Result
    }

    Algorithm <|-- FCFS
    Algorithm <|-- SJF
    Algorithm <|-- RoundRobin

    class Scheduler {
        -List~Process~ processes
        -Algorithm strategy
        +set_strategy(Algorithm a)
        +run() Result
    }
    
    Scheduler o-- Algorithm
    Scheduler *-- Process
```

## 4. Module Description

1. **Process Module**: Contains the Data Structure representing an OS Process. Includes state variables like remaining burst time.
2. **Algorithm Engine Module**: Implements the Strategy Pattern. Each scheduling algorithm is a strategy that can be plugged into the context (Scheduler).
3. **Metrics Engine Module**: Calculates mathematical averages across all processes after simulation (e.g., Average TAT, Throughput).
4. **Visualization Module (Frontend)**: Uses React state management to map JSON output timelines to CSS/SVG-based Gantt charts.
