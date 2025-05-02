# CPU Scheduler Simulation with Web Interface

This project provides a comprehensive simulation of CPU scheduling algorithms with both a command-line interface and a web-based graphical interface. It allows users to configure, run, and visualize different CPU scheduling algorithms to understand their behavior and performance characteristics.

## Features

- **Multiple Scheduling Algorithms**:
  - First-Come, First-Served (FCFS)
  - Shortest Job First (SJF)
  - Priority Scheduling
  - Round Robin (RR)
  - Priority + Round Robin

- **Command-Line Interface**:
  - Generate random processes
  - Read processes from files (CSV, JSON)
  - Configure simulation parameters
  - Visualize scheduling with Gantt charts
  - Compare algorithm performance

- **Web Interface**:
  - User-friendly form for simulation configuration
  - Process generation with customizable parameters
  - File upload for custom process data
  - Visualization of scheduling results
  - Comparative analysis of different algorithms
  - Performance metrics and insights

## Requirements

- Python 3.6+
- Flask and Flask extensions
- Matplotlib
- NumPy
- Other dependencies listed in `requirements.yml`

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/Douae-MEJHOUDI/cpu-scheduler-simulation.git
   cd cpu-scheduler-simulation
   ```

2. Create a virtual environment for the required dependencies:
   ```
   conda env create -f requirements.yml
   ```

3. activate the virtual environment :
   ```
   conda activate schedule
   ```

## Usage

### Web Interface

1. Start the Flask application:
   ```
   python run.py --debug
   ```

2. Open a web browser and navigate to:
   ```
   http://127.0.0.1:5000/
   ```

3. Use the web interface to:
   - Configure simulation parameters
   - Generate random processes or upload a file (a file example is given in data folder)
   - Run the simulation
   - View and analyze the results

### Command-Line Interface

#### Running the Simulation

You can run the simulation with default parameters:

```bash
python main.py
```

Or specify parameters:

```bash
python main.py --algorithm fcfs --processes 10 --min_burst 1 --max_burst 10 --min_arrival 0 --max_arrival 20 --quantum 2
```
#### Command Line Arguments

- `--algorithm`, `-a`: Scheduling algorithm to use (fcfs, sjf, priority, rr, priority_rr, all)
- `--processes`, `-p`: Number of processes to generate
- `--min_burst`, `-mb`: Minimum burst time
- `--max_burst`, `-xb`: Maximum burst time
- `--min_arrival`, `-ma`: Minimum arrival time
- `--max_arrival`, `-xa`: Maximum arrival time
- `--min_priority`, `-mp`: Minimum priority (1 is highest)
- `--max_priority`, `-xp`: Maximum priority (higher number is lower priority)
- `--quantum`, `-q`: Time quantum for Round Robin
- `--input_file`, `-i`: Input file with process data
- `--output_dir`, `-o`: Directory to save visualizations (By default the directory is created and named output in which we store the plots)

#### Input File Format

You can provide a CSV file with process data:

```csv
pid,arrival_time,burst_time,priority
1,0,5,2
2,2,3,1
3,4,1,3
4,6,4,2
5,8,2,1
```

## Project Structure

```
cpu_scheduler_simulation/
├── app/                      # Flask web application
│   ├── __init__.py           # Flask app initialization
│   ├── routes.py             # API and page routes
│   ├── forms.py              # Form definitions
│   ├── config.py             # Application configuration
│   ├── static/               # Static assets (CSS, JS)
│   └── templates/            # HTML templates
├── src/                      # Core simulation code
│   ├── process.py            # Process class definition
│   ├── schedulers/           # Scheduling algorithms
│   ├── utils/                # Utility functions
│   └── visualization/        # Visualization logic
├── data/                     # Sample input files
├── output/                   # Output directory for visualizations
├── run.py                    # Enhanced Flask application runner 
├── main.py                   # Command-line interface entry point
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## Implementation Details

### Process Representation

Each process is represented by a `Process` class with the following attributes:
- Process ID (pid)
- Arrival time
- Burst time (CPU time required)
- Priority
- Remaining time
- Start time
- Finish time
- Waiting time
- Turnaround time

### Algorithms

#### First-Come, First-Served (FCFS)
- Non-preemptive algorithm
- Processes are executed in order of arrival
- Simple to implement but can lead to convoy effect

#### Shortest Job First (SJF)
- Non-preemptive algorithm
- Processes with the shortest burst time are executed first
- Provides optimal average waiting time but can cause starvation

#### Priority Scheduling
- Non-preemptive algorithm
- Processes are executed based on priority
- Important processes get CPU first but lower priority processes may starve

#### Round Robin (RR)
- Preemptive algorithm
- Each process gets a small unit of CPU time (quantum)
- Fair for all processes but can increase context switching overhead

#### Priority + Round Robin
- Combines priority scheduling with round robin
- Processes are grouped by priority, with round robin within each priority level
- Balances importance with fairness

### Performance Metrics

The simulation calculates the following performance metrics:
- **Turnaround Time**: Time from arrival to completion
- **Waiting Time**: Time spent in the ready queue
- **CPU Utilization**: Percentage of time the CPU is busy

### Example Output

The simulation generates Gantt charts for each scheduling algorithm and comparative visualizations:

1. Individual Gantt charts for each algorithm
2. Comparative bar charts for average turnaround time, average waiting time, and CPU utilization
3. Timeline comparison of all algorithms

## Acknowledgments

- Flask web framework
- Bootstrap for responsive design
- Matplotlib for visualization
- All contributors to this project
