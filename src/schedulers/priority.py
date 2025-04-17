"""
Priority Scheduler Module
This module implements the Priority CPU scheduling algorithm.
"""

from src.schedulers.base_scheduler import BaseScheduler


class PriorityScheduler(BaseScheduler):
    """
    Priority Scheduler
    
    This scheduler executes the process with the highest priority first (lowest priority number).
    It is a non-preemptive scheduler, meaning once a process starts executing, it runs until
    completion.
    """
    
    def get_next_process(self, ready_queue):
        """
        Get the next process to execute according to Priority scheduling.
        
        In Priority scheduling, the next process is the one with the highest priority
        (lowest priority number).
        
        Args:
            ready_queue (list): List of processes that are ready to execute.
        
        Returns:
            Process or None: The next process to execute, or None if no process is ready.
        """
        if not ready_queue:
            return None
        
         
        ready_queue.sort(key=lambda p: p.priority)
        return ready_queue[0]
    
    def execute_process(self, process, ready_queue):
        """
        Execute the given process according to Priority scheduling.
        
        In Priority scheduling, the process runs until completion.
        
        Args:
            process (Process): The process to execute.
            ready_queue (list): The list of processes in the ready queue.
        """
         
        if process.start_time is None:
            process.start(self.current_time)
        
         
        time_slice = process.remaining_time
        process.execute(time_slice)
        
         
        self.schedule.append((process.pid, time_slice))
        
         
        self.current_time += time_slice
    
    def schedule(self, processes):
        """
        Schedule the given processes according to Priority scheduling.
        
        Args:
            processes (list): List of Process objects to schedule.
        
        Returns:
            list: The schedule as a list of (pid, time_slice) tuples.
        """
        return self.schedule_processes(processes)