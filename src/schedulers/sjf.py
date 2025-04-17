"""
Shortest Job First (SJF) Scheduler Module
This module implements the SJF CPU scheduling algorithm.
"""

from src.schedulers.base_scheduler import BaseScheduler


class SJFScheduler(BaseScheduler):
    """
    Shortest Job First (SJF) Scheduler
    
    This scheduler executes the process with the shortest burst time first. It is a
    non-preemptive scheduler, meaning once a process starts executing, it runs until
    completion.
    """
    
    def get_next_process(self, ready_queue):
        """
        Get the next process to execute according to SJF.
        
        In SJF, the next process is the one with the shortest burst time.
        
        Args:
            ready_queue (list): List of processes that are ready to execute.
        
        Returns:
            Process or None: The next process to execute, or None if no process is ready.
        """
        if not ready_queue:
            return None
        
         
        ready_queue.sort(key=lambda p: p.remaining_time)
        return ready_queue[0]
    
    def execute_process(self, process, ready_queue):
        """
        Execute the given process according to SJF.
        
        In SJF, the process runs until completion.
        
        Args:
            process (Process): The process to execute.
            ready_queue (list): The list of processes in the ready queue.
        """
         
        if process.start_time is None:
            process.start(self.current_time)
        
         
        time_slice = process.remaining_time
        process.execute(time_slice)
        
         
        self.schedule_result.append((process.pid, time_slice))
        
         
        self.current_time += time_slice
    
    def schedule(self, processes):
        """
        Schedule the given processes according to SJF.
        
        Args:
            processes (list): List of Process objects to schedule.
        
        Returns:
            list: The schedule as a list of (pid, time_slice) tuples.
        """
        return self.schedule_processes(processes)