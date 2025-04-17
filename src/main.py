#!/usr/bin/env python3
"""
CPU Scheduler Simulation - Main Entry Point
This module serves as the entry point for the CPU scheduler simulation program.
It handles user interaction, scheduler selection, and result visualization.
"""

import argparse
import os
from src.process import Process
from src.utils.process_generator import generate_random_processes, read_processes_from_file
from src.utils.metrics import calculate_metrics
from src.schedulers.fcfs import FCFSScheduler
from src.schedulers.sjf import SJFScheduler
from src.schedulers.priority import PriorityScheduler
from src.schedulers.round_robin import RoundRobinScheduler
from src.schedulers.priority_rr import PriorityRRScheduler
from src.visualization.visualizer import visualize_schedule, compare_schedulers


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="CPU Scheduler Simulation")
    parser.add_argument("--algorithm", "-a", type=str, choices=["fcfs", "sjf", "priority", "rr", "priority_rr", "all"],
                        default="all", help="Scheduling algorithm to use")
    parser.add_argument("--processes", "-p", type=int, default=5,
                        help="Number of processes to generate")
    parser.add_argument("--min_burst", "-mb", type=int, default=1,
                        help="Minimum burst time")
    parser.add_argument("--max_burst", "-xb", type=int, default=10,
                        help="Maximum burst time")
    parser.add_argument("--min_arrival", "-ma", type=int, default=0,
                        help="Minimum arrival time")
    parser.add_argument("--max_arrival", "-xa", type=int, default=10,
                        help="Maximum arrival time")
    parser.add_argument("--min_priority", "-mp", type=int, default=1,
                        help="Minimum priority (1 is highest)")
    parser.add_argument("--max_priority", "-xp", type=int, default=10,
                        help="Maximum priority (higher number is lower priority)")
    parser.add_argument("--quantum", "-q", type=int, default=2,
                        help="Time quantum for Round Robin")
    parser.add_argument("--input_file", "-i", type=str,
                        help="Input file with process data")
    parser.add_argument("--output_dir", "-o", type=str, default="output",
                        help="Directory to save visualizations")
    
    return parser.parse_args()


def run_simulation(algorithm, processes, quantum=2):
    """Run the selected scheduling algorithm."""
    schedulers = {
        "fcfs": FCFSScheduler(),
        "sjf": SJFScheduler(),
        "priority": PriorityScheduler(),
        "rr": RoundRobinScheduler(quantum),
        "priority_rr": PriorityRRScheduler(quantum)
    }
    
    if algorithm in schedulers:
        scheduler = schedulers[algorithm]
        schedule = scheduler.schedule(processes)
        metrics = calculate_metrics(schedule, processes)
        return schedule, metrics
    else:
        raise ValueError(f"Unknown algorithm: {algorithm}")


def run_all_simulations(processes, quantum=2):
    """Run all scheduling algorithms and compare their performance."""
    results = {}
    algorithms = ["fcfs", "sjf", "priority", "rr", "priority_rr"]
    
    for algorithm in algorithms:
        schedule, metrics = run_simulation(algorithm, processes, quantum)
        results[algorithm] = {
            "schedule": schedule,
            "metrics": metrics
        }
    
    return results


def main():
    """Main function to run the CPU scheduler simulation."""
    args = parse_arguments()
    
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)
    
    if args.input_file:
        processes = read_processes_from_file(args.input_file)
    else:
        processes = generate_random_processes(
            args.processes,
            args.min_burst,
            args.max_burst,
            args.min_arrival,
            args.max_arrival,
            args.min_priority,
            args.max_priority
        )
    
    print("Process Information:")
    for process in processes:
        print(f"Process {process.pid}: Arrival={process.arrival_time}, "
              f"Burst={process.burst_time}, Priority={process.priority}")
    
    if args.algorithm == "all":
        results = run_all_simulations(processes, args.quantum)
        compare_schedulers(results, args.output_dir)
        
        print("\nPerformance Comparison:")
        print(f"{'Algorithm':<15} {'Avg Turnaround':<15} {'Avg Waiting':<15} {'CPU Utilization':<15}")
        print("-" * 60)
        for algorithm, result in results.items():
            metrics = result["metrics"]
            print(f"{algorithm:<15} {metrics['avg_turnaround_time']:<15.2f} "
                  f"{metrics['avg_waiting_time']:<15.2f} "
                  f"{metrics['cpu_utilization']:<15.2f}%")
    else:
        schedule, metrics = run_simulation(args.algorithm, processes, args.quantum)
        visualize_schedule(schedule, processes, args.algorithm, args.output_dir)
        
        print(f"\n{args.algorithm.upper()} Metrics:")
        print(f"Average Turnaround Time: {metrics['avg_turnaround_time']:.2f}")
        print(f"Average Waiting Time: {metrics['avg_waiting_time']:.2f}")
        print(f"CPU Utilization: {metrics['cpu_utilization']:.2f}%")


if __name__ == "__main__":
    main()