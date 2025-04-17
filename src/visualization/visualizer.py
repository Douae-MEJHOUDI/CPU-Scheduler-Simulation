"""
Visualizer Module
This module provides functions to visualize CPU scheduling results.
"""

import os
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch


def generate_colors(num_processes):
    """
    Generate a list of distinct colors for processes.
    
    Args:
        num_processes (int): Number of processes.
    
    Returns:
        list: List of color hex codes.
    """
     
    base_colors = [
        '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
        '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf',
        '#aec7e8', '#ffbb78', '#98df8a', '#ff9896', '#c5b0d5'
    ]
    
     
    if num_processes <= len(base_colors):
        return base_colors[:num_processes]
    else:
         
        import colorsys
        
        colors = list(base_colors)   
        n = num_processes - len(base_colors)
        
        for i in range(n):
            hue = i / n
            saturation = 0.7 + 0.3 * (i % 3) / 2   
            value = 0.7 + 0.3 * ((i // 3) % 3) / 2   
            
            rgb = colorsys.hsv_to_rgb(hue, saturation, value)
            hex_color = '#{:02x}{:02x}{:02x}'.format(
                int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255)
            )
            colors.append(hex_color)
        
        return colors


def visualize_schedule(schedule, processes, algorithm_name, output_dir="output"):
    """
    Visualize the schedule using a Gantt chart.
    
    Args:
        schedule (list): List of (pid, time_slice) tuples.
        processes (list): List of Process objects.
        algorithm_name (str): Name of the scheduling algorithm.
        output_dir (str): Directory to save the visualization.
    
    Returns:
        str: Path to the saved visualization file.
    """
     
    process_map = {process.pid: process for process in processes}
    
     
    colors = generate_colors(len(processes) + 1)   
    color_map = {process.pid: colors[i] for i, process in enumerate(processes)}
    color_map[-1] = '#d3d3d3'  # Light gray for idle time
    
     
    fig, ax = plt.subplots(figsize=(12, 6))
    
    current_time = 0
    y_ticks = []
    y_labels = []
    
     
    for i, (pid, time_slice) in enumerate(schedule):
        if pid == -1:   
            ax.broken_barh([(current_time, time_slice)], (0, len(processes)), facecolors=color_map[-1])
        else:
             
            process_idx = next((i for i, p in enumerate(processes) if p.pid == pid), None)
            if process_idx is not None:
                ax.broken_barh([(current_time, time_slice)], (process_idx, 1), facecolors=color_map[pid])
        
         
        ax.text(current_time + time_slice / 2, len(processes) + 0.5, str(current_time + time_slice),
                ha='center', va='center', fontsize=8)
        
        current_time += time_slice
    
     
    ax.set_xlabel('Time')
    ax.set_ylabel('Process')
    ax.set_title(f'CPU Schedule - {algorithm_name.upper()}')
    
     
    ax.set_yticks(np.arange(len(processes)) + 0.5)
    ax.set_yticklabels([f'P{process.pid}' for process in processes])
    
     
    legend_elements = [
        Patch(facecolor=color_map[process.pid], label=f'P{process.pid}')
        for process in processes
    ]
    legend_elements.append(Patch(facecolor=color_map[-1], label='Idle'))
    ax.legend(handles=legend_elements, loc='upper right')
    
     
    ax.grid(True, axis='x', linestyle='--', alpha=0.7)
    
     
    metrics_text = (
        f"Average Turnaround Time: {sum(p.turnaround_time for p in processes) / len(processes):.2f}\n"
        f"Average Waiting Time: {sum(p.waiting_time for p in processes) / len(processes):.2f}\n"
    )
    plt.gcf().text(0.02, 0.02, metrics_text, fontsize=10)
    
     
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f"{algorithm_name}_gantt.png")
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    
    return output_file


