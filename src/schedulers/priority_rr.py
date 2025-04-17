"""
Priority + Round Robin Scheduler Module
This module implements a combination of Priority and Round Robin CPU scheduling algorithms.
"""

from src.schedulers.base_scheduler import BaseScheduler
from collections import defaultdict, deque


class PriorityRRScheduler(BaseScheduler):
    """
    Priority + Round Robin Scheduler
    
    This scheduler combines priority scheduling with round robin. Processes are grouped
    by priority, and within each priority level, round robin scheduling is applied.
    """
    
    def __init__(self, quantum=2):
        """
        Initialize the Priority + Round Robin scheduler.
        
        Args:
            quantum (int): Time quantum for each process execution.
        """
        super().__init__()
        self.quantum = quantum
        self.priority_queues = defaultdict(deque)
        self.current_priority = None
    
    def get_next_process(self, ready_queue):
        """
        Get the next process to execute according to Priority + Round Robin.
        
        Args:
            ready_queue (list): List of processes that are ready to execute.
        
        Returns:
            Process or None: The next process to execute, or None if no process is ready.
        """
         
        for process in ready_queue:
            if (not any(process in queue for queue in self.priority_queues.values()) and
                    not process.is_completed()):
                self.priority_queues[process.priority].append(process)
        
         
        empty_priorities = [p for p, q in self.priority_queues.items() if not q]
        for priority in empty_priorities:
            del self.priority_queues[priority]
        
        if not self.priority_queues:
            return None
        
         
        self.current_priority = min(self.priority_queues.keys())
        
         
        return self.priority_queues[self.current_priority].popleft()
    
    def execute_process(self, process, ready_queue):
        """
        Execute the given process according to Priority + Round Robin.
        
        Args:
            process (Process): The process to execute.
            ready_queue (list): The list of processes in the ready queue.
        """
         
        if process.start_time is None:
            process.start(self.current_time)
        
         
        time_slice = min(self.quantum, process.remaining_time)
        process.execute(time_slice)
        
         
        self.schedule_result.append((process.pid, time_slice))
        
         
        self.current_time += time_slice
        
         
        for p in ready_queue:
            if (p.arrival_time <= self.current_time and
                    not any(p in queue for queue in self.priority_queues.values()) and
                    not p.is_completed() and
                    p != process):
                self.priority_queues[p.priority].append(p)
        
         
        if not process.is_completed():
            self.priority_queues[process.priority].append(process)
        else:
             
            process.complete(self.current_time)
    
    def schedule(self, processes):
        """
        Schedule the given processes according to Priority + Round Robin.
        
        Args:
            processes (list): List of Process objects to schedule.
        
        Returns:
            list: The schedule as a list of (pid, time_slice) tuples.
        """
         
        self.priority_queues = defaultdict(deque)
        self.current_priority = None
        return self.schedule_processes(processes)