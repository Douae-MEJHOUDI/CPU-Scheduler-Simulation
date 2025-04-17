"""
Utils Package
This package contains utility functions for the CPU scheduler simulation.
"""

from src.utils.metrics import calculate_metrics
from src.utils.process_generator import generate_random_processes, read_processes_from_file
from src.utils.file_handler import read_processes_from_file as read_file
from src.utils.file_handler import write_processes_to_file, write_results_to_file

__all__ = [
    'calculate_metrics',
    'generate_random_processes',
    'read_processes_from_file',
    'read_file',
    'write_processes_to_file',
    'write_results_to_file'
]