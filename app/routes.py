"""
Routes for the CPU Scheduler Simulation web interface.
"""

import os
import uuid
import json
import matplotlib
matplotlib.use('Agg')
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, session, jsonify, send_from_directory
from werkzeug.utils import secure_filename

from app.forms import SimulationForm
from src.process import Process
from src.utils.process_generator import generate_random_processes, read_processes_from_file
from src.utils.metrics import calculate_metrics
from src.schedulers.fcfs import FCFSScheduler
from src.schedulers.sjf import SJFScheduler
from src.schedulers.priority import PriorityScheduler
from src.schedulers.round_robin import RoundRobinScheduler
from src.schedulers.priority_rr import PriorityRRScheduler
from src.visualization.visualizer import visualize_schedule, compare_schedulers

main = Blueprint('main', __name__)

def allowed_file(filename):
    """Check if the file extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def save_upload_file(file):
    """Save an uploaded file and return the path."""
    filename = secure_filename(file.filename)
    unique_filename = f"{uuid.uuid4()}_{filename}"
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
    file.save(file_path)
    return file_path

def get_processes_from_session():
    """Get processes from session or return None."""
    if 'processes' in session:
        processes_data = session['processes']
        processes = []
        for p_data in processes_data:
            process = Process(
                pid=p_data['pid'],
                arrival_time=p_data['arrival_time'],
                burst_time=p_data['burst_time'],
                priority=p_data['priority']
            )
            process.start_time = p_data.get('start_time')
            process.finish_time = p_data.get('finish_time')
            process.waiting_time = p_data.get('waiting_time', 0)
            process.turnaround_time = p_data.get('turnaround_time', 0)
            process.remaining_time = p_data.get('remaining_time', process.burst_time)
            processes.append(process)
        return processes
    return None

def save_processes_to_session(processes):
    """Save processes to session."""
    processes_data = []
    for process in processes:
        p_data = {
            'pid': process.pid,
            'arrival_time': process.arrival_time,
            'burst_time': process.burst_time,
            'priority': process.priority,
            'start_time': process.start_time,
            'finish_time': process.finish_time,
            'waiting_time': process.waiting_time,
            'turnaround_time': process.turnaround_time,
            'remaining_time': process.remaining_time
        }
        processes_data.append(p_data)
    session['processes'] = processes_data

def run_simulation(algorithm, processes, quantum=2):
    """Run the selected scheduling algorithm."""
    import copy

    process_copies = copy.deepcopy(processes)
    for process in process_copies:
        process.reset()

    schedulers = {
        "fcfs": FCFSScheduler(),
        "sjf": SJFScheduler(),
        "priority": PriorityScheduler(),
        "rr": RoundRobinScheduler(quantum),
        "priority_rr": PriorityRRScheduler(quantum)
    }
    
    if algorithm in schedulers:
        scheduler = schedulers[algorithm]
        schedule = scheduler.schedule(process_copies)
        metrics = calculate_metrics(schedule, process_copies)
        return schedule, metrics, process_copies
    else:
        raise ValueError(f"Unknown algorithm: {algorithm}")

def run_all_simulations(processes, quantum=2):
    """Run all scheduling algorithms and compare their performance."""
    results = {}
    algorithms = ["fcfs", "sjf", "priority", "rr", "priority_rr"]
    
    for algorithm in algorithms:
        schedule, metrics, updated_processes = run_simulation(algorithm, processes, quantum)
        results[algorithm] = {
            "schedule": schedule,
            "metrics": metrics,
            "processes": updated_processes
        }
    
    return results

@main.route('/', methods=['GET', 'POST'])
def index():
    """Home page with simulation form."""
    form = SimulationForm()
    
    if form.validate_on_submit():
        session_id = str(uuid.uuid4())
        session['session_id'] = session_id
        
        algorithm = form.algorithm.data
        quantum = form.quantum.data

        if form.process_file.data:
            file = form.process_file.data
            if allowed_file(file.filename):
                file_path = save_upload_file(file)
                processes = read_processes_from_file(file_path)
                os.remove(file_path)
            else:
                flash('Invalid file type. Please upload a CSV or JSON file.', 'danger')
                return redirect(url_for('main.index'))
        else:
            processes = generate_random_processes(
                form.process_count.data,
                form.min_burst.data,
                form.max_burst.data,
                form.min_arrival.data,
                form.max_arrival.data,
                form.min_priority.data,
                form.max_priority.data
            )

        save_processes_to_session(processes)

        output_dir = os.path.join(current_app.config['OUTPUT_FOLDER'], session_id)
        os.makedirs(output_dir, exist_ok=True)
        
        if algorithm == 'all':
            results = run_all_simulations(processes, quantum)
            compare_schedulers(results, output_dir)

            session['results'] = {
                'type': 'comparison',
                'algorithms': list(results.keys()),
                'metrics': {algo: result['metrics'] for algo, result in results.items()},
                'session_id': session_id
            }
            
            return redirect(url_for('main.comparison_results'))
        else:
            schedule, metrics, updated_processes = run_simulation(algorithm, processes, quantum)

            save_processes_to_session(updated_processes)

            output_file = visualize_schedule(schedule, updated_processes, algorithm, output_dir)

            session['results'] = {
                'type': 'single',
                'algorithm': algorithm,
                'metrics': metrics,
                'schedule': [(int(pid), int(time_slice)) for pid, time_slice in schedule],
                'session_id': session_id
            }
            
            return redirect(url_for('main.algorithm_results'))

    processes = get_processes_from_session()
    
    return render_template('index.html', form=form, processes=processes)

@main.route('/results/algorithm')
def algorithm_results():
    """Display results for a single algorithm."""
    if 'results' not in session or session['results']['type'] != 'single':
        flash('No simulation results to display. Please run a simulation first.', 'warning')
        return redirect(url_for('main.index'))
    
    results = session['results']
    processes = get_processes_from_session()

    session_id = results['session_id']
    algorithm = results['algorithm']
    gantt_image = f"output/{session_id}/{algorithm}_gantt.png"
    
    return render_template(
        'algorithm_results.html',
        algorithm=algorithm,
        metrics=results['metrics'],
        schedule=results['schedule'],
        processes=processes,
        gantt_image=gantt_image
    )

@main.route('/results/comparison')
def comparison_results():
    """Display comparison results for all algorithms."""
    if 'results' not in session or session['results']['type'] != 'comparison':
        flash('No comparison results to display. Please run a comparison first.', 'warning')
        return redirect(url_for('main.index'))
    
    results = session['results']
    processes = get_processes_from_session()

    session_id = results['session_id']
    comparison_image = f"output/{session_id}/scheduler_comparison.png"
    timeline_image = f"output/{session_id}/timeline_comparison.png"

    algorithms = results['algorithms']
    metrics = results['metrics']
    
    best_algo_waiting = algorithms[0]
    best_algo_utilization = algorithms[0]

    for algo in algorithms:
        if metrics[algo]['avg_waiting_time'] < metrics[best_algo_waiting]['avg_waiting_time']:
            best_algo_waiting = algo

    for algo in algorithms:
        if metrics[algo]['cpu_utilization'] > metrics[best_algo_utilization]['cpu_utilization']:
            best_algo_utilization = algo
    
    return render_template(
        'comparison_results.html',
        algorithms=algorithms,
        metrics=metrics,
        processes=processes,
        comparison_image=comparison_image,
        timeline_image=timeline_image,
        best_algo_waiting=best_algo_waiting,
        best_algo_utilization=best_algo_utilization
    )

@main.route('/processes/clear', methods=['POST'])
def clear_processes():
    """Clear processes from session."""
    if 'processes' in session:
        del session['processes']
    if 'results' in session:
        del session['results']
    flash('Process data has been cleared.', 'success')
    return redirect(url_for('main.index'))

@main.route('/processes/json')
def get_processes_json():
    """Return processes as JSON for AJAX calls."""
    processes = get_processes_from_session()
    if not processes:
        return jsonify([])
    
    return jsonify([{
        'pid': p.pid,
        'arrival_time': p.arrival_time,
        'burst_time': p.burst_time,
        'priority': p.priority,
        'waiting_time': p.waiting_time,
        'turnaround_time': p.turnaround_time,
        'start_time': p.start_time,
        'finish_time': p.finish_time
    } for p in processes])