"""
Base Scheduler Module
This module defines the BaseScheduler class, which serves as the foundation for all
scheduling algorithm implementations.
"""

from abc import ABC, abstractmethod
import copy


class BaseScheduler(ABC):
    """
    Abstract base class for CPU schedulers.
    
    This class defines the common interface and functionality for all CPU scheduling
    algorithms. Specific algorithms should inherit from this class and implement
    the abstract methods.
    """
    
    def __init__(self):
        """Initialize the scheduler."""
        self.current_time = 0
        self.schedule_result = []
    
    @abstractmethod
    def get_next_process(self, ready_queue):
        """
        Get the next process to execute according to the scheduling algorithm.
        
        Args:
            ready_queue (list): List of processes that are ready to execute.
        
        Returns:
            Process or None: The next process to execute, or None if no process is ready.
        """
        pass
    
    def schedule_processes(self, processes):
        """
        Schedule the given processes according to the scheduling algorithm.
        
        Args:
            processes (list): List of Process objects to schedule.
        
        Returns:
            list: The schedule as a list of (pid, time_slice) tuples.
        """
         
        processes_copy = copy.deepcopy(processes)
        
         
        self.current_time = 0
        self.schedule_result = []
        
         
        ready_queue = []
        
         
        completed_processes = {}
        
         
        while len(completed_processes) < len(processes_copy):
             
            for process in processes_copy:
                if (process.arrival_time <= self.current_time and
                        process.pid not in completed_processes and
                        process not in ready_queue and
                        not process.is_completed()):
                    ready_queue.append(process)
            
             
            if not ready_queue:
                next_arrival = float('inf')
                for process in processes_copy:
                    if process.arrival_time > self.current_time and process.pid not in completed_processes:
                        next_arrival = min(next_arrival, process.arrival_time)
                
                if next_arrival == float('inf'):
                     
                     
                    break
                
                 
                idle_time = next_arrival - self.current_time
                self.schedule_result.append((-1, idle_time))
                self.current_time = next_arrival
                continue
            
             
            next_process = self.get_next_process(ready_queue)
            
            if next_process is None:
                 
                break
            
             
            self.execute_process(next_process, ready_queue)
            
             
            if next_process.is_completed():
                next_process.complete(self.current_time)
                completed_processes[next_process.pid] = next_process
                
                 
                for original_process in processes:
                    if original_process.pid == next_process.pid:
                        original_process.start_time = next_process.start_time
                        original_process.finish_time = next_process.finish_time
                        original_process.waiting_time = next_process.waiting_time
                        original_process.turnaround_time = next_process.turnaround_time
                        original_process.remaining_time = 0
                        break
                
                 
                if next_process in ready_queue:
                    ready_queue.remove(next_process)
        
        return self.schedule_result
    
    @abstractmethod
    def execute_process(self, process, ready_queue):
        """
        Execute the given process according to the scheduling algorithm.
        
        Args:
            process (Process): The process to execute.
            ready_queue (list): The list of processes in the ready queue.
        """
        pass