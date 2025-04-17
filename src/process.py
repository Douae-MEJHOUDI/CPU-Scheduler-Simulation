"""
Process Class Module
This module defines the Process class, which represents a process in the CPU scheduler simulation.
"""


class Process:
    """
    A class representing a process in the CPU scheduler simulation.
    
    Attributes:
        pid (int): Process ID.
        arrival_time (int): Time at which the process arrives.
        burst_time (int): Total CPU time required by the process.
        priority (int): Priority of the process (lower number means higher priority).
        remaining_time (int): Remaining CPU time needed to complete the process.
        start_time (int): Time at which the process starts execution.
        finish_time (int): Time at which the process completes execution.
        waiting_time (int): Time the process spends waiting.
        turnaround_time (int): Total time from arrival to completion.
    """
    
    def __init__(self, pid, arrival_time, burst_time, priority=1):
        """
        Initialize a new Process instance.
        
        Args:
            pid (int): Process ID.
            arrival_time (int): Time at which the process arrives.
            burst_time (int): Total CPU time required by the process.
            priority (int, optional): Priority of the process (default: 1).
        """
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority
        
         
        self.remaining_time = burst_time
        self.start_time = None
        self.finish_time = None
        self.waiting_time = 0
        self.turnaround_time = 0
    
    def reset(self):
        """Reset the process to its initial state."""
        self.remaining_time = self.burst_time
        self.start_time = None
        self.finish_time = None
        self.waiting_time = 0
        self.turnaround_time = 0
    
    def start(self, time):
        """
        Mark the process as started at the given time.
        
        Args:
            time (int): The current time when the process starts execution.
        """
        if self.start_time is None:
            self.start_time = time
    
    def execute(self, time_quantum):
        """
        Execute the process for the given time quantum.
        
        Args:
            time_quantum (int): Amount of time to execute the process.
            
        Returns:
            int: The actual time executed (may be less than time_quantum if the process completes).
        """
        executed_time = min(time_quantum, self.remaining_time)
        self.remaining_time -= executed_time
        return executed_time
    
    def is_completed(self):
        """
        Check if the process has completed execution.
        
        Returns:
            bool: True if the process has completed execution, False otherwise.
        """
        return self.remaining_time <= 0
    
    def complete(self, time):
        """
        Mark the process as completed at the given time.
        
        Args:
            time (int): The current time when the process completes execution.
        """
        self.finish_time = time
        self.calculate_metrics()
    
    def calculate_metrics(self):
        """Calculate turnaround time and waiting time for the process."""
        if self.start_time is not None and self.finish_time is not None:
            self.turnaround_time = self.finish_time - self.arrival_time
            self.waiting_time = self.turnaround_time - self.burst_time
    
    def __str__(self):
        """Return a string representation of the process."""
        status = "Completed" if self.is_completed() else "Pending"
        return (f"Process {self.pid}: Arrival={self.arrival_time}, Burst={self.burst_time}, "
                f"Priority={self.priority}, Status={status}")
    
    def __repr__(self):
        """Return a formal string representation of the process."""
        return (f"Process(pid={self.pid}, arrival_time={self.arrival_time}, "
                f"burst_time={self.burst_time}, priority={self.priority})")