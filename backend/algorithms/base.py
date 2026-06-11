from abc import ABC, abstractmethod

class SchedulingAlgorithm(ABC):
    @abstractmethod
    def execute(self, processes):
        """
        Executes the scheduling algorithm on the given processes.
        Returns a tuple: (list_of_updated_processes, gantt_chart)
        gantt_chart is a list of dicts: {"pid": pid, "start": start_time, "end": end_time}
        """
        pass
