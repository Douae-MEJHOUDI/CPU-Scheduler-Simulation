"""
File Handler Module
This module provides functions to read and write process data from/to files.
"""

import csv
import json
import os
from src.process import Process


def read_csv_file(filename):
    """
    Read process data from a CSV file.
    
    Args:
        filename (str): Path to the CSV file.
    
    Returns:
        list: List of Process objects.
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
    
    except (KeyError, ValueError) as e:
        print(f"Error: Invalid file format - {str(e)}")
    
    return processes


def read_json_file(filename):
    """
    Read process data from a JSON file.
    
    Args:
        filename (str): Path to the JSON file.
    
    Returns:
        list: List of Process objects.
    """
    processes = []
    
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
            
            for process_data in data:
                pid = int(process_data['pid'])
                arrival_time = int(process_data['arrival_time'])
                burst_time = int(process_data['burst_time'])
                priority = int(process_data.get('priority', 1))   
                
                processes.append(Process(pid, arrival_time, burst_time, priority))
    
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    
    except (json.JSONDecodeError, KeyError, ValueError) as e:
        print(f"Error: Invalid file format - {str(e)}")
    
    return processes


def write_csv_file(processes, filename):
    """
    Write process data to a CSV file.
    
    Args:
        processes (list): List of Process objects.
        filename (str): Path to the CSV file.
    
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
        print(f"Error writing to file: {str(e)}")
        return False


def write_json_file(processes, filename):
    """
    Write process data to a JSON file.
    
    Args:
        processes (list): List of Process objects.
        filename (str): Path to the JSON file.
    
    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        process_data = []
        
        for process in processes:
            process_data.append({
                'pid': process.pid,
                'arrival_time': process.arrival_time,
                'burst_time': process.burst_time,
                'priority': process.priority
            })
        
        with open(filename, 'w') as file:
            json.dump(process_data, file, indent=4)
        
        return True
    
    except Exception as e:
        print(f"Error writing to file: {str(e)}")
        return False


def read_processes_from_file(filename):
    """
    Read processes from a file based on its extension.
    
    Args:
        filename (str): Path to the input file.
    
    Returns:
        list: List of Process objects.
    """
    _, ext = os.path.splitext(filename)
    
    if ext.lower() == '.csv':
        return read_csv_file(filename)
    elif ext.lower() == '.json':
        return read_json_file(filename)
    else:
        print(f"Error: Unsupported file format '{ext}'")
        return []


def write_processes_to_file(processes, filename):
    """
    Write processes to a file based on its extension.
    
    Args:
        processes (list): List of Process objects.
        filename (str): Path to the output file.
    
    Returns:
        bool: True if successful, False otherwise.
    """
    _, ext = os.path.splitext(filename)
    
    if ext.lower() == '.csv':
        return write_csv_file(processes, filename)
    elif ext.lower() == '.json':
        return write_json_file(processes, filename)
    else:
        print(f"Error: Unsupported file format '{ext}'")
        return False


def write_results_to_file(results, filename):
    """
    Write simulation results to a file.
    
    Args:
        results (dict): Simulation results.
        filename (str): Path to the output file.
    
    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        with open(filename, 'w') as file:
            file.write("CPU Scheduler Simulation Results\n")
            file.write("===============================\n\n")
            
            for algorithm, result in results.items():
                metrics = result["metrics"]
                file.write(f"{algorithm.upper()} Metrics:\n")
                file.write(f"  Average Turnaround Time: {metrics['avg_turnaround_time']:.2f}\n")
                file.write(f"  Average Waiting Time: {metrics['avg_waiting_time']:.2f}\n")
                file.write(f"  CPU Utilization: {metrics['cpu_utilization']:.2f}%\n")
                file.write(f"  Total Time: {metrics['total_time']}\n\n")
        
        return True
    
    except Exception as e:
        print(f"Error writing results to file: {str(e)}")
        return False