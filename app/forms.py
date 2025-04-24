"""
Forms for the CPU Scheduler Simulation web interface.
"""

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Optional

class SimulationForm(FlaskForm):
    """Form for configuring the CPU scheduler simulation."""

    algorithm = SelectField(
        'Scheduling Algorithm', 
        choices=[
            ('all', 'Compare All Algorithms'),
            ('fcfs', 'First-Come, First-Served (FCFS)'),
            ('sjf', 'Shortest Job First (SJF)'),
            ('priority', 'Priority Scheduling'),
            ('rr', 'Round Robin (RR)'),
            ('priority_rr', 'Priority + Round Robin')
        ],
        validators=[DataRequired()]
    )

    process_count = IntegerField(
        'Number of Processes',
        validators=[NumberRange(min=1, max=50)],
        default=5
    )
    
    min_burst = IntegerField(
        'Minimum Burst Time',
        validators=[NumberRange(min=1)],
        default=1
    )
    
    max_burst = IntegerField(
        'Maximum Burst Time',
        validators=[NumberRange(min=1)],
        default=10
    )
    
    min_arrival = IntegerField(
        'Minimum Arrival Time',
        validators=[NumberRange(min=0)],
        default=0
    )
    
    max_arrival = IntegerField(
        'Maximum Arrival Time',
        validators=[NumberRange(min=0)],
        default=10
    )
    
    min_priority = IntegerField(
        'Minimum Priority (lower number = higher priority)',
        validators=[NumberRange(min=1)],
        default=1
    )
    
    max_priority = IntegerField(
        'Maximum Priority',
        validators=[NumberRange(min=1)],
        default=10
    )
    
    quantum = IntegerField(
        'Time Quantum (for RR algorithms)',
        validators=[NumberRange(min=1)],
        default=2
    )

    process_file = FileField(
        'Upload Process Data (CSV or JSON)',
        validators=[
            Optional(),
            FileAllowed(['csv', 'json'], 'CSV or JSON files only!')
        ]
    )

    submit = SubmitField('Run Simulation')