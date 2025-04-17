# scheduler.py
# Implements the CPU scheduling algorithms: FCFS, SJF, Priority, Round Robin.

import copy
from collections import deque
from process import Process # Assuming process.py is in the same directory

def fcfs(processes):
    """
    First-Come, First-Served (FCFS) Scheduling Algorithm (Non-Preemptive).

    Args:
        processes (list): A list of Process objects.

    Returns:
        tuple: Contains:
            - list: Gantt chart entries [(p_id, start, end), ...].
            - float: Average waiting time.
            - float: Average turnaround time.
            - list: List of completed Process objects with calculated metrics.
    """
    # Create a deep copy to avoid modifying the original list
    process_queue = sorted(copy.deepcopy(processes), key=lambda p: p.arrival_time)
    completed_processes = []
    gantt_chart = []
    current_time = 0
    total_waiting_time = 0
    total_turnaround_time = 0

    while process_queue:
        # Get the next process based on arrival time
        proc = process_queue.pop(0)

        # If CPU is idle before process arrival, advance time
        if current_time < proc.arrival_time:
            gantt_chart.append(("Idle", current_time, proc.arrival_time))
            current_time = proc.arrival_time

        # Assign start time
        proc.start_time = current_time

        # Execute the process
        execution_start = current_time
        current_time += proc.burst_time
        proc.completion_time = current_time

        # Add to Gantt chart
        gantt_chart.append((proc.p_id, execution_start, proc.completion_time))

        # Calculate metrics for this process
        proc.calculate_metrics()
        total_waiting_time += proc.waiting_time
        total_turnaround_time += proc.turnaround_time

        completed_processes.append(proc)

    if not completed_processes:
        return [], 0.0, 0.0, []

    avg_waiting_time = total_waiting_time / len(completed_processes)
    avg_turnaround_time = total_turnaround_time / len(completed_processes)

    # Sort completed processes by ID for consistent output
    completed_processes.sort(key=lambda p: p.p_id)

    return gantt_chart, avg_waiting_time, avg_turnaround_time, completed_processes


def sjf(processes):
    """
    Shortest Job First (SJF) Scheduling Algorithm (Non-Preemptive).

    Args:
        processes (list): A list of Process objects.

    Returns:
        tuple: Contains:
            - list: Gantt chart entries [(p_id, start, end), ...].
            - float: Average waiting time.
            - float: Average turnaround time.
            - list: List of completed Process objects with calculated metrics.
    """
    process_list = sorted(copy.deepcopy(processes), key=lambda p: p.arrival_time)
    completed_processes = []
    gantt_chart = []
    current_time = 0
    total_waiting_time = 0
    total_turnaround_time = 0
    n = len(process_list)
    remaining_processes = list(process_list) # Keep track of processes not yet completed

    while len(completed_processes) < n:
        # Find processes that have arrived and are ready
        ready_queue = [p for p in remaining_processes if p.arrival_time <= current_time]

        if not ready_queue:
            # If no process is ready, find the next arrival time
            next_arrival_time = min(p.arrival_time for p in remaining_processes)
            if current_time < next_arrival_time:
                 gantt_chart.append(("Idle", current_time, next_arrival_time))
                 current_time = next_arrival_time
            # Re-check ready queue after advancing time
            ready_queue = [p for p in remaining_processes if p.arrival_time <= current_time]


        if ready_queue:
             # Select the process with the shortest burst time from the ready queue
            ready_queue.sort(key=lambda p: p.burst_time)
            proc = ready_queue[0]

            # Remove selected process from remaining list
            remaining_processes.remove(proc)

            # Assign start time if not already set (first time it runs)
            if proc.start_time == -1:
                 proc.start_time = current_time

            # Execute the process
            execution_start = current_time
            current_time += proc.burst_time
            proc.completion_time = current_time

            # Add to Gantt chart
            gantt_chart.append((proc.p_id, execution_start, proc.completion_time))

            # Calculate metrics
            proc.calculate_metrics()
            total_waiting_time += proc.waiting_time
            total_turnaround_time += proc.turnaround_time

            completed_processes.append(proc)
        elif not remaining_processes:
             # Should not happen if logic is correct, but break just in case
             break


    if not completed_processes:
        return [], 0.0, 0.0, []

    avg_waiting_time = total_waiting_time / len(completed_processes)
    avg_turnaround_time = total_turnaround_time / len(completed_processes)

    # Sort completed processes by ID for consistent output
    completed_processes.sort(key=lambda p: p.p_id)

    return gantt_chart, avg_waiting_time, avg_turnaround_time, completed_processes


