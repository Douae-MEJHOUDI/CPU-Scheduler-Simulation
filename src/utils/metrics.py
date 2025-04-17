"""
Metrics Module
This module provides functions to calculate performance metrics for the CPU scheduler simulation.
"""


def calculate_turnaround_time(process):
    """
    Calculate turnaround time for a process.
    
    Turnaround Time = Completion Time - Arrival Time
    
    Args:
        process (Process): Process object.
    
    Returns:
        int: Turnaround time.
    """
    if process.finish_time is not None:
        return process.finish_time - process.arrival_time
    return None


def calculate_waiting_time(process):
    """
    Calculate waiting time for a process.
    
    Waiting Time = Turnaround Time - Burst Time
    
    Args:
        process (Process): Process object.
    
    Returns:
        int: Waiting time.
    """
    turnaround_time = calculate_turnaround_time(process)
    if turnaround_time is not None:
        return turnaround_time - process.burst_time
    return None


def calculate_cpu_utilization(schedule, total_time):
    """
    Calculate CPU utilization.
    
    CPU Utilization = (Total Busy Time / Total Time) * 100%
    
    Args:
        schedule (list): List of scheduled process IDs and time slices.
        total_time (int): Total simulation time.
    
    Returns:
        float: CPU utilization percentage.
    """
    busy_time = sum(time_slice for _, time_slice in schedule if _ != -1)
    return (busy_time / total_time) * 100 if total_time > 0 else 0


def calculate_metrics(schedule, processes):
    """
    Calculate performance metrics for the scheduler.
    
    Args:
        schedule (list): List of (pid, time_slice) tuples.
        processes (list): List of Process objects.
    
    Returns:
        dict: Dictionary containing performance metrics.
    """
     
    total_time = sum(time_slice for _, time_slice in schedule)
    
     
    turnaround_times = []
    waiting_times = []
    
    for process in processes:
        turnaround_time = calculate_turnaround_time(process)
        waiting_time = calculate_waiting_time(process)
        
        if turnaround_time is not None:
            turnaround_times.append(turnaround_time)
        
        if waiting_time is not None:
            waiting_times.append(waiting_time)
    
     
    avg_turnaround_time = sum(turnaround_times) / len(turnaround_times) if turnaround_times else 0
    avg_waiting_time = sum(waiting_times) / len(waiting_times) if waiting_times else 0
    cpu_utilization = calculate_cpu_utilization(schedule, total_time)
    
    return {
        'avg_turnaround_time': avg_turnaround_time,
        'avg_waiting_time': avg_waiting_time,
        'cpu_utilization': cpu_utilization,
        'total_time': total_time
    }