def compare_schedulers(results, output_dir="output"):
    """
    Create comparative visualizations for different scheduling algorithms.
    
    Args:
        results (dict): Dictionary of results from different schedulers.
        output_dir (str): Directory to save the visualizations.
    
    Returns:
        str: Path to the saved comparison visualization file.
    """
     
    os.makedirs(output_dir, exist_ok=True)
    
     
    algorithms = list(results.keys())
    avg_turnaround_times = [results[algo]["metrics"]["avg_turnaround_time"] for algo in algorithms]
    avg_waiting_times = [results[algo]["metrics"]["avg_waiting_time"] for algo in algorithms]
    cpu_utilizations = [results[algo]["metrics"]["cpu_utilization"] for algo in algorithms]
    
     
    fig, axes = plt.subplots(3, 1, figsize=(10, 15))
    
     
    axes[0].bar(algorithms, avg_turnaround_times, color='skyblue')
    axes[0].set_title('Average Turnaround Time')
    axes[0].set_ylabel('Time')
    for i, v in enumerate(avg_turnaround_times):
        axes[0].text(i, v + 0.1, f'{v:.2f}', ha='center')
    
     
    axes[1].bar(algorithms, avg_waiting_times, color='lightgreen')
    axes[1].set_title('Average Waiting Time')
    axes[1].set_ylabel('Time')
    for i, v in enumerate(avg_waiting_times):
        axes[1].text(i, v + 0.1, f'{v:.2f}', ha='center')
    
     
    axes[2].bar(algorithms, cpu_utilizations, color='salmon')
    axes[2].set_title('CPU Utilization')
    axes[2].set_ylabel('Percentage (%)')
    axes[2].set_ylim(0, 100)
    for i, v in enumerate(cpu_utilizations):
        axes[2].text(i, v + 1, f'{v:.2f}%', ha='center')
    
    plt.tight_layout()
    
     
    output_file = os.path.join(output_dir, "scheduler_comparison.png")
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    
     
    visualize_timeline_comparison(results, output_dir)
    
    return output_file


def visualize_timeline_comparison(results, output_dir="output"):
    """
    Create a timeline comparison visualization for different scheduling algorithms.
    
    Args:
        results (dict): Dictionary of results from different schedulers.
        output_dir (str): Directory to save the visualizations.
    
    Returns:
        str: Path to the saved timeline comparison visualization file.
    """
     
    algorithms = list(results.keys())
    n_algorithms = len(algorithms)
    
     
    fig, axes = plt.subplots(n_algorithms, 1, figsize=(12, 2 * n_algorithms))
    if n_algorithms == 1:
        axes = [axes]
    
     
    first_algorithm = algorithms[0]
    first_schedule = results[first_algorithm]["schedule"]
    
     
    max_time = 0
    for algo in algorithms:
        schedule = results[algo]["schedule"]
        total_time = sum(time_slice for _, time_slice in schedule)
        max_time = max(max_time, total_time)
    
     
    process_pids = set()
    for algo in algorithms:
        schedule = results[algo]["schedule"]
        for pid, _ in schedule:
            if pid != -1:   
                process_pids.add(pid)
    
    colors = generate_colors(len(process_pids) + 1)   
    color_map = {pid: colors[i] for i, pid in enumerate(sorted(process_pids))}
    color_map[-1] = '#d3d3d3'  # Light gray for idle time
    
     
    for i, algorithm in enumerate(algorithms):
        ax = axes[i]
        schedule = results[algorithm]["schedule"]
        
        current_time = 0
        for pid, time_slice in schedule:
            ax.broken_barh([(current_time, time_slice)], (0, 1), facecolors=color_map[pid])
            
             
            if time_slice > 1:   
                ax.text(current_time + time_slice / 2, 0.5, f'P{pid}' if pid != -1 else 'Idle',
                        ha='center', va='center', fontsize=8)
            
            current_time += time_slice
        
         
        ax.set_xlim(0, max_time)
        ax.set_ylim(0, 1)
        ax.set_yticks([0.5])
        ax.set_yticklabels([algorithm.upper()])
        ax.grid(True, axis='x', linestyle='--', alpha=0.7)
        
         
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
    
     
    axes[-1].set_xlabel('Time')
    
     
    fig.suptitle('CPU Scheduling Algorithms Timeline Comparison', fontsize=14)
    
     
    legend_elements = [
        Patch(facecolor=color_map[pid], label=f'P{pid}')
        for pid in sorted(process_pids)
    ]
    legend_elements.append(Patch(facecolor=color_map[-1], label='Idle'))
    fig.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(1, 1))
    
    plt.tight_layout()
    plt.subplots_adjust(top=0.9, right=0.85)
    
     
    output_file = os.path.join(output_dir, "timeline_comparison.png")
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    
    return output_file