def priority_scheduling(processes):
    """
    Priority Scheduling Algorithm (Non-Preemptive).
    Lower priority number means higher priority.

    Args:
        processes (list): A list of Process objects.

    Returns:
        tuple: Contains:
            - list: Gantt chart entries [(p_id, start, end), ...].
            - float: Average waiting time.
            - float: Average turnaround time.
            - list: List of completed Process objects with calculated metrics.
    """
    process_list = sorted(copy.deepcopy(processes), key=lambda p: p.arrival_time)
    completed_processes = []
    gantt_chart = []
    current_time = 0
    total_waiting_time = 0
    total_turnaround_time = 0
    n = len(process_list)
    remaining_processes = list(process_list)

    while len(completed_processes) < n:
        # Find processes that have arrived
        ready_queue = [p for p in remaining_processes if p.arrival_time <= current_time]

        if not ready_queue:
            # If no process is ready, find the next arrival time
            next_arrival_time = min(p.arrival_time for p in remaining_processes)
            if current_time < next_arrival_time:
                 gantt_chart.append(("Idle", current_time, next_arrival_time))
                 current_time = next_arrival_time
            # Re-check ready queue
            ready_queue = [p for p in remaining_processes if p.arrival_time <= current_time]

        if ready_queue:
            # Select the process with the highest priority (lowest priority number)
            ready_queue.sort(key=lambda p: p.priority)
            proc = ready_queue[0]

            # Remove selected process from remaining list
            remaining_processes.remove(proc)

            # Assign start time
            if proc.start_time == -1:
                proc.start_time = current_time

            # Execute the process
            execution_start = current_time
            current_time += proc.burst_time
            proc.completion_time = current_time

            # Add to Gantt chart
            gantt_chart.append((proc.p_id, execution_start, proc.completion_time))

            # Calculate metrics
            proc.calculate_metrics()
            total_waiting_time += proc.waiting_time
            total_turnaround_time += proc.turnaround_time

            completed_processes.append(proc)
        elif not remaining_processes:
             break


    if not completed_processes:
        return [], 0.0, 0.0, []

    avg_waiting_time = total_waiting_time / len(completed_processes)
    avg_turnaround_time = total_turnaround_time / len(completed_processes)

    # Sort completed processes by ID for consistent output
    completed_processes.sort(key=lambda p: p.p_id)

    return gantt_chart, avg_waiting_time, avg_turnaround_time, completed_processes


def round_robin(processes, time_quantum):
    """
    Round Robin (RR) Scheduling Algorithm.

    Args:
        processes (list): A list of Process objects.
        time_quantum (int): The time slice allocated to each process.

    Returns:
        tuple: Contains:
            - list: Gantt chart entries [(p_id, start, end), ...].
            - float: Average waiting time.
            - float: Average turnaround time.
            - list: List of completed Process objects with calculated metrics.
    """
    if time_quantum <= 0:
        raise ValueError("Time quantum must be positive.")

    process_list = sorted(copy.deepcopy(processes), key=lambda p: p.arrival_time)
    completed_processes_dict = {} # Use dict for easy lookup by p_id
    gantt_chart = []
    current_time = 0
    total_waiting_time = 0
    total_turnaround_time = 0
    n = len(process_list)

    ready_queue = deque()
    process_idx = 0 # To track next process to check for arrival

    last_gantt_entry = None # To merge consecutive runs of the same process

    while len(completed_processes_dict) < n:
        # Add newly arrived processes to the ready queue
        while process_idx < n and process_list[process_idx].arrival_time <= current_time:
            process_list[process_idx].remaining_burst_time = process_list[process_idx].burst_time # Initialize remaining time
            ready_queue.append(process_list[process_idx])
            process_idx += 1

        if not ready_queue:
            # If ready queue is empty, check if there are future arrivals
            if process_idx < n:
                next_arrival_time = process_list[process_idx].arrival_time
                if current_time < next_arrival_time:
                     # Add Idle time to Gantt chart only if it's different from last entry
                     if last_gantt_entry is None or last_gantt_entry[0] != "Idle":
                         gantt_chart.append(("Idle", current_time, next_arrival_time))
                         last_gantt_entry = ("Idle", current_time, next_arrival_time)
                     elif last_gantt_entry[0] == "Idle": # Extend previous idle block
                         gantt_chart[-1] = ("Idle", last_gantt_entry[1], next_arrival_time)
                         last_gantt_entry = gantt_chart[-1]

                     current_time = next_arrival_time
                continue # Go back to check for arrivals at the new current_time
            else:
                # No processes left to arrive and queue is empty, simulation ends
                break

        # Get process from front of the ready queue
        proc = ready_queue.popleft()

        # Record start time if it's the first time the process runs
        if proc.start_time == -1:
            proc.start_time = current_time

        execution_start = current_time
        time_slice = min(time_quantum, proc.remaining_burst_time)

        # Execute for the time slice
        proc.remaining_burst_time -= time_slice
        current_time += time_slice

        # Add to Gantt chart
        # Merge with the previous entry if it's the same process
        if last_gantt_entry and last_gantt_entry[0] == proc.p_id and last_gantt_entry[2] == execution_start:
             gantt_chart[-1] = (proc.p_id, last_gantt_entry[1], current_time)
        else:
             gantt_chart.append((proc.p_id, execution_start, current_time))
        last_gantt_entry = gantt_chart[-1]


        # Add any processes that arrived *during* this time slice execution
        while process_idx < n and process_list[process_idx].arrival_time <= current_time:
             process_list[process_idx].remaining_burst_time = process_list[process_idx].burst_time
             ready_queue.append(process_list[process_idx])
             process_idx += 1


        if proc.remaining_burst_time == 0:
            # Process completed
            proc.completion_time = current_time
            proc.calculate_metrics() # Calculate metrics here
            total_waiting_time += proc.waiting_time
            total_turnaround_time += proc.turnaround_time
            completed_processes_dict[proc.p_id] = proc # Store completed process
        else:
            # Process not finished, add back to the end of the ready queue
            ready_queue.append(proc)


    if not completed_processes_dict:
        return [], 0.0, 0.0, []

    avg_waiting_time = total_waiting_time / n
    avg_turnaround_time = total_turnaround_time / n

    # Convert completed processes dict back to a list sorted by ID
    completed_processes_list = sorted(list(completed_processes_dict.values()), key=lambda p: p.p_id)

    return gantt_chart, avg_waiting_time, avg_turnaround_time, completed_processes_list

