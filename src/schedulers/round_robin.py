"""
Round Robin (RR) Scheduler Module
This module implements the Round Robin CPU scheduling algorithm.
"""

from src.schedulers.base_scheduler import BaseScheduler
from collections import deque


class RoundRobinScheduler(BaseScheduler):
    """
    Round Robin (RR) Scheduler
    
    This scheduler executes processes in a circular order, giving each process a fixed
    time quantum. It is a preemptive scheduler, meaning a process will be interrupted
    if it exceeds its time quantum.
    """
    
    def __init__(self, quantum=2):
        """
        Initialize the Round Robin scheduler.
        
        Args:
            quantum (int): Time quantum for each process execution.
        """
        super().__init__()
        self.quantum = quantum
        self.ready_queue = deque()
    
    def get_next_process(self, ready_queue):
        """
        Get the next process to execute according to Round Robin.
        
        In Round Robin, processes are executed in a FIFO manner with a time quantum.
        
        Args:
            ready_queue (list): List of processes that are ready to execute.
        
        Returns:
            Process or None: The next process to execute, or None if no process is ready.
        """
        if not self.ready_queue and ready_queue:
             
            self.ready_queue = deque(sorted(ready_queue, key=lambda p: p.arrival_time))
        
        if not self.ready_queue:
            return None
        
        return self.ready_queue.popleft()
    
    def execute_process(self, process, ready_queue):
        """
        Execute the given process according to Round Robin.
        
        In Round Robin, a process executes for a fixed time quantum or until completion.
        
        Args:
            process (Process): The process to execute.
            ready_queue (list): The list of processes in the ready queue.
        """
         
        if process.start_time is None:
            process.start(self.current_time)
        
         
        time_slice = min(self.quantum, process.remaining_time)
        process.execute(time_slice)
        
         
        self.schedule.append((process.pid, time_slice))
        
         
        self.current_time += time_slice
        
         
        if not process.is_completed():
             
            for p in ready_queue:
                if (p.arrival_time <= self.current_time and
                        p not in self.ready_queue and
                        not p.is_completed() and
                        p != process):
                    self.ready_queue.append(p)
            
             
            self.ready_queue.append(process)
        else:
             
            process.complete(self.current_time)
    
    def schedule(self, processes):
        """
        Schedule the given processes according to Round Robin.
        
        Args:
            processes (list): List of Process objects to schedule.
        
        Returns:
            list: The schedule as a list of (pid, time_slice) tuples.
        """
         
        self.ready_queue = deque()
        return self.schedule_processes(processes)