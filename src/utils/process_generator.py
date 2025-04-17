"""
Process Generator Module
This module provides functions to generate processes for the CPU scheduler simulation.
"""

import random
import csv
from src.process import Process


def generate_random_processes(num_processes, min_burst, max_burst,
                             min_arrival, max_arrival, min_priority, max_priority):
    """
    Generate a list of random processes.
    
    Args:
        num_processes (int): Number of processes to generate.
        min_burst (int): Minimum burst time.
        max_burst (int): Maximum burst time.
        min_arrival (int): Minimum arrival time.
        max_arrival (int): Maximum arrival time.
        min_priority (int): Minimum priority value.
        max_priority (int): Maximum priority value.
    
    Returns:
        list: A list of Process objects.
    """
    processes = []
    
    for pid in range(1, num_processes + 1):
        arrival_time = random.randint(min_arrival, max_arrival)
        burst_time = random.randint(min_burst, max_burst)
        priority = random.randint(min_priority, max_priority)
        processes.append(Process(pid, arrival_time, burst_time, priority))
    
     
    processes.sort(key=lambda p: p.arrival_time)
    
    return processes


def read_processes_from_file(filename):
    """
    Read processes from a CSV file.
    
    The file should have columns: pid, arrival_time, burst_time, priority.
    
    Args:
        filename (str): Path to the input file.
    
    Returns:
        list: A list of Process objects.
    """
    processes = []
    
    try:
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                pid = int(row['pid'])
                arrival_time = int(row['arrival_time'])
                burst_time = int(row['burst_time'])
                priority = int(row.get('priority', 1))   
                
                processes.append(Process(pid, arrival_time, burst_time, priority))
    
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return []
    
    except (KeyError, ValueError) as e:
        print(f"Error: Invalid file format - {str(e)}")
        return []
    
     
    processes.sort(key=lambda p: p.arrival_time)
    
    return processes


def save_processes_to_file(processes, filename):
    """
    Save processes to a CSV file.
    
    Args:
        processes (list): List of Process objects.
        filename (str): Path to the output file.
    
    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            
             
            writer.writerow(['pid', 'arrival_time', 'burst_time', 'priority'])
            
             
            for process in processes:
                writer.writerow([
                    process.pid,
                    process.arrival_time,
                    process.burst_time,
                    process.priority
                ])
        
        return True
    
    except Exception as e:
        print(f"Error saving to file: {str(e)}")
        return False