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
        self.ready_queue = []  
        self.process_index = 0 
    
    def get_next_process(self, ready_queue):
        """
        Get the next process to execute according to Round Robin.
        
        In Round Robin, processes are executed in a FIFO manner with a time quantum.
        
        Args:
            ready_queue (list): List of processes that are ready to execute.
        
        Returns:
            Process or None: The next process to execute, or None if no process is ready.
        """

        while (self.process_index < len(ready_queue) and 
               ready_queue[self.process_index].arrival_time <= self.current_time):
            process = ready_queue[self.process_index]
            self.ready_queue.append((process, process.remaining_time))
            self.process_index += 1
        
        if not self.ready_queue:
            if self.process_index < len(ready_queue):
                next_process = ready_queue[self.process_index]
                idle_time = next_process.arrival_time - self.current_time

                self.schedule_result.append((-1, idle_time))
                self.current_time += idle_time

                return self.get_next_process(ready_queue)
            else:
                return None

        process, remaining_time = self.ready_queue.pop(0)
        return process
    
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

        self.schedule_result.append((process.pid, time_slice))

        self.current_time += time_slice

        while (self.process_index < len(ready_queue) and 
               ready_queue[self.process_index].arrival_time <= self.current_time):
            new_process = ready_queue[self.process_index]
            self.ready_queue.append((new_process, new_process.remaining_time))
            self.process_index += 1

        if not process.is_completed():
            self.ready_queue.append((process, process.remaining_time))
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
        processes.sort(key=lambda p: p.arrival_time)

        self.current_time = 0
        self.schedule_result = []
        self.ready_queue = []
        self.process_index = 0

        while self.process_index < len(processes) or self.ready_queue:
            process = self.get_next_process(processes)
            if process is None:
                break
            
            self.execute_process(process, processes)
        
        return self.schedule_